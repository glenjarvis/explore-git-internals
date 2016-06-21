"""
Module to parse raw commit messages

The ParsedCommit class is provided and it is a subclass of dictionary.
This allows one to take the raw format of a commit and process it as in
this example:

Example raw commit:

> tree 0ea3ee5e56e3123de49422ac3315b1cee3d74910
> parent 3d5f868982cc7ccf4dddcfd14560d1f25507dc1d
> parent 39f0875dfc705ced8250155e61801554198e0d5f
> author Glen Jarvis <glen@glenjarvis.com> 1465164241 -0700
> committer Glen Jarvis <glen@glenjarvis.com> 1465164241 -0700
>
> Merge pull request #4 from glenjarvis/get_branch_commit

>>> from commit import ParsedCommit
>>> ParsedCommit(raw_commit)
{'committer': 'Glen Jarvis <glen@glenjarvis.com> 1465164241 -0700',
 'message': 'Merge pull request #4 from glenjarvis/get_branch_commit',
 'tree': '0ea3ee5e56e3123de49422ac3315b1cee3d74910',
 'parent': '39f0875dfc705ced8250155e61801554198e0d5f',
 'author': 'Glen Jarvis <glen@glenjarvis.com> 1465164241 -0700'}
"""

import datetime
import pytz


def swap_sign(sign):
    """Given a sign (+ or -), return opposite"""

    assert sign in ["+", "-"]
    if sign == "+":
        return "-"
    if sign == "-":
        return "+"


def epoch_to_utc(epoch_seconds):
    """Given seconds form the Epoch, return tz aware UTC datetime"""

    return pytz.utc.localize(
        datetime.datetime.utcfromtimestamp(float(epoch_seconds))
    )


def zone_from_offset(offset_string):
    """Given Git offset string, return pytz timezone

    Example:
    >> offset_string = "-0700"
    >> time_zone = zone_from_offset(offset)
    >> type(time_zone)
    <class 'pytz.tzfile.Etc/GMT+7'>

    Note: The swapped sign "GMT+7" vs "-0700" is intentional:

    https://en.wikipedia.org/wiki/ISO_8601#Time_offsets_from_UTC

    Feedback regarding the philosophy of GMT, UTC, and Zulu here
    and suggestions for more clarity appreciated.
    """
    sign = offset_string[0]
    hour = offset_string[1:3]
    return pytz.timezone("Etc/GMT{0}{1}".format(swap_sign(sign),
                                                int(hour)))


class ParsedCommit(dict):
    """Commit Parser used to parse raw commit messages

    There are only two sections of a raw commit. The first is headers
    and the second is a message typed by users. Three states are needed
    when parsing headers and multi-line values (e.g., gpgsig) are
    encountered.
    """

    # PyLint, it's okay that this has so many public methods
    # pylint: disable=R0904

    HEADERS_STATE = 1
    GPGSIG_HEADER_STATE = 2
    MESSAGE_TEXT_STATE = 3

    def __init__(self, raw_commit):
        self.message = []
        self.gpgsig = []
        self.raw_commit = raw_commit
        dict.__init__(self)
        self.current_state = self.HEADERS_STATE
        self.parse_commit()

    def start_gpg_parse(self, line):
        """Take gpg start line from raw commit, fix state

        Take gpg start line from raw commit (a multi-lined value) which
        looks similar to the following subset of a potential commit message:

        gpgsig -----BEGIN PGP SIGNATURE-----
         Version: GnuPG v1

         iQIcBAABAgAGBQJXVJ/8AAoJEJF24vsEed5c44IP/R+4nVUKjRBmEyEnmWEI9NuA
         [snip]
         =bnDB
         -----END PGP SIGNATURE-----

        Return a tuple of values:
          * The new state `read_gpgsig_header`
          * The first line of the PGP signature
        """
        _, first_line = line.split(" ", 1)
        return (self.GPGSIG_HEADER_STATE, first_line)

    def handle_headers_state(self, line):
        """Handle the HEADERS_STATE when receiving line of data

        Assume the HEADERS_STATE is the current state in the tiny
        parsing state machine. Expect input to be in key value format
        (with a space between key and value) as in this example:

        tree 0ea3ee5e56e3123de49422ac3315b1cee3d74910

        This input is parsed and stored in self (dictionary).

        HOWEVER, if the line encountered is a `gpgsig` key instead of
        `tree` or others, then switch to the GPGSIG_HEADER_STATE state
        and begin parsing the first line of the multi-line value output.
        The gpgsig key is only present when commits are signed (not the
        default case).
        """

        if line.startswith("gpgsig"):
            self.current_state, pgp_header = self.start_gpg_parse(line)
            self.gpgsig.append(pgp_header)
        if len(line) == 0:
            self.current_state = self.MESSAGE_TEXT_STATE
        else:
            key, value = line.split(" ", 1)
            self[key] = value

    def handle_message_text_state(self, line):
        """Handle the MESSAGE_TEXT_STATE when receiving line of data

        Assume the MESSAGE_TEXT_STATE is the current state in the tiny
        parsing state machine. Expect input to be lines of text (a
        description of the commit).
        """
        self.message.append(line)

    def handle_gpgsig_header_state(self, line):
        """Handle the GPGSIG_HEADER_STATE when receiving line of data

        Assume the special GPGSIG_HEADER_STATE is the curernt state in
        the tiny parsing state machine. Expect lines to be lines of text
        (the multi-line PGP signature) and transition back to the
        HEADERS_STATE when all lines have been found.
        """

        if "END PGP SIGNATURE" in line:
            self.current_state = self.HEADERS_STATE
        self.gpgsig.append(line.strip())

    def update_field_datetime(self, field):
        """Given field name update post-parsing

        Some fields (i.e., author|committer) contain date-time
        information. For example:
        > Glen Jarvis <glen@glenjarvis.com> 1466463764 -0700

        Process field, moving the date time information to its own field
        and converted the an aware datetime.  For example:

        'author': 'Glen Jarvis <glen@glenjarvis.com>'
        'author_datetime': datetime.datetime(
            2016, 6, 20, 16, 2, 44, tzinfo=<StaticTzInfo 'Etc/GMT+7'>)
        """
        components = self[field].split()
        epoch, offset = components[-2:]
        # Remove time component from field:
        self[field] = " ".join(components[:-2])

        utc_date_time = epoch_to_utc(epoch)
        time_zone = zone_from_offset(offset)

        # Add new field {field}_time:
        self["{0}_datetime".format(field)] =\
            utc_date_time.astimezone(time_zone)

    def update_timestamps(self):
        """Update author and committer fields after basic commit is parsed"""

        self.update_field_datetime("author")
        self.update_field_datetime("committer")

    def parse_commit(self):
        """Parse raw commit as given by `git cat-file -p`

        Given a raw large string that represents the raw commit as given by
        a `git cat-file -p <hash>` command, return a dictionary of values
        for the headers, including the commit message as typed by the user.

        Potentials keys for dictionary are: author, committer, gpgsig,
        parent, tree and message.
        """

        for line in self.raw_commit.split("\n"):
            if self.current_state == self.HEADERS_STATE:
                self.handle_headers_state(line)
            elif self.current_state == self.GPGSIG_HEADER_STATE:
                self.handle_gpgsig_header_state(line)
            elif self.current_state == self.MESSAGE_TEXT_STATE:
                self.handle_message_text_state(line)

        if self.gpgsig:
            self["gpgsig"] = "\n".join(self.gpgsig)

        self["message"] = "\n".join(self.message)
        self.update_timestamps()
        return self

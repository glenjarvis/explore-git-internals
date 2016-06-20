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


class ParsedCommit(dict):
    """Commit Parser used to parse raw commit messages

    There are only two sections of a raw commit. The first is headers
    and the second is a message typed by users. Three states are needed
    when parsing headers and multi-line values (e.g., gpgsig) are
    encountered.
    """

    # PyLint, it's okay that this has so many (22) public methods
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
        return self

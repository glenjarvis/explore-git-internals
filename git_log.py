#!/usr/bin/env python
# Allow print() to have parethesis:
# pylint: disable=C0325

"""
Supporting code for the "Explore Git internals using Python"
talk:

http://www.meetup.com/silicon-valley-python/events/228160092/

For simplicity in presentation of the code, we will keep these in a
single file.
"""


import os
from pprint import pprint
import subprocess

from commit import ParsedCommit



class GitError(RuntimeError):
    """A Git Error Exception"""


def check_base_case(cwd, potential):
    """Stop looking if .git not found at /

    Check the current working directory (cwd) to see if it is at the
    root of the filesystem. If it is, and there is not a .git directory
    there, then we have reached the top of the heirarchy and have to
    stop looking.
    """
    if cwd == "/" and not os.path.exists(potential):
        print("fatal: Not a git repository (or any of the parent " +
              "directories): .git")
        exit(128)


def git_root(cwd=None):
    """Return the full path to the .git directory"""

    if cwd is None:
        cwd = os.getcwd()
    git_dir = os.path.join(cwd, ".git")

    if os.path.exists(git_dir):
        return git_dir
    else:
        check_base_case(cwd, git_dir)
        return git_root(os.path.dirname(cwd))


def big_head(root=None):
    """Return contents of git HEAD variable"""

    if root is None:
        root = git_root()

    with open(os.path.join(root, "HEAD"), "r") as head_file:
        head = head_file.read().strip()

    return head


def parse_head(head_contents):
    """Given contents of HEAD, return file path to branch head file

    Example head_contents include:
      ref: refs/heads/master

    Given the above example, the following would be returned:
      .git/refs/heads/master
    """

    if head_contents.startswith("ref: "):
        return head_contents.replace("ref: ", "", 1)
    else:
        return head_contents


def branch_head_filename():
    """Return the full path to the branch filename pointed to by HEAD"""

    return os.path.join(git_root(), parse_head(big_head()))


def branch_head():
    """Return commit being referenced by branch referenced by HEAD"""

    with open(branch_head_filename(), "r") as branch_head_file:
        head = branch_head_file.read().strip()

    return head


def get_commit_contents(commit):
    """Return commit cotents for commit"""

    output = subprocess.check_output(["git", "cat-file", "-p", commit])
    return ParsedCommit(output)


def git_log():
    """Eqiuvalent of `git log`"""
    current = branch_head()
    pprint(get_commit_contents(current))


git_log()

#!/usr/bin/env python

"""
Supporting code for the "Explore Git internals using Python"
talk:

http://www.meetup.com/silicon-valley-python/events/228160092/

For simplicity in presentation of the code, we will keep these in a
single file.
"""


import os

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
        raise GitError(
            "fatal: Not a git repository (or any of the parent " +
            "directories): .git")


def git_root(cwd):
    """Return the full path to the .git"""

    git_dir = os.path.join(cwd, ".git")

    if os.path.exists(git_dir):
        return git_dir
    else:
        check_base_case(cwd, git_dir)
        return git_root(os.path.dirname(cwd))

print(git_root(os.getcwd()))

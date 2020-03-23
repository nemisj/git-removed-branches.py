from __future__ import print_function
import unittest
from git_removed_branches.main import find_local_branches
from mock import patch

local_branches = {
  "branch.zork.remote": "other-remote",
  "branch.master.remote": "the-remote",
}


def side_effect(*args, **kwargs):
    parts = args[0]
    command = parts[1]

    if command == "branch":
        return """  * master
  zork
"""
    elif command == "config":
        branch = parts[-1]
        remote = None

        try:
            remote = local_branches[branch]
        except KeyError:
            raise Exception("No such branch '{}'".format(branch))
        else:
            return remote


class TestStringMethods(unittest.TestCase):
    @patch('git_removed_branches.main.subprocess')
    def test_find_local_branches(self, subprocess_mock):
        subprocess_mock.check_output.side_effect = side_effect
        self.assertEqual(find_local_branches("other-remote"), ['zork'])


if __name__ == '__main__':
    unittest.main()

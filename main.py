#!/usr/bin/env python

import subprocess
import re
import argparse

def find_local_branches(remote):
  branches = subprocess.check_output(["git", "branch"], encoding="utf-8");
  correct_branches = [];
  for line in branches.splitlines():
    # take out the active branch, we are only intersted in the name of the
    # branch
    branch_name = re.sub(r"\*", "", line).strip()

    # skip empty lines
    if branch_name is "":
      continue

    # find out what is the remote of the branch
    try:
      remoteName = subprocess.check_output(
        ["git", "config", "--get", "branch.%s.remote" % branch_name],
        encoding="utf-8"
      )
    except Exception as e:
      # Branch has no config"
      remoteName = ""
    
    remoteName = remoteName.strip();

    if "%s" % remoteName == remote:
      correct_branches.append(branch_name)

  return correct_branches


def find_remote_branches(remote):
  branches = subprocess.check_output(["git", "branch", "-r"], encoding="utf-8")
  correct_branches = [];

  for line in branches.splitlines():
    branch_name = line.strip();
    result = re.search(r"%s/([^\s]*)" % remote, branch_name)
    if result:
      correct_branches.append(result.group(1))

  return correct_branches

def find_live_branches(remote):
  correct_branches = []

  try:
    branches = subprocess.check_output(["git", "ls-remote", "-h", remote], encoding="utf-8")
  except Exception as e:
    #TODO: test that this is error 128

    return None

  for line in branches.splitlines():
    branch_name = line.strip();
    result = re.search(r"refs/heads/([^\s]*)", branch_name)

    if result:
      correct_branches.append(result.group(1))

  return correct_branches


def delete_branches(branches, prune=False, force=False):

  broken = []

  if not branches:
    print("No removed branches found")
    return

  if not prune:
    print("Found removed branches:")

  print("")

  for branch_name in branches:
    if (prune):
      print("")
      print("Removing %s" % branch_name)

      if force:
        deleteFlag = "-D"
      else:
        deleteFlag = "-d"

      return_code = subprocess.call(["git", "branch", deleteFlag, branch_name]);
      if return_code != 0:
        print("ERROR: Unable to remove branch")
        broken.append(branch_name)
    else:
      print("  - %s" % branch_name)

  print("")
  if broken:
    print("Not all branches are removed:")

    for branch_name in broken:
      print("  - %s" % branch_name)

    print("INFO: To force removal use --force flag")

  elif prune:
    print("INFO: All branches are removed")

  else:
    print("INFO: To remove all found branches use --prune flag")

def analyze_live_and_remote(live_branches, remote_branches):
  if live_branches == None:
    return remote_branches

  notFound = []

  for branch_name in remote_branches:
    if branch_name != 'HEAD':
      try:
        index = live_branches.index(branch_name)
      except ValueError:
        notFound.append(branch_name)

  if notFound:
    print("WARNING: Your git repository is outdated, please run \"git fetch -p\"")
    print("         Following branches are not pruned:")
    print("")

    for name in notFound:
      print("  - %s" % name)
    print("")

  return live_branches

def find_to_remove(local=[], remote=[]):
  will_remove = []

  for branch_name in local:
    try:
      index = remote.index(branch_name)
    except ValueError:
      will_remove.append(branch_name)

  return will_remove

def main():
  parser = argparse.ArgumentParser(description="Remove local branches, which are no longer available in the remote")
  parser.add_argument("--prune", action="store_true", help="Remove branches")
  parser.add_argument("--force", action="store_true", help="Force deletion")
  parser.add_argument("--remote", default="origin", help="Remote name")
  args = parser.parse_args()

  # test whether this is the git repo
  try:
    subprocess.check_output(["git", "rev-parse", "--show-toplevel"]);
    is_git = True
  except Exception:
    is_git = False

  if is_git:
    # walk through the local branches
    # if local branch is not in remote branch list
    # prepare for removing
    remote = args.remote
    remote_branches = find_remote_branches(remote)
    local_branches = find_local_branches(remote) 
    live_branches = find_live_branches(remote)
    remote_branches = analyze_live_and_remote(live_branches, remote_branches)

    to_remove = find_to_remove(local=local_branches, remote=remote_branches)

    delete_branches(to_remove, args.prune, args.force)

if __name__ == "__main__":
  main()

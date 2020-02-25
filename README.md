Remove local branches that are no longer present in the remote git.

## Why?

Because I'm tired of doing every time `git fetch -p`, `git branch -r`, `git branch` and keep comparing which branches are gone from the GitHub, but still available locally and doing `git branch -D ${branch_name}` on one by one of them.

## What does it do

This command will compare your local branches with remote and will show you branches that are no longer available on remote but are still presented in your local repository. You can use it to view and to delete all (remotely) removed branches in one go using `--prune` flag.

This command works without the need to run `git fetch -p`, but working network connection to your remote is required. If no connection can be established with the remote repository, then local information about your remote will be used instead. If your local repository is not in sync with the remote repository, it will warn you about this.


## Installation

To install this package, you can use pip:

```
pip install git-removed-branches
```

## Usage

```bash
$ git removed-branches
```

This command will look through the branches which are no longer available on the remote and will display them.
In case you haven't run `git fetch -p` before, it will warn you to do so.


### Removing

To delete local branches, use `--prune` or `-p` flag.

```bash
$ git removed-branches --prune
```

### Different remote

If you have configured remote alias to something different than **'origin'**, you can use `--remote` or `-r` flag to specify the name of the remote. e.g., to set remote to be `upstream` execute:

```bash
$ git removed-branches --remote upstream
```

## Forcing removal

If you get an error when trying to delete branches:

```bash
The branch {branch_name} is not fully merged.
```

you can force deletion by using `--force` flag or use `-f` alias

```bash
$ git removed-branches --prune --force
```

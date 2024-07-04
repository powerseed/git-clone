import argparse
import collections
import configparser
from datetime import datetime
from fnmatch import fnmatch
import hashlib
from math import ceil
import os
import re
import sys
import zlib

argument_parser = argparse.ArgumentParser()
argument_subparsers = argument_parser.add_subparsers(title="Commands", dest="command")
argument_subparsers.required = True
init_subparser = argument_subparsers.add_parser("init", help="Initialize a new and empty repository. ")
init_subparser.add_argument("path", nargs="?", default=".", help="The directory to create the repository. ")

def main(argv=sys.argv[1:]):
    args = argument_parser.parse_args(argv)
    match args.command:
        case "add":
            cmd_add(args)
        case "cat-file":
            cmd_cat_file(args)
        case "check-ignore":
            cmd_check_ignore(args)
        case "checkout":
            cmd_checkout(args)
        case "commit":
            cmd_commit(args)
        case "hash-object":
            cmd_hash_object(args)
        case "init":
            cmd_init(args)
        case "log":
            cmd_log(args)
        case "ls-files":
            cmd_ls_files(args)
        case "ls-tree":
            cmd_ls_tree(args)
        case "rev-parse":
            cmd_rev_parse(args)
        case "rm":
            cmd_rm(args)
        case "show-ref":
            cmd_show_ref(args)
        case "status":
            cmd_status(args)
        case "tag":
            cmd_tag(args)
        case _:
            print("Bad command.")


# def cmd_init(args):

class GitRepo(object):
    worktree = None
    gitdir = None
    config_parser = None

    def __init__(self, path, is_forcing=False):
        self.worktree = path
        self.gitdir = os.path.join(path, ".git")
        self.config_parser = configparser.ConfigParser()

        if is_forcing:
            return
        else:
            if not os.path.isdir(self.gitdir):
                raise Exception("Not a git repository %s." % path)

            config_file_path = get_file_path(self, "config")

            if config_file_path:
                self.config_parser.read([config_file_path])
            else:
                raise Exception("Config file %s does not exist." % config_file_path)

            version = int(self.config_parser.get("core", "repositoryformatversion"))

            if version != 0:
                raise Exception("Unsupported repository format version %s." % version)


def get_file_path(repo, *path, is_making_directory=False):
    path = os.path.join(repo.gitdir, *path)

    if os.path.exists(path):
        if os.path.isdir(path):
            return path
        else:
            raise Exception("Path exists but is invalid: %s." % path)
    else:
        if is_making_directory:
            os.makedirs(path)
            return path
        else:
            return None


def create_new_repo(path):
    repo = GitRepo(path, True)

    if os.path.exists(repo.worktree):
        if not os.path.isdir(repo.worktree):
            raise Exception("%s is not a valid directory. " % path)
        if os.path.exists(repo.gitdir) and os.listdir(repo.gitdir):
            raise Exception(".git folder is not empty: %s" % repo.gitdir)
    else:
        os.makedirs(repo.worktree)

    assert get_file_path(repo, "branches", is_making_directory=True)
    assert get_file_path(repo, "objects", is_making_directory=True)
    assert get_file_path(repo, "refs", "tags", is_making_directory=True)
    assert get_file_path(repo, "refs", "heads", is_making_directory=True)

    with open(os.path.join(repo.gitdir, "description"), "w") as f:
        f.write("Unnamed repository; edit this file 'description' to name the repository.\n")

    with open(os.path.join(repo.gitdir, "HEAD"), "w") as f:
        f.write("ref: refs/heads/master\n")

    with open(os.path.join(repo.gitdir, "config"), "w") as f:
        config_parser = get_repo_default_config_parser()
        config_parser.write(f)

    return repo


def get_repo_default_config_parser():
    config_parser = configparser.ConfigParser()

    config_parser.add_section("core")
    config_parser.set("core", "repositoryformatversion", "0")
    config_parser.set("core", "filemode", "false")
    config_parser.set("core", "bare", "false")

    return config_parser


def cmd_init(args):
    create_new_repo(args.path)

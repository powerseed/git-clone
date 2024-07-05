import argparse
import os
import sys

from functions.cat_file import cat_file
from functions.create_new_repo import create_new_repo
from functions.get_gitdir import get_gitdir

argument_parser = argparse.ArgumentParser()
argument_subparsers = argument_parser.add_subparsers(title="Commands", dest="command")
argument_subparsers.required = True

init_subparser = argument_subparsers.add_parser("init", help="Initialize a new and empty repository. ")
init_subparser.add_argument("path", nargs="?", default=".", help="The directory to create the repository. ")

cat_file_subparser = argument_subparsers.add_parser("cat-file", help="Provide content of objects. ")
cat_file_subparser.add_argument("object_type", choices=["blob", "commit", "tag", "tree"], help="The type of the object to cat. ")
cat_file_subparser.add_argument("object_name", help="The object to cat. ")


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


def cmd_init(args):
    create_new_repo(args.path)


def cmd_cat_file(args):
    gitdir = get_gitdir(os.getcwd())
    cat_file(gitdir, args.object_type, args.object_name)


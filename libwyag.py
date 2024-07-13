import argparse
import os
import sys

from functions.cat_file import cat_file
from functions.create_new_repo import create_new_repo
from functions.get_gitdir import get_gitdir
from functions.list_refs import get_refs_as_ordered_dictionary
from functions.log_commit import log_commit
from functions.ls_tree import ls_tree
from functions.object_hash import hash_object
from functions.print_out_refs_ordered_dictionary import print_out_refs_ordered_dictionary
from functions.read_object import read_object
from functions.tree_checkout import tree_checkout

argument_parser = argparse.ArgumentParser()
argument_subparsers = argument_parser.add_subparsers(title="Commands", dest="command")
argument_subparsers.required = True

init_subparser = argument_subparsers.add_parser("init", help="Initialize a new and empty repository. ")
init_subparser.add_argument("path", nargs="?", default=".", help="The directory to create the repository. ")

cat_file_subparser = argument_subparsers.add_parser("cat-file", help="Provide content of objects. ")
cat_file_subparser.add_argument("object_type", choices=["blob", "commit", "tag", "tree"],
                                help="The type of the object to cat. ")
cat_file_subparser.add_argument("object_name", help="The object to cat. ")

hash_object_subparser = argument_subparsers.add_parser("hash-object", help="Compute object ID and optionally creates a "
                                                                           "blob from a file. ")
hash_object_subparser.add_argument("-w", dest="is_writing", action="store_true", help="Flag that when true writes the "
                                                                                      "object into database. ")
hash_object_subparser.add_argument("-t", dest="object_type", choices=["blob", "commit", "tag", "tree"], default="blob",
                                   help="The type of the object to hash. ")
hash_object_subparser.add_argument("file_path", help="Path of the file to hash. ")

log_subparser = argument_subparsers.add_parser("log", help="Display history of a given commit. ")
log_subparser.add_argument("commit_sha", default="HEAD", nargs="?", help="The sha of the commit. ")

ls_tree_subparser = argument_subparsers.add_parser("ls-tree", help="Pretty-print a tree object. ")
ls_tree_subparser.add_argument("-r", dest="is_recursive", action="store_true", help="Set whether it is recursing into "
                                                                                    "sub-trees. ")
ls_tree_subparser.add_argument("tree_sha", help="The sha of the tree. ")

ls_tree_subparser = argument_subparsers.add_parser("checkout", help="Checkout a commit inside of a directory. ")
ls_tree_subparser.add_argument("sha", help="Sha of the git object (commit or tree) to checkout. ")
ls_tree_subparser.add_argument("path", help="Path of the directory to checkout the commit. ")

show_ref_subparser = argument_subparsers.add_parser("show-ref", help="List all references. ")


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
            cmd_show_ref()
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


def cmd_hash_object(args):
    if args.is_writing:
        gitdir = get_gitdir(os.getcwd())
    else:
        gitdir = None

    with open(args.file_path, "rb") as file:
        sha = hash_object(file, args.object_type, gitdir)
        print(sha)


def cmd_log(args):
    gitdir = get_gitdir(os.getcwd())
    log_commit(gitdir, args.commit_sha)


def cmd_ls_tree(args):
    gitdir = get_gitdir(os.getcwd())
    ls_tree(gitdir, args.is_recursive, args.tree_sha)


def cmd_checkout(args):
    gitdir = get_gitdir(os.getcwd())
    git_object = read_object(gitdir, args.sha)

    if git_object.object_type == b'commit':
        commit_key_value_pairs = git_object.get_key_value_pairs()
        tree_sha = commit_key_value_pairs.get(b'tree')[0].decode('ascii')
        git_object = read_object(gitdir, tree_sha)

    if os.path.exists(args.path):
        if not os.path.isdir(args.path):
            raise Exception("%s is not a directory" % args.path)
        if len(os.listdir(args.path)) > 0:
            raise Exception("%s is not empty" % args.path)
    else:
        os.makedirs(args.path)

    tree_checkout(gitdir, git_object, args.path)


def cmd_show_ref():
    gitdir = get_gitdir(os.getcwd())
    ref_folder_path = os.path.join(gitdir, "refs")
    ordered_dictionary = get_refs_as_ordered_dictionary(ref_folder_path)
    print_out_refs_ordered_dictionary(ordered_dictionary)


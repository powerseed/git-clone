import os

from classes.GitRepo import GitRepo
from functions.get_file_path import get_file_path
from functions.get_repo_default_config_parser import get_repo_default_config_parser


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

import os
import configparser

from functions.get_file_path import get_file_path


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
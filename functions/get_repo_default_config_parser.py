import configparser


def get_repo_default_config_parser():
    config_parser = configparser.ConfigParser()

    config_parser.add_section("core")
    config_parser.set("core", "repositoryformatversion", "0")
    config_parser.set("core", "filemode", "false")
    config_parser.set("core", "bare", "false")

    return config_parser

DEFAULT_CONFIG = {
    "mode": "644",
    "messy_chars": "[]()'*?$#`|\\\" ",
    "substitute": "_",
    "temp_patterns": "*~,*.tmp,*.swp,*.bak",
    "duplicates_dir": "_dups",
}


def load_config(config_file):
    config = dict(DEFAULT_CONFIG)
    lines = []

    with open(config_file, "r") as file_handle:
        lines = file_handle.readlines()

    for line in lines:
        key, value = line.split("=", 1)
        config[key.strip()] = value.strip()

    return config


def get_mode(config):
    return int(config["mode"], 8)


def get_messy_chars(config):
    return list(config["messy_chars"])


def get_temp_patterns(config):
    return config["temp_patterns"].split(";")


def get_substitute_char(config):
    return config["substitute"]


def get_duplicates_dir(config):
    return config["duplicates_dir"]

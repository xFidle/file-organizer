DEFAULT_CONFIG = {
    "mode": "644",
    "messy_chars": "[]()'*?$#`|\\\" ",
    "substitute": "_",
    "temp_patterns": "*~,*.tmp,*.swp,*.bak",
}


def load_config(config_file):
    config = DEFAULT_CONFIG
    lines = []

    if config_file.exists():
        with open(config_file, "r") as file_handle:
            lines = file_handle.readlines()

    for i in range(1, len(lines)):
        key, value = lines[i].split("=", 1)
        config[key.strip()] = value.strip()

    return config


def get_mode(config):
    return int(config["mode"], 8)


def get_messy_chars(config):
    return list(config["messy_chars"])


def get_temp_patterns(config):
    return config["temp_patterns"].split(",")


def get_substitute_char(config):
    return config["substitute"]

DEFAULT_CONFIG = {
    "mode": "644",
    "messy_chars": "[]()'*?$#`|\\\" ",
    "substitute": "_",
    "temp_patterns": "*~;*.tmp;*.swp;*.bak",
}


def load_options(config_file):
    if not config_file.exists():
        return DEFAULT_CONFIG

    config = {}
    with open(config_file, "r") as file_handle:
        lines = file_handle.readlines()
    for line in lines:
        key, value = line.split("=", 1)
        config[key.strip()] = value.strip()
    return config


class Config:
    def __init__(self, options):
        self.mode = int(options["mode"], 8)
        self.messy_chars = list(options["messy_chars"])
        self.substitute = options["substitute"]
        self.temp_patterns = options["temp_patterns"].split(";")

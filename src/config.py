DEFAULT_CONFIG = {
    "mode": "644",
    "messy_chars": "[]()'*?$#`|\\\" ",
    "substitute": "_",
    "temp_patterns": "*~,*.tmp,*.swp,*.bak",
}


class Config:
    def __init__(self, config_file):
        cfg = self._load_from_file(config_file)
        self.mode = int(cfg["mode"], 8)
        self.messy_chars = list(cfg["messy_chars"])
        self.substitute = cfg["substitute"]
        self.temp_patterns = cfg["temp_patterns"].split(";")

    def _load_from_file(self, config_file):
        config = {}
        with open(config_file, "r") as file_handle:
            lines = file_handle.readlines()

        for line in lines:
            key, value = line.split("=", 1)
            config[key.strip()] = value.strip()

        return config

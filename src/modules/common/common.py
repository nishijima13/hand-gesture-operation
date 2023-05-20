import yaml


def load_config(
    config_path: str
):
    """Load config from yaml file.

    Args:
        config_path (str): Path to the config file.

    Returns:
        config (dict): Config dictionary.
    """
    with open(config_path, 'r') as f:
        config = yaml.load(f, Loader=yaml.Loader)
    return config

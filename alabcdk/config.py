from typing import TypedDict, Any, Dict
import tomli as toml


class ConfigOptions(TypedDict, total=False):
    """Options for loading configuration from TOML files."""

    deployment_name: str
    environment_name: str
    context: Dict[str, Any]


def load_toml_config_files(options: ConfigOptions) -> ConfigOptions:
    """Function to implement configuration loading from TOML files.

    The configuration data is loaded from the following files, in order:

    - The environment name, followed by
      ".toml"
    - The deployment name, followed by ".toml"
    - The deployment name, followed by "-", followed by the environment name,
      followed by ".toml"
    """
    deployment_name = options.get("deployment_name", "")
    env_name = options.get("environment_name", "")
    config_paths = []
    if env_name != "":
        config_paths.append(f"{env_name}.toml")
    if deployment_name != "":
        config_paths.append(f"{deployment_name}.toml")
    if deployment_name != "" and env_name != "":
        config_paths.append(f"{deployment_name}-{env_name}.toml")

    config_result: dict[str, Any] = options.get("context", {})
    for config_path in config_paths:
        try:
            with open(config_path, "rb") as f:
                config_result.update(toml.load(f))
        except FileNotFoundError:
            pass
    return config_result

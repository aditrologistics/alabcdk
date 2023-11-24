from typing import TypedDict, Any, Dict, List, Union
import tomli as toml
import constructs as cons


class ConfigOptions(TypedDict, total=False):
    """Options for loading configuration from TOML files."""

    deployment_name: str
    environment_name: str
    context: Dict[str, Any]


def load_toml_config_files(options: ConfigOptions) -> Dict[str, Any]:
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


def get_config_data(
    config: Dict[str, Any], key: Union[str, List[str]], default_value: Any = None
) -> Union[Any, None]:
    """Get a config data item"""
    if isinstance(key, str):
        return config.get(key, default_value)
    else:
        config = config.get(key[0])
        for k in key[1:]:
            if config is None:
                return default_value
            config = config.get(k)
        return config


def get_context_data(
    scope: cons.Construct, key: Union[str, List[str]]
) -> Union[Any, None]:
    """Get the context data for a construct"""
    if isinstance(key, str):
        return scope.node.try_get_context(key)
    else:
        context = scope.node.try_get_context(key[0])
        for k in key[1:]:
            if context is None:
                break
            context = context.get(k)
        return context

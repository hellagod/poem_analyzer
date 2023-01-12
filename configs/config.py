import logging
import os
import sys

from dynaconf import Dynaconf


def check_main_config():
    project_path = sys.path[0]
    
    if os.path.exists(os.path.join(project_path, 'configs', 'config.toml')):
        path_config = os.path.join(project_path, 'configs', 'config.toml')
        envvar_prefix = "API"
    else:
        err_string = ('File of configuration is missing. Add the config file' +
                    ' to directory' + project_path)
        logging.error(err_string)
        exit()
    return path_config, envvar_prefix


def load_settings(path_config: str = '', envvar_prefix: str = 'API', redis=False) -> Dynaconf:
    if not path_config:
        path, env = check_main_config()
    else:
        path, env = path_config, envvar_prefix
        
    dyn = Dynaconf(
        envvar_prefix=env,  # export envvars with `export DYNACONF_FOO=bar`
        settings_files=[path],  # Load these files in the order
        redis_enabled=redis,
    )
    return dyn


settings = load_settings()
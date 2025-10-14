import glob
import os
from pathlib import Path
from dotenv import find_dotenv, load_dotenv


import yaml

from pepper import logger
from pepper.utils import get_process_path

from .types.options import ServerOption
from .types.res_options import ResolverOption

_ = load_dotenv(find_dotenv())

class Config:
    options: ServerOption = ServerOption()
    resolvers: list[ResolverOption] = []
    app_path: str = ""
    config_path: str = "."

    def __init__(self):
        self.app_path = get_process_path()
        self.config_path = os.path.join(self.app_path, "config")
        if not os.path.isdir(self.config_path):
            raise ValueError(f"config directory '{self.config_path}' does not exist.")

        yaml_files = glob.glob(os.path.join(self.config_path, "*.yaml")) + glob.glob(
            os.path.join(self.config_path, "*.yml")
        )

        for file_path in yaml_files:
            try:
                with open(file_path, "r", encoding="utf-8") as file:
                    file_name = Path(file_path)
                    config_name: str = file_name.stem
                    data = yaml.safe_load(file)  # pyright: ignore[reportAny]
                    is_valid = isinstance(data, dict)

                    if is_valid and config_name == "options":
                        validated_option = ServerOption(**data)  # pyright: ignore[reportUnknownArgumentType]
                        self.options = validated_option
                    elif is_valid and config_name.startswith("sync"):
                        resolver = ResolverOption(**data)  # pyright: ignore[reportUnknownArgumentType]
                        self.resolvers.append(resolver)
                    else:
                        logger.warning(
                            f"config - {file_path} schema is incorrect. Skipping."
                        )
            except Exception as e:
                logger.error(f"Error loading {file_path}: {e}")

    async def load(self):
        pass

config = Config()


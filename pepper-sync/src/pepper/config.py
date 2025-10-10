import glob
import os
from pathlib import Path
from typing import List

import yaml

from pepper.logger import logger
from pepper.utils import get_process_path

from .types.options import ServerOption
from .types.res_options import ResolverOption


class Config:
    options: ServerOption = ServerOption()
    resolvers: List[ResolverOption] = []
    app_path = ""
    config_path = "."

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
                    data = yaml.safe_load(file)
                    is_valid = isinstance(data, dict)

                    if is_valid and config_name == "options":
                        validated_option = ServerOption(**data)
                        self.options = validated_option
                    elif is_valid and config_name.startswith("sync"):
                        resolver = ResolverOption(**data)
                        self.resolvers.append(resolver)
                    else:
                        logger.warning(
                            f"config - {file_path} schema is incorrect. Skipping."
                        )
            except Exception as e:
                logger.error(f"Error loading {file_path}: {e}")

        # print("---->>", self.resolvers)

    async def load(self):
        pass

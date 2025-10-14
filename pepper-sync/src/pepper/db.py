from functools import partial

from pepper.settings import config
from tortoise.contrib.fastapi import RegisterTortoise


TORTOISE_ORM = {
    "connections": {
        "default": config.options.database
        # "default": "mysql://pepper:pepper@127.0.0.1:3306/pepper"
        # "default": "postgres://pepper:pepper@127.0.0.1:5432/pepper"
    },
    "apps": {
        "models": {
            "models": ["pepper.models", "aerich.models"],
            "default_connection": "default",
        },
    },
}

register_orm = partial(
    RegisterTortoise,
    config=TORTOISE_ORM,
    modules={"models": ["pepper.models"],},
    generate_schemas=True,
    add_exception_handlers=True,
)


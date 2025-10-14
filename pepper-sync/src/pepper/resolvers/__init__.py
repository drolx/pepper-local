from typing import Literal
from fastapi_crons import CronJob  # pyright: ignore[reportMissingTypeStubs]
from pepper.utils import list_subclass_names  # pyright: ignore[reportUnknownVariableType]
from pepper import config, logger
from .base import BaseResolver
from .traccar import TraccarResolver
from .wox import WoxResolver
from .ihs import IhsResolver

__all__ = ["BaseResolver", "WoxResolver", "TraccarResolver", "IhsResolver"]

def get_children():
    children = list_subclass_names(BaseResolver)
    print(children)

# Dynamically initialize resolver class using its name as a string
def create_resolver_instance(class_name, *args, **kwargs):  # pyright: ignore[reportUnknownParameterType, reportMissingParameterType, reportAny]
    """
    Dynamically create an instance of a class by its name.
    """
    if class_name in globals():
        return globals()[class_name](*args, **kwargs)  # pyright: ignore[reportAny]
    else:
        raise ValueError(f"Class '{class_name}' not found.")

        
class ResolverState():
    name: str
    enable: bool
    interval: str
    resover_type: str
    resolver_direction: Literal["in", "out"]
    class_name: str
    instance: BaseResolver

def load_resolvers() -> list[ResolverState]:
    resolvers: list[ResolverState] = []
    for res in config.resolvers:
        resolver_type = res.type.capitalize()
        resolver_class_name = f"{resolver_type}Resolver"
        state = ResolverState()
        state.name = res.name
        state.interval = res.interval or "* * * * *"
        state.class_name = resolver_class_name
        state.resover_type = res.type
        state.resolver_direction = res.direction
        state.enable = res.enable or False
        state.instance = create_resolver_instance(resolver_class_name, res)  # pyright: ignore[reportAny]

        resolvers.append(state)

    return resolvers

def load_resolver_jobs() -> list[CronJob]:
    local_jobs: list[CronJob] = []
    for res in load_resolvers():
        if res.enable == True:
            logger.info(f"Loading {res.name} resolver")
            job = CronJob(
                func=res.instance.process,
                expr=res.interval or "* * * * *",
                name=res.name,
                tags=[f"resolver-{res.resolver_direction}", res.resover_type]
            )
            local_jobs.append(job)

    return local_jobs

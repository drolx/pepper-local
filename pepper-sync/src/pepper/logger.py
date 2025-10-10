import logging

logging.basicConfig(
    level=logging.INFO, format="[%(levelname)s] %(asctime)s %(message)s"
)
logging.getLogger("sqlalchemy").setLevel(logging.ERROR)
logging.getLogger("sqlalchemy.pool").setLevel(logging.ERROR)
logging.getLogger("sqlalchemy.engine.Engine.app").setLevel(logging.ERROR)
logging.getLogger("alembic.runtime.migration").setLevel(logging.ERROR)

logger = logging.getLogger(__name__)

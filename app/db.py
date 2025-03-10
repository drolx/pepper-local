# Copyright (c) 2025 <Godwin peter. O>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#
#  Project: thalia
#  Author: Godwin peter. O (me@godwin.dev)
#  Created At: Mon 06 Jan 2025 11:47:32
#  Modified By: Godwin peter. O (me@godwin.dev)
#  Modified At: Mon 06 Jan 2025 11:47:32

from typing import TypeVar

from alembic import command
from alembic.config import Config
from sqlalchemy import create_engine
from sqlalchemy.ext.serializer import dumps, loads
from sqlalchemy.orm import Session, scoped_session, sessionmaker

from app import app_logger, get_process_path
from app.settings import DATABASE_LOG, DATABASE_URL
from app.models import Base

T = TypeVar("T")
engine = create_engine(
    DATABASE_URL,
    echo=DATABASE_LOG,
    future=True,
    logging_name="app",
    hide_parameters=True,
)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
ScopedSession = scoped_session(SessionLocal)


def get_db() -> Session:
    return ScopedSession()


async def run_migrations():
    try:
        path = get_process_path("alembic.ini")
        alembic_cfg = Config(path)
        # alembic_cfg.set_main_option('script_location', 'migrations')
        # alembic_cfg.set_main_option("keys", "root,sqlalchemy,alembic,app")
        command.upgrade(alembic_cfg, "head")
        app_logger.info("Migrations applied successfully.")
    except Exception as e:
        app_logger.error(f"Error commiting migrations - {e}")


async def init_db() -> None:
    try:
        Base.metadata.create_all(bind=engine)
        # await run_migrations()
    except Exception as e:
        app_logger.error(f"Error initializing database - {e}")


def alchemy_serializer(obj: object):
    serialized_obj = dumps(obj)
    obj = loads(serialized_obj)

    return obj

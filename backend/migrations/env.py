from logging.config import fileConfig

from flask import current_app
from alembic import context

# --- This is the only part we need to change from the default ---

# 1. Import your db object and all of your models
#    This is crucial so that Alembic knows what tables your app needs.
from app.extensions import db
from app.models.user import User
from app.models.skill import Skill
from app.models.match import Match
from app.models.message import Message

# 2. Get the Alembic Config object
config = context.config

# 3. Tell Alembic to use the config from the app that's ALREADY RUNNING
#    This is the magic line that solves the "two kitchens" problem.
#    It gets the database URL from the app the `flask` command created.
config.set_main_option("sqlalchemy.url", current_app.config.get("SQLALCHEMY_DATABASE_URI"))

# 4. Get the metadata from your app's db object
target_metadata = db.metadata

# --- The rest is standard Alembic configuration ---

# Interpret the config file for Python logging.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    # Use the engine from the app's db object
    connectable = db.get_engine()

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()



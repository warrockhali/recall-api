from alembic import context
from sqlalchemy import pool

from recall_api.db.models import Base
from recall_api.db.session import get_database_url


def run_migrations_offline() -> None:
    context.configure(
        url=get_database_url(),
        target_metadata=Base.metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    from sqlalchemy import create_engine

    engine = create_engine(
        get_database_url(),
        connect_args={"options": "-c timezone=UTC"},
        poolclass=pool.NullPool,
    )
    with engine.connect() as connection:
        context.configure(connection=connection, target_metadata=Base.metadata)
        with context.begin_transaction():
            context.run_migrations()
    engine.dispose()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()

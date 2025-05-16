from advanced_alchemy.extensions.fastapi import (
    AsyncSessionConfig,
    SQLAlchemyAsyncConfig,
)

sqlalchemy_config = SQLAlchemyAsyncConfig(
    connection_string='sqlite+aiosqlite:///test.sqlite',
    session_config=AsyncSessionConfig(expire_on_commit=False),
    create_all=True,
    commit_mode='autocommit',
)

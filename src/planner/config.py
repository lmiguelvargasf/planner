from functools import cached_property

from pydantic import PostgresDsn
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: PostgresDsn
    USE_TEST_DB: bool = False

    @cached_property
    def db_url(self) -> str:
        url = self.DATABASE_URL.unicode_string()
        if self.USE_TEST_DB:
            return f"{url}_test"
        return url


settings = Settings()

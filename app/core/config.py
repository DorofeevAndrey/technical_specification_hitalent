from pydantic import ConfigDict
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Optional full DB URL (useful for tests / one-line config).
    # Example: postgresql+psycopg2://user:pass@db:5432/hitalent
    # Example (tests): sqlite+pysqlite:///./test.db
    DATABASE_URL: str | None = None

    DB_USER: str = "postgres"
    DB_PASS: str = "postgres"
    DB_HOST: str = "localhost"
    DB_PORT: str = "5432"
    DB_NAME: str = "hitalent"

    @property
    def database_url(self) -> str:
        if self.DATABASE_URL:
            return self.DATABASE_URL
        return (
            f"postgresql+psycopg2://{self.DB_USER}:{self.DB_PASS}"
            f"@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        )

    model_config = ConfigDict(env_file=".env")


settings = Settings()
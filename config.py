from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict


class RunConfig(BaseModel):
    host: str
    port: int


class DatabaseConfig(BaseModel):
    url: str
    echo: bool = False

    naming_convention: dict[str, str] = {
        'ix': 'ix_%(column_0_label)s',
        'uq': 'uq_%(table_name)s_%(column_0_N_name)s',
        'ck': 'ck_%(table_name)s_%(constraint_name)s',
        'fk': 'fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s',
        'pk': 'pk_%(table_name)s',
    }


class WeatherConfig(BaseModel):
    url: str


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=('.env',),  # value of next parameter overrides value previous one.
        case_sensitive=False,
        env_nested_delimiter='__',
    )
    token: str
    base_webhook_url: str
    webhook_path: str
    webhook_secret: str
    email: str
    domain: str
    admin_ids: frozenset[int]

    run: RunConfig
    db: DatabaseConfig
    weather: WeatherConfig


settings = Settings()

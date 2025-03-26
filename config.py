from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=('.env',),  # value of next parameter overrides value previous one.
        case_sensitive=False,
    )

    token: str
    url: str
    lat: float
    lon: float


settings = Settings()

from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    # WFS Configuration
    wfs_url: str = "https://gds.hessen.de/wfs/hlnug/wasserschutz"
    wfs_layer: str = "he_wasserschutz_zonen"
    wfs_page_size: int = 1000
    wfs_max_retries: int = 3
    wfs_use_fixture: bool = True 

    # Database Configuration (Staging only)
    postgres_host: str = "localhost"
    postgres_port: int = 5432
    postgres_user: str = "postgres"
    postgres_password: str = "postgres"
    postgres_db: str = "iris_staging"

    # Target Table
    staging_schema: str = "iris_staging"
    staging_table: str = "water_protection_zones"
    target_srid: int = 25832

settings = Settings()
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASS: str
    DB_NAME: str

    # Данные для jwt-токена
    SECRET_KEY: str
    ALGORIHM: str


    # Метод получения адреса к БД
    @property
    def get_db_url(self):
        return (
            f'postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}'
            f'@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}'
        )
    
    
    # Откуда брать чувствительные данные 
    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()




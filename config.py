from pydantic_settings import BaseSettings # type: ignore

class Settings(BaseSettings):
    app_name: str = "API de receitas"
    debug: bool = True
    database_url: str 

    class config:
        env_file = ".env"

settings = Settings()        

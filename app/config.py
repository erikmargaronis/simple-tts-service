from pydantic_settings import BaseSettings
from pydantic import Field

class Config(BaseSettings):
    tts_home: str = Field(..., env='TTS_HOME')
    host: str = Field(..., env='HOST')
    port: int = Field(..., env='PORT')
    debug: int = Field(..., env='DEBUG')

    class Config:
        env_file = './.env'

config = Config()

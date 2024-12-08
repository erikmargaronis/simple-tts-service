import os
from dotenv import load_dotenv
from pydantic_settings import BaseSettings
from pydantic import Field

# Set TTS_HOME so that Coqui can read it.
load_dotenv(dotenv_path='./.env')
os.environ['TTS_HOME'] = os.getenv('TTS_HOME', './data/')

class Config(BaseSettings):
    """
    Configuration class for managing environment variables using Pydantic.

    Attributes:
        tts_home (str): Path to the TTS home directory, loaded from the 'TTS_HOME' environment variable.
        host (str): Hostname or IP address for the application, loaded from the 'HOST' environment variable.
        port (int): Port number for the application, loaded from the 'PORT' environment variable.
        debug (int): Debug mode flag (e.g., 1 for debug, 0 for production), loaded from the 'DEBUG' environment variable.

    Notes:
        Environment variables are loaded from the specified `.env` file by default.
    """
    tts_home: str = Field(default='./data/', env='TTS_HOME', description='Path to Coqui model directory')
    host: str = Field(default='127.0.0.1', env='HOST', description='Hostname or IP address for the application')
    port: int = Field(default=8080, env='PORT', description='Port number for the application')
    debug: int = Field(default=0, env='DEBUG', description='Debug mode flag')

    class Config:
        """Nested configuration class for Pydantic settings."""
        env_file = './.env'

config = Config()

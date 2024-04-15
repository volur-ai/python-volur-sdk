from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class VolurApiSettings(BaseSettings):
    """Settings for Völur API client.

    This class is used to obtain required configurations for the client to work
    properly.

    This class requires two environment variables to be set:

    - `VOLUR_API_ADDRESS`: Address of the Völur API server,
    - `VOLUR_API_TOKEN`: Token for authenticating to the Völur API server.

    Please contact Völur to obtain the endpoint address and the token.

    Examples:
        ```python title="example.py" linenums="1"
        settings = VolurApiSettings()
        ```
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_prefix="VOLUR_API_",
    )
    address: str
    token: SecretStr
    debug: bool = Field(False, description="Enable debug mode")

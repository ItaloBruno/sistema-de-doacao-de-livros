import os


class VariaveisDeAmbiente:
    URL_POSTGRES: str = os.environ["URL_POSTGRES"]
    CHAVE_SECRETA_HASH: str = os.environ["CHAVE_SECRETA_HASH"]
    CHAVE_SECRETA_JWT: str = os.environ["CHAVE_SECRETA_JWT"]

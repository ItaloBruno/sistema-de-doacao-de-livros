# ruff: noqa
from sqlalchemy import MetaData
from sqlalchemy.orm import registry

metadata = MetaData()
mapper_registry = registry(metadata=metadata)


def inicializar_mapeamento_orm():
    from contextos_de_negocio.doacao.repositorio import (
        orm,
    )
    from contextos_de_negocio.doador.repositorio import (
        orm,
    )
    from contextos_de_negocio.instituicao.repositorio import (
        orm,
    )
    from contextos_de_negocio.livros.repositorio import (
        orm,
    )

import pytest

from contextos_de_negocio.doacao.casos_de_uso.criar_doacao import CriarDoacao
from contextos_de_negocio.doacao.casos_de_uso.dtos import (
    EntradaCriarDoacaoCasoDeUso,
)
from contextos_de_negocio.doacao.excecoes import (
    InstituicaoNaoEncontrada,
    LivroNaoEncontrado,
)
from contextos_de_negocio.doador.dominio.objetos_de_valor import DoadorId
from contextos_de_negocio.instituicao.dominio.objetos_de_valor import (
    InstituicaoId,
)
from contextos_de_negocio.livros.dominio.objetos_de_valor import LivroId
from testes.contextos_de_negocio.doacao.casos_de_uso import (
    obter_uow_fake,
)


def test_deve_criar_doacao_com_sucesso():
    doador_id = DoadorId.gerar()
    instituicao_id = InstituicaoId.gerar()
    livro_id_1 = LivroId.gerar()
    livro_id_2 = LivroId.gerar()

    uow = obter_uow_fake()
    uow.repositorio_doacoes.adicionar_instituicao_existente(instituicao_id)
    uow.repositorio_doacoes.adicionar_livro_existente(livro_id_1)
    uow.repositorio_doacoes.adicionar_livro_existente(livro_id_2)

    entrada = EntradaCriarDoacaoCasoDeUso(
        instituicao_id=str(instituicao_id),
        livros_ids=[str(livro_id_1), str(livro_id_2)],
    )

    caso_de_uso = CriarDoacao(
        entrada=entrada,
        doador_id=doador_id,
        obter_uow=lambda: uow,
    )
    saida = caso_de_uso.executar()

    assert saida.id is not None
    assert saida.doador_id == str(doador_id)
    assert saida.instituicao_id == str(instituicao_id)
    assert len(saida.livros_ids) == 2
    assert str(livro_id_1) in saida.livros_ids
    assert str(livro_id_2) in saida.livros_ids


def test_deve_criar_doacao_com_um_livro():
    doador_id = DoadorId.gerar()
    instituicao_id = InstituicaoId.gerar()
    livro_id = LivroId.gerar()

    uow = obter_uow_fake()
    uow.repositorio_doacoes.adicionar_instituicao_existente(instituicao_id)
    uow.repositorio_doacoes.adicionar_livro_existente(livro_id)

    entrada = EntradaCriarDoacaoCasoDeUso(
        instituicao_id=str(instituicao_id),
        livros_ids=[str(livro_id)],
    )

    caso_de_uso = CriarDoacao(
        entrada=entrada,
        doador_id=doador_id,
        obter_uow=lambda: uow,
    )
    saida = caso_de_uso.executar()

    assert saida.id is not None
    assert saida.doador_id == str(doador_id)
    assert saida.instituicao_id == str(instituicao_id)
    assert len(saida.livros_ids) == 1
    assert str(livro_id) in saida.livros_ids


def test_deve_lancar_excecao_quando_instituicao_nao_existe():
    doador_id = DoadorId.gerar()
    instituicao_id_inexistente = InstituicaoId.gerar()
    livro_id = LivroId.gerar()

    uow = obter_uow_fake()
    uow.repositorio_doacoes.adicionar_livro_existente(livro_id)

    entrada = EntradaCriarDoacaoCasoDeUso(
        instituicao_id=str(instituicao_id_inexistente),
        livros_ids=[str(livro_id)],
    )

    caso_de_uso = CriarDoacao(
        entrada=entrada,
        doador_id=doador_id,
        obter_uow=lambda: uow,
    )

    with pytest.raises(InstituicaoNaoEncontrada):
        caso_de_uso.executar()


def test_deve_lancar_excecao_quando_livro_nao_existe():
    doador_id = DoadorId.gerar()
    instituicao_id = InstituicaoId.gerar()
    livro_id_inexistente = LivroId.gerar()

    uow = obter_uow_fake()
    uow.repositorio_doacoes.adicionar_instituicao_existente(instituicao_id)

    entrada = EntradaCriarDoacaoCasoDeUso(
        instituicao_id=str(instituicao_id),
        livros_ids=[str(livro_id_inexistente)],
    )

    caso_de_uso = CriarDoacao(
        entrada=entrada,
        doador_id=doador_id,
        obter_uow=lambda: uow,
    )

    with pytest.raises(LivroNaoEncontrado):
        caso_de_uso.executar()


def test_deve_lancar_excecao_quando_algum_livro_nao_existe():
    doador_id = DoadorId.gerar()
    instituicao_id = InstituicaoId.gerar()
    livro_id_1 = LivroId.gerar()
    livro_id_2_inexistente = LivroId.gerar()

    uow = obter_uow_fake()
    uow.repositorio_doacoes.adicionar_instituicao_existente(instituicao_id)
    uow.repositorio_doacoes.adicionar_livro_existente(livro_id_1)

    entrada = EntradaCriarDoacaoCasoDeUso(
        instituicao_id=str(instituicao_id),
        livros_ids=[str(livro_id_1), str(livro_id_2_inexistente)],
    )

    caso_de_uso = CriarDoacao(
        entrada=entrada,
        doador_id=doador_id,
        obter_uow=lambda: uow,
    )

    with pytest.raises(LivroNaoEncontrado):
        caso_de_uso.executar()

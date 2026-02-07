from datetime import datetime
from typing import Optional

from sistema_de_doacao_de_livros.schemas import (
    DoacaoDB,
    DoadorDB,
    InstituicaoDB,
    LivroDB,
    StatusDoacao,
)

doadores: list[DoadorDB] = []
instituicoes: list[InstituicaoDB] = []
livros: list[LivroDB] = []
doacoes: list[DoacaoDB] = []
livros_nas_doacoes: list[dict] = []


def buscar_doador_por_email(email: str) -> Optional[DoadorDB]:
    for doador in doadores:
        if doador.email == email:
            return doador
    return None


def buscar_doador_por_id(doador_id: int) -> Optional[DoadorDB]:
    for doador in doadores:
        if doador.id == doador_id:
            return doador
    return None


def buscar_instituicao_por_email(email: str) -> Optional[InstituicaoDB]:
    for instituicao in instituicoes:
        if instituicao.email == email:
            return instituicao
    return None


def buscar_instituicao_por_id(instituicao_id: int) -> Optional[InstituicaoDB]:
    for instituicao in instituicoes:
        if instituicao.id == instituicao_id:
            return instituicao
    return None


def buscar_livro_por_id(livro_id: int) -> Optional[LivroDB]:
    for livro in livros:
        if livro.id == livro_id:
            return livro
    return None


def buscar_livros_por_titulo(titulo: str) -> list[LivroDB]:
    resultado = []
    titulo_lower = titulo.lower()
    for livro in livros:
        if titulo_lower in livro.titulo.lower():
            resultado.append(livro)
    return resultado


def buscar_doacao_por_id(doacao_id: int) -> Optional[DoacaoDB]:
    for doacao in doacoes:
        if doacao.id == doacao_id:
            return doacao
    return None


def buscar_doacoes_por_doador(doador_id: int) -> list[DoacaoDB]:
    return [d for d in doacoes if d.doador_id == doador_id]


def buscar_doacoes_por_instituicao(instituicao_id: int) -> list[DoacaoDB]:
    return [d for d in doacoes if d.instituicao_id == instituicao_id]


def buscar_livros_da_doacao(doacao_id: int) -> list[dict]:
    return [
        livro
        for livro in livros_nas_doacoes
        if livro["doacao_id"] == doacao_id
    ]


def contar_livros_da_doacao(doacao_id: int) -> int:
    return len([
        livro
        for livro in livros_nas_doacoes
        if livro["doacao_id"] == doacao_id
    ])


def incrementar_livros_recebidos_instituicao(
    instituicao_id: int, quantidade: int
):
    instituicao = buscar_instituicao_por_id(instituicao_id)
    if instituicao:
        instituicao.livros_recebidos += quantidade


def livro_esta_em_doacao_pendente(livro_id: int) -> bool:
    for livro_doacao in livros_nas_doacoes:
        if livro_doacao["livro_id"] == livro_id:
            doacao = buscar_doacao_por_id(livro_doacao["doacao_id"])
            if doacao and doacao.status == StatusDoacao.PENDENTE:
                return True
    return False


def atualizar_doador(
    doador_id: int,
    nome: str,
    email: str,
    telefone: str,
    senha: Optional[str] = None,
) -> Optional[DoadorDB]:
    for i, doador in enumerate(doadores):
        if doador.id != doador_id:
            continue
        doadores[i] = DoadorDB(
            id=doador.id,
            nome=nome,
            email=email,
            telefone=telefone,
            senha=senha if senha else doador.senha,
        )
        return doadores[i]
    return None


def atualizar_instituicao(
    instituicao_id: int,
    nome: str,
    email: str,
    descricao: str,
    data_fundacao,
    endereco: str,
    foto_url: Optional[str] = None,
    site: Optional[str] = None,
    senha: Optional[str] = None,
) -> Optional[InstituicaoDB]:
    for i, instituicao in enumerate(instituicoes):
        if instituicao.id != instituicao_id:
            continue
        instituicoes[i] = InstituicaoDB(
            id=instituicao.id,
            nome=nome,
            email=email,
            descricao=descricao,
            data_fundacao=data_fundacao,
            endereco=endereco,
            foto_url=foto_url,
            site=site,
            senha=senha if senha else instituicao.senha,
            data_registro=instituicao.data_registro,
            livros_recebidos=instituicao.livros_recebidos,
        )
        return instituicoes[i]
    return None


def inicializar_instituicoes_teste():
    instituicoes.append(
        InstituicaoDB(
            id=1,
            nome="Biblioteca Comunitária Chico Parafuso",
            email="contato@bibliotecachicoparafuso.org",
            senha="senha123",
            descricao=(
                "Espaço cultural dedicado à promoção da leitura e cultura no Parque Araxá. "
                "Oferece atividades de contação de histórias, oficinas literárias e acesso gratuito a um acervo diversificado."
            ),
            data_fundacao=datetime(2010, 5, 15).date(),
            data_registro=datetime(2024, 1, 10, 10, 0, 0),
            livros_recebidos=150,
            foto_url="/static/imagens/biblioteca_comunitaria_chico_parafuso.jpeg",
            site="https://www.instagram.com/bibliotecachicoparafuso",
            endereco="Avenida Jovita Feitosa, 843 - Parque Araxá, Fortaleza - CE",
        )
    )

    instituicoes.append(
        InstituicaoDB(
            id=2,
            nome="Biblioteca Comunitária Leônidas Magalhães",
            email="contato@leonidasmagalhaes.org",
            senha="senha123",
            descricao=(
                "Biblioteca comunitária que promove o acesso democrático à leitura no bairro Álvaro Weyne. "
                "Realiza saraus literários, clubes de leitura e atividades educativas para todas as idades."
            ),
            data_fundacao=datetime(2015, 8, 20).date(),
            data_registro=datetime(2024, 2, 5, 14, 30, 0),
            livros_recebidos=320,
            foto_url="/static/imagens/biblioteca_comunitaria_leonidas_magalhaes.png",
            site="https://www.instagram.com/leonidasmagalhaes1",
            endereco="Rua Ferreira dos Santos, 197 - Álvaro Weyne, Fortaleza - CE",
        )
    )

    instituicoes.append(
        InstituicaoDB(
            id=3,
            nome="Biblioteca Comunitária Sorriso da Criança",
            email="contato@bibliotecasorriso.org",
            senha="senha123",
            descricao=(
                "Biblioteca voltada para o público infantil e juvenil, incentivando o hábito da leitura desde a infância. "
                "Promove contação de histórias, teatro de fantoches e atividades lúdicas educativas."
            ),
            data_fundacao=datetime(2012, 3, 10).date(),
            data_registro=datetime(2024, 3, 1, 9, 15, 0),
            livros_recebidos=85,
            foto_url="/static/imagens/biblioteca_comunitaria_sorriso_da_crianca.png",
            site="https://www.instagram.com/bibliotecasorriso",
            endereco="Rua Planalto, 167 - Presidente Kennedy, Fortaleza - CE",
        )
    )


def inicializar_livros_teste():
    livros.append(
        LivroDB(
            id=1,
            titulo="Dom Casmurro",
            autores=["Machado de Assis"],
            isbn="978-8535911664",
            foto_url="/static/imagens/dom_casmurro.jpeg",
            observacao="Livro em bom estado, capa dura",
        )
    )

    livros.append(
        LivroDB(
            id=2,
            titulo="O Cortiço",
            autores=["Aluísio Azevedo"],
            isbn="978-8508040704",
            foto_url="/static/imagens/o_cortico.jpeg",
            observacao="Algumas páginas amareladas",
        )
    )

    livros.append(
        LivroDB(
            id=3,
            titulo="Grande Sertão: Veredas",
            autores=["Guimarães Rosa"],
            isbn="978-8535908770",
            foto_url="/static/imagens/grande_sertao.jpg",
        )
    )

    livros.append(
        LivroDB(
            id=4,
            titulo="Capitães da Areia",
            autores=["Jorge Amado"],
            isbn="978-8535914063",
            foto_url="/static/imagens/capitaoes_da_areia.jpeg",
        )
    )

    livros.append(
        LivroDB(
            id=5,
            titulo="Memórias Póstumas de Brás Cubas",
            autores=["Machado de Assis"],
            isbn="978-8535911657",
            foto_url="/static/imagens/memorias_postumas_de_bras_cubas.jpg",
        )
    )


def inicializar_doadores_teste():
    doadores.append(
        DoadorDB(
            id=1,
            nome="João Silva",
            email="joao@email.com",
            senha="senha123",
            telefone="(11) 98765-4321",
        )
    )


def inicializar_doacoes_teste():
    doacoes.append(
        DoacaoDB(
            id=1,
            instituicao_id=1,
            doador_id=1,
            data_criacao=datetime(2024, 11, 15, 10, 30, 0),
            status=StatusDoacao.PENDENTE,
        )
    )


def inicializar_livros_nas_doacoes_teste():
    livros_nas_doacoes.append({
        "id": 1,
        "doacao_id": 1,
        "livro_id": 1,
    })

    livros_nas_doacoes.append({
        "id": 2,
        "doacao_id": 1,
        "livro_id": 2,
    })


def inicializar_dados_teste():
    inicializar_instituicoes_teste()
    inicializar_livros_teste()
    inicializar_doadores_teste()
    inicializar_doacoes_teste()
    inicializar_livros_nas_doacoes_teste()

from collections.abc import Callable
from datetime import date

from contextos_de_negocio.instituicao.casos_de_uso.dtos import (
    EntradaCriarInstituicaoCasoDeUso,
    SaidaCriarInstituicao,
)
from contextos_de_negocio.instituicao.dominio.entidades import Instituicao
from contextos_de_negocio.instituicao.dominio.objetos_de_valor import (
    DadosParaCriacaoInstituicao,
    DataFundacaoInstituicao,
    DescricaoInstituicao,
    EmailInstituicao,
    EnderecoInstituicao,
    FotoInstituicao,
    NomeInstituicao,
    SenhaInstituicao,
    SiteInstituicao,
    TelefoneInstituicao,
)
from contextos_de_negocio.instituicao.excecoes import EmailJaCadastrado
from utilitarios.provedor_de_armazenamento import ProvedorDeArmazenamento
from utilitarios.provedor_de_hash import ProvedorDeHash
from utilitarios.unidade_de_trabalho import (
    UnidadeDeTrabalhoAbstrata,
)


class CriarInstituicao:
    def __init__(
        self,
        entrada: EntradaCriarInstituicaoCasoDeUso,
        obter_uow: Callable[[], UnidadeDeTrabalhoAbstrata],
        provedor_de_hash: ProvedorDeHash,
        provedor_de_armazenamento: ProvedorDeArmazenamento,
    ):
        self.entrada = entrada
        self.obter_uow = obter_uow
        self.provedor_de_hash = provedor_de_hash
        self.provedor_de_armazenamento = provedor_de_armazenamento

    def executar(self) -> SaidaCriarInstituicao:
        with self.obter_uow() as uow:
            self._validar_email_disponivel(uow)

            senha_hash = self.provedor_de_hash.gerar_hash(self.entrada.senha)
            foto_obj = self._fazer_upload_foto()

            dados = DadosParaCriacaoInstituicao(
                nome=NomeInstituicao(self.entrada.nome),
                email=EmailInstituicao(self.entrada.email),
                telefone=TelefoneInstituicao(self.entrada.telefone),
                senha=SenhaInstituicao(senha_hash),
                descricao=DescricaoInstituicao(self.entrada.descricao),
                data_fundacao=DataFundacaoInstituicao(
                    date.fromisoformat(self.entrada.data_fundacao)
                ),
                endereco=EnderecoInstituicao(self.entrada.endereco),
                site=SiteInstituicao(self.entrada.site)
                if self.entrada.site
                else None,
                foto=foto_obj,
            )

            instituicao = Instituicao.criar(dados)

            instituicao_criada = uow.repositorio_instituicoes.adicionar(
                instituicao
            )
            uow.commit()

            return SaidaCriarInstituicao(
                id=str(instituicao_criada.id),
                nome=instituicao_criada.nome.valor,
                email=instituicao_criada.email.valor,
                telefone=instituicao_criada.telefone.valor,
                descricao=instituicao_criada.descricao.valor,
                data_fundacao=str(instituicao_criada.data_fundacao),
                endereco=instituicao_criada.endereco.valor,
                site=instituicao_criada.site.valor
                if instituicao_criada.site
                else None,
                foto=instituicao_criada.foto.valor
                if instituicao_criada.foto
                else None,
            )

    def _fazer_upload_foto(self) -> FotoInstituicao | None:
        if self.entrada.foto and self.entrada.nome_arquivo_foto:
            caminho_foto = self.provedor_de_armazenamento.fazer_upload(
                self.entrada.foto, self.entrada.nome_arquivo_foto
            )
            return FotoInstituicao(caminho_foto)
        return None

    def _validar_email_disponivel(
        self, uow: UnidadeDeTrabalhoAbstrata
    ) -> None:
        instituicao_existente = uow.repositorio_instituicoes.buscar_por_email(
            self.entrada.email
        )
        if instituicao_existente:
            raise EmailJaCadastrado()

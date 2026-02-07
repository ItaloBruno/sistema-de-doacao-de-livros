from collections.abc import Callable
from datetime import date
from uuid import UUID

from contextos_de_negocio.instituicao.casos_de_uso.dtos import (
    EntradaAtualizarInstituicaoCasoDeUso,
    SaidaAtualizarInstituicao,
)
from contextos_de_negocio.instituicao.dominio.entidades import Instituicao
from contextos_de_negocio.instituicao.dominio.objetos_de_valor import (
    DadosParaEdicaoInstituicao,
    DataFundacaoInstituicao,
    DescricaoInstituicao,
    EmailInstituicao,
    EnderecoInstituicao,
    FotoInstituicao,
    InstituicaoId,
    NomeInstituicao,
    SenhaInstituicao,
    SiteInstituicao,
    TelefoneInstituicao,
)
from contextos_de_negocio.instituicao.excecoes import (
    EmailJaCadastrado,
    InstituicaoNaoEncontrada,
)
from utilitarios.provedor_de_armazenamento import ProvedorDeArmazenamento
from utilitarios.unidade_de_trabalho import (
    UnidadeDeTrabalhoAbstrata,
)


class AtualizarInstituicao:
    def __init__(
        self,
        entrada: EntradaAtualizarInstituicaoCasoDeUso,
        obter_uow: Callable[[], UnidadeDeTrabalhoAbstrata],
        provedor_de_armazenamento: ProvedorDeArmazenamento,
    ):
        self.entrada = entrada
        self.obter_uow = obter_uow
        self.provedor_de_armazenamento = provedor_de_armazenamento

    def executar(self) -> SaidaAtualizarInstituicao:
        with self.obter_uow() as uow:
            instituicao = uow.repositorio_instituicoes.buscar_por_id(
                InstituicaoId(UUID(self.entrada.instituicao_id))
            )
            if not instituicao:
                raise InstituicaoNaoEncontrada()

            self._validar_email_disponivel(uow, instituicao)

            foto_obj = self._fazer_upload_foto(instituicao.foto)

            dados = DadosParaEdicaoInstituicao(
                senha_atual=SenhaInstituicao(self.entrada.senha_atual),
                nome=NomeInstituicao(self.entrada.nome),
                email=EmailInstituicao(self.entrada.email),
                telefone=TelefoneInstituicao(self.entrada.telefone),
                descricao=DescricaoInstituicao(self.entrada.descricao),
                data_fundacao=DataFundacaoInstituicao(
                    date.fromisoformat(self.entrada.data_fundacao)
                ),
                endereco=EnderecoInstituicao(self.entrada.endereco),
                site=SiteInstituicao(self.entrada.site)
                if self.entrada.site
                else None,
                foto=foto_obj,
                nova_senha=SenhaInstituicao(self.entrada.nova_senha)
                if self.entrada.nova_senha
                else None,
            )

            instituicao.editar(dados)

            instituicao_atualizada = uow.repositorio_instituicoes.adicionar(
                instituicao
            )
            uow.commit()

            return SaidaAtualizarInstituicao(
                id=str(instituicao_atualizada.id),
                nome=instituicao_atualizada.nome.valor,
                email=instituicao_atualizada.email.valor,
                telefone=instituicao_atualizada.telefone.valor,
                descricao=instituicao_atualizada.descricao.valor,
                data_fundacao=str(instituicao_atualizada.data_fundacao),
                endereco=instituicao_atualizada.endereco.valor,
                site=instituicao_atualizada.site.valor
                if instituicao_atualizada.site
                else None,
                foto=instituicao_atualizada.foto.valor
                if instituicao_atualizada.foto
                else None,
            )

    def _fazer_upload_foto(
        self, foto_atual: FotoInstituicao | None
    ) -> FotoInstituicao | None:
        if self.entrada.foto and self.entrada.nome_arquivo_foto:
            caminho_foto = self.provedor_de_armazenamento.fazer_upload(
                self.entrada.foto, self.entrada.nome_arquivo_foto
            )
            return FotoInstituicao(caminho_foto)
        return foto_atual

    def _validar_email_disponivel(
        self, uow: UnidadeDeTrabalhoAbstrata, instituicao: Instituicao
    ) -> None:
        if self.entrada.email != instituicao.email.valor:
            instituicao_existente = (
                uow.repositorio_instituicoes.buscar_por_email(
                    self.entrada.email
                )
            )
            if instituicao_existente:
                raise EmailJaCadastrado()

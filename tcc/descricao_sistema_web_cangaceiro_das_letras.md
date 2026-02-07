# Sistema Web Cangaceiro das Letras

## Resumo do Sistema

O **Cangaceiro das Letras** é uma plataforma web desenvolvida para facilitar a doação de livros entre doadores e instituições beneficentes. O sistema permite que doadores cadastrem livros e realizem doações para instituições cadastradas, enquanto as instituições podem gerenciar as solicitações recebidas.

## Tecnologias Utilizadas

### Backend
- **FastAPI**: Framework web moderno e de alta performance para construção de APIs
- **Pydantic**: Validação de dados e serialização
- **Python 3.13**: Linguagem de programação

### Frontend
- **Jinja2 Templates**: Motor de templates para renderização de páginas HTML
- **HTML/CSS/JavaScript**: Tecnologias web padrão

### Ferramentas de Desenvolvimento
- **Poetry**: Gerenciador de dependências e ambientes virtuais
- **Pytest**: Framework de testes unitários
- **Pytest-cov**: Cobertura de testes
- **Ruff**: Linter e formatador de código Python
- **Taskipy**: Gerenciador de tarefas de desenvolvimento

### Armazenamento
- **PostgreSQL**: Banco de dados relacional para persistência de dados
- **Google Cloud Storage (GCS)**: Armazenamento de fotos de livros e instituições

## Arquitetura do Sistema

### Estrutura de Diretórios

```
sistema_de_doacao_de_livros/
├── api/                    # API REST
│   ├── autenticacao.py     # Endpoints de login
│   ├── doacoes.py          # Endpoints de doações
│   ├── doadores.py         # Endpoints de doadores
│   ├── instituicoes.py     # Endpoints de instituições
│   ├── livros.py           # Endpoints de livros
│   ├── usuarios.py         # Endpoints de usuários (CRUD básico)
│   └── schemas.py          # Schemas da API
├── web/                    # Interface Web
│   ├── rotas/              # Rotas das páginas HTML
│   ├── templates/          # Templates Jinja2
│   └── static/             # Arquivos estáticos (CSS, JS, imagens)
├── app.py                  # Aplicação principal
├── banco_de_dados.py       # Camada de acesso ao PostgreSQL
└── schemas.py              # Modelos de dados Pydantic
```

## Modelos de Dados

### Doador
- **id**: Identificador único
- **nome**: Nome completo
- **email**: Email (único)
- **senha**: Senha de acesso
- **telefone**: Telefone de contato

### Instituição
- **id**: Identificador único
- **nome**: Nome da instituição
- **email**: Email (único)
- **senha**: Senha de acesso
- **descricao**: Descrição da instituição
- **data_fundacao**: Data de fundação
- **data_registro**: Data de cadastro no sistema
- **livros_recebidos**: Contador de livros recebidos
- **foto_url**: URL da foto da instituição
- **site**: Site institucional (opcional)
- **endereco**: Endereço completo

### Livro
- **id**: Identificador único
- **titulo**: Título do livro
- **subtitulo**: Subtítulo (opcional)
- **autores**: Lista de autores
- **isbn**: Código ISBN (opcional)
- **foto_url**: URL da foto do livro
- **observacao**: Observações sobre o estado do livro

### Doação
- **id**: Identificador único
- **instituicao_id**: ID da instituição receptora
- **doador_id**: ID do doador
- **data_criacao**: Data de criação da doação
- **status**: Status da doação (PENDENTE, ACEITA, REJEITADA, CONCLUIDA)
- **livros**: Lista de livros incluídos na doação

## Rotas da API REST

### Autenticação
- **POST /api/login**: Realiza login de doador ou instituição

### Usuários (CRUD Básico)
- **POST /api/usuarios/**: Cria novo usuário
- **GET /api/usuarios/**: Lista todos os usuários
- **GET /api/usuarios/{id}**: Busca usuário específico
- **PUT /api/usuarios/{id}**: Atualiza usuário
- **DELETE /api/usuarios/{id}**: Deleta usuário

### Doadores
- **POST /api/doadores**: Cria novo doador
- **GET /api/doadores/{id}**: Busca doador por ID
- **PUT /api/doadores/{id}**: Atualiza dados do doador

### Instituições
- **POST /api/instituicoes**: Cria nova instituição
- **GET /api/instituicoes**: Lista instituições (com paginação)
- **GET /api/instituicoes/{id}**: Busca instituição por ID
- **PUT /api/instituicoes/{id}**: Atualiza dados da instituição (com upload de foto)

### Livros
- **POST /api/livros**: Cadastra novo livro (com upload de foto)
- **GET /api/livros**: Lista todos os livros
- **GET /api/livros/buscar**: Busca livros por título
- **GET /api/livros/{id}**: Busca livro por ID
- **PUT /api/livros/{id}**: Atualiza livro (com upload de foto)
- **DELETE /api/livros/{id}**: Exclui livro

### Doações
- **POST /api/doacoes**: Cria nova doação (com múltiplos livros e fotos)
- **GET /api/doacoes/doador/{id}**: Lista doações de um doador
- **GET /api/doacoes/instituicao/{id}**: Lista doações de uma instituição
- **GET /api/doacoes/{id}**: Busca doação completa por ID
- **PATCH /api/doacoes/{id}/status**: Atualiza status da doação
- **DELETE /api/doacoes/{id}**: Deleta doação (apenas se pendente)

## Rotas da Interface Web

### Páginas Públicas
- **GET /**: Página inicial do sistema
- **GET /entrar**: Página de login
- **GET /registrar**: Página de registro de novo usuário
- **GET /instituicoes**: Listagem de instituições cadastradas
- **GET /instituicoes/cadastrar**: Formulário de cadastro de instituição

### Área do Doador
- **GET /doador**: Dashboard do doador
- **GET /doador/cadastrar-livro**: Formulário de cadastro de livro
- **GET /doador/editar-livro**: Formulário de edição de livro
- **GET /doador/editar-perfil**: Formulário de edição de perfil do doador

### Área da Instituição
- **GET /instituicao**: Dashboard da instituição
- **GET /instituicao/editar-perfil**: Formulário de edição de perfil da instituição
- **GET /solicitacoes**: Página de gerenciamento de solicitações de doação

### Doações
- **GET /instituicoes/{id}/doacao**: Página de criação de doação para uma instituição específica

## Fluxos Principais

### Fluxo de Cadastro de Doador
1. Usuário acessa `/registrar`
2. Preenche formulário com dados pessoais
3. Sistema valida email único
4. Doador é criado via **POST /api/doadores**
5. Redirecionamento para login

### Fluxo de Cadastro de Instituição
1. Usuário acessa `/instituicoes/cadastrar`
2. Preenche formulário com dados institucionais
3. Faz upload de foto (opcional)
4. Sistema valida email único
5. Instituição é criada via **POST /api/instituicoes**
6. Redirecionamento para login

### Fluxo de Login
1. Usuário acessa `/entrar`
2. Informa email e senha
3. Sistema valida credenciais via **POST /api/login**
4. Retorna tipo de usuário (DOADOR ou INSTITUICAO)
5. Redirecionamento para dashboard correspondente

### Fluxo de Cadastro de Livro
1. Doador acessa `/doador/cadastrar-livro`
2. Preenche informações do livro (título, autores, ISBN, etc.)
3. Faz upload das imagens
4. Sistema cria livro via **POST /api/livros**
5. Livro fica disponível para doação

### Fluxo de Criação de Doação (Doador Cadastrado)
1. Doador acessa listagem de instituições
2. Seleciona instituição desejada
3. Acessa `/instituicoes/{id}/doacao`
4. Seleciona livros cadastrados para doar
5. Adiciona observações sobre cada livro (opcional)
6. Faz upload de fotos dos livros (opcional)
7. Sistema cria doação via **POST /api/doacoes**
8. Status inicial: PENDENTE

### Fluxo de Criação de Doação (Doador Novo)
1. Usuário acessa listagem de instituições
2. Seleciona instituição desejada
3. Acessa `/instituicoes/{id}/doacao`
4. Preenche dados de cadastro (nome, email, telefone, senha)
5. Cadastra livros a serem doados
6. Sistema cria doador e doação simultaneamente
7. Status inicial: PENDENTE

### Fluxo de Gerenciamento de Doações (Instituição)
1. Instituição acessa `/solicitacoes`
2. Visualiza lista de doações recebidas
3. Para cada doação, pode:
   - Visualizar detalhes completos
   - Aceitar doação (status: ACEITA)
   - Rejeitar doação (status: REJEITADA)
   - Marcar como concluída (status: CONCLUIDA)
4. Ao concluir, contador de livros recebidos é incrementado

### Fluxo de Edição de Perfil
1. Usuário acessa página de edição de perfil
2. Atualiza informações desejadas
3. Confirma senha atual
4. Pode alterar senha (opcional)
5. Pode fazer upload de nova foto (instituições)
6. Sistema valida e atualiza dados

### Fluxo de Edição de Livro
1. Doador acessa `/doador/editar-livro`
2. Seleciona livro a ser editado
3. Sistema verifica se livro não está em doação pendente
4. Atualiza informações do livro
5. Pode fazer upload de nova foto
6. Sistema salva alterações via **PUT /api/livros/{id}**

### Fluxo de Exclusão de Livro
1. Doador solicita exclusão de livro
2. Sistema verifica se livro não está em doação pendente
3. Se permitido, livro é removido via **DELETE /api/livros/{id}**

## Regras de Negócio

### Validações de Email
- Email deve ser único no sistema
- Não pode haver doador e instituição com mesmo email
- Validação de formato de email via Pydantic

### Gerenciamento de Livros
- Livros em doação pendente não podem ser editados
- Livros em doação pendente não podem ser excluídos
- Cada livro pode ter múltiplos autores

### Gerenciamento de Doações
- Apenas doações pendentes podem ser excluídas
- Ao concluir doação, contador de livros da instituição é incrementado
- Doação pode incluir múltiplos livros
- Doador pode ser criado durante o processo de doação

### Upload de Arquivos
- Fotos de livros armazenadas no Google Cloud Storage (bucket: `cangaceiro-letras-fotos-livros`)
- Fotos de instituições armazenadas no Google Cloud Storage (bucket: `cangaceiro-letras-fotos-instituicoes`)
- Fotos de doações armazenadas no Google Cloud Storage (bucket: `cangaceiro-letras-fotos-doacoes`)
- Nomes de arquivo gerados com UUID para evitar conflitos
- URLs públicas geradas automaticamente pelo GCS

### Paginação
- Listagem de instituições suporta paginação
- Parâmetros: `pagina` (padrão: 1) e `tamanho_pagina` (padrão: 10, máximo: 50)

## Status de Doação

O sistema utiliza 4 status para gerenciar o ciclo de vida das doações:

1. **PENDENTE**: Doação criada, aguardando avaliação da instituição
2. **ACEITA**: Instituição aceitou a doação, aguardando entrega
3. **REJEITADA**: Instituição rejeitou a doação
4. **CONCLUIDA**: Doação foi entregue e finalizada

## Segurança

### Autenticação
- Senhas armazenadas com hash bcrypt no PostgreSQL
- Validação de senha atual necessária para alterações de perfil
- Sistema diferencia doadores e instituições no login

### Autorização
- Doadores só podem editar seus próprios livros
- Instituições só podem gerenciar doações recebidas
- Validações de propriedade em cada operação

## Dados de Teste

O sistema pode ser populado com dados de teste através de migrations ou scripts SQL, incluindo:
- Doadores de exemplo
- Instituições de exemplo
- Livros de exemplo
- Doações de exemplo

## Endpoints de Arquivos Estáticos

- **/static**: Arquivos estáticos (CSS, JS, imagens) servidos localmente
- **GCS URLs**: Fotos de livros, instituições e doações servidas via URLs públicas do Google Cloud Storage

## Observações Técnicas

### Padrões de Código
- Linha máxima: 79 caracteres
- Formatação automática com Ruff
- Type hints em funções críticas
- Validação de dados com Pydantic

### Testes
- Cobertura de código com pytest-cov
- Testes unitários para API
- Geração de relatório HTML de cobertura

### Organização
- Separação clara entre API REST e interface web
- Schemas Pydantic para validação consistente
- Camada de acesso ao PostgreSQL isolada com connection pooling
- Templates Jinja2 reutilizáveis
- Integração com Google Cloud Storage via biblioteca oficial

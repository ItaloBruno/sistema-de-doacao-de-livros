Cangaceiro das Letras: Conectando Doadores de Livros a Instituições Sociais

Rafael Coelho Silva ¹
Italo Bruno ²

Instituto Federal de Educação, Ciência e Tecnologia do Ceará
rafaellcoellho@gmail.com
rt.italo.bruno.silva@gmail.com

RESUMO. O Cangaceiro das Letras é um sistema web desenvolvido com o objetivo de conectar doadores de livros a instituições sociais, promovendo o acesso à leitura e à cultura literária. Para sua construção, foi elaborada uma especificação funcional inicial que serviu para delinear a ideia do projeto e guiar o desenvolvimento inicial, definindo os requisitos e o escopo do sistema. Durante o desenvolvimento, foram utilizados casos de uso como instrumento de modelagem, auxiliando na compreensão dos fluxos do sistema e na validação dos requisitos funcionais. A arquitetura adotada segue os princípios do Domain-Driven Design (DDD), estruturando o código em camadas bem definidas de domínio, aplicação, infraestrutura e apresentação. O backend foi desenvolvido em FastAPI, responsável pela disponibilização de uma API RESTful e pela documentação automática por meio do padrão OpenAPI. O frontend utiliza templates HTML com Jinja2, complementados por JavaScript.

ABSTRACT. Cangaceiro das Letras is a web-based system developed to connect book donors with social institutions, promoting access to reading and literary culture. Its development was guided by an initial functional specification that outlined the project's concept and guided early development, defining system requirements and scope. Throughout the development process, use cases were employed as a modeling tool to support the understanding of system workflows and the validation of functional requirements. The architecture follows the principles of Domain-Driven Design (DDD), organizing the codebase into well-defined layers: domain, application, infrastructure, and presentation. The backend was implemented using FastAPI, providing a RESTful API and automatic documentation through the OpenAPI standard. The frontend is built with HTML templates rendered via Jinja2, complemented with JavaScript.

1. Introdução

Nos últimos anos, a democratização do acesso à leitura tem se consolidado como um desafio social relevante, especialmente em um país onde milhões de pessoas ainda enfrentam barreiras para ter contato com livros e materiais literários. Em um cenário onde a educação e a cultura são fundamentais para o desenvolvimento humano, o Sistema Cangaceiro das Letras foi desenvolvido como uma solução tecnológica para facilitar a doação de livros, conectando diretamente doadores a instituições sociais que promovem a leitura em suas comunidades. O sistema permite que doadores cadastrem seus livros, visualizem instituições beneficentes e realizem doações. O sistema é constituído de dois perfis principais: Doador, usado por pessoas que desejam doar livros, e Instituição, usado por organizações sociais que recebem e gerenciam as doações.

Para o desenvolvimento do sistema, foi adotada uma abordagem estruturada que combina especificação funcional detalhada, modelagem por casos de uso e arquitetura baseada em Domain-Driven Design (DDD). A especificação funcional inicial permitiu delinear a ideia do projeto e guiar o desenvolvimento inicial, definindo claramente os requisitos e o escopo do sistema, enquanto os casos de uso auxiliaram na compreensão dos fluxos de interação entre os usuários e o sistema. A arquitetura DDD organizou o código em camadas bem definidas de domínio, aplicação, infraestrutura e apresentação, promovendo modularidade, facilidade de manutenção e escalabilidade da solução.

No desenvolvimento do backend, foi aplicado o FastAPI para criar uma API RESTful, com o OpenAPI para documentação automática e integração. O PostgreSQL foi utilizado como sistema gerenciador de banco de dados para persistência e consistência dos dados. O frontend do sistema foi construído com templates HTML renderizados via Jinja2, complementados por JavaScript. O armazenamento de fotos foi implementado utilizando Google Cloud Storage. O gerenciamento de dependências e tarefas de desenvolvimento foi realizado com Poetry e Taskipy, enquanto testes automatizados foram implementados com Pytest.

Esse texto tem como objetivo descrever o processo de desenvolvimento do Cangaceiro das Letras e explicar suas telas e as funcionalidades do sistema. Na Seção 2, veremos a metodologia e as ferramentas utilizadas para organizar e gerenciar o desenvolvimento da aplicação. Já na Seção 3, veremos como as peças que compõem o sistema foram organizadas, analisando sua arquitetura. A Seção 4 apresenta o detalhamento das tecnologias que foram essenciais para seu desenvolvimento. As telas contendo os fluxos do sistema, também conhecidos como jornadas, são apresentados na Seção 5. Na Seção 6 são descritas as melhorias futuras planejadas para o sistema e na Seção 7, são apresentadas considerações finais.

2. Materiais e Métodos

Nesta seção são apresentadas as metodologias e ferramentas utilizadas no desenvolvimento do sistema Cangaceiro das Letras. A abordagem adotada combinou técnicas de especificação funcional, modelagem por casos de uso e arquitetura orientada a domínio, visando estruturar o processo de desenvolvimento de forma organizada e sistemática.

2.1. Especificação Funcional

A especificação funcional foi o ponto de partida para o desenvolvimento do sistema, permitindo documentar e definir os requisitos antes da implementação. Segundo Visure Solutions (2025), "Um Documento de Especificação Funcional (DFS) é um documento formal de requisitos que descreve como um sistema de software, aplicativo ou produto deve funcionar. Ele define os requisitos funcionais, incluindo fluxos de trabalho, comportamento do sistema, entradas, saídas e interações da perspectiva do usuário. Em resumo, o DFS responde à seguinte pergunta: 'O que o sistema deve fazer?'"

No contexto do Cangaceiro das Letras, a especificação funcional foi elaborada para delinear os principais fluxos do sistema, identificar os perfis de usuário e definir as funcionalidades essenciais. O documento estabeleceu como objetivo principal facilitar a doação de livros de pessoas físicas para instituições sociais, conectando doadores e instituições de forma organizada. Foram identificados dois tipos de usuários principais: doadores, que são pessoas físicas interessadas em doar livros, e instituições sociais, que são organizações cadastradas para receber doações.

A especificação definiu as principais ações de cada perfil de usuário. Para doadores, foram especificadas funcionalidades como criar conta, fazer login, consultar lista de instituições sociais, enviar solicitações de doação, acompanhar o status das doações e editar ou excluir doações pendentes. Para instituições sociais, foram definidas ações como criar conta, fazer login, receber e gerenciar solicitações de doação, avaliar doações recebidas, entrar em contato com doadores quando a doação for aceita e editar perfil institucional.

O documento também especificou a estrutura do sistema, definindo oito páginas principais: página inicial, página de listagem de instituições sociais, página de doação, página de login, página de registro, página principal logada para doador, página principal logada para instituição social e página de avaliação da solicitação. Para cada página, foram detalhados os elementos de interface, campos obrigatórios, fluxos de interação e ações disponíveis. Por exemplo, a página de doação foi especificada para permitir que doadores preencham dados pessoais, pesquisem livros por nome com preenchimento automático de metadados, adicionem múltiplos livros com fotos e observações, e enviem a solicitação completa para a instituição selecionada.

A especificação funcional também estabeleceu requisitos de navegação entre páginas, definindo origem, ação e destino para cada fluxo de interação do usuário. Foram documentados requisitos funcionais como validação de campos obrigatórios, preenchimento automático de dados, gerenciamento de estados de doação (pendente, aceita, rejeitada, concluída) e redirecionamento após ações de sucesso. Este documento serviu como guia durante as fases iniciais do desenvolvimento, auxiliando na compreensão do escopo do projeto, na comunicação entre os membros da equipe e na priorização de funcionalidades a serem implementadas.

Durante o desenvolvimento, algumas adaptações foram realizadas em relação à especificação funcional inicial. O sistema implementado incluiu funcionalidades adicionais não previstas na especificação, como a possibilidade de doadores cadastrarem livros previamente em uma área dedicada antes de realizar doações, permitindo reutilização de livros já cadastrados em múltiplas doações. Também foi adicionada a funcionalidade de edição e exclusão de livros cadastrados, com validações para impedir alterações em livros que estejam vinculados a doações pendentes. O fluxo de criação de doação foi expandido para suportar dois cenários distintos: doadores já cadastrados que selecionam livros de sua biblioteca pessoal, e novos doadores que podem se cadastrar e adicionar livros simultaneamente durante o processo de doação. O sistema também incorporou regras de negócio mais específicas, como a validação de unicidade de email entre doadores e instituições, e o incremento automático do contador de livros recebidos pelas instituições ao concluir uma doação.

Essas diferenças entre a especificação funcional e o sistema implementado refletem a natureza iterativa do desenvolvimento de software, onde requisitos são refinados e novas necessidades são identificadas durante a implementação. A especificação funcional cumpriu seu papel como documento inicial de planejamento, estabelecendo a base conceitual do sistema e os fluxos principais de interação. No entanto, o processo de desenvolvimento revelou oportunidades de melhoria na experiência do usuário e na organização das funcionalidades. A adição do cadastro prévio de livros, por exemplo, surgiu da percepção de que doadores poderiam querer manter uma biblioteca pessoal de livros disponíveis para doação, facilitando doações futuras. As validações adicionais emergiram como necessidades práticas durante a implementação da lógica de negócio. Essas adaptações demonstram que, embora a especificação funcional seja fundamental para o planejamento inicial, o desenvolvimento de software requer flexibilidade para incorporar melhorias identificadas ao longo do processo.

2.2. Casos de Uso

Os casos de uso foram utilizados como técnica de modelagem para documentar os fluxos de interação entre usuários e o sistema. Segundo DevMedia (2025), "Esse diagrama documenta o que o sistema faz do ponto de vista do usuário. Em outras palavras, ele descreve as principais funcionalidades do sistema e a interação dessas funcionalidades com os usuários do mesmo sistema. Nesse diagrama não nos aprofundamos em detalhes técnicos que dizem como o sistema faz." No contexto do Cangaceiro das Letras, os casos de uso auxiliaram na compreensão dos fluxos principais do sistema, permitindo identificar as etapas necessárias para cada funcionalidade e validar se os requisitos especificados atendiam às necessidades dos usuários.

2.2.1. Fluxo de Criação de Doação (Doador Cadastrado)

O doador acessa a listagem de instituições e seleciona a instituição desejada. Em seguida, seleciona livros previamente cadastrados em sua biblioteca pessoal, adiciona observações opcionais sobre cada livro e faz upload de fotos. O sistema cria a doação com status inicial pendente.

2.2.2. Fluxo de Criação de Doação (Doador Novo)

O usuário acessa a listagem de instituições e seleciona a instituição desejada. Durante o processo de doação, preenche dados de cadastro como nome, email, telefone e senha, e cadastra os livros a serem doados. O sistema cria o doador e a doação simultaneamente, com status inicial pendente.

2.2.3. Fluxo de Gerenciamento de Doações

A instituição acessa a página de solicitações e visualiza a lista de doações recebidas. Para cada doação, pode visualizar detalhes completos dos livros e do doador, aceitar a doação alterando seu status para aceita, rejeitar a doação ou marcar como concluída. Ao concluir uma doação, o contador de livros recebidos da instituição é incrementado automaticamente.

Referências

VISURE SOLUTIONS. Functional Specification Document. Disponível em: https://visuresolutions.com/pt/alm-guide/functional-specification-document/. Acesso em: 29 dez. 2025.

DEVMEDIA. O que é UML e Diagramas de Caso de Uso: Introdução Prática à UML. Disponível em: https://www.devmedia.com.br/o-que-e-uml-e-diagramas-de-caso-de-uso-introducao-pratica-a-uml/23408. Acesso em: 30 dez. 2025.


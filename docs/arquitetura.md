# Arquitetura - TechIncident AI

## Visão geral

O TechIncident AI é uma aplicação de inteligência artificial para análise inicial de incidentes técnicos de software.

A solução utiliza LangGraph para organizar o processamento em etapas, combinando validações determinísticas, classificação com LLM, consulta de SLA, memória de contexto e geração de diagnóstico.

## Fluxo principal

O fluxo implementado realiza as seguintes etapas:

1. Receber e validar o incidente informado pelo usuário.
2. Bloquear entradas que apresentem padrões de prompt injection ou tentativa de acesso a informações sensíveis.
3. Analisar o incidente.
4. Avaliar a criticidade.
5. Avaliar o risco.
6. Classificar a categoria do incidente.
7. Consultar o SLA correspondente à criticidade.
8. Consolidar as informações obtidas.
9. Decidir o fluxo conforme criticidade e risco.
10. Priorizar incidentes quando necessário.
11. Gerar o diagnóstico estruturado.

## Fluxo do LangGraph

```text
START
  |
  v
Validar entrada
  |
  v
Analisar incidente
  |
  +--------------------+--------------------+
  |                    |                    |
  v                    v                    v
Avaliar             Avaliar              Avaliar
criticidade           risco               categoria
  |                    |                    |
  +--------------------+--------------------+
                       |
                       v
                Consultar SLA
                       |
                       v
               Consolidar análise
                       |
                       v
                 Decidir fluxo
                  /         \
                 /           \
                v             v
          Priorizar       Gerar diagnóstico
                \             /
                 \           /
                      END
```

## Componentes principais

### agent.py

Contém o fluxo principal do agente construído com LangGraph. É responsável pela validação da entrada, análise do incidente, classificação, avaliação de criticidade e risco, consulta de SLA, consolidação das informações e geração do diagnóstico.

### tools.py

Contém a ferramenta utilizada para consulta do SLA de acordo com a criticidade do incidente. A ferramenta foi separada do fluxo principal para permitir reutilização e testes independentes.

### Memória e contexto

O projeto utiliza o `MemorySaver` do LangGraph para manter o estado das interações.

Cada execução pode utilizar um identificador de thread, permitindo que o estado associado à interação seja preservado e utilizado pelo fluxo do agente.

O histórico faz parte do estado do incidente e permite manter informações relevantes durante o processamento.

### Segurança

A entrada é validada antes de seguir pelo fluxo principal.

Foram implementadas verificações para bloquear padrões relacionados a prompt injection e tentativas de obtenção de informações sensíveis, como solicitações para ignorar instruções ou revelar chaves.

O projeto também possui teste automatizado específico para validar esse comportamento.

### Integração com LLM

A solução utiliza uma LLM para apoiar etapas de análise e classificação do incidente.

Para aumentar a resiliência da integração, foram implementados timeout, tentativas limitadas e fallback, permitindo que o fluxo continue de maneira controlada em situações de indisponibilidade do serviço externo.

### Observabilidade

O fluxo registra informações de execução para auxiliar no acompanhamento do processamento e na identificação de falhas.

Além dos registros de execução, o projeto utiliza os resultados dos testes automatizados e da pipeline de CI como evidências para acompanhamento da estabilidade da solução.

### Testes automatizados

Os testes estão localizados no diretório `tests`.

São validados cenários relacionados a:

- consulta de SLA;
- criticidade válida e inválida;
- entrada vazia ou inválida;
- segurança contra prompt injection;
- fluxo completo do agente;
- integração do fluxo LangGraph utilizando uma LLM simulada.

### Integração contínua

O projeto utiliza GitHub Actions para executar automaticamente as validações da aplicação.

A pipeline executa:

- instalação das dependências;
- testes automatizados com pytest;
- validação de sintaxe dos arquivos Python com compileall.

Esse processo permite identificar falhas durante a evolução do projeto e reduzir o risco de regressões.

## Integração low-code com n8n

O projeto possui documentação da integração com n8n no arquivo `docs/integracao-n8n.md`.

Também é disponibilizado o arquivo `docs/workflow-n8n.json`, representando o workflow exportável da integração.

A proposta da integração é permitir que um incidente seja recebido por um webhook e utilizado em um fluxo de automação low-code.

## Estrutura principal do projeto

```text
techincident-ai/
├── .github/
│   └── workflows/
│       └── ci.yml
├── docs/
│   ├── arquitetura.md
│   ├── integracao-n8n.md
│   └── workflow-n8n.json
├── tests/
│   ├── test_agent.py
│   └── test_tools.py
├── .env.example
├── .gitignore
├── agent.py
├── README.md
├── requirements.txt
└── tools.py
```

## Resumo da arquitetura

A arquitetura do TechIncident AI foi estruturada para separar as principais responsabilidades da solução.

O LangGraph controla o fluxo do agente, a LLM apoia a análise e classificação dos incidentes, a ferramenta de SLA representa uma integração independente, o MemorySaver mantém o estado das interações, os testes automatizados validam os principais cenários e o GitHub Actions executa as verificações de integração contínua.

A integração com n8n complementa a solução demonstrando uma possibilidade de automação low-code para entrada e tratamento de incidentes.
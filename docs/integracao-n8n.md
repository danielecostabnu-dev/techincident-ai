# Integração Low-Code com n8n

O projeto TechIncident AI utiliza o n8n como ferramenta low-code para demonstrar uma integração externa por meio de Webhook.

## Fluxo

O workflow criado no n8n possui os seguintes nós:

1. Webhook
2. Respond to Webhook

O Webhook recebe uma requisição HTTP POST contendo os dados de um incidente.

Exemplo de entrada:

{
  "incidente": "Erro 500 na API de usuarios"
}

Após o recebimento, o workflow retorna uma resposta JSON confirmando o processamento da requisição.

## Configuração

- Método HTTP: POST
- Path: techincident
- Tipo de integração: Webhook
- Ferramenta low-code: n8n

## Validação

A integração foi testada através de uma requisição HTTP POST.

O n8n recebeu corretamente o campo `incidente` e os dois nós do workflow foram executados com sucesso.

O workflow também foi publicado no n8n, permitindo a utilização da URL de produção.

## Objetivo

Esta integração demonstra a utilização de uma ferramenta low-code/no-code em conjunto com o projeto TechIncident AI, permitindo receber eventos externos através de uma API baseada em Webhook.
# TechIncident AI

## Descrição da solução

O TechIncident AI é uma aplicação de inteligência artificial voltada à análise inicial de incidentes técnicos de software.

O projeto é uma evolução do mini-projeto Agente de Resumos Técnicos, ampliando o fluxo anterior para realizar análise, classificação e diagnóstico de incidentes técnicos.

## Problema

Equipes de desenvolvimento, QA e suporte técnico recebem erros, logs e relatos de incidentes que precisam ser analisados para identificar possíveis causas e ações recomendadas.

O TechIncident AI tem como objetivo apoiar essa análise, processando as informações do incidente e produzindo um diagnóstico inicial estruturado.

## Público-alvo

- Desenvolvedores;
- Profissionais de QA;
- Equipes de suporte técnico.

## Entrada

A aplicação recebe uma descrição textual de um incidente técnico, que pode conter mensagens de erro, logs ou informações sobre o comportamento apresentado pelo sistema.

## Saída

A aplicação deverá produzir uma saída estruturada contendo informações como:

- categoria do incidente;
- criticidade;
- resumo;
- possíveis causas;
- ação recomendada;
- indicação de necessidade de aprovação humana.

## Limites da solução

O TechIncident AI atua como ferramenta de apoio à análise de incidentes.

A aplicação não deverá executar automaticamente ações destrutivas ou irreversíveis, revelar credenciais ou permitir que conteúdos fornecidos na entrada substituam suas regras de segurança.

## Cenários de uso

### Cenário 1 — Fluxo principal

O usuário informa um incidente técnico, como um erro de API acompanhado de timeout.

A aplicação deverá validar a entrada, classificar o incidente, recuperar informações relevantes, analisar o problema e produzir um diagnóstico estruturado.

### Cenário 2 — Entrada adversarial

O usuário fornece uma descrição de incidente contendo uma tentativa de prompt injection, solicitando que o agente ignore suas regras ou revele informações sensíveis.

A aplicação deverá identificar a entrada não confiável, impedir ações não autorizadas e não revelar credenciais ou informações sensíveis.

## Evidências de CI e análise de anomalias

O projeto utiliza GitHub Actions para executar automaticamente testes e validações do código a cada push ou pull request.

A pipeline possui as seguintes validações:
- instalação das dependências do projeto;
- execução dos testes automatizados com pytest;
- validação de sintaxe dos arquivos Python com compileall.

Durante o desenvolvimento, a CI identificou falhas reais. Uma das execuções falhou porque a variável `GROQ_API_KEY` não estava disponível no ambiente de testes. O problema foi analisado e corrigido utilizando uma chave fictícia exclusivamente no contexto dos testes, sem realizar chamadas externas.

Também foi identificada uma falha de sintaxe YAML após a inclusão da etapa de validação do código. A própria execução do GitHub Actions indicou a linha do problema, permitindo corrigir a indentação do workflow.

Após as correções, as execuções seguintes da pipeline foram concluídas com sucesso, demonstrando a utilização da CI como mecanismo de detecção e prevenção de regressões.

### Tendência e risco da pipeline

Considerando as 8 execuções registradas durante o desenvolvimento, 2 apresentaram falha e 6 foram concluídas com sucesso, resultando em uma taxa observada de sucesso de 75%.

As falhas ocorreram durante a evolução da configuração da CI e foram identificadas e corrigidas. Como as execuções posteriores às respectivas correções foram concluídas com sucesso, a tendência atual indica redução do risco de falha da pipeline.

Essa estimativa utiliza uma amostra pequena e representa apenas o histórico observado durante o desenvolvimento do projeto.

## Testes e apoio de IA

A IA foi utilizada como apoio durante o desenvolvimento para revisar alterações do código, identificar possíveis falhas e sugerir melhorias no fluxo do agente.

Também foi utilizada para apoiar a criação e o refinamento dos testes automatizados. O projeto possui testes da ferramenta de consulta de SLA, teste de segurança contra entrada adversarial e teste de integração do fluxo LangGraph utilizando uma LLM simulada, evitando dependência de chamadas externas durante a execução dos testes.

O cenário de integração foi priorizado por possuir maior impacto sobre a solução, pois valida conjuntamente o fluxo do agente, a classificação do incidente, a avaliação de risco e a consulta de SLA. Uma falha nesse fluxo comprometeria diretamente o resultado principal da aplicação.

Durante a revisão do projeto também foram identificadas oportunidades de melhoria relacionadas à resiliência da integração com a LLM. Como resultado, foram adicionados timeout, tentativas limitadas e fallback para permitir que o fluxo continue de forma controlada em caso de indisponibilidade do serviço externo.
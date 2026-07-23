# Clinical Nutrition Automation Demo

A fully local portfolio project that demonstrates how a clinical nutrition review workflow can be organized, prioritized, recorded and presented through a clear dashboard. Every person, identifier, care area and clinical detail included in this repository is fictional.

> Status: functional portfolio demonstration, version 1.0.0.

## Objective

Showcase a maintainable automation architecture for turning structured nutrition cases into an auditable review queue without connecting to any real service.

## Problem

Nutrition teams often need to consolidate repeated checks, identify priority cases and communicate follow-up needs consistently. This demonstration models that workflow with deterministic rules and synthetic input so the engineering approach can be evaluated safely.

## Features

- Local dashboard with full and care-area-focused review modes.
- Two rotating synthetic scenarios to demonstrate changing daily conditions.
- Deterministic risk evaluation and recommended actions.
- Summary metrics, route distribution and workflow trace.
- Local SQLite history with a one-click reset.
- Downloadable JSON report generated from fictional cases.
- Responsive interface for desktop and mobile widths.
- Unit and local web tests using only the Python standard library.

## Technologies

- Python 3.10+
- SQLite
- Standard-library threaded HTTP server
- HTML, CSS and vanilla JavaScript
- `unittest`

## Architecture

```text
Synthetic JSON fixture
        |
        v
SyntheticCaseAdapter -> NutritionWorkflowService -> SQLiteRunRepository
                                |
                                v
                    Local web dashboard + JSON report
```

The source adapter is isolated behind a small protocol. The service owns filtering, review rules and summary generation. The repository stores only demonstration runs. The web layer serves the interface and coordinates local requests.

## Installation

No third-party package is required.

```powershell
git clone <repository-url>
cd clinical-nutrition-automation-demo
python --version
```

Python 3.10 or newer is recommended.

## Run

```powershell
python run_demo.py
```

Open `http://127.0.0.1:8765` in a browser. Use `--port` to select another local port and `--database` to select another disposable database path.

## Demonstration

1. Choose all care areas or one focused area.
2. Select **Run demonstration**.
3. Review totals, priority flags, recommended actions and distribution.
4. Download the fictional JSON report or reset the local history.
5. Run again to load the second synthetic scenario.

## Tests

```powershell
python -m unittest discover -s tests -v
```

## Project Structure

```text
clinical-nutrition-automation-demo/
|-- clinical_demo/
|   |-- adapters.py       # Synthetic input adapter
|   |-- models.py         # Typed case model
|   |-- repository.py     # Disposable local persistence
|   |-- service.py        # Review workflow and rules
|   `-- web.py            # Local interface server
|-- fixtures/
|   `-- synthetic_cases.json
|-- static/
|   |-- app.js
|   |-- index.html
|   `-- styles.css
|-- tests/
|   |-- test_service.py
|   `-- test_web.py
|-- LICENSE
|-- pyproject.toml
`-- run_demo.py
```

## Limitations

- The workflow uses a small deterministic fixture and does not represent clinical decision support.
- Recommendations are illustrative labels, not medical guidance.
- The local database is designed for demonstration history only.
- There are no multi-user or deployment features.

## Security and Privacy

- All included data is deliberately synthetic.
- The application binds to `127.0.0.1` by default.
- No real service is contacted and no network integration is implemented.
- Runtime database files are excluded from version control.
- The generated report contains only the selected fictional scenario.

## Status and Next Steps

The core demonstration, dashboard, persistence and tests are complete. Suitable future improvements include configurable synthetic scenario generation, accessibility testing, richer report formats and a replaceable in-memory repository for teaching examples.

## License

Copyright © 2026 João Morais. All rights reserved. See [LICENSE](LICENSE).

---

# Demonstração de Automação em Nutrição Clínica

Projeto de portfólio totalmente local que demonstra como um fluxo de revisão em nutrição clínica pode ser organizado, priorizado, registrado e apresentado em um painel claro. Todas as pessoas, identificações, áreas de cuidado e informações clínicas deste repositório são fictícias.

> Status: demonstração funcional para portfólio, versão 1.0.0.

## Objetivo

Apresentar uma arquitetura de automação sustentável para transformar casos nutricionais estruturados em uma fila de revisão auditável, sem conexão com qualquer serviço real.

## Problema

Equipes de nutrição precisam consolidar verificações recorrentes, identificar casos prioritários e comunicar acompanhamentos com consistência. Esta demonstração representa esse fluxo com regras determinísticas e entradas sintéticas, permitindo avaliar a solução com segurança.

## Funcionalidades

- Painel local com revisão completa ou focada por área de cuidado.
- Dois cenários sintéticos alternados para demonstrar mudanças entre execuções.
- Avaliação determinística de risco e ações recomendadas.
- Métricas, distribuição por via nutricional e rastreio do fluxo.
- Histórico local em SQLite com opção de limpeza.
- Relatório JSON gerado exclusivamente com casos fictícios.
- Interface responsiva para computadores e dispositivos móveis.
- Testes unitários e web local usando apenas a biblioteca padrão do Python.

## Tecnologias

- Python 3.10+
- SQLite
- Servidor HTTP concorrente da biblioteca padrão
- HTML, CSS e JavaScript puro
- `unittest`

## Arquitetura

```text
Fixture JSON sintética
        |
        v
SyntheticCaseAdapter -> NutritionWorkflowService -> SQLiteRunRepository
                                |
                                v
                     Painel local + relatório JSON
```

O adaptador de entrada fica isolado por um protocolo pequeno. O serviço concentra filtros, regras de revisão e resumos. O repositório armazena somente execuções demonstrativas. A camada web fornece a interface e coordena requisições locais.

## Instalação

Nenhum pacote de terceiros é necessário.

```powershell
git clone <url-do-repositorio>
cd clinical-nutrition-automation-demo
python --version
```

Recomenda-se Python 3.10 ou mais recente.

## Execução

```powershell
python run_demo.py
```

Abra `http://127.0.0.1:8765` no navegador. Use `--port` para escolher outra porta local e `--database` para escolher outro caminho de banco descartável.

## Demonstração

1. Selecione todas as áreas ou uma área específica.
2. Clique em **Run demonstration**.
3. Analise totais, prioridades, ações recomendadas e distribuição.
4. Baixe o relatório JSON fictício ou limpe o histórico local.
5. Execute novamente para carregar o segundo cenário sintético.

## Testes

```powershell
python -m unittest discover -s tests -v
```

## Estrutura

```text
clinical-nutrition-automation-demo/
|-- clinical_demo/        # Domínio, adaptador, serviço, persistência e web
|-- fixtures/             # Casos inteiramente fictícios
|-- static/               # Interface local
|-- tests/                # Testes automatizados
|-- LICENSE
|-- pyproject.toml
`-- run_demo.py
```

## Limitações

- O fluxo usa uma fixture determinística pequena e não representa apoio à decisão clínica.
- As recomendações são rótulos ilustrativos, não orientação médica.
- O banco local serve apenas ao histórico da demonstração.
- Não há recursos para múltiplos usuários ou implantação.

## Segurança e Privacidade

- Todos os dados incluídos foram criados para esta demonstração.
- A aplicação usa `127.0.0.1` por padrão.
- Nenhum serviço real é contatado e nenhuma integração de rede foi implementada.
- Bancos gerados durante a execução não entram no controle de versão.
- O relatório contém somente o cenário fictício selecionado.

## Status e Próximos Passos

O núcleo da demonstração, painel, persistência e testes está concluído. Evoluções adequadas incluem geração configurável de cenários sintéticos, testes de acessibilidade, novos formatos de relatório e um repositório em memória substituível para exemplos didáticos.

## Licença

Copyright © 2026 João Morais. Todos os direitos reservados. Consulte [LICENSE](LICENSE).


# War Board Game

[![CI/CD Pipeline](https://github.com/DuarteFrugoli/war-board-game/actions/workflows/ci-cd.yml/badge.svg)](https://github.com/DuarteFrugoli/war-board-game/actions/workflows/ci-cd.yml)
[![Python Version](https://img.shields.io/badge/python-3.9%2B%20%7C%203.13-blue.svg)](https://python.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code Coverage](https://codecov.io/gh/DuarteFrugoli/war-board-game/branch/main/graph/badge.svg)](https://codecov.io/gh/DuarteFrugoli/war-board-game)

## Sobre o Projeto

Este projeto implementa o clássico jogo de tabuleiro **War** (conhecido como Risk em outros países) em Python, com foco em práticas modernas de desenvolvimento de software:

- Versionamento de código com Git e GitHub
- Gerenciamento de dependências com pyproject.toml
- Testes unitários com pytest (56 testes implementados)
- CI/CD Pipeline com GitHub Actions

## Como Executar

### Pré-requisitos
- Python 3.9 ou superior (testado até Python 3.13.5)
- pip (gerenciador de pacotes Python)

### Instalação Rápida

```bash
# 1. Clonar o repositório
git clone https://github.com/DuarteFrugoli/war-board-game.git
cd war-board-game

# 2. Instalar dependências
pip install -e .

# 3. Executar o jogo
python main.py
```

### Instalação para Desenvolvimento

```bash
# 1. Clonar e entrar no diretório
git clone https://github.com/DuarteFrugoli/war-board-game.git
cd war-board-game

# 2. Instalar com dependências de desenvolvimento
pip install -e ".[dev,test]"

# 3. Executar testes
pytest tests/

# 4. Executar o jogo
python main.py
```

### Instalação com Scripts (Linux/macOS)

```bash
# Configurar ambiente automaticamente
chmod +x scripts/setup_environment.sh
./scripts/setup_environment.sh

# Executar testes com relatórios
chmod +x scripts/run_tests.sh
./scripts/run_tests.sh

# Criar pacote de distribuição
chmod +x scripts/create_package.sh
./scripts/create_package.sh
```

## Como Jogar

### Objetivo
Conquistar territórios e eliminar todos os adversários ou cumprir missões secretas específicas.

### Fluxo do Jogo
1. **Distribuição inicial**: Cada jogador recebe territórios aleatoriamente
2. **Colocação de exércitos**: Distribua seus exércitos nos territórios
3. **Fases do turno**:
   - **Recebimento**: Ganhe novos exércitos baseado em territórios/continentes
   - **Ataque**: Ataque territórios adjacentes de oponentes
   - **Remanejamento**: Mova exércitos entre seus territórios

### Controles
- Use as opções apresentadas no menu textual
- Digite números para selecionar opções
- Siga as instruções na tela

## Arquitetura do Projeto

```
war-board-game/
├── 📁 war/                  # Módulos principais do jogo
│   ├── card.py             # Sistema de cartas e missões
│   ├── continent.py        # Lógica de continentes
│   ├── enums.py           # Enumerações e constantes
│   ├── game.py            # Engine principal do jogo
│   ├── player.py          # Lógica de jogadores
│   ├── territory.py       # Sistema de territórios
│   └── utils.py           # Utilitários gerais
├── 📁 tests/               # Testes unitários (56 testes)
│   ├── test_card.py       # Testes das cartas
│   ├── test_game.py       # Testes do jogo
│   ├── test_player.py     # Testes dos jogadores
│   ├── test_territory.py  # Testes dos territórios
│   └── test_utils.py      # Testes dos utilitários
├── 📁 data/               # Dados do jogo
│   ├── map.json          # Configuração do mapa
│   └── missions.json     # Missões disponíveis
├── 📁 scripts/           # Scripts de automação
│   ├── setup_environment.sh    # Configuração do ambiente
│   ├── run_tests.sh            # Execução de testes
│   ├── create_package.sh       # Criação de pacotes
│   └── send_notification.py    # Notificações por email
├── 📁 .github/workflows/  # CI/CD Pipeline
│   └── ci-cd.yml         # Pipeline principal
├── main.py               # Ponto de entrada principal
├── pyproject.toml        # Configuração e dependências
└── README.md            # Este arquivo
```

### Componentes Principais

#### Core Game Engine (`war/game.py`)
- Controla o fluxo principal do jogo
- Gerencia turnos e fases
- Coordena interações entre jogadores e territórios

#### Sistema de Jogadores (`war/player.py`)
- Gerencia estado individual de cada jogador
- Controla exércitos, territórios e cartas
- Implementa estratégias de IA (futuro)

#### Sistema de Territórios (`war/territory.py`)
- Representa cada território do mapa
- Gerencia conexões e fronteiras
- Controla ocupação e exércitos

#### Sistema de Cartas (`war/card.py`)
- Gerencia cartas de território e missões
- Implementa trocas de cartas por exércitos
- Controla missões secretas

## Testes

O projeto possui **56 testes unitários** cobrindo todos os módulos principais:

```bash
# Executar todos os testes
pytest tests/

# Executar testes com cobertura
pytest tests/ --cov=war --cov-report=html

# Executar testes específicos
pytest tests/test_game.py::TestGame::test_game_initialization

# Executar com verbose
pytest tests/ -v
```

### Cobertura de Testes
- **game.py**: 15 testes (inicialização, turnos, vitória)
- **player.py**: 14 testes (ações, cartas, territórios)
- **territory.py**: 10 testes (conexões, ocupação, ataques)
- **card.py**: 9 testes (cartas, missões, trocas)
- **utils.py**: 8 testes (utilitários, validações)

## CI/CD Pipeline

O projeto utiliza **GitHub Actions** com pipeline automatizado:

### Jobs do Pipeline
1. **Testes**: Executa todos os testes unitários com cobertura em Python 3.9-3.13
2. **Build**: Cria pacotes de distribuição
3. **Qualidade**: Análise de código (Black, Flake8, MyPy, Bandit)
4. **Notificação**: Envia emails sobre status do pipeline

### Triggers
- Push para branches `main` e `develop`
- Pull requests para `main`
- Execução manual via GitHub interface

### Artefatos Gerados
- Relatórios de teste (JUnit XML, Coverage HTML/XML)
- Pacotes de distribuição (.tar.gz)
- Relatórios de qualidade de código
- Relatórios de segurança

## Análise de Qualidade

### Ferramentas Utilizadas
- **Black**: Formatação automática de código
- **Flake8**: Análise de estilo (PEP 8)
- **MyPy**: Verificação de tipos estáticos
- **Bandit**: Análise de segurança
- **Safety**: Verificação de vulnerabilidades em dependências
- **pytest-cov**: Cobertura de testes

### Padrões Seguidos
- PEP 8 (Style Guide for Python Code)
- PEP 257 (Docstring Conventions)
- Type hints quando aplicável
- Nomenclatura em português nos comentários e strings de usuário

## Desenvolvimento

### Estrutura de Branches
- `main`: Branch principal com código estável
- `develop`: Branch de desenvolvimento
- `feature/*`: Branches para novas funcionalidades
- `bugfix/*`: Branches para correções

### Workflow de Contribuição
1. Fork o repositório
2. Crie uma branch para sua feature (`git checkout -b feature/nova-funcionalidade`)
3. Faça commits com mensagens descritivas
4. Escreva/atualize testes para suas mudanças
5. Execute os testes (`pytest tests/`)
6. Faça push da branch (`git push origin feature/nova-funcionalidade`)
7. Abra um Pull Request

### Comandos Úteis

```bash
# Instalar em modo de desenvolvimento
pip install -e ".[dev,test]"

# Executar testes com watch (reexecuta ao salvar arquivos)
ptw tests/

# Formatar código automaticamente
black war/ tests/ main.py

# Verificar estilo
flake8 war/ tests/ main.py

# Verificar tipos
mypy war/

# Análise de segurança
bandit -r war/

# Gerar documentação
pdoc war/ --html --output-dir docs/
```

## Roadmap

### Versão 1.1
- Interface gráfica com pygame
- IA para jogadores automáticos
- Modo multiplayer local
- Animações de batalha

### Versão 1.2
- Modo online/rede
- Sistema de ranking
- Replays de partidas
- Mapas customizáveis

### Versão 2.0
- Interface web com Flask/Django
- Banco de dados para estatísticas
- Sistema de usuários
- Torneios automáticos

## Autores e Contribuidores

### Desenvolvedores Principais
- **Pedro Henrique Duarte Frugoli** - [GitHub](https://github.com/DuarteFrugoli)
  - Arquitetura principal e CI/CD
  - pedro.frugoli@ges.inatel.br

- **Thiago Damas** - [GitHub](https://github.com/ThiagoDamasz)
  - Lógica de jogo e testes

- **Fabio Miguel** - [GitHub](https://github.com/FabioDeriva)
  - Sistema de territórios e cartas

### Como Contribuir
Sinta-se à vontade para:
- Reportar bugs através das [Issues](https://github.com/DuarteFrugoli/war-board-game/issues)
- Sugerir melhorias
- Enviar Pull Requests
- Melhorar a documentação
- Dar uma estrela no repositório!

## Licença

Este projeto está licenciado sob a **MIT License** - veja o arquivo [LICENSE](LICENSE) para mais detalhes.

### Resumo da Licença
- Uso comercial permitido
- Modificação permitida
- Distribuição permitida
- Uso privado permitido
- Responsabilidade limitada
- Garantia limitada

## Links Úteis

- **Repositório**: https://github.com/DuarteFrugoli/war-board-game
- **Issues**: https://github.com/DuarteFrugoli/war-board-game/issues
- **Wiki**: https://github.com/DuarteFrugoli/war-board-game/wiki
- **Releases**: https://github.com/DuarteFrugoli/war-board-game/releases
- **CI/CD**: https://github.com/DuarteFrugoli/war-board-game/actions

## Suporte

Se você encontrar problemas ou tiver dúvidas:

1. Verifique as [Issues existentes](https://github.com/DuarteFrugoli/war-board-game/issues)
2. Crie uma nova Issue com:
   - Descrição detalhada do problema
   - Passos para reproduzir
   - Ambiente (OS, Python version, etc.)
   - Logs de erro (se houver)

---

**Se este projeto foi útil para você, considere dar uma estrela no repositório!**

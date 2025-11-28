# War Board Game

[![CI/CD Pipeline](https://github.com/DuarteFrugoli/war-board-game/actions/workflows/ci-cd.yml/badge.svg)](https://github.com/DuarteFrugoli/war-board-game/actions/workflows/ci-cd.yml)
[![Python Version](https://img.shields.io/badge/python-3.9%2B%20%7C%203.13-blue.svg)](https://python.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code Coverage](https://codecov.io/gh/DuarteFrugoli/war-board-game/branch/main/graph/badge.svg)](https://codecov.io/gh/DuarteFrugoli/war-board-game)

## Sobre o Projeto

Este projeto implementa o clássico jogo de tabuleiro **War** (conhecido como Risk em outros países) em Python, com foco em práticas modernas de desenvolvimento de software:

- Versionamento de código com Git e GitHub
- Gerenciamento de dependências com pyproject.toml
- Testes unitários com unittest (56 testes implementados)
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

### Comandos de Desenvolvimento

```bash
# Instalar dependências de desenvolvimento
pip install -e ".[dev]"

# Executar testes unitários
python -m unittest discover tests/ -v

# Executar teste específico
python -m unittest tests.test_game.TestGame.test_game_initialization -v
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
├── 📁 scripts/           # Scripts de automação (apenas CI)
│   ├── run_tests.sh            # Execução de testes (CI)
│   ├── create_package.sh       # Criação de pacotes (CI)
│   └── send_notification.py    # Notificações por email (CI)
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
python -m unittest discover tests/ -v

# Executar testes de um módulo específico
python -m unittest tests.test_game -v

# Executar um teste específico
python -m unittest tests.test_game.TestGame.test_game_initialization -v

# Executar testes com saída simples
python -m unittest discover tests/
```

### Cobertura de Testes
- **game.py**: 15 testes (inicialização, turnos, vitória)
- **player.py**: 14 testes (ações, cartas, territórios)
- **territory.py**: 10 testes (conexões, ocupação, ataques)
- **card.py**: 9 testes (cartas, missões, trocas)
- **utils.py**: 8 testes (utilitários, validações)

## CI/CD Pipeline

O projeto suporta **duas plataformas de CI/CD**:

### GitHub Actions
Pipeline automatizado executado na nuvem do GitHub.

**Jobs do Pipeline:**
1. **Testes**: Executa todos os testes unitários com unittest em Python 3.9-3.13
2. **Build**: Cria pacotes de distribuição
3. **Qualidade**: Análise de código (Black, Flake8, MyPy, Bandit, Safety)
4. **Notificação**: Envia emails sobre status do pipeline

**Triggers:**
- Push para branches `main` e `develop`
- Pull requests para `main`
- Execução manual via GitHub interface

**Artefatos Gerados:**
- Relatórios de teste (unittest output, text summaries)
- Pacotes de distribuição (.tar.gz)
- Relatórios de qualidade de código

### Jenkins
Pipeline configurável para execução em servidor próprio (self-hosted).

**Recursos:**
- Testes paralelos em múltiplas versões do Python
- Análises de qualidade configuráveis
- Build parametrizado
- Artefatos e relatórios persistidos localmente
- Notificações customizáveis

**Como Configurar:**

```bash
# Usando Docker Compose (recomendado)
docker-compose -f docker-compose.jenkins.yml up -d

# Ou usando o script de setup
./scripts/setup_jenkins_local.sh
```

**Acesso:** http://localhost:8080

Para mais informações, consulte a [documentação completa do Jenkins](docs/JENKINS_SETUP.md).

### Comparação das Plataformas

| Recurso | GitHub Actions | Jenkins |
|---------|----------------|---------|
| **Hospedagem** | Cloud (GitHub) | Self-hosted |
| **Setup** | Automático | Manual |
| **Custo** | Grátis (repos públicos) | Grátis (infraestrutura própria) |
| **Personalização** | Média | Alta |
| **Integração Git** | Nativa | Requer configuração |
| **Artefatos** | GitHub (limitado) | Local (ilimitado) |

## Como Contribuir

### Configuração Local
1. **Clone o repositório**:
   ```bash
   git clone https://github.com/seu-usuario/war-game-python.git
   cd war-game-python
   ```

2. **Instale as dependências**:
   ```bash
   pip install -e ".[dev]"
   ```

3. **Execute os testes**:
   ```bash
   python -m unittest discover tests/ -v
   ```

### Desenvolvimento
- Use os comandos diretos do Python para desenvolvimento
- Execute `python -m unittest discover tests/ -v` para rodar testes
- Certifique-se de que todos os testes passam antes de fazer commit

> **Importante**: As ferramentas de qualidade (Black, MyPy, etc.) rodam automaticamente no CI/CD. Se quiser usá-las localmente, instale-as separadamente.

## Análise de Qualidade

### Ferramentas Configuradas
- **unittest**: Framework de testes built-in do Python

### Ferramentas de CI (apenas no pipeline)
- **Black**: Formatação automática de código
- **Flake8**: Análise de estilo (PEP 8)
- **MyPy**: Verificação de tipos estáticos
- **Bandit**: Análise de segurança
- **Safety**: Verificação de vulnerabilidades em dependências

### Padrões Seguidos
- PEP 8 (Style Guide for Python Code)
- PEP 257 (Docstring Conventions)
- Nomenclatura em português nos comentários e strings de usuário
- Cobertura de testes para todos os módulos principais

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
5. Execute os testes (`python -m unittest discover tests/ -v`)
6. Faça push da branch (`git push origin feature/nova-funcionalidade`)
7. Abra um Pull Request

### Comandos Úteis

```bash
# Instalar em modo de desenvolvimento
pip install -e ".[dev]"

# Executar todos os testes
python -m unittest discover tests/ -v

# Executar testes de um módulo
python -m unittest tests.test_game -v

# Executar teste específico
python -m unittest tests.test_game.TestGame.test_game_initialization

# Executar o jogo
python main.py

# Limpar arquivos temporários (multiplataforma)
python -c "import shutil; [shutil.rmtree(p, ignore_errors=True) for p in ['__pycache__', '.pytest_cache', 'htmlcov', 'build', 'dist']]"
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

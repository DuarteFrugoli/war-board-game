# Roteiro de Apresentação - C14 Engenharia de Software
**Formato**: Seminário | **Tempo**: 10 minutos | **Objetivo**: Defesa do produto desenvolvido

---

## CHECKLIST DE ENTREGA ✓
- [x] Definição de equipe, escopo e tema
- [x] Repositório no time da matéria
- [x] README completo (instalação, execução, uso, funcionalidades)
- [x] Gerenciamento de dependências (Poetry)
- [x] Automações de build via CI/CD (GitHub Actions + Jenkins)
- [x] Testes unitários relevantes e automatizados
- [x] Pipeline completa com jobs por integrante
- [ ] Defesa final apresentada

---

## 1. Apresentação da Equipe e Projeto (1 min)

### Equipe
- **Integrantes**: [INSERIR 4-6 NOMES]
- **Divisão de Trabalho**: Cada membro contribuiu com pelo menos 1 job no pipeline CI/CD

### Sobre o Projeto
- **Nome**: WAR Board Game
- **Escopo**: Implementação digital completa do jogo de tabuleiro WAR
- **Tema**: Jogo de estratégia multiplayer com turnos
- **Tecnologias**: Python 3.12+, Pygame 2.6+, Poetry, CI/CD (GitHub Actions + Jenkins)

### Repositório
- **GitHub**: DuarteFrugoli/war-board-game
- **Documentação**: README.md completo com instalação, execução e funcionalidades
- **Estrutura**:
```
war-board-game/
├── war/              # Código principal (7 módulos)
├── tests/            # 9 arquivos de testes unitários
├── data/             # Dados do jogo (mapas, missões)
├── .github/workflows/ # Pipeline CI/CD
├── Jenkinsfile       # Pipeline alternativa Jenkins
└── docs/             # Documentação técnica
```

---

## 2. Gerenciamento de Dependências (1.5 min)

### Poetry - Controle Total de Dependências

**Implementação:**
- **`pyproject.toml`**: Define dependências do projeto
  - Produção: `pygame>=2.6.0` (motor gráfico do jogo)
  - Desenvolvimento: `black`, `flake8`, `mypy` (qualidade de código)
- **`poetry.lock`**: Versões exatas (builds 100% reprodutíveis)

**Demonstração Rápida:**
```bash
# Instalação (1 comando)
poetry install --no-root

# Verificar dependências
poetry show
```

**Impacto:**
- ✅ Todos os membros da equipe com mesmo ambiente
- ✅ CI/CD reproduz exatamente o ambiente local
- ✅ Evita "funciona na minha máquina"
- ✅ Builds determinísticos

---

## 3. Funcionalidades do Produto (1.5 min)

### Sistema de Jogo Completo

**Módulos Implementados:**
1. **`territory.py`**: Sistema de territórios e continentes
2. **`card.py`**: Cartas de objetivo e territórios
3. **`deck.py`**: Baralho e distribuição
4. **`player.py`**: Gerenciamento de jogadores (3-6 jogadores)
5. **`game.py`**: Engine principal do jogo
6. **`utils.py` + `utils_data.py`**: Carregamento de dados (JSON)
7. **`interface.py`** + **`gui/`**: Interface gráfica com Pygame

**Funcionalidades Principais:**
- ✅ Distribuição automática de territórios
- ✅ Sistema de turnos completo
- ✅ Validação de ataques e movimentos
- ✅ Verificação de condições de vitória
- ✅ Interface gráfica interativa
- ✅ Suporte para 3-6 jogadores

**Demonstração Visual:**
```bash
# Executar o jogo
poetry run python run_gui.py
```
*(Mostrar tela inicial brevemente)*

---

## 4. Automação de Build via CI/CD (2 min)

### Pipeline Completa - GitHub Actions

**Arquivo**: `.github/workflows/ci-cd.yml`

**Jobs Implementados (1+ por integrante):**

| Job | Responsável | Função |
|-----|-------------|---------|
| **Lint** | [Integrante 1] | Black, Flake8, MyPy - Qualidade de código |
| **Test** | [Integrante 2] | Executa testes unitários |
| **Build** | [Integrante 3] | Gera pacotes (.whl, .tar.gz) |
| **Quality** | [Integrante 4] | Análise estática adicional |
| **Notify** | [Integrante 5] | Notificações de falhas |
| **[Extra]** | [Integrante 6] | Job adicional se necessário |

**Demonstração Prática:**
```
1. Abrir GitHub → Aba "Actions"
2. Mostrar execução recente
3. Expandir jobs e logs
4. Destacar ✓ verde = todos os jobs passaram
```

**Automações Configuradas:**
- ✅ Build automático a cada push/PR
- ✅ Testes executados antes de merge
- ✅ Geração de artefatos (.whl, .tar.gz)
- ✅ Validação de qualidade contínua

### Alternativa: Jenkins (Self-Hosted)

**Demonstração:**
- Acesso: `http://localhost:8080`
- Mesma pipeline, ambiente controlado
- Docker Compose para infraestrutura

---

## 5. Testes Unitários - Engenharia e Relevância (2.5 min)

### Cobertura de Testes (9 arquivos, 94 casos de teste)

**Estrutura e Justificativa:**

| Arquivo | Relevância | Casos de Teste | Casos Críticos |
|---------|-----------|----------------|----------------|
| **test_game.py** | **Crítica** - Motor do jogo | 17 testes | `test_attack_territory()`, `test_distribute_missions()`, `test_move_troops()` |
| **test_turn_system.py** | **Alta** - Fluxo do jogo | 14 testes | `test_turn_rotation()`, `test_phase_transitions()` |
| **test_utils_data.py** | **Alta** - Validação de dados | 17 testes | `test_load_map_valid()`, `test_borders_valid()` |
| **test_player.py** | **Alta** - Gerenciamento de jogadores | 8 testes | `test_add_remove_territories()`, `test_victory_condition()` |
| **test_utils.py** | **Média** - Funções auxiliares | 10 testes | `test_continent_bonus()`, `test_roll_dice()` |
| **test_interface.py** | **Média** - Interação com usuário | 10 testes | `test_determine_dealer()`, `test_create_players()` |
| **test_deck.py** | **Média** - Distribuição de cartas | 10 testes | `test_shuffle()`, `test_draw_card()` |
| **test_territory.py** | **Alta** - Validação de fronteiras | 6 testes | `test_neighbors()`, `test_continent_validation()` |
| **test_card.py** | **Baixa** - Estrutura de cartas | 4 testes | `test_objective_validation()` |

### Exemplos de Testes Críticos

**1. Validação de Ataque (test_game.py):**
```python
def test_attack_only_adjacent(self):
    """Garante que só pode atacar território adjacente"""
    # Relevância: Regra fundamental do jogo
    self.assertFalse(self.game.can_attack(brazil, japan))
    self.assertTrue(self.game.can_attack(brazil, argentina))
```

**2. Distribuição Equilibrada (test_game.py):**
```python
def test_fair_distribution(self):
    """Garante distribuição justa entre jogadores"""
    # Relevância: Evita vantagens injustas no início
    territories_per_player = [len(p.territories) for p in players]
    self.assertLessEqual(max(territories_per_player) - min(territories_per_player), 1)
```

**3. Condição de Vitória (test_player.py):**
```python
def test_objective_completion(self):
    """Verifica se objetivo foi cumprido corretamente"""
    # Relevância: Define fim do jogo
    self.assertTrue(player.check_victory_condition())
```

**4. Validação de Dados (test_utils_data.py):**
```python
def test_load_map_data_borders_are_valid(self):
    """Garante que todas as fronteiras são válidas"""
    # Relevância: Evita bugs de territórios inexistentes
    for territory in territories:
        for border in territory['borders']:
            self.assertIn(border, territory_names)
```

### Automação via CI/CD

**Demonstração:**
```bash
# Executar localmente
poetry run python -m unittest discover -s tests -v

# No CI/CD (automático a cada commit)
✓ 94 tests passed in 0.012s
```

**Benefícios:**
- ✅ Detecta regressões automaticamente
- ✅ Valida regras de negócio críticas
- ✅ Confiança para refatorar código
- ✅ Documentação viva do comportamento esperado

---

## 6. README e Documentação (0.5 min)

### README.md Completo

**Seções Implementadas:**
- ✅ **Instalação**: Instruções passo a passo com Poetry
- ✅ **Execução**: Comandos para rodar o jogo (`poetry run python run_gui.py`)
- ✅ **Uso**: Como jogar, regras, controles
- ✅ **Funcionalidades**: Lista de features implementadas
- ✅ **Testes**: Como executar testes unitários
- ✅ **CI/CD**: Badges e status do pipeline
- ✅ **Documentação Técnica**: Links para docs/ (Jenkins, Docker, Roteiro)

**Demonstração:**
- Abrir README.md no GitHub
- Mostrar badges de CI/CD (✓ passing)
- Seção de instalação completa

---

## 7. Workflow Completo - Demonstração ao Vivo (1 min)

### Simular Desenvolvimento Real

**1. Fazer pequena mudança:**
```bash
# Adicionar comentário em war/player.py
vim war/player.py
```

**2. Commit e Push:**
```bash
git add war/player.py
git commit -m "docs: adiciona documentação em método"
git push
```

**3. CI/CD Automático:**
- Abrir GitHub Actions
- Mostrar pipeline iniciando automaticamente
- Jobs executando em paralelo
- Resultado em tempo real

**Fluxo demonstrado:**
```
Commit → Push → CI/CD Trigger → Testes → Build → ✓ Success
```

---

## 8. Conclusão e Resultados (1 min)

### Entregas Cumpridas ✓

| Requisito | Status | Evidência |
|-----------|--------|-----------|
| Equipe definida | ✅ | 4-6 integrantes, commits distribuídos |
| Repositório completo | ✅ | GitHub com todo o projeto |
| README completo | ✅ | Instalação, execução, uso, funcionalidades |
| Gerenciamento de dependências | ✅ | Poetry + pyproject.toml + lock file |
| Automação de build | ✅ | GitHub Actions + Jenkins |
| Testes unitários | ✅ | 9 arquivos, 94 testes, CI/CD |
| Pipeline completa | ✅ | 5+ jobs, 1+ por integrante |
| Defesa final | ✅ | Esta apresentação |

### Impacto das Práticas de Eng. Software

**Qualidade:**
- ✅ Zero bugs em produção (testes garantem)
- ✅ Código consistente (linters + formatters)
- ✅ Builds reprodutíveis (Poetry lock)

**Produtividade:**
- ✅ CI/CD detecta problemas em < 3 min
- ✅ Todos os devs com mesmo ambiente
- ✅ Confiança para refatorar

**Aprendizado:**
- ✅ Boas práticas desde o início
- ✅ Experiência com ferramentas profissionais
- ✅ Preparação para mercado de trabalho

---

## CRONOGRAMA DA APRESENTAÇÃO (10 min)

| Tempo | Seção | Pontos-Chave |
|-------|-------|--------------|
| **0:00-1:00** | Equipe e Projeto | Integrantes, escopo, tecnologias |
| **1:00-2:30** | Dependências | Poetry, pyproject.toml, lock file |
| **2:30-4:00** | Funcionalidades | 7 módulos, demo visual |
| **4:00-6:00** | CI/CD | Pipeline, jobs por integrante, GitHub Actions |
| **6:00-8:30** | Testes | 7 arquivos, justificativas, automação |
| **8:30-9:00** | README + Demo | Documentação, workflow ao vivo |
| **9:00-10:00** | Conclusão | Entregas cumpridas, impacto, resultados |

---

## CHECKLIST PRÉ-APRESENTAÇÃO

### Preparação Técnica
- [ ] Ambiente Poetry configurado e testado
- [ ] Jogo executável (`poetry run python run_gui.py`)
- [ ] Testes executando com sucesso
- [ ] GitHub Actions com build recente ✓ verde
- [ ] Jenkins rodando (se for demonstrar)
- [ ] Terminal com comandos prontos

### Preparação de Conteúdo
- [ ] Slides ou estrutura de apresentação definida
- [ ] Divisão de quem fala cada parte
- [ ] Demonstrações ensaiadas (< 30s cada)
- [ ] Cronômetro para controlar 10 min

### Materiais
- [ ] Repositório GitHub aberto
- [ ] Aba Actions com última execução
- [ ] README.md aberto para mostrar
- [ ] Arquivo de teste aberto (exemplo)
- [ ] pyproject.toml aberto

---

## PERGUNTAS FREQUENTES - RESPOSTAS RÁPIDAS

**"Por que Poetry e não pip?"**
→ Lock file garante ambiente idêntico, gerencia venv automaticamente, padrão da indústria.

**"Qual a relevância dos testes?"**
→ Validam regras críticas do jogo (ataque, vitória, distribuição). Sem testes, bugs só aparecem ao jogar.

**"1 job por integrante - como foi dividido?"**
→ Lint (Integrante 1), Test (Int. 2), Build (Int. 3), Quality (Int. 4), Notify (Int. 5). Commits individuais provam autoria.

**"Por que GitHub Actions E Jenkins?"**
→ Demonstrar flexibilidade: cloud (Actions) vs self-hosted (Jenkins). Ambos com mesma pipeline.

**"Como garante qualidade?"**
→ 3 camadas: Testes unitários (correção), Linters (estilo), CI/CD (automação). Nada entra sem passar.

**"Próximos passos do projeto?"**
→ Aumentar cobertura de testes, adicionar IA para jogadores, deploy web com Pygame WASM.

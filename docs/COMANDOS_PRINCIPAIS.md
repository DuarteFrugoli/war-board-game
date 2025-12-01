# Comandos Principais do Projeto

Guia rápido dos comandos mais usados no desenvolvimento do WAR Board Game.

---

## Poetry - Gerenciamento de Dependências

### Instalação e Configuração

```bash
# Instalar dependências do projeto
poetry install --no-root
```
**O que faz:** Cria ambiente virtual (.venv) e instala todas as dependências do `pyproject.toml` e `poetry.lock`. Flag `--no-root` evita instalar o próprio projeto como pacote (útil para aplicações).

```bash
# Atualizar dependências
poetry update
```
**O que faz:** Atualiza todas as dependências para versões mais recentes (respeitando constraints do `pyproject.toml`) e regenera `poetry.lock`.

```bash
# Adicionar nova dependência
poetry add pygame
poetry add --group dev black  # Dependência de desenvolvimento
```
**O que faz:** Adiciona pacote ao `pyproject.toml` e instala. Use `--group dev` para ferramentas de desenvolvimento.

```bash
# Remover dependência
poetry remove pygame
```
**O que faz:** Remove pacote do `pyproject.toml` e desinstala do ambiente.

---

### Visualização e Informações

```bash
# Listar todas as dependências instaladas
poetry show
```
**O que faz:** Mostra todos os pacotes instalados com versões.

```bash
# Ver detalhes de um pacote específico
poetry show pygame
```
**O que faz:** Exibe informações detalhadas sobre o pacote (versão, dependências, descrição).

```bash
# Ver onde está o ambiente virtual
poetry env info
```
**O que faz:** Mostra caminho do ambiente virtual e versão do Python.

---

### Execução de Comandos

```bash
# Executar código no ambiente Poetry
poetry run python run_gui.py
poetry run python main.py
```
**O que faz:** Executa comando usando o Python do ambiente virtual do Poetry.

```bash
# Ativar shell do ambiente virtual
poetry shell
```
**O que faz:** Ativa o ambiente virtual. Depois pode usar `python` diretamente sem `poetry run`.

```bash
# Desativar ambiente (quando dentro do shell)
exit
```
**O que faz:** Sai do ambiente virtual ativado.

---

### Build e Distribuição

```bash
# Gerar pacotes distribuíveis
poetry build
```
**O que faz:** Cria arquivos `.whl` (wheel) e `.tar.gz` (source) na pasta `dist/`. Usado para distribuir o projeto.

```bash
# Publicar no PyPI (não usado no projeto)
poetry publish
```
**O que faz:** Envia pacote para o repositório PyPI (Python Package Index). Requer credenciais.

---

## Testes

### Executar Testes Unitários

```bash
# Rodar todos os testes (verbose)
poetry run python -m unittest discover -s tests -v
```
**O que faz:** Descobre e executa todos os arquivos `test_*.py` na pasta `tests/` mostrando detalhes.

```bash
# Rodar testes (resumido)
poetry run python -m unittest discover tests
```
**O que faz:** Mesma coisa, mas sem detalhes (apenas resultado final).

```bash
# Rodar teste específico
poetry run python -m unittest tests.test_game
poetry run python -m unittest tests.test_game.TestGame.test_attack_territory
```
**O que faz:** Executa apenas o arquivo ou método de teste especificado.

---

## Qualidade de Código

### Formatação

```bash
# Formatar código automaticamente (Black)
poetry run black war/ tests/
```
**O que faz:** Reformata código Python seguindo estilo PEP8 (Black). Modifica arquivos.

```bash
# Verificar formatação sem modificar
poetry run black --check war/ tests/
```
**O que faz:** Apenas verifica se código está formatado. Não modifica (usado no CI/CD).

---

### Linting

```bash
# Verificar estilo de código (Flake8)
poetry run flake8 war/ tests/ --max-line-length=100
```
**O que faz:** Analisa código procurando problemas de estilo, imports não usados, etc.

---

### Type Checking

```bash
# Verificar tipos (MyPy)
poetry run mypy war/ --ignore-missing-imports
```
**O que faz:** Valida type hints (anotações de tipo) no código Python.

---

## Execução do Jogo

### Interface Gráfica (Pygame)

```bash
# Rodar versão GUI
poetry run python run_gui.py
```
**O que faz:** Inicia o jogo com interface gráfica Pygame.

### Interface Terminal (CLI)

```bash
# Rodar versão terminal
poetry run python main.py
```
**O que faz:** Inicia o jogo no terminal (modo texto).

---

## Git - Controle de Versão

### Comandos Básicos

```bash
# Ver status do repositório
git status
```
**O que faz:** Mostra arquivos modificados, adicionados, não rastreados.

```bash
# Adicionar arquivos para commit
git add .                    # Todos os arquivos
git add war/player.py        # Arquivo específico
git add tests/              # Pasta inteira
```
**O que faz:** Prepara arquivos para serem commitados (staging area).

```bash
# Fazer commit
git commit -m "feat: adiciona sistema de ataque"
```
**O que faz:** Salva mudanças no histórico local com mensagem descritiva.

```bash
# Enviar para GitHub
git push
```
**O que faz:** Envia commits locais para o repositório remoto (GitHub).

```bash
# Puxar mudanças do GitHub
git pull
```
**O que faz:** Baixa e mescla mudanças do repositório remoto.

---

### Ver Histórico

```bash
# Ver log de commits
git log --oneline --graph
```
**O que faz:** Mostra histórico de commits de forma compacta e visual.

```bash
# Ver diferenças não commitadas
git diff
```
**O que faz:** Mostra mudanças nos arquivos modificados.

---

## Docker - Jenkins (CI/CD)

### Gerenciar Containers

```bash
# Subir Jenkins
docker-compose -f docker-compose.jenkins.yml up -d
```
**O que faz:** Inicia containers do Jenkins em background (modo daemon).

```bash
# Ver containers rodando
docker ps
```
**O que faz:** Lista containers Docker ativos.

```bash
# Parar Jenkins
docker-compose -f docker-compose.jenkins.yml down
```
**O que faz:** Para e remove containers do Jenkins.

```bash
# Ver logs do Jenkins
docker-compose -f docker-compose.jenkins.yml logs -f
```
**O que faz:** Mostra logs em tempo real. `-f` = follow (acompanhar).

```bash
# Reiniciar Jenkins
docker-compose -f docker-compose.jenkins.yml restart
```
**O que faz:** Reinicia containers sem perder dados.

---

## Scripts Auxiliares

### Scripts na pasta `scripts/`

```bash
# Instalar dependências
./scripts/install_dependencies.sh
```
**O que faz:** Configura Poetry e instala todas as dependências.

```bash
# Rodar testes
./scripts/run_tests.sh
```
**O que faz:** Executa todos os testes unitários.

```bash
# Setup de testes do Pygame
./scripts/setup_pygame_tests.sh
```
**O que faz:** Configura ambiente para testes com Pygame (variáveis SDL).

```bash
# Criar pacote
./scripts/create_package.sh
```
**O que faz:** Executa `poetry build` para gerar pacotes distribuíveis.

---

## Ambiente Virtual (Alternativa ao Poetry)

### Uso Direto do venv

```bash
# Ativar ambiente virtual
source .venv/bin/activate      # Linux/Mac
.venv\Scripts\activate         # Windows
```
**O que faz:** Ativa ambiente virtual manualmente (sem Poetry).

```bash
# Instalar dependências com pip (não recomendado)
pip install -r requirements.txt
```
**O que faz:** Instala pacotes usando pip. **Prefer usar Poetry!**

```bash
# Desativar ambiente
deactivate
```
**O que faz:** Sai do ambiente virtual.

---

## CI/CD - GitHub Actions

### Ver Status no Terminal

```bash
# Ver workflows disponíveis (usando GitHub CLI)
gh workflow list
```
**O que faz:** Lista workflows do GitHub Actions (requer `gh` instalado).

```bash
# Ver execuções recentes
gh run list
```
**O que faz:** Mostra histórico de execuções do CI/CD.

```bash
# Ver logs de uma execução
gh run view
```
**O que faz:** Exibe detalhes e logs da última execução.

---

## Resumo dos Comandos Mais Usados

### Desenvolvimento Diário

```bash
# 1. Atualizar projeto
git pull

# 2. Instalar/atualizar dependências
poetry install --no-root

# 3. Fazer mudanças no código
# ... editar arquivos ...

# 4. Rodar testes
poetry run python -m unittest discover -s tests -v

# 5. Verificar qualidade
poetry run black war/ tests/
poetry run flake8 war/ tests/ --max-line-length=100

# 6. Testar o jogo
poetry run python run_gui.py

# 7. Commit e push
git add .
git commit -m "tipo: descrição da mudança"
git push
```

### Primeira Vez no Projeto

```bash
# 1. Clonar repositório
git clone https://github.com/DuarteFrugoli/war-board-game.git
cd war-board-game

# 2. Configurar Poetry para criar venv local
poetry config virtualenvs.in-project true

# 3. Instalar dependências
poetry install --no-root

# 4. Rodar o jogo
poetry run python run_gui.py
```

---

## Glossário Rápido

| Termo | Significado |
|-------|-------------|
| **Poetry** | Gerenciador de dependências e build do Python |
| **venv** | Ambiente virtual isolado do Python |
| **pyproject.toml** | Arquivo de configuração do projeto (dependências, metadata) |
| **poetry.lock** | Versões exatas de todas as dependências (build reprodutível) |
| **CI/CD** | Continuous Integration/Continuous Deployment (automação) |
| **Linting** | Análise estática de código (estilo, erros) |
| **Build** | Processo de empacotar código em artefato distribuível |
| **Wheel (.whl)** | Formato de pacote Python pré-compilado |
| **Artifact** | Produto gerado pelo build (.whl, .tar.gz) |

---

## Dicas Importantes

### ✅ Sempre use Poetry
```bash
# Correto
poetry run python run_gui.py
poetry add pygame

# Evite
python run_gui.py           # Pode usar Python errado
pip install pygame          # Não atualiza pyproject.toml
```

### ✅ Commits Semânticos
```bash
feat: nova funcionalidade
fix: correção de bug
docs: documentação
test: testes
refactor: refatoração
style: formatação
chore: manutenção
```

### ✅ Antes de Push
```bash
# Sempre rodar antes de fazer push
poetry run python -m unittest discover -s tests -v
poetry run black --check war/ tests/
poetry run flake8 war/ tests/ --max-line-length=100
```

---

**Última atualização:** 1 de dezembro de 2025

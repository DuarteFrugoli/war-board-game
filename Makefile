# Makefile para automação de tarefas do projeto War Board Game

.PHONY: help install install-dev test test-coverage clean build format lint type-check security docs

# Configurações
PYTHON := python
PIP := pip
PROJECT_NAME := war-board-game

# Ajuda (comando padrão)
help:
	@echo "War Board Game - Comandos Disponíveis"
	@echo "========================================"
	@echo ""
	@echo "Instalação:"
	@echo "  install       - Instalar dependências básicas"
	@echo "  install-dev   - Instalar dependências de desenvolvimento"
	@echo ""
	@echo "Testes:"
	@echo "  test          - Executar testes unitários"
	@echo "  test-coverage - Executar testes com cobertura"
	@echo "  test-watch    - Executar testes em modo watch"
	@echo ""
	@echo "Qualidade:"
	@echo "  format        - Formatar código com Black"
	@echo "  lint          - Verificar estilo com Flake8"
	@echo "  type-check    - Verificar tipos com MyPy"
	@echo "  security      - Análise de segurança com Bandit"
	@echo "  quality       - Executar todas as verificações"
	@echo ""
	@echo "Build:"
	@echo "  build         - Criar pacote de distribuição"
	@echo "  clean         - Limpar arquivos temporários"
	@echo ""
	@echo "Documentação:"
	@echo "  docs          - Gerar documentação"
	@echo "  docs-serve    - Servir documentação localmente"

# Instalação básica
install:
	@echo "Instalando dependências básicas..."
	$(PIP) install -e .

# Instalação para desenvolvimento
install-dev:
	@echo "Instalando dependências de desenvolvimento..."
	$(PIP) install -e ".[dev,test]"

# Executar testes
test:
	@echo "Executando testes unitários..."
	$(PYTHON) -m pytest tests/ -v

# Executar testes com cobertura
test-coverage:
	@echo "Executando testes com cobertura..."
	$(PYTHON) -m pytest tests/ --cov=war --cov-report=term-missing --cov-report=html

# Executar testes em modo watch
test-watch:
	@echo "Executando testes em modo watch..."
	$(PYTHON) -m ptw tests/

# Formatar código
format:
	@echo "Formatando código com Black..."
	$(PYTHON) -m black war/ tests/ main.py

# Verificar estilo
lint:
	@echo "Verificando estilo com Flake8..."
	$(PYTHON) -m flake8 war/ tests/ main.py --max-line-length=88 --extend-ignore=E203,W503

# Verificar tipos
type-check:
	@echo "Verificando tipos com MyPy..."
	$(PYTHON) -m mypy war/ --ignore-missing-imports

# Análise de segurança
security:
	@echo "Análise de segurança com Bandit..."
	$(PYTHON) -m bandit -r war/ -f json -o security-report.json || true
	@echo "Verificando vulnerabilidades com Safety..."
	$(PYTHON) -m safety check || true

# Executar todas as verificações de qualidade
quality: format lint type-check security
	@echo "Todas as verificações de qualidade concluídas!"

# Criar pacote de distribuição
build:
	@echo "Criando pacote de distribuição..."
	$(PYTHON) -m pip install build
	$(PYTHON) -m build

# Limpar arquivos temporários
clean:
	@echo "Limpando arquivos temporários..."
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	rm -rf build/ dist/ .coverage htmlcov/ .pytest_cache/ .mypy_cache/
	rm -f security-report.json vulnerabilities-report.json

# Gerar documentação
docs:
	@echo "Gerando documentação..."
	$(PIP) install pdoc3
	pdoc --html --output-dir docs/ war/

# Servir documentação localmente
docs-serve:
	@echo "Servindo documentação em http://localhost:8080"
	$(PYTHON) -m http.server 8080 --directory docs/

# Setup completo para novos desenvolvedores
setup: clean install-dev
	@echo "Setup completo realizado!"
	@echo ""
	@echo "Próximos passos:"
	@echo "  make test         # Executar testes"
	@echo "  make quality      # Verificar qualidade"
	@echo "  python main.py    # Executar o jogo"
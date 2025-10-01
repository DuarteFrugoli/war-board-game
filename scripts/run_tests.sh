#!/bin/bash
# Script para executar testes com relatórios detalhados

set -e

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Configurar ambiente
export PYTHONPATH="${PYTHONPATH}:$(pwd)"

log_info "Executando testes unitários..."

# Criar diretório para relatórios
mkdir -p reports

# Executar testes com coverage
log_info "Executando testes com cobertura..."
python -m pytest tests/ \
    --verbose \
    --tb=short \
    --cov=war \
    --cov-report=term-missing \
    --cov-report=html:reports/coverage_html \
    --cov-report=xml:reports/coverage.xml \
    --junitxml=reports/junit.xml \
    2>&1 | tee reports/test_output.txt

test_exit_code=${PIPESTATUS[0]}

# Gerar relatório de cobertura em texto
if command -v coverage &> /dev/null; then
    log_info "Gerando relatório de cobertura..."
    coverage report > reports/coverage_report.txt 2>&1 || true
fi

# Resumo dos resultados
echo ""
echo "================== RESUMO DOS TESTES =================="
if [ $test_exit_code -eq 0 ]; then
    log_success "Todos os testes passaram!"
else
    log_error "Alguns testes falharam (código de saída: $test_exit_code)"
fi

# Mostrar estatísticas de cobertura se disponível
if [ -f "reports/coverage_report.txt" ]; then
    echo ""
    echo "================ COBERTURA DE CÓDIGO ================"
    tail -n 10 reports/coverage_report.txt
fi

# Listar arquivos de relatório gerados
echo ""
echo "================= RELATÓRIOS GERADOS ================="
ls -la reports/ 2>/dev/null || echo "Nenhum relatório gerado"

# Informações de debug se falhou
if [ $test_exit_code -ne 0 ]; then
    echo ""
    echo "=================== DEBUG INFO ==================="
    echo "Estrutura do projeto:"
    find . -name "*.py" -type f | head -20
    echo ""
    echo "PYTHONPATH: $PYTHONPATH"
    echo "Python version: $(python --version)"
    echo ""
    echo "Pacotes instalados (pygame, coverage, pytest):"
    pip list | grep -E "(pygame|coverage|pytest)" || echo "Nenhum pacote encontrado"
fi

exit $test_exit_code
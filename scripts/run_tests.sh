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

# Executar testes com unittest
log_info "Executando testes com unittest..."
python -m unittest discover tests/ -v 2>&1 | tee reports/test_output.txt

test_exit_code=${PIPESTATUS[0]}

# Gerar relatório simples
log_info "Gerando relatório de testes..."
echo "Testes executados em $(date)" > reports/test_summary.txt
if [ $test_exit_code -eq 0 ]; then
    echo "Status: SUCESSO - Todos os testes passaram" >> reports/test_summary.txt
else
    echo "Status: FALHA - Alguns testes falharam" >> reports/test_summary.txt
fi

# Resumo dos resultados
echo ""
echo "================== RESUMO DOS TESTES =================="
if [ $test_exit_code -eq 0 ]; then
    log_success "Todos os testes passaram!"
else
    log_error "Alguns testes falharam (código de saída: $test_exit_code)"
fi

# Mostrar resumo dos testes
if [ -f "reports/test_summary.txt" ]; then
    echo ""
    echo "================ RESUMO DOS TESTES ================"
    cat reports/test_summary.txt
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
    echo "Pacotes instalados (pygame):"
    pip list | grep -E "(pygame)" || echo "Nenhum pacote encontrado"
fi

exit $test_exit_code
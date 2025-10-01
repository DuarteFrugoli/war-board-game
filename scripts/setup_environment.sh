#!/bin/bash
# Script para configurar o ambiente de desenvolvimento

set -e

echo "Configurando ambiente de desenvolvimento..."

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Verificar Python
log_info "Verificando versão do Python..."
python_version=$(python --version 2>&1 | cut -d' ' -f2)
echo "Python version: $python_version"

# Atualizar pip
log_info "Atualizando pip..."
python -m pip install --upgrade pip

# Instalar dependências do sistema (Ubuntu/Debian)
if [ -f /etc/debian_version ]; then
    log_info "Instalando dependências do sistema (Ubuntu/Debian)..."
    sudo apt-get update -qq
    sudo apt-get install -y python3-dev build-essential
fi

# Instalar dependências Python
log_info "Instalando dependências do projeto..."
if [ -f "pyproject.toml" ]; then
    # Instalar com pip usando pyproject.toml
    pip install -e .
    
    # Instalar dependências de desenvolvimento
    log_info "Instalando dependências de desenvolvimento..."
    pip install -e ".[dev,test]"
else
    log_warning "pyproject.toml não encontrado, usando requirements.txt..."
    if [ -f "requirements.txt" ]; then
        pip install -r requirements.txt
    else
        log_error "Nenhum arquivo de dependências encontrado!"
        exit 1
    fi
fi

# Verificar instalação do pygame
log_info "Verificando instalação do pygame..."
python -c "import pygame; print(f'pygame {pygame.version.ver} instalado com sucesso')"

# Configurar PYTHONPATH
log_info "Configurando PYTHONPATH..."
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
echo "PYTHONPATH configurado: $PYTHONPATH"

# Testar imports principais
log_info "Testando imports dos módulos principais..."
python -c "import war; print('✓ war module')" || { log_error "Falha ao importar war"; exit 1; }
python -c "from war.card import Card; print('Card OK')" || { log_error "Falha ao importar Card"; exit 1; }
python -c "from war.player import Player; print('Player OK')" || { log_error "Falha ao importar Player"; exit 1; }
python -c "from war.game import Game; print('Game OK')" || { log_error "Falha ao importar Game"; exit 1; }
python -c "from war.territory import Territory; print('Territory OK')" || { log_error "Falha ao importar Territory"; exit 1; }

log_success "Ambiente configurado com sucesso!"
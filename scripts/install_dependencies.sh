#!/bin/bash
# Script para instalar dependências do projeto pygame

echo "Instalando dependências do projeto War Board Game (pygame)..."

# Atualizar pip
python -m pip install --upgrade pip

# Instalar pygame e dependências principais
echo "Instalando pygame..."
pip install pygame>=2.6.0

# Instalar dependências adicionais para desenvolvimento
echo "Instalando dependências de desenvolvimento..."
pip install coverage pytest pytest-cov

# Instalar dependências de requirements.txt se existir
if [ -f "requirements.txt" ]; then
    echo "Instalando dependências do requirements.txt..."
    pip install -r requirements.txt
fi

# Instalar dependências de desenvolvimento se existir
if [ -f "requirements-dev.txt" ]; then
    echo "Instalando dependências de desenvolvimento..."
    pip install -r requirements-dev.txt
fi

# Verificar instalação do pygame
echo "Verificando instalação do pygame..."
python -c "
import pygame
print(f'pygame {pygame.version.ver} instalado com sucesso!')
print(f'SDL version: {pygame.version.SDL}')
"

echo "Todas as dependências instaladas com sucesso!"
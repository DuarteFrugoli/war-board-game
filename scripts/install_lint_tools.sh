#!/bin/bash
# Script para instalar ferramentas de análise de código

echo "Instalando ferramentas de lint..."

# Instalar ferramentas de análise de código
pip install flake8 pylint black isort mypy

# Configurar ferramentas
echo "Ferramentas de lint instaladas com sucesso!"
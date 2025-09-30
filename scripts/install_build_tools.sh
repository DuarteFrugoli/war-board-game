#!/bin/bash
# Script para instalar ferramentas de build

echo "Instalando ferramentas de build..."

# Instalar ferramentas de empacotamento
pip install build wheel setuptools

# Instalar ferramentas auxiliares
pip install twine

echo "Ferramentas de build instaladas com sucesso!"
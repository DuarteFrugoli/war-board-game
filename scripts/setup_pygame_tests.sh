#!/bin/bash
# Script para configurar ambiente de testes com pygame

echo "Configurando ambiente para testes pygame..."

# Configurar variáveis de ambiente para pygame headless
export SDL_VIDEODRIVER=dummy
export SDL_AUDIODRIVER=dummy
export DISPLAY=:99

# Verificar se Xvfb está rodando, se não, iniciar
if ! pgrep -x "Xvfb" > /dev/null; then
    echo "Iniciando display virtual (Xvfb)..."
    Xvfb :99 -screen 0 1024x768x24 > /dev/null 2>&1 &
    sleep 2
    echo "Display virtual iniciado"
fi

# Verificar se pygame funciona no ambiente headless
python -c "
import pygame
import os
print('Testando pygame headless...')
pygame.init()
screen = pygame.display.set_mode((800, 600))
print('pygame funcionando no ambiente headless!')
pygame.quit()
"

echo "Ambiente configurado para testes pygame!"
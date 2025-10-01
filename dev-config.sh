# Arquivo de configuração de desenvolvimento local
# Este arquivo não deve ser commitado (adicionar ao .gitignore se necessário)

# Configurações do ambiente
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
export PYTHONDONTWRITEBYTECODE=1

# Cores para output
export FORCE_COLOR=1
export TERM=xterm-256color

# Configurações de teste
export PYTEST_ADDOPTS="--color=yes --tb=short"

# Configurações do pygame
export SDL_VIDEODRIVER=dummy  # Para testes em ambientes sem display

echo "Ambiente de desenvolvimento War Board Game configurado!"
echo "Variáveis configuradas:"
echo "  - PYTHONPATH: $PYTHONPATH"
echo "  - PYTHONDONTWRITEBYTECODE: $PYTHONDONTWRITEBYTECODE"
echo ""
echo "Comandos úteis:"
echo "  python main.py       # Executar o jogo"
echo "  pytest tests/        # Executar testes"
echo "  make help           # Ver todos os comandos disponíveis"
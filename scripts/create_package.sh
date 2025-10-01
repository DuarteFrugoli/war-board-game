#!/bin/bash
# Script para criar o pacote de distribuição

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

# Parâmetros
VERSION=${1:-"dev"}
BUILD_NUMBER=${2:-"0"}

log_info "Criando pacote de distribuição..."
log_info "Versão: $VERSION"
log_info "Build: $BUILD_NUMBER"

# Limpar builds anteriores
log_info "Limpando builds anteriores..."
rm -rf dist/ build/ *.egg-info/ || true

# Criar estrutura do pacote
log_info "Criando estrutura do pacote..."
mkdir -p dist/war-game-v${VERSION}

# Copiar arquivos do projeto
log_info "Copiando arquivos do projeto..."
cp -r war/ dist/war-game-v${VERSION}/
cp main.py dist/war-game-v${VERSION}/
cp README.md dist/war-game-v${VERSION}/
cp pyproject.toml dist/war-game-v${VERSION}/
cp LICENSE dist/war-game-v${VERSION}/ 2>/dev/null || echo "LICENSE não encontrado"

# Copiar dados se existirem
if [ -d "data" ]; then
    log_info "Copiando dados do jogo..."
    cp -r data/ dist/war-game-v${VERSION}/
fi

# Criar script de instalação
log_info "Criando script de instalação..."
cat > dist/war-game-v${VERSION}/install.sh << 'EOF'
#!/bin/bash
echo "Instalando War Board Game..."

# Verificar Python
if ! command -v python3 &> /dev/null; then
    echo "Python 3 não encontrado. Instale Python 3.9+ primeiro."
    exit 1
fi

# Verificar pip
if ! command -v pip &> /dev/null && ! command -v pip3 &> /dev/null; then
    echo "pip não encontrado. Instale pip primeiro."
    exit 1
fi

# Usar pip3 se disponível, senão pip
PIP_CMD="pip"
if command -v pip3 &> /dev/null; then
    PIP_CMD="pip3"
fi

echo "Instalando dependências..."
$PIP_CMD install pygame>=2.6.0

echo "Instalação concluída!"
echo ""
echo "Para executar o jogo:"
echo "  python main.py"
echo "  ou"
echo "  python run_game.py"
EOF

chmod +x dist/war-game-v${VERSION}/install.sh

# Criar launcher executável
log_info "Criando launcher executável..."
cat > dist/war-game-v${VERSION}/run_game.py << 'EOF'
#!/usr/bin/env python3
"""
War Board Game - Launcher
Versão de distribuição com verificações de dependências
"""
import sys
import os

def check_dependencies():
    """Verifica se as dependências estão instaladas"""
    try:
        import pygame
        print(f"pygame {pygame.version.ver} encontrado")
        return True
    except ImportError:
        print("pygame não encontrado!")
        print("Execute: pip install pygame>=2.6.0")
        return False

def main():
    """Função principal do launcher"""
    print("War Board Game - Launcher")
    print("=" * 40)
    
    # Verificar dependências
    if not check_dependencies():
        sys.exit(1)
    
    # Adicionar diretório do jogo ao path
    game_dir = os.path.dirname(os.path.abspath(__file__))
    sys.path.insert(0, game_dir)
    
    try:
        print("Iniciando War Board Game...")
        from main import main as game_main
        game_main()
    except ImportError as e:
        print(f"Erro ao importar módulos do jogo: {e}")
        print("Verifique se todos os arquivos estão presentes.")
        sys.exit(1)
    except Exception as e:
        print(f"Erro ao executar o jogo: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
EOF

chmod +x dist/war-game-v${VERSION}/run_game.py

# Criar README do pacote
log_info "Criando README do pacote..."
cat > dist/war-game-v${VERSION}/README_PACKAGE.md << EOF
# War Board Game - Pacote Distribuível v${VERSION}

## Sobre o Jogo
War Board Game é uma implementação em Python do clássico jogo de tabuleiro War (Risk), desenvolvido para fins educacionais focando em:
- Versionamento de código com Git
- Gerenciamento de dependências
- Testes unitários
- CI/CD com GitHub Actions

## 📋 Requisitos do Sistema
- Python 3.9 ou superior
- pygame 2.6.0 ou superior
- Sistema operacional: Windows, macOS, ou Linux

## 🚀 Instalação Rápida

### Opção 1: Script de Instalação (Linux/macOS)
\`\`\`bash
chmod +x install.sh
./install.sh
\`\`\`

### Opção 2: Instalação Manual
\`\`\`bash
pip install pygame>=2.6.0
\`\`\`

## 🎯 Como Executar

### Método 1: Launcher (Recomendado)
\`\`\`bash
python run_game.py
\`\`\`

### Método 2: Diretamente
\`\`\`bash
python main.py
\`\`\`

## 📁 Estrutura do Pacote
- \`main.py\` - Arquivo principal do jogo
- \`run_game.py\` - Launcher com verificações de dependências
- \`war/\` - Módulos principais do jogo
  - \`card.py\` - Sistema de cartas
  - \`player.py\` - Lógica de jogadores
  - \`game.py\` - Engine principal do jogo
  - \`territory.py\` - Sistema de territórios
  - \`continent.py\` - Sistema de continentes
  - \`utils.py\` - Utilitários
- \`data/\` - Dados do jogo (mapas, missões)
- \`tests/\` - Testes unitários (56 testes)

## 🔧 Desenvolvimento
Para contribuir com o projeto:
1. Clone o repositório: https://github.com/DuarteFrugoli/war-board-game
2. Instale dependências de desenvolvimento: \`pip install -e ".[dev,test]"\`
3. Execute os testes: \`pytest tests/\`

## 📊 Informações do Build
- Versão: ${VERSION}
- Build: ${BUILD_NUMBER}
- Data: $(date)
- Plataforma: $(uname -s 2>/dev/null || echo "Unknown")

## 👥 Autores
- Pedro Henrique Duarte Frugoli
- Thiago Damas
- Fabio Miguel

## 📄 Licença
MIT License - Veja LICENSE para mais detalhes.
EOF

# Criar arquivo ZIP/TAR.GZ
log_info "Criando arquivo compactado..."
cd dist
tar -czf war-game-v${VERSION}-build${BUILD_NUMBER}.tar.gz war-game-v${VERSION}/
zip -r war-game-v${VERSION}-build${BUILD_NUMBER}.zip war-game-v${VERSION}/ >/dev/null 2>&1 || echo "zip não disponível"
cd ..

# Relatório final
echo ""
echo "================= PACOTE CRIADO =================="
log_success "Pacote criado com sucesso!"
echo "Localização: dist/"
echo "Arquivos gerados:"
ls -la dist/ | grep -E "\.(tar\.gz|zip)$" || echo "  - war-game-v${VERSION}/ (diretório)"
echo ""
echo "Para testar o pacote:"
echo "  cd dist/war-game-v${VERSION}/"
echo "  ./install.sh"
echo "  python run_game.py"
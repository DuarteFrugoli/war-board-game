#!/bin/bash

# Script para configurar Jenkins localmente usando Docker
# Este script facilita o setup de um ambiente Jenkins para testes

set -e

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Variáveis
JENKINS_HOME="${HOME}/.jenkins_war_game"
JENKINS_PORT="${JENKINS_PORT:-8080}"
JENKINS_AGENT_PORT="${JENKINS_AGENT_PORT:-50000}"
JENKINS_IMAGE="jenkins/jenkins:lts"

echo -e "${GREEN}=== Configuração do Jenkins para War Board Game ===${NC}\n"

# Verificar se Docker está instalado
if ! command -v docker &> /dev/null; then
    echo -e "${RED}Erro: Docker não está instalado!${NC}"
    echo "Instale o Docker primeiro: https://docs.docker.com/get-docker/"
    exit 1
fi

# Verificar se Docker está rodando
if ! docker info &> /dev/null; then
    echo -e "${RED}Erro: Docker não está rodando!${NC}"
    echo "Inicie o Docker e tente novamente."
    exit 1
fi

echo -e "${YELLOW}[1/5]${NC} Criando diretório para dados do Jenkins..."
mkdir -p "${JENKINS_HOME}"
echo -e "${GREEN}✓${NC} Diretório criado: ${JENKINS_HOME}\n"

echo -e "${YELLOW}[2/5]${NC} Verificando se já existe um container Jenkins rodando..."
if docker ps -a | grep -q jenkins-war-game; then
    echo -e "${YELLOW}Container Jenkins já existe. Removendo...${NC}"
    docker stop jenkins-war-game 2>/dev/null || true
    docker rm jenkins-war-game 2>/dev/null || true
fi
echo -e "${GREEN}✓${NC} Pronto para criar novo container\n"

echo -e "${YELLOW}[3/5]${NC} Baixando imagem do Jenkins..."
docker pull ${JENKINS_IMAGE}
echo -e "${GREEN}✓${NC} Imagem baixada\n"

echo -e "${YELLOW}[4/5]${NC} Criando e iniciando container Jenkins..."
docker run -d \
    --name jenkins-war-game \
    --restart unless-stopped \
    -p ${JENKINS_PORT}:8080 \
    -p ${JENKINS_AGENT_PORT}:50000 \
    -v "${JENKINS_HOME}":/var/jenkins_home \
    -v /var/run/docker.sock:/var/run/docker.sock \
    -e JAVA_OPTS="-Djenkins.install.runSetupWizard=false" \
    ${JENKINS_IMAGE}

echo -e "${GREEN}✓${NC} Container iniciado\n"

echo -e "${YELLOW}[5/5]${NC} Aguardando Jenkins inicializar..."
echo -e "${YELLOW}Isso pode levar alguns minutos...${NC}\n"

# Aguardar Jenkins ficar disponível
MAX_ATTEMPTS=30
ATTEMPT=0
while [ $ATTEMPT -lt $MAX_ATTEMPTS ]; do
    if docker logs jenkins-war-game 2>&1 | grep -q "Jenkins is fully up and running"; then
        echo -e "${GREEN}✓${NC} Jenkins está rodando!\n"
        break
    fi
    ATTEMPT=$((ATTEMPT + 1))
    echo -e "${YELLOW}Tentativa ${ATTEMPT}/${MAX_ATTEMPTS}...${NC}"
    sleep 10
done

if [ $ATTEMPT -eq $MAX_ATTEMPTS ]; then
    echo -e "${RED}Erro: Timeout aguardando Jenkins inicializar${NC}"
    echo "Verifique os logs: docker logs jenkins-war-game"
    exit 1
fi

# Obter senha inicial do admin
echo -e "${GREEN}=== Jenkins Configurado com Sucesso! ===${NC}\n"
echo -e "${YELLOW}Informações de Acesso:${NC}"
echo -e "  URL: ${GREEN}http://localhost:${JENKINS_PORT}${NC}"
echo -e "  Usuário: ${GREEN}admin${NC}"

# Tentar obter senha inicial
if docker exec jenkins-war-game test -f /var/jenkins_home/secrets/initialAdminPassword 2>/dev/null; then
    INITIAL_PASSWORD=$(docker exec jenkins-war-game cat /var/jenkins_home/secrets/initialAdminPassword)
    echo -e "  Senha Inicial: ${GREEN}${INITIAL_PASSWORD}${NC}"
else
    echo -e "  ${YELLOW}A senha inicial será exibida nos logs do container${NC}"
    echo -e "  Execute: ${GREEN}docker logs jenkins-war-game${NC}"
fi

echo -e "\n${YELLOW}Próximos Passos:${NC}"
echo "1. Acesse http://localhost:${JENKINS_PORT}"
echo "2. Faça login com as credenciais acima"
echo "3. Instale os plugins sugeridos"
echo "4. Crie um novo job do tipo 'Pipeline'"
echo "5. Configure o job para usar o repositório do projeto"
echo "6. No job, em 'Pipeline', selecione 'Pipeline script from SCM'"
echo "7. Configure o SCM como 'Git' e aponte para o repositório"
echo "8. Em 'Script Path', digite: Jenkinsfile"
echo "9. Salve e execute o build!"

echo -e "\n${YELLOW}Comandos Úteis:${NC}"
echo -e "  Ver logs: ${GREEN}docker logs -f jenkins-war-game${NC}"
echo -e "  Parar Jenkins: ${GREEN}docker stop jenkins-war-game${NC}"
echo -e "  Iniciar Jenkins: ${GREEN}docker start jenkins-war-game${NC}"
echo -e "  Remover Jenkins: ${GREEN}docker rm -f jenkins-war-game${NC}"
echo -e "  Acessar container: ${GREEN}docker exec -it jenkins-war-game bash${NC}"

echo -e "\n${YELLOW}Instalação de Plugins Recomendados:${NC}"
echo "Após o primeiro acesso, instale os seguintes plugins:"
echo "  - Pipeline"
echo "  - Git"
echo "  - GitHub"
echo "  - JUnit"
echo "  - Code Coverage API"
echo "  - Warnings Next Generation"
echo "  - Email Extension (opcional)"

echo -e "\n${GREEN}Para mais informações, consulte: docs/JENKINS_SETUP.md${NC}\n"

# Oferecer para abrir o navegador (Linux com xdg-open)
if command -v xdg-open &> /dev/null; then
    read -p "Deseja abrir o Jenkins no navegador? (y/N) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        xdg-open "http://localhost:${JENKINS_PORT}" &
    fi
fi

exit 0

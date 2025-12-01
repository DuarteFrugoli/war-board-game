# Arquivos de Configuração do Jenkins

## Visão Geral

O Jenkins no projeto é executado usando **Docker**, e existem dois arquivos principais que configuram isso:

- **`Dockerfile.jenkins`** - Define a imagem customizada do Jenkins
- **`docker-compose.jenkins.yml`** - Orquestra os containers

---

## `Dockerfile.jenkins` - Imagem Customizada

### O que é?

Um "Dockerfile" é uma **receita** para criar uma imagem Docker. É como uma lista de instruções para montar um container.

### Por que precisamos?

A imagem oficial do Jenkins (`jenkins/jenkins:lts`) **não tem Python instalado**. Como nosso projeto precisa de Python para rodar os testes, criamos uma **imagem customizada** que inclui Python.

### O que faz? (linha por linha)

```dockerfile
FROM jenkins/jenkins:lts
```
- Começa com a imagem oficial do Jenkins (versão LTS - Long Term Support)

```dockerfile
USER root
```
- Muda para usuário root (administrador) para poder instalar pacotes

```dockerfile
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python3-venv \
    && rm -rf /var/lib/apt/lists/*
```
- **Atualiza** lista de pacotes (`apt-get update`)
- **Instala** Python 3, pip e venv
- **Limpa** cache do apt (economiza espaço)

```dockerfile
RUN ln -s /usr/bin/python3 /usr/bin/python
```
- Cria um **atalho** para `python` apontar para `python3`
- Agora `python` e `python3` funcionam

```dockerfile
USER jenkins
```
- Volta para usuário jenkins (boa prática de segurança)

### Resultado

Uma imagem Docker com:
- ✅ Jenkins
- ✅ Java (vem no Jenkins)
- ✅ Python 3.13
- ✅ pip
- ✅ venv

---

## `docker-compose.jenkins.yml` - Orquestração

### O que é?

Docker Compose é uma ferramenta para **gerenciar múltiplos containers**. Define como os containers devem ser criados, conectados e configurados.

### Por que usar?

Sem Docker Compose, você precisaria rodar comandos enormes:
```bash
docker build -f Dockerfile.jenkins -t jenkins-custom .
docker network create jenkins-network
docker volume create jenkins_home
docker run -d -p 8080:8080 -p 50000:50000 -v jenkins_home:/var/jenkins_home --name jenkins-war-game jenkins-custom
# ... e mais comandos
```

Com Docker Compose:
```bash
docker-compose -f docker-compose.jenkins.yml up -d
```

**Muito mais fácil!**

### Estrutura do arquivo

#### 1. Serviço `jenkins` (Principal)

```yaml
jenkins:
  build:
    context: .
    dockerfile: Dockerfile.jenkins
```
- **Build**: Constrói a imagem usando `Dockerfile.jenkins`
- **Context**: Usa o diretório atual (`.`)

```yaml
  container_name: jenkins-war-game
  restart: unless-stopped
```
- **Nome**: Container se chama `jenkins-war-game`
- **Restart**: Reinicia automaticamente se cair (exceto se você parar manualmente)

```yaml
  ports:
    - "8080:8080"    # Interface web
    - "50000:50000"  # Porta para agentes
```
- **8080**: Porta da interface web (acessa em http://localhost:8080)
- **50000**: Porta para agentes Jenkins se conectarem

```yaml
  volumes:
    - jenkins_home:/var/jenkins_home
    - /var/run/docker.sock:/var/run/docker.sock
    - pip_cache:/root/.cache/pip
```
- **jenkins_home**: Persiste dados do Jenkins (configurações, jobs, builds)
  - Mesmo se você deletar o container, os dados ficam salvos
- **docker.sock**: Permite Jenkins rodar comandos Docker (Docker-in-Docker)
- **pip_cache**: Cache do pip para acelerar instalações

```yaml
  environment:
    - JAVA_OPTS=-Djenkins.install.runSetupWizard=true
    - TZ=America/Sao_Paulo
```
- **JAVA_OPTS**: Opções do Java (mostra wizard de configuração inicial)
- **TZ**: Timezone (fuso horário de São Paulo)

```yaml
  networks:
    - jenkins-network
```
- Conecta à rede `jenkins-network` (permite comunicação entre containers)

```yaml
  healthcheck:
    test: ["CMD-SHELL", "curl -f http://localhost:8080/login || exit 1"]
    interval: 30s
    timeout: 10s
    retries: 5
    start_period: 60s
```
- **Healthcheck**: Verifica se Jenkins está funcionando
- Testa acessar `/login` a cada 30 segundos
- Espera 60 segundos para primeira verificação (Jenkins demora para iniciar)

---

#### 2. Serviço `jenkins-agent` (Opcional)

```yaml
jenkins-agent:
  image: jenkins/inbound-agent:latest
  container_name: jenkins-agent-python
```
- Container separado para executar builds
- Útil para distribuir carga de trabalho
- **Atualmente não está configurado** (linhas comentadas)

---

#### 3. Volumes

```yaml
volumes:
  jenkins_home:
  agent_workspace:
  pip_cache:
```
- **Volumes nomeados**: Docker gerencia onde ficam armazenados
- **Persistentes**: Dados não são perdidos quando container é removido

---

#### 4. Networks

```yaml
networks:
  jenkins-network:
    driver: bridge
```
- Rede interna para containers se comunicarem
- Jenkins e agent podem se falar via `http://jenkins:8080`

---

## Fluxo Completo

### 1. Build da imagem
```bash
docker-compose -f docker-compose.jenkins.yml build
```
- Lê `Dockerfile.jenkins`
- Cria imagem com Jenkins + Python

### 2. Subir os containers
```bash
docker-compose -f docker-compose.jenkins.yml up -d
```
- Cria rede `jenkins-network`
- Cria volumes (`jenkins_home`, etc.)
- Inicia container `jenkins-war-game`
- Inicia container `jenkins-agent-python`

### 3. Acessar
- http://localhost:8080

### 4. Parar
```bash
docker-compose -f docker-compose.jenkins.yml down
```
- Para e remove containers
- **Mantém** volumes (dados persistem)

### 5. Remover tudo (inclusive dados)
```bash
docker-compose -f docker-compose.jenkins.yml down -v
```
- Remove containers **e** volumes
- ⚠️ **Perde todas as configurações do Jenkins!**

---

## Comparação Visual

### Sem Docker:
```
Instalar Java ➜ Baixar Jenkins ➜ Configurar ➜ Instalar Python ➜ Configurar paths
❌ Complexo
❌ Pode dar conflito com sistema
❌ Difícil de replicar
```

### Com Docker:
```
docker-compose up
✅ Tudo pronto em 1 comando
✅ Isolado do sistema
✅ Qualquer um replica igual
```

---

## Benefícios dessa Estrutura

### 1. **Reprodutibilidade**
Qualquer pessoa (até em Windows com Docker Desktop) pode rodar:
```bash
docker-compose -f docker-compose.jenkins.yml up -d
```
E ter **exatamente** o mesmo ambiente.

### 2. **Isolamento**
Jenkins roda em container isolado:
- Não interfere com Python do sistema
- Não interfere com outros projetos
- Fácil de remover completamente

### 3. **Versionamento**
- `Dockerfile.jenkins` vai pro Git
- `docker-compose.jenkins.yml` vai pro Git
- Todos da equipe têm mesma configuração

### 4. **Portabilidade**
Funciona em:
- ✅ Linux
- ✅ macOS
- ✅ Windows (com Docker Desktop ou WSL2)

---

## Resumo

| Arquivo | Função | Analogia |
|---------|--------|----------|
| `Dockerfile.jenkins` | Receita da imagem customizada | Receita de bolo |
| `docker-compose.jenkins.yml` | Orquestração dos containers | Lista de ingredientes + instruções |
| Imagem Docker | Jenkins + Python empacotado | Bolo pronto |
| Container | Instância rodando | Bolo sendo servido |
| Volume | Armazenamento persistente | Geladeira (guarda sobras) |

**TL;DR**: 
- `Dockerfile.jenkins` = Como fazer uma imagem Jenkins com Python
- `docker-compose.jenkins.yml` = Como rodar e configurar tudo de uma vez

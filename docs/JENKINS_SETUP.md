# Configuração do Jenkins

## Instalação Local com Docker

### 1. Subir o Jenkins

```bash
# Na raiz do projeto
docker-compose -f docker-compose.jenkins.yml up -d
```

### 2. Acessar a Interface Web

Abra o navegador em: `http://localhost:8080`

### 3. Desbloquear o Jenkins (Primeira Vez)

```bash
# Obter a senha inicial
docker logs jenkins
```

Procure por uma linha como:
```
*************************************************************
*************************************************************
*************************************************************

Jenkins initial setup is required. An admin user has been created and a password generated.
Please use the following password to proceed to installation:

<SENHA_AQUI>

*************************************************************
*************************************************************
*************************************************************
```

Cole essa senha na interface web.

### 4. Instalar Plugins

Escolha "Install suggested plugins" e aguarde a instalação.

### 5. Criar Usuário Admin

Preencha os dados do primeiro usuário administrador.

### 6. Configurar URL

Mantenha `http://localhost:8080` e clique em "Save and Finish".

## Configurar o Projeto

### 1. Criar um Novo Pipeline

1. Na página inicial, clique em "New Item"
2. Digite o nome: `war-board-game`
3. Selecione "Pipeline"
4. Clique em "OK"

### 2. Configurar o Pipeline

Na página de configuração:

1. **General**
   - Marque "GitHub project" (opcional)
   - Project url: `https://github.com/DuarteFrugoli/war-board-game/`

2. **Build Triggers** (opcional)
   - Marque "Poll SCM" se quiser verificação automática
   - Schedule: `H/5 * * * *` (verifica a cada 5 minutos)

3. **Pipeline**
   - Definition: `Pipeline script from SCM`
   - SCM: `Git`
   - Repository URL: `https://github.com/DuarteFrugoli/war-board-game.git`
   - Branch Specifier: `*/main`
   - Script Path: `Jenkinsfile`

4. Clique em "Save"

### 3. Executar o Pipeline

1. Clique em "Build Now"
2. Acompanhe o progresso clicando no número do build (ex: #1)
3. Clique em "Console Output" para ver os logs em tempo real

## Comandos Úteis

```bash
# Parar o Jenkins
docker-compose -f docker-compose.jenkins.yml down

# Reiniciar o Jenkins
docker-compose -f docker-compose.jenkins.yml restart

# Ver logs
docker logs -f jenkins

# Remover tudo (incluindo dados)
docker-compose -f docker-compose.jenkins.yml down -v
```

## Troubleshooting

### Porta 8080 já está em uso

Edite o arquivo `docker-compose.jenkins.yml` e mude a porta:
```yaml
ports:
  - "8081:8080"  # Mude 8081 para outra porta disponível
```

### Jenkins não inicia

Verifique os logs:
```bash
docker logs jenkins
```

### Problemas de permissão

```bash
# Dar permissões corretas ao volume
sudo chown -R 1000:1000 jenkins_home/
```

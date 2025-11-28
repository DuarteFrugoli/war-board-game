# Como Usar o Jenkins

## Acesso Rápido

- **URL**: http://localhost:8080
- **Credenciais**: Use o usuário/senha criados na configuração inicial

## Interface Principal

### Dashboard

A página inicial mostra:
- Lista de todos os jobs/pipelines
- Status dos últimos builds (✓ sucesso, ✗ falha)
- Gráfico de tendência de builds

### Cores dos Ícones

- 🔵 **Azul**: Build com sucesso
- 🔴 **Vermelho**: Build falhou
- ⚪ **Cinza**: Nunca executado
- 🟡 **Amarelo**: Build instável (testes falharam mas compilou)

## Executar um Build

### Manualmente

1. No dashboard, clique no nome do projeto: `war-board-game`
2. Clique em "Build Now" no menu lateral esquerdo
3. O build aparecerá em "Build History"
4. Clique no número do build (ex: #1, #2, etc)
5. Clique em "Console Output" para ver os logs

### Automaticamente

Se configurou "Poll SCM", o Jenkins verifica o repositório periodicamente e executa quando detecta mudanças.

## Visualizar Resultados

### Console Output

Mostra todos os logs da execução:
- Checkout do código
- Instalação de dependências
- Execução dos testes
- Erros (se houver)

### Status do Build

No detalhe do build você vê:
- **Stages**: Cada etapa do pipeline (Setup, Lint, Test, Build)
- **Duração**: Quanto tempo levou
- **Changes**: Commits que foram incluídos nesse build

### Test Results

Se os testes gerarem relatórios JUnit/XML:
- Quantidade de testes executados
- Testes que passaram/falharam
- Detalhes de cada teste

## Estrutura do Pipeline

O `Jenkinsfile` define 4 estágios:

1. **Setup**: Configura Python e instala dependências
2. **Lint**: Verifica qualidade do código (black, flake8, mypy)
3. **Test**: Executa os testes unitários
4. **Build**: Verifica se o projeto pode ser empacotado

## Notificações

O pipeline atual envia notificações:
- ✅ Quando o build passa
- ❌ Quando o build falha
- 🔧 Quando o build volta a funcionar após falha

## Comparação com GitHub Actions

| Recurso | GitHub Actions | Jenkins |
|---------|---------------|---------|
| **Localização** | Nuvem do GitHub | Seu servidor/máquina |
| **Acesso** | github.com/repo/actions | http://localhost:8080 |
| **Configuração** | `.github/workflows/*.yml` | `Jenkinsfile` |
| **Execução Manual** | Tab "Actions" > "Run workflow" | "Build Now" |
| **Logs** | Tab "Actions" > Build > Job | Build # > "Console Output" |
| **Custo** | Grátis (repos públicos) | Grátis (autohospedado) |

## Dicas

### Ver apenas builds recentes
No dashboard, a lista já mostra os builds mais recentes.

### Cancelar um build em execução
1. Clique no build em execução
2. Clique no "X" vermelho no canto superior direito

### Limpar builds antigos
Configuração automática no `Jenkinsfile`:
```groovy
options {
    buildDiscarder(logRotator(numToKeepStr: '10'))
}
```

### Executar apenas um estágio específico
Não é possível via interface. Você precisa modificar o `Jenkinsfile` ou executar comandos manualmente.

### Debugging

Para debug mais detalhado, adicione no `Jenkinsfile`:
```groovy
sh 'echo "Debug: verificando variável X"'
sh 'pwd'  // Diretório atual
sh 'ls -la'  // Listar arquivos
```

## Gerenciamento

### Parar/Reiniciar Jenkins

```bash
# Parar
docker-compose -f docker-compose.jenkins.yml down

# Iniciar
docker-compose -f docker-compose.jenkins.yml up -d

# Reiniciar
docker-compose -f docker-compose.jenkins.yml restart
```

### Backup

Os dados ficam no volume Docker `jenkins_home`:
```bash
# Backup
docker run --rm -v jenkins_home:/data -v $(pwd):/backup ubuntu tar czf /backup/jenkins_backup.tar.gz /data

# Restore
docker run --rm -v jenkins_home:/data -v $(pwd):/backup ubuntu tar xzf /backup/jenkins_backup.tar.gz -C /
```

### Atualizar Jenkins

```bash
# Pull nova imagem
docker pull jenkins/jenkins:lts

# Recriar container
docker-compose -f docker-compose.jenkins.yml up -d --force-recreate
```

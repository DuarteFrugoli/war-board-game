# Pipeline Jenkins - Explicação Detalhada

Este documento explica linha por linha o funcionamento da pipeline Jenkins do projeto WAR Board Game.

---

## O que é uma Pipeline?

Uma **pipeline** é um conjunto de etapas (stages) automatizadas que executam em sequência para:
- ✅ Verificar qualidade do código
- ✅ Executar testes
- ✅ Gerar builds
- ✅ Garantir que nada quebrou

**Analogia:** É como uma linha de montagem de carros - cada estação faz uma verificação antes de passar para a próxima.

---

## Estrutura Geral

```groovy
pipeline {
    agent any          // Onde executar
    options { ... }    // Configurações gerais
    stages { ... }     // Etapas do processo
    post { ... }       // Ações após execução
}
```

---

## 1. Declaração da Pipeline

```groovy
pipeline {
    agent any
```

### `agent any`
**O que faz:** Define onde a pipeline será executada.
- `any` = Qualquer agente Jenkins disponível
- No nosso caso: container Docker com Python 3.13

**Por que importa:** Garante que há um ambiente disponível para rodar os jobs.

---

## 2. Options - Configurações Globais

```groovy
options {
    buildDiscarder(logRotator(numToKeepStr: '10'))
    timeout(time: 30, unit: 'MINUTES')
    timestamps()
}
```

### `buildDiscarder(logRotator(numToKeepStr: '10'))`
**O que faz:** Mantém apenas as últimas 10 execuções da pipeline.
**Por que:** Economiza espaço em disco - logs antigos são deletados automaticamente.

### `timeout(time: 30, unit: 'MINUTES')`
**O que faz:** Cancela a pipeline se demorar mais de 30 minutos.
**Por que:** Evita builds travados consumindo recursos indefinidamente.

### `timestamps()`
**O que faz:** Adiciona timestamp em cada linha do log.
**Por que:** Facilita debug - você sabe exatamente quando cada comando executou.

---

## 3. Stages - Etapas da Pipeline

As **stages** são executadas em **ordem sequencial**. Se uma falhar, as seguintes não executam (por padrão).

---

### Stage 1: Checkout

```groovy
stage('Checkout') {
    steps {
        echo 'Fazendo checkout do código...'
        checkout scm
    }
}
```

**O que faz:**
- `echo` - Imprime mensagem no console
- `checkout scm` - Baixa código do repositório Git (GitHub)

**SCM** = Source Control Management (sistema de controle de versão)

**Resultado:** Código-fonte disponível no workspace do Jenkins.

---

### Stage 2: Setup

```groovy
stage('Setup') {
    steps {
        echo 'Instalando dependências...'
        sh '''
            python3 --version
            
            # Criar ambiente virtual
            python3 -m venv .venv
            
            # Ativar ambiente virtual e instalar dependências
            . .venv/bin/activate
            pip install --upgrade pip
            pip install poetry
            poetry install --no-root
        '''
    }
}
```

**O que faz:**
1. **`python3 --version`** - Verifica versão do Python instalada
2. **`python3 -m venv .venv`** - Cria ambiente virtual isolado
3. **`. .venv/bin/activate`** - Ativa o ambiente virtual
4. **`pip install --upgrade pip`** - Atualiza o pip
5. **`pip install poetry`** - Instala Poetry no ambiente
6. **`poetry install --no-root`** - Instala todas as dependências do projeto

**`sh '''...'''`** = Executa comandos shell (bash) em bloco.

**Por que importante:** Sem setup, os comandos seguintes falhariam (sem Poetry, sem dependências).

---

### Stage 3: Lint

```groovy
stage('Lint') {
    steps {
        echo 'Verificando qualidade do código...'
        sh '''
            . .venv/bin/activate
            pip install black flake8 mypy
            echo "=== Black (formatação) ==="
            black --check war/ tests/ main.py run_gui.py || true
            
            echo "=== Flake8 (estilo) ==="
            flake8 war/ tests/ main.py run_gui.py --max-line-length=100 --extend-ignore=E203,W503 || true
            
            echo "=== MyPy (tipos) ==="
            mypy war/ --ignore-missing-imports || true
        '''
    }
}
```

**O que cada ferramenta faz:**

#### Black (formatação)
```groovy
black --check war/ tests/ main.py run_gui.py || true
```
- **`--check`** - Verifica formatação sem modificar arquivos
- **`|| true`** - Continua mesmo se encontrar problemas (não falha a pipeline)
- **Verifica:** Indentação, espaços, linhas em branco (PEP8)

#### Flake8 (estilo)
```groovy
flake8 war/ tests/ main.py run_gui.py --max-line-length=100 --extend-ignore=E203,W503 || true
```
- **`--max-line-length=100`** - Permite linhas até 100 caracteres
- **`--extend-ignore=E203,W503`** - Ignora regras específicas (conflito com Black)
- **Verifica:** Imports não usados, variáveis não utilizadas, complexidade

#### MyPy (tipos)
```groovy
mypy war/ --ignore-missing-imports || true
```
- **`--ignore-missing-imports`** - Não reclama de bibliotecas sem type hints
- **Verifica:** Anotações de tipo (type hints) estão corretas

**Por que `|| true`?**
Permite que o linting **avise** sobre problemas sem **quebrar** a pipeline. Em produção, você removeria isso para forçar qualidade.

---

### Stage 4: Test

```groovy
stage('Test') {
    steps {
        echo 'Executando testes...'
        sh '''
            . .venv/bin/activate
            python -m pytest tests/ -v --tb=short || python -m unittest discover -s tests -p "test_*.py" -v
        '''
    }
}
```

**O que faz:**

```groovy
python -m pytest tests/ -v --tb=short || python -m unittest discover -s tests -p "test_*.py" -v
```

**Primeira tentativa:** `pytest`
- **`-v`** - Verbose (mostra todos os testes)
- **`--tb=short`** - Traceback curto em erros

**Fallback (||):** Se pytest não estiver instalado, usa `unittest`
- **`discover -s tests`** - Descobre testes na pasta `tests/`
- **`-p "test_*.py"`** - Padrão de arquivos (test_*.py)
- **`-v`** - Verbose

**Se falhar:** Pipeline para aqui ❌ (testes são críticos!)

---

### Stage 5: Build

```groovy
stage('Build') {
    steps {
        echo 'Verificando se o projeto pode ser empacotado...'
        sh '''
            . .venv/bin/activate
            poetry build --format wheel || echo "Build check completed"
        '''
    }
}
```

**O que faz:**

```groovy
poetry build --format wheel || echo "Build check completed"
```

- **`poetry build`** - Empacota o projeto
- **`--format wheel`** - Gera apenas arquivo .whl (mais rápido que tar.gz)
- **`|| echo "Build check completed"`** - Se falhar, mostra mensagem mas não quebra

**Resultado:** Arquivo `.whl` na pasta `dist/` (se bem-sucedido)

**Por que importante:** Valida que o projeto **pode ser distribuído**.

---

## 4. Post - Ações Pós-Execução

Executam **independente** do sucesso/falha das stages.

```groovy
post {
    always { ... }    // Sempre executa
    success { ... }   // Só se sucesso
    failure { ... }   // Só se falha
}
```

---

### Always - Sempre Executa

```groovy
always {
    echo 'Pipeline finalizado!'
    
    // Arquivar artefatos do build (se existirem)
    script {
        if (fileExists('dist/')) {
            archiveArtifacts artifacts: 'dist/*.whl,dist/*.tar.gz', 
                           allowEmptyArchive: true,
                           fingerprint: true
        }
    }
    
    cleanWs()
}
```

#### Arquivamento de Artefatos
```groovy
archiveArtifacts artifacts: 'dist/*.whl,dist/*.tar.gz'
```
**O que faz:** Salva arquivos `.whl` e `.tar.gz` no Jenkins.
- **`allowEmptyArchive: true`** - Não falha se pasta dist/ estiver vazia
- **`fingerprint: true`** - Gera hash MD5 para rastrear mudanças

**Benefício:** Você pode baixar o `.whl` diretamente do Jenkins!

#### Limpeza do Workspace
```groovy
cleanWs()
```
**O que faz:** Deleta todos os arquivos do workspace.
**Por que:** Libera espaço em disco, garante builds limpos.

---

### Success - Só em Sucesso

```groovy
success {
    echo 'Build completado com sucesso! ✓'
}
```
**Quando executa:** Todas as stages passaram ✅
**Uso futuro:** Poderia enviar notificação, fazer deploy, etc.

---

### Failure - Só em Falha

```groovy
failure {
    echo 'Build falhou! ✗'
}
```
**Quando executa:** Alguma stage falhou ❌
**Uso futuro:** Enviar email, criar issue no GitHub, etc.

---

## Fluxo Visual da Pipeline

```
┌─────────────────────────────────────────────────────────────┐
│                    INÍCIO DA PIPELINE                        │
└─────────────────┬───────────────────────────────────────────┘
                  │
                  ▼
         ┌────────────────┐
         │   CHECKOUT     │  Baixa código do GitHub
         └────────┬───────┘
                  │
                  ▼
         ┌────────────────┐
         │     SETUP      │  Cria venv, instala Poetry + dependências
         └────────┬───────┘
                  │
                  ▼
         ┌────────────────┐
         │      LINT      │  Black, Flake8, MyPy (qualidade)
         └────────┬───────┘
                  │
                  ▼
         ┌────────────────┐
         │      TEST      │  Executa 94 testes unitários
         └────────┬───────┘  ❌ Se falhar, para aqui!
                  │
                  ▼
         ┌────────────────┐
         │     BUILD      │  Gera .whl (pacote distribuível)
         └────────┬───────┘
                  │
                  ▼
         ┌────────────────┐
         │      POST      │  Arquiva .whl, limpa workspace
         └────────┬───────┘
                  │
                  ▼
    ┌─────────────┴──────────────┐
    │                            │
    ▼                            ▼
┌─────────┐                 ┌─────────┐
│ SUCCESS │                 │ FAILURE │
│    ✓    │                 │    ✗    │
└─────────┘                 └─────────┘
```

---

## Comparação: Jenkins vs GitHub Actions

| Aspecto | Jenkins | GitHub Actions |
|---------|---------|----------------|
| **Hospedagem** | Self-hosted (seu servidor/Docker) | Cloud (servidores GitHub) |
| **Configuração** | `Jenkinsfile` (Groovy) | `.github/workflows/*.yml` (YAML) |
| **Custo** | Grátis (você paga infraestrutura) | Grátis (público), limitado (privado) |
| **Controle** | Total (você gerencia tudo) | Limitado (ambiente pré-configurado) |
| **Manutenção** | Você atualiza Jenkins | GitHub gerencia |
| **Integração** | Plugins (manual) | Nativa com GitHub |

**Quando usar Jenkins:**
- ✅ Precisa de controle total
- ✅ Infraestrutura própria (on-premise)
- ✅ Integração com ferramentas internas
- ✅ Sem limites de minutos

**Quando usar GitHub Actions:**
- ✅ Projeto pequeno/médio
- ✅ Hospedado no GitHub
- ✅ Sem infraestrutura própria
- ✅ Setup rápido

---

## Equivalência das Stages

Nossa pipeline Jenkins tem **5 stages**. No GitHub Actions:

| Jenkins Stage | GitHub Actions Job |
|---------------|-------------------|
| Checkout | `actions/checkout@v3` |
| Setup | `actions/setup-python@v4` + `poetry install` |
| Lint | Job separado com black/flake8/mypy |
| Test | Job separado com unittest |
| Build | Job separado com `poetry build` |

**Diferença:** GitHub Actions executa jobs em **paralelo**, Jenkins em **sequência**.

---

## Triggers - Quando a Pipeline Executa

No Jenkins (não configurado no Jenkinsfile, mas no Jenkins UI):
- **Push no GitHub** - Webhook dispara build
- **Pull Request** - Testa antes de mergear
- **Schedule** - Execução agendada (cron)
- **Manual** - Botão "Build Now"

No GitHub Actions (configurado no `.yml`):
```yaml
on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]
```

---

## Variáveis de Ambiente Disponíveis

Dentro da pipeline Jenkins, você tem acesso a:

```groovy
env.BUILD_NUMBER      // Número da build (1, 2, 3...)
env.BUILD_ID          // ID único da build
env.JOB_NAME          // Nome do job
env.WORKSPACE         // Caminho do workspace
env.GIT_COMMIT        // Hash do commit atual
env.GIT_BRANCH        // Branch atual
```

**Exemplo de uso:**
```groovy
echo "Building commit ${env.GIT_COMMIT} on ${env.GIT_BRANCH}"
```

---

## Logs e Debug

### Ver logs no Jenkins:
1. Acesse `http://localhost:8080`
2. Clique no job
3. Clique em "Console Output"

### Logs detalhados (adicionar no Jenkinsfile):
```groovy
// No início das stages
echo "=== DEBUG: Variáveis de ambiente ==="
sh 'env | sort'

echo "=== DEBUG: Arquivos no workspace ==="
sh 'ls -la'
```

---

## Otimizações Possíveis

### 1. Cache de Dependências
```groovy
// Adicionar antes do Setup
stage('Cache') {
    steps {
        // Usa cache do Poetry para não reinstalar sempre
        sh 'poetry config cache-dir .poetry-cache'
    }
}
```

### 2. Paralelização de Stages
```groovy
stage('Qualidade') {
    parallel {
        stage('Lint') { ... }
        stage('Test') { ... }
    }
}
```

### 3. Notificações por Email
```groovy
post {
    failure {
        emailext(
            subject: "Build Falhou: ${env.JOB_NAME} #${env.BUILD_NUMBER}",
            body: "Verifique: ${env.BUILD_URL}",
            to: "dev@example.com"
        )
    }
}
```

---

## Troubleshooting - Problemas Comuns

### ❌ "poetry: command not found"
**Causa:** Poetry não instalado no ambiente.
**Solução:** Adicionar `pip install poetry` no stage Setup.

### ❌ "Permission denied"
**Causa:** Script sem permissão de execução.
**Solução:** `sh 'chmod +x script.sh'` antes de executar.

### ❌ "No module named 'pygame'"
**Causa:** Dependências não instaladas.
**Solução:** Verificar se `poetry install` executou com sucesso.

### ❌ Pipeline trava indefinidamente
**Causa:** Comando aguardando input ou em loop.
**Solução:** Configurar `timeout` nas options.

---

## Boas Práticas

### ✅ Sempre use ambientes virtuais
```groovy
python3 -m venv .venv
. .venv/bin/activate
```
Evita conflitos com sistema.

### ✅ Adicione mensagens descritivas
```groovy
echo "=== Instalando Poetry ${POETRY_VERSION} ==="
```
Facilita debug nos logs.

### ✅ Use `|| true` com cuidado
```groovy
flake8 war/ || true  // ⚠️ Ignora erros
```
Só em ferramentas não-críticas (lint). **Nunca** em testes!

### ✅ Limpe o workspace
```groovy
cleanWs()  // Sempre no post.always
```
Evita resíduos de builds anteriores.

### ✅ Versione suas ferramentas
```groovy
pip install poetry==1.7.1  // Fixa versão
```
Evita quebras por atualizações.

---

## Resumo - O que Aprende com Esta Pipeline

1. **CI/CD prático** - Automatização real de qualidade
2. **Groovy/Jenkins** - Linguagem de pipeline
3. **Ambientes isolados** - venv para builds reprodutíveis
4. **Qualidade de código** - Linters e formatadores
5. **Testes automáticos** - Validação contínua
6. **Build/Empacotamento** - Distribuição de software
7. **DevOps** - Cultura de automação

---

## Próximos Passos

- [ ] Adicionar cobertura de testes (`coverage.py`)
- [ ] Integrar com SonarQube (análise de código)
- [ ] Deploy automático após build (CD)
- [ ] Notificações no Slack/Discord
- [ ] Matriz de testes (Python 3.9, 3.10, 3.11, 3.12)

---

**Última atualização:** 1 de dezembro de 2025

**Autor:** Time WAR Board Game

**Referências:**
- [Documentação Jenkins Pipeline](https://www.jenkins.io/doc/book/pipeline/)
- [Poetry Documentation](https://python-poetry.org/docs/)
- [GitHub Actions vs Jenkins](https://www.jenkins.io/blog/2020/05/25/github-actions-jenkins/)

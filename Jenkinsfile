pipeline {
    agent any
    
    environment {
        PYTHON_VERSION = '3.9'
        PYTHON_LATEST = '3.13'
        // Diretório do ambiente virtual
        VENV_DIR = '.venv'
    }
    
    parameters {
        choice(
            name: 'PYTHON_TEST_VERSION',
            choices: ['3.9', '3.10', '3.11', '3.12', '3.13', 'all'],
            description: 'Versão do Python para executar os testes'
        )
        booleanParam(
            name: 'RUN_QUALITY_CHECKS',
            defaultValue: true,
            description: 'Executar análises de qualidade de código'
        )
        booleanParam(
            name: 'SEND_NOTIFICATION',
            defaultValue: false,
            description: 'Enviar notificação por email ao final'
        )
    }
    
    options {
        // Manter apenas os últimos 10 builds
        buildDiscarder(logRotator(numToKeepStr: '10', artifactNumToKeepStr: '5'))
        // Timeout de 30 minutos para o pipeline completo
        timeout(time: 30, unit: 'MINUTES')
        // Adicionar timestamps aos logs
        timestamps()
        // Não permitir builds concorrentes do mesmo branch
        disableConcurrentBuilds()
    }
    
    triggers {
        // Poll SCM a cada 5 minutos (apenas se houver mudanças)
        pollSCM('H/5 * * * *')
    }
    
    stages {
        stage('Checkout') {
            steps {
                echo 'Fazendo checkout do código...'
                checkout scm
                script {
                    // Obter informações do commit
                    env.GIT_COMMIT_SHORT = sh(
                        script: "git rev-parse --short HEAD",
                        returnStdout: true
                    ).trim()
                    env.GIT_COMMIT_MSG = sh(
                        script: "git log -1 --pretty=%B",
                        returnStdout: true
                    ).trim()
                }
            }
        }
        
        stage('Setup Environment') {
            steps {
                echo 'Configurando ambiente Python...'
                sh '''
                    # Verificar se Python está disponível
                    python3 --version
                    
                    # Criar ambiente virtual se não existir
                    if [ ! -d "${VENV_DIR}" ]; then
                        python3 -m venv ${VENV_DIR}
                    fi
                    
                    # Ativar ambiente virtual e atualizar pip
                    . ${VENV_DIR}/bin/activate
                    pip install --upgrade pip
                    
                    # Instalar Poetry se necessário
                    if ! command -v poetry &> /dev/null; then
                        pip install poetry
                    fi
                    
                    # Configurar Poetry para usar venv local
                    poetry config virtualenvs.in-project true
                    
                    # Instalar dependências do projeto
                    poetry install --no-root
                    
                    # Instalar dependências de desenvolvimento
                    pip install black flake8 mypy bandit safety
                '''
            }
        }
        
        stage('Tests') {
            parallel {
                stage('Unit Tests - Python 3.9') {
                    when {
                        expression { params.PYTHON_TEST_VERSION == '3.9' || params.PYTHON_TEST_VERSION == 'all' }
                    }
                    steps {
                        runTests('3.9')
                    }
                }
                
                stage('Unit Tests - Python 3.10') {
                    when {
                        expression { params.PYTHON_TEST_VERSION == '3.10' || params.PYTHON_TEST_VERSION == 'all' }
                    }
                    steps {
                        runTests('3.10')
                    }
                }
                
                stage('Unit Tests - Python 3.11') {
                    when {
                        expression { params.PYTHON_TEST_VERSION == '3.11' || params.PYTHON_TEST_VERSION == 'all' }
                    }
                    steps {
                        runTests('3.11')
                    }
                }
                
                stage('Unit Tests - Python 3.12') {
                    when {
                        expression { params.PYTHON_TEST_VERSION == '3.12' || params.PYTHON_TEST_VERSION == 'all' }
                    }
                    steps {
                        runTests('3.12')
                    }
                }
                
                stage('Unit Tests - Python 3.13') {
                    when {
                        expression { params.PYTHON_TEST_VERSION == '3.13' || params.PYTHON_TEST_VERSION == 'all' }
                    }
                    steps {
                        runTests('3.13')
                    }
                }
            }
        }
        
        stage('Quality Checks') {
            when {
                expression { params.RUN_QUALITY_CHECKS == true }
            }
            parallel {
                stage('Code Formatting (Black)') {
                    steps {
                        catchError(buildResult: 'SUCCESS', stageResult: 'UNSTABLE') {
                            sh '''
                                . ${VENV_DIR}/bin/activate
                                black --check --diff war/ tests/ main.py run_gui.py
                            '''
                        }
                    }
                }
                
                stage('Style Check (Flake8)') {
                    steps {
                        catchError(buildResult: 'SUCCESS', stageResult: 'UNSTABLE') {
                            sh '''
                                . ${VENV_DIR}/bin/activate
                                flake8 war/ tests/ main.py run_gui.py \
                                    --max-line-length=88 \
                                    --extend-ignore=E203,W503 \
                                    --format=pylint \
                                    --output-file=reports/flake8-report.txt || true
                            '''
                        }
                    }
                }
                
                stage('Type Checking (MyPy)') {
                    steps {
                        catchError(buildResult: 'SUCCESS', stageResult: 'UNSTABLE') {
                            sh '''
                                . ${VENV_DIR}/bin/activate
                                mypy war/ \
                                    --ignore-missing-imports \
                                    --python-version=3.9 \
                                    --txt-report reports/mypy || true
                            '''
                        }
                    }
                }
                
                stage('Security Analysis (Bandit)') {
                    steps {
                        catchError(buildResult: 'SUCCESS', stageResult: 'UNSTABLE') {
                            sh '''
                                . ${VENV_DIR}/bin/activate
                                mkdir -p reports
                                bandit -r war/ \
                                    -f json \
                                    -o reports/security-report.json || true
                                bandit -r war/ \
                                    -f txt \
                                    -o reports/security-report.txt || true
                            '''
                        }
                    }
                }
                
                stage('Vulnerability Check (Safety)') {
                    steps {
                        catchError(buildResult: 'SUCCESS', stageResult: 'UNSTABLE') {
                            sh '''
                                . ${VENV_DIR}/bin/activate
                                mkdir -p reports
                                safety check \
                                    --json \
                                    --output reports/vulnerabilities-report.json || true
                            '''
                        }
                    }
                }
            }
        }
        
        stage('Build Package') {
            steps {
                echo 'Criando pacote do projeto...'
                sh '''
                    . ${VENV_DIR}/bin/activate
                    chmod +x scripts/create_package.sh
                    scripts/create_package.sh "v1.0.${BUILD_NUMBER}" "${BUILD_NUMBER}"
                '''
            }
        }
        
        stage('Archive Artifacts') {
            steps {
                echo 'Arquivando artefatos...'
                script {
                    // Arquivar pacote
                    archiveArtifacts artifacts: 'dist/war-game-*.tar.gz', 
                                   fingerprint: true,
                                   allowEmptyArchive: false
                    
                    // Arquivar relatórios
                    archiveArtifacts artifacts: 'reports/**/*', 
                                   fingerprint: true,
                                   allowEmptyArchive: true
                }
            }
        }
    }
    
    post {
        always {
            echo 'Pipeline finalizado!'
            
            // Publicar relatórios de testes
            junit allowEmptyResults: true, testResults: 'reports/test-results.xml'
            
            // Publicar relatório de cobertura (se existir)
            script {
                if (fileExists('reports/coverage.xml')) {
                    publishCoverage adapters: [coberturaAdapter('reports/coverage.xml')]
                }
            }
            
            // Limpar workspace se necessário
            cleanWs(
                deleteDirs: true,
                disableDeferredWipeout: true,
                patterns: [
                    [pattern: '.venv/**', type: 'INCLUDE'],
                    [pattern: '**/__pycache__/**', type: 'INCLUDE'],
                    [pattern: '**/*.pyc', type: 'INCLUDE']
                ]
            )
        }
        
        success {
            echo 'Build executado com sucesso! ✓'
            script {
                if (params.SEND_NOTIFICATION) {
                    sendNotification('SUCCESS')
                }
            }
        }
        
        failure {
            echo 'Build falhou! ✗'
            script {
                if (params.SEND_NOTIFICATION) {
                    sendNotification('FAILURE')
                }
            }
        }
        
        unstable {
            echo 'Build instável (alguns checks falharam)'
            script {
                if (params.SEND_NOTIFICATION) {
                    sendNotification('UNSTABLE')
                }
            }
        }
    }
}

// Função auxiliar para executar testes
def runTests(pythonVersion) {
    echo "Executando testes com Python ${pythonVersion}..."
    
    sh """
        . ${VENV_DIR}/bin/activate
        
        # Criar diretório de relatórios
        mkdir -p reports
        
        # Executar testes
        chmod +x scripts/run_tests.sh
        scripts/run_tests.sh
        
        # Renomear relatórios para incluir versão do Python
        if [ -f reports/test-results.xml ]; then
            cp reports/test-results.xml reports/test-results-python-${pythonVersion}.xml
        fi
        
        if [ -f reports/coverage.xml ]; then
            cp reports/coverage.xml reports/coverage-python-${pythonVersion}.xml
        fi
    """
}

// Função auxiliar para enviar notificações
def sendNotification(status) {
    echo "Enviando notificação: Status = ${status}"
    
    // Verificar se as credenciais estão configuradas
    if (env.NOTIFICATION_EMAIL && env.FROM_EMAIL) {
        sh """
            . ${VENV_DIR}/bin/activate
            
            python scripts/send_notification.py \
                --to-email "${env.NOTIFICATION_EMAIL}" \
                --pipeline-status "${status}" \
                --run-number "${BUILD_NUMBER}" \
                --commit-sha "${GIT_COMMIT}" \
                --branch "${GIT_BRANCH}" || true
        """
    } else {
        echo "Credenciais de email não configuradas. Pulando notificação."
        echo "Configure as variáveis de ambiente: NOTIFICATION_EMAIL, FROM_EMAIL, EMAIL_PASSWORD"
    }
}

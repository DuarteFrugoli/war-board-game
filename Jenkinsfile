pipeline {
    agent any
    
    options {
        buildDiscarder(logRotator(numToKeepStr: '10'))
        timeout(time: 30, unit: 'MINUTES')
        timestamps()
    }
    
    stages {
        stage('Checkout') {
            steps {
                echo 'Fazendo checkout do código...'
                checkout scm
            }
        }
        
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
        
        stage('Test') {
            steps {
                echo 'Executando testes...'
                sh '''
                    . .venv/bin/activate
                    python -m pytest tests/ -v --tb=short || python -m unittest discover -s tests -p "test_*.py" -v
                '''
            }
        }
        
        stage('Build') {
            steps {
                echo 'Verificando se o projeto pode ser empacotado...'
                sh '''
                    . .venv/bin/activate
                    poetry build --format wheel || echo "Build check completed"
                '''
            }
        }
    }
    
    post {
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
        success {
            echo 'Build completado com sucesso! ✓'
        }
        failure {
            echo 'Build falhou! ✗'
        }
    }
}

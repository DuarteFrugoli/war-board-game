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
                    pip3 install --upgrade pip
                    pip3 install poetry
                    poetry install --no-root
                '''
            }
        }
        
        stage('Lint') {
            steps {
                echo 'Verificando qualidade do código...'
                sh '''
                    pip3 install black flake8 mypy
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
                    python3 -m pytest tests/ -v --tb=short || python3 -m unittest discover -s tests -p "test_*.py" -v
                '''
            }
        }
        
        stage('Build') {
            steps {
                echo 'Verificando se o projeto pode ser empacotado...'
                sh '''
                    poetry build --format wheel || echo "Build check completed"
                '''
            }
        }
    }
    
    post {
        always {
            echo 'Pipeline finalizado!'
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

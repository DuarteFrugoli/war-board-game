# Roteiro de Apresentação - C14 Engenharia de Software

## 1. Introdução ao Projeto (2-3 min)

### Sobre o Projeto
- **Nome**: WAR Board Game
- **Descrição**: Implementação digital do jogo de tabuleiro WAR em Python
- **Objetivo Educacional**: Aprender e aplicar boas práticas de Engenharia de Software
- **Tecnologias**: Python 3.9+, Pygame, Poetry

### Estrutura do Projeto
```
war-board-game/
├── war/              # Código principal do jogo
├── tests/            # Testes unitários
├── data/             # Dados do jogo (mapas, missões)
├── scripts/          # Scripts auxiliares
└── docs/             # Documentação
```

---

## 2. Gerenciamento de Dependências com Poetry (5 min)

### Por que usar um Gerenciador de Dependências?

**Problemas sem gerenciador:**
- ❌ "Funciona na minha máquina"
- ❌ Versões incompatíveis
- ❌ Dependências não documentadas
- ❌ Conflitos entre projetos

**Soluções com Poetry:**
- ✅ Ambiente isolado e reprodutível
- ✅ Versionamento de dependências
- ✅ Lock file (poetry.lock)
- ✅ Builds consistentes

### Demonstração Prática

**1. Arquivo `pyproject.toml`**
```toml
[project]
name = "war-board-game"
version = "0.1.0"
requires-python = ">=3.9"

dependencies = [
    "pygame>=2.6.0,<3.0.0",
]

[project.optional-dependencies]
dev = [
    "black>=23.0.0",
    "flake8>=6.0.0",
    "mypy>=1.0.0",
]
```

**Demonstrar comandos:**
```bash
# Criar ambiente virtual
python3 -m venv .venv

# Instalar Poetry no ambiente
source .venv/bin/activate
pip install poetry

# Instalar dependências do projeto
poetry install --no-root

# Verificar dependências instaladas
poetry show
```

**2. Poetry.lock**
- Garante versões exatas
- Todos da equipe usam mesmas versões
- Builds reprodutíveis em qualquer máquina

---

## 3. Versionamento com Git/GitHub (5 min)

### Estrutura de Branches
- **main**: Branch principal (código estável)
- Features desenvolvidas em branches separadas (se houver)

### Boas Práticas Implementadas

**Commits Semânticos:**
```bash
git commit -m "feat: adiciona sistema de turnos"
git commit -m "fix: corrige validação de território"
git commit -m "docs: atualiza README com instruções"
```

**Demonstração do Histórico:**
```bash
# Ver histórico de commits
git log --oneline --graph

# Ver mudanças específicas
git show <commit-hash>
```

### Estrutura do Repositório

**Arquivos importantes:**
- `.gitignore` - Ignora arquivos desnecessários (`.venv/`, `__pycache__/`, etc.)
- `README.md` - Documentação principal
- `LICENSE` - Licença MIT

**Demonstrar GitHub:**
- Issues (se houver)
- Pull Requests (se houver)
- Histórico de commits
- Aba Actions (CI/CD)

---

## 4. CI/CD - Integração e Deploy Contínuos (7 min)

### O que é CI/CD?

**CI (Continuous Integration):**
- Integração contínua de código
- Testes automáticos a cada commit
- Detecção precoce de bugs

**CD (Continuous Deployment/Delivery):**
- Build automático
- Deploy automatizado (se aplicável)

### GitHub Actions - Demonstração

**Arquivo `.github/workflows/ci.yml`:**

**Pipeline executa:**
1. **Checkout** - Baixa o código
2. **Setup** - Configura Python e instala dependências
3. **Lint** - Verifica qualidade do código
   - Black (formatação)
   - Flake8 (estilo PEP8)
   - MyPy (type checking)
4. **Test** - Executa testes unitários
5. **Build** - Verifica se pode gerar pacote

**Demonstração na Interface:**
```
1. Acessar repositório no GitHub
2. Ir na aba "Actions"
3. Mostrar execuções recentes
4. Clicar em uma execução
5. Mostrar logs de cada etapa
6. Explicar badges (✓ verde = passou, ✗ vermelho = falhou)
```

**Benefícios:**
- ✅ Feedback imediato se algo quebrou
- ✅ Código sempre testado antes de mergear
- ✅ Qualidade garantida

### Jenkins - Demonstração Alternativa

**Por que Jenkins também?**
- Opção self-hosted (roda no seu servidor)
- Controle total da infraestrutura
- Alternativa ao GitHub Actions

**Demonstração:**
```
1. Acessar http://localhost:8080
2. Mostrar dashboard
3. Clicar no projeto war-board-game
4. Executar "Build Now"
5. Mostrar console output
6. Explicar os estágios (Setup, Lint, Test, Build)
```

**Configuração via Docker:**
```bash
# Subir Jenkins localmente
docker-compose -f docker-compose.jenkins.yml up -d

# Acessar em http://localhost:8080
```

**Arquivo `Jenkinsfile`:**
- Pipeline as Code
- Versionado junto com o projeto
- Mesmos estágios do GitHub Actions

---

## 5. Testes Automatizados (3 min)

### Cobertura de Testes

**Estrutura de testes:**
```
tests/
├── test_card.py       # Testa sistema de cartas
├── test_deck.py       # Testa baralho
├── test_game.py       # Testa lógica do jogo
├── test_player.py     # Testa jogadores
├── test_territory.py  # Testa territórios
└── test_turn_system.py # Testa turnos
```

**Demonstração de execução:**
```bash
# Executar todos os testes
python -m unittest discover -s tests -p "test_*.py" -v

# Resultado esperado: X tests passed
```

**Exemplo de teste:**
```python
def test_attack_validation(self):
    """Testa se ataque só é válido entre territórios adjacentes"""
    result = self.game.validate_attack(territory1, territory2)
    self.assertTrue(result)
```

---

## 6. Qualidade de Código (2 min)

### Ferramentas de Análise Estática

**Black - Formatação Automática:**
```bash
black war/ tests/
# Formata código automaticamente
```

**Flake8 - Verificação de Estilo:**
```bash
flake8 war/ tests/ --max-line-length=100
# Verifica: imports não usados, linhas muito longas, etc.
```

**MyPy - Type Checking:**
```bash
mypy war/ --ignore-missing-imports
# Verifica tipos de dados (type hints)
```

**Benefícios:**
- Código consistente
- Fácil de ler e manter
- Menos bugs

---

## 7. Workflow Completo - Demonstração Prática (3 min)

### Simular desenvolvimento de uma feature:

**1. Fazer uma mudança no código:**
```bash
# Editar algum arquivo
vim war/player.py  # Adicionar um método simples
```

**2. Testar localmente:**
```bash
# Rodar testes
python -m unittest discover -s tests

# Verificar formatação
black --check war/

# Verificar estilo
flake8 war/
```

**3. Commit e Push:**
```bash
git add .
git commit -m "feat: adiciona método de validação de jogador"
git push
```

**4. Ver CI/CD em ação:**
- Mostrar GitHub Actions rodando automaticamente
- OU executar build no Jenkins
- Mostrar resultado (success/failure)

---

## 8. Conclusão (2 min)

### Principais Aprendizados

**Gerenciamento de Dependências:**
- Poetry garante ambiente consistente
- Versionamento de dependências
- Builds reprodutíveis

**Versionamento:**
- Git/GitHub como fonte única de verdade
- Histórico completo de mudanças
- Colaboração facilitada

**CI/CD:**
- Testes automáticos a cada commit
- Qualidade garantida
- Feedback imediato

**Impacto no Desenvolvimento:**
- ✅ Menos bugs em produção
- ✅ Código mais limpo e consistente
- ✅ Desenvolvimento mais ágil
- ✅ Maior confiança nas mudanças

### Próximos Passos
- Aumentar cobertura de testes
- Adicionar testes de integração
- Configurar deploy automático (se aplicável)
- Adicionar badges no README

---

## Dicas para a Apresentação

### Preparação
- [ ] Testar todos os comandos antes
- [ ] Ter terminal aberto com ambiente já configurado
- [ ] Jenkins rodando (se for demonstrar)
- [ ] GitHub aberto na aba Actions
- [ ] Exemplos de código prontos para mostrar

### Durante a Apresentação
- Explicar o "porquê" além do "como"
- Mostrar exemplos práticos
- Relacionar com problemas reais de desenvolvimento
- Ser objetivo e direto

### Perguntas Comuns
**"Por que não usar apenas pip?"**
- Poetry gerencia ambiente virtual também
- Lock file garante versões exatas
- Resolve dependências automaticamente

**"Por que usar CI/CD em projeto pequeno?"**
- Aprender boas práticas desde cedo
- Evitar "technical debt"
- Preparação para projetos maiores

**"Jenkins vs GitHub Actions?"**
- GitHub Actions: mais fácil, integrado
- Jenkins: mais controle, self-hosted, gratuito sempre

**"Por que tantas ferramentas de qualidade?"**
- Cada uma tem um foco específico
- Juntas garantem código de alta qualidade
- Padrão da indústria

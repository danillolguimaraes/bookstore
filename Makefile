# Definição de variáveis padrão
PYTHON_VERSION ?= 3.8.10
LIBRARY_DIRS = mylibrary
BUILD_DIR ?= build

# Opções para PyTest
PYTEST_HTML_OPTIONS = --html=$(BUILD_DIR)/report.html --self-contained-html
PYTEST_TAP_OPTIONS = --tap-combined --tap-outdir $(BUILD_DIR)
PYTEST_COVERAGE_OPTIONS = --cov=$(LIBRARY_DIRS)
PYTEST_OPTIONS ?= $(PYTEST_HTML_OPTIONS) $(PYTEST_TAP_OPTIONS) $(PYTEST_COVERAGE_OPTIONS)

# Opções para MyPy
MYPY_OPTS ?= --python-version $(PYTHON_VERSION) --show-column-numbers --pretty --html-report $(BUILD_DIR)/mypy

# Ferramentas de gerenciamento de pacotes
PIP ?= pip3
POETRY ?= poetry

##@ Utility
.PHONY: help
help:  ## Exibe esta ajuda
	@awk 'BEGIN {FS = ":.*##"; printf "\nUso:\n  make \033[36m\033[0m\n"} /^[a-zA-Z0-9_-]+:.*?##/ { printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2 } /^##@/ { printf "\n\033[1m%s\033[0m\n", substr($$0, 5) } ' $(MAKEFILE_LIST)

.PHONY: version-python
version-python: ## Exibe a versão do Python em uso
	@echo $(PYTHON_VERSION)

##@ Testing
.PHONY: test
test: ## Executa os testes
	$(POETRY) run pytest $(PYTEST_OPTIONS) tests/*.py

##@ Building and Publishing
.PHONY: build
build: ## Executa o build
	$(POETRY) build

.PHONY: publish
publish: ## Publica o build no repositório configurado
	$(POETRY) publish $(POETRY_PUBLISH_OPTIONS_SET_BY_CI_ENV)

.PHONY: deps-py-update
deps-py-update: pyproject.toml ## Atualiza as dependências do Poetry
	$(POETRY) update

##@ Setup
.PHONY: deps
deps: deps-brew deps-py  ## Instala todas as dependências

.PHONY: deps-brew
deps-brew: Brewfile ## Instala dependências de desenvolvimento usando Homebrew
	brew bundle --file=Brewfile
	@echo "Certifique-se de que o pyenv está configurado no seu shell."
	@echo "Deve haver algo como 'eval \$$(pyenv init -)' no seu shell."

.PHONY: deps-py
deps-py: $(PYTHON_VERSION_FILE) ## Instala dependências de desenvolvimento e runtime do Python
	$(PIP) install --upgrade pip
	$(PIP) install --upgrade poetry
	$(POETRY) install

##@ Code Quality
.PHONY: check
check: check-py ## Executa linters e outras ferramentas importantes

.PHONY: check-py
check-py: check-py-flake8 check-py-black check-py-mypy ## Verifica apenas arquivos Python

.PHONY: check-py-flake8
check-py-flake8: ## Executa o linter flake8
	poetry run flake8 .

.PHONY: check-py-black
check-py-black: ## Executa o black em modo de verificação (sem alterações)
	poetry run black --check --line-length 118 --fast .

.PHONY: check-py-mypy
check-py-mypy: ## Executa o mypy
	poetry run mypy $(MYPY_OPTS) $(LIBRARY_DIRS)

.PHONY: format-py
format-py: ## Formata o código usando black
	poetry run black .

.PHONY: format-autopep8
format-autopep8:
	poetry run autopep8 --in-place --recursive .

.PHONY: format-isort
format-isort:
	poetry run isort --recursive .

.PHONY: migrate
migrate:
	docker-compose exec web python manage.py migrate --noinput

.PHONY: seed
seed:
	poetry run python manage.py seed

"""
Ponto de entrada da aplicação CloudTask AI SaaS.

Este módulo instancia o objeto :class:`fastapi.FastAPI` que será servido
pelo ``uvicorn`` e registra os routers HTTP. Em aulas futuras este arquivo
crescerá com configuração via ``.env`` (Aula 4), conexão com banco
(Aula 3), middlewares de logging/CORS, etc.

Formas de execução:
    Local (com venv)::

        $ uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

    Docker (target dev)::

        $ docker build --target dev -t cloudtask-api:dev .
        $ docker run --rm -p 8000:8000 cloudtask-api:dev

    Devcontainer (VS Code)::

        F1 → "Dev Containers: Reopen in Container"

URLs úteis após subir:
    * Swagger UI:    http://localhost:8000/docs
    * ReDoc:         http://localhost:8000/redoc
    * OpenAPI JSON:  http://localhost:8000/openapi.json
"""

from __future__ import annotations

from fastapi import FastAPI, status

from app import __version__
from app.api import routes_health
from app.schemas import RootResponse

# ---------------------------------------------------------------------------
# Instância principal do FastAPI.
#
# Os parâmetros abaixo aparecem na página do Swagger:
#   * `title`       → topo da página.
#   * `description` → bloco introdutório (aceita Markdown).
#   * `version`     → tag de versão exibida ao lado do título.
# ---------------------------------------------------------------------------
app = FastAPI(
    title="CloudTask AI SaaS",
    description=(
        "Mini SaaS de gerenciamento de tarefas construído ao longo da "
        "disciplina **Computação em Nuvem** (N-CPU / UNINTER).\n\n"
        "Esta é a versão da **Aula 1**: apenas endpoints básicos para "
        "validar a estrutura do projeto, do Docker e do devcontainer.\n\n"
        "Veja [a issue da aula](https://github.com/N-CPUninter/"
        "Computa-o-em-Nuvem---Projeto-exemplo-CloudTask-AI-SaaS/issues/1) "
        "e o roadmap completo em `docs/ROADMAP.md`."
    ),
    version=__version__,
    contact={
        "name": "Prof. Guilherme Patriota",
        "url": "https://github.com/guipatriota",
    },
    license_info={
        "name": "GNU GPL v3.0",
        "url": "https://www.gnu.org/licenses/gpl-3.0.html",
    },
)

# Registra os endpoints do módulo `routes_health` na aplicação.
app.include_router(routes_health.router)


@app.get(
    "/",
    response_model=RootResponse,
    status_code=status.HTTP_200_OK,
    summary="Metadados da aplicação",
    tags=["meta"],
    response_description="Identificação básica do serviço.",
    responses={
        200: {
            "description": "Metadados retornados com sucesso.",
            "content": {
                "application/json": {
                    "example": {
                        "name": "CloudTask AI SaaS",
                        "version": "0.1.0",
                        "docs": "/docs",
                    }
                }
            },
        }
    },
)
def root() -> RootResponse:
    """Devolve identificação básica do serviço.

    Usado por humanos para descobrir rapidamente onde acessar a
    documentação interativa e por monitores externos para confirmar
    qual versão está implantada.

    Returns:
        RootResponse: Nome, versão e caminho do Swagger.

    Example:
        Chamada via ``curl``::

            $ curl -s http://localhost:8000/
            {"name":"CloudTask AI SaaS","version":"0.1.0","docs":"/docs"}

        Chamada via ``httpx``::

            >>> import httpx
            >>> r = httpx.get("http://localhost:8000/")
            >>> r.status_code, r.json()["docs"]
            (200, '/docs')
    """
    return RootResponse(
        name="CloudTask AI SaaS",
        version=__version__,
        docs="/docs",
    )

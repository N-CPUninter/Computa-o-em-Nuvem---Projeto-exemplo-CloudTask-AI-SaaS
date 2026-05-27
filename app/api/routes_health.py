"""
Rotas de health-check da API CloudTask AI SaaS.

Endpoints leves usados por:

* ``HEALTHCHECK`` do Docker (definido no ``Dockerfile``).
* ``readinessProbe`` / ``livenessProbe`` do Kubernetes (Aulas 6 e 8).
* Load Balancers (ELB/ALB/NLB) na frente do EKS (Aula 8).

Não dependem de banco nem de serviços externos — manter assim. Em aulas
futuras (Aula 3+) introduziremos um ``/health/ready`` separado que
verifica conexão com PostgreSQL/RDS, S3, etc.
"""

from __future__ import annotations

from fastapi import APIRouter, status

from app.schemas import HealthResponse

router = APIRouter(tags=["health"])


@router.get(
    "/health",
    response_model=HealthResponse,
    status_code=status.HTTP_200_OK,
    summary="Liveness probe da aplicação",
    response_description="Estado do processo da API.",
    responses={
        200: {
            "description": "Aplicação viva e respondendo.",
            "content": {
                "application/json": {
                    "example": {"status": "ok"},
                }
            },
        },
    },
)
def health() -> HealthResponse:
    """Indica se o processo da API está vivo.

    Endpoint **leve** e **sem dependências externas**, projetado para ser
    chamado por orquestradores (Docker / Kubernetes / ELB) milhares de
    vezes por dia sem custo perceptível.

    Returns:
        HealthResponse: Objeto contendo ``status == "ok"`` quando o
        processo Python responde corretamente a requisições HTTP.

    Example:
        Chamada via ``curl``::

            $ curl -s http://localhost:8000/health
            {"status":"ok"}

        Chamada via ``httpx``::

            >>> import httpx
            >>> httpx.get("http://localhost:8000/health").json()
            {'status': 'ok'}
    """
    return HealthResponse(status="ok")

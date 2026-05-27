"""
CloudTask AI SaaS — pacote principal da aplicação.

Este pacote concentra todo o código de servidor: ponto de entrada
(:mod:`app.main`), camada HTTP (:mod:`app.api`), modelos e schemas
compartilhados (:mod:`app.schemas`).

A variável :data:`__version__` é a fonte única de verdade para a versão
exposta no Swagger (``/docs``) e no endpoint raiz (``GET /``).

Aulas futuras vão expandir este pacote com:
    * ``app.core`` — configuração via ``.env`` (Aula 4)
    * ``app.db`` — SQLAlchemy + modelos (Aula 3)
    * ``app.services`` — integrações S3 / DynamoDB (Aulas 5 e 10)

Attributes:
    __version__ (str): Versão semântica da aplicação (``MAJOR.MINOR.PATCH``).
"""

__version__: str = "0.1.0"

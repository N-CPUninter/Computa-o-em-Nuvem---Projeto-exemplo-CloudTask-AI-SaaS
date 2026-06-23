# Arquitetura final — CloudTask AI SaaS

Visão consolidada do que a disciplina construiu, da máquina local à nuvem.

> Documento de **fechamento** (Aula 12). Resume as 6 semanas em um só lugar.

---

## Linha do tempo (o que cada semana somou)

| Semana | Camada adicionada | Tema |
| -----: | --- | --- |
| 1 | API FastAPI + Docker + devcontainer | base |
| 2 | PostgreSQL + CRUD + `.env` + HTTPS (conceito) | persistência + config |
| 3 | Uploads (S3 / local) + Kubernetes local (Kind) | storage + orquestração local |
| 4 | Imagem no ECR + deploy no EKS | nuvem (registry + cluster gerenciado) |
| 5 | HPA + custos + eventos (DynamoDB / JSON) | elasticidade + NoSQL |
| 6 | CDK (IaC) + entrega final | infra como código + consolidação |

---

## Arquitetura de produção (alvo final)

```text
                         Internet (HTTPS)
                              │
                       www.seu-dominio  ── Route 53 (DNS)
                              │
                         ┌────▼─────┐
                         │   ALB    │ ◄── ACM (certificado TLS)
                         └────┬─────┘
                  TLS termina aqui; HTTP interno
                              │
              ┌───────────────▼────────────────┐
              │        Amazon EKS (cluster)     │
              │   ┌──────────┐   HPA 2..5       │
              │   │ Pods API │ ◄── escala c/ CPU│
              │   └────┬─────┘                  │
              └────────┼───────────────────────┘
                       │
        ┌──────────────┼───────────────┬──────────────┐
        ▼              ▼               ▼              ▼
  RDS PostgreSQL   Amazon S3      DynamoDB        ECR (imagem)
  (tarefas)        (uploads)      (eventos/logs)  (origem do deploy)

  Infra descrita como código (CDK): S3, ECR, VPC  →  reprodutível e versionada.
```

> Esta é a topologia **alvo** (demonstrada na conta pessoal do professor, com
> domínio real). No Learner Lab, partes ficam simplificadas (sem Route53/ACM;
> Postgres pode rodar como Pod em vez de RDS).

---

## Componentes e responsabilidades

| Componente | Papel | Onde nasceu |
| --- | --- | --- |
| **FastAPI** | API REST + Swagger | Semana 1 |
| **PostgreSQL / RDS** | dados relacionais (tarefas) | Semana 2 / 6 |
| **Amazon S3** | arquivos (uploads), base de Data Lake | Semana 3 |
| **Kubernetes (Kind→EKS)** | orquestração de containers | Semanas 3–4 |
| **Amazon ECR** | registry da imagem da API | Semana 4 |
| **HPA** | escala automática de réplicas | Semana 5 |
| **DynamoDB** | eventos/logs (NoSQL) | Semana 5 |
| **ALB + ACM + Route 53** | borda HTTPS + domínio | Semana 6 (demo) |
| **AWS CDK** | infra como código (S3, ECR, VPC) | Semana 6 |

---

## Decisões de projeto (e por quê)

- **Fallback local em tudo que depende de nuvem** (S3→disco, DynamoDB→JSON):
  o aluno completa as aulas **sem AWS**.
- **Imagem `prod` embute o código** (`COPY`), `dev` usa volume: cluster precisa
  de imagem autossuficiente.
- **Cada banco para seu uso:** SQL (tarefas) + NoSQL (eventos). Não é "um
  substitui o outro".
- **Custo é cidadão de primeira classe:** todo recurso caro tem aviso + roteiro
  de destruição.

---

## Para a entrega

- Preencha o [`final-report-template.md`](final-report-template.md).
- Rode o [`deployment-checklist.md`](deployment-checklist.md) antes de demonstrar.
- Confirme o [`lgpd-checklist.md`](lgpd-checklist.md).

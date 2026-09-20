# TCC - Migração de Monólito para Microsserviços

Projeto desenvolvido como parte do Trabalho de Conclusão de Curso do MBA em Engenharia de Software da USP/Esalq.

O objetivo foi implementar e comparar uma aplicação web em duas abordagens arquiteturais:

- arquitetura monolítica;
- arquitetura baseada em microsserviços.

A comparação considerou comportamento sob carga, latência, throughput, consumo de CPU, consumo de memória, containerização com Docker e implantação em Kubernetes.

---

## Visão geral

A aplicação representa um sistema simples de pedidos composto por três domínios principais:

- Products
- Customers
- Orders

O mesmo escopo funcional foi preservado nas duas arquiteturas para permitir uma comparação mais consistente.

---

## Arquitetura monolítica

Na versão monolítica, os domínios de produtos, clientes e pedidos são executados em uma única aplicação FastAPI e compartilham a mesma camada de persistência.

### Fluxo simplificado

```text
Customer
   ↓
Order
   ↓
Product
   ↓
Stock
```

A criação de um pedido consulta cliente e produto dentro da própria aplicação e realiza a atualização de estoque diretamente na mesma camada de negócio.

### Estrutura conceitual

```text
┌─────────────────────────────┐
│       Aplicação FastAPI     │
│                             │
│ Products | Customers | Orders
└──────────────┬──────────────┘
               │
               ▼
        ┌──────────────┐
        │ PostgreSQL   │
        └──────────────┘
```

---

## Arquitetura de microsserviços

A aplicação foi posteriormente decomposta em três serviços independentes:

- `product-service`
- `customer-service`
- `order-service`

Cada serviço possui responsabilidade específica e comunicação por API HTTP.

### Estrutura conceitual

```text
┌─────────────────┐      ┌──────────────────┐
│ product-service │      │ customer-service │
└────────┬────────┘      └─────────┬────────┘
         │                         │
         └──────────┬──────────────┘
                    ▼
            ┌───────────────┐
            │ order-service │
            └───────┬───────┘
                    │
                    ▼
               PostgreSQL
```

O `order-service` passou a consultar os demais serviços por requisições HTTP, substituindo dependências internas do monólito por contratos explícitos entre APIs.

---

## Tecnologias utilizadas

### Back-end

- Python
- FastAPI
- SQLAlchemy
- PostgreSQL

### Infraestrutura

- Docker
- Docker Compose
- Kubernetes
- kind
- kubectl

### Testes e análise

- Locust
- monitoramento com `docker stats`
- scripts Python para consolidação dos resultados

---

## Funcionalidades

### Products

- criação de produtos;
- listagem;
- consulta por ID;
- atualização;
- exclusão;
- controle de estoque.

### Customers

- criação de clientes;
- listagem;
- consulta por ID;
- atualização;
- exclusão;
- validação de e-mail duplicado.

### Orders

- criação de pedidos;
- listagem;
- consulta por ID;
- validação da existência do cliente;
- validação da existência do produto;
- validação de estoque;
- cálculo do valor total;
- atualização do estoque após criação do pedido.

---

## Banco de dados

Foi utilizado PostgreSQL.

Na arquitetura de microsserviços, foram utilizadas bases lógicas separadas:

```text
product_db
customer_db
order_db
```

O ambiente também foi configurado com persistência de dados no Kubernetes utilizando `PersistentVolume` e `PersistentVolumeClaim`.

---

## Execução com Docker Compose

Para iniciar o ambiente:

```bash
docker compose up -d
```

Para verificar os containers:

```bash
docker ps
```

---

## Endpoints locais

### Monólito

```text
http://127.0.0.1:8000/docs
```

### Microsserviços

```text
http://127.0.0.1:8001/docs
http://127.0.0.1:8002/docs
http://127.0.0.1:8003/docs
```

---

## Testes de carga

Os testes foram executados com Locust utilizando três cenários:

| Usuários simultâneos | Spawn rate | Duração |
|---:|---:|---:|
| 10 | 2 usuários/s | 120 s |
| 50 | 5 usuários/s | 120 s |
| 100 | 10 usuários/s | 120 s |

Cada cenário foi repetido três vezes para cada arquitetura.

Foram avaliadas rotas HTTP GET funcionalmente equivalentes de:

- produtos;
- clientes;
- pedidos.

---

## Métricas avaliadas

Foram coletadas as seguintes métricas:

- requisições por segundo (RPS);
- latência média;
- mediana;
- P90;
- P95;
- P99;
- falhas;
- CPU média;
- CPU de pico;
- memória média;
- memória de pico.

CPU e memória foram coletadas automaticamente em intervalos de 5 segundos durante os testes.

---

## Resultados resumidos

### Throughput

O throughput permaneceu muito semelhante entre as duas arquiteturas.

| Usuários | Monólito | Microsserviços |
|---:|---:|---:|
| 10 | 6,53 RPS | 6,56 RPS |
| 50 | 32,03 RPS | 32,08 RPS |
| 100 | 64,04 RPS | 64,20 RPS |

### Latência média

| Usuários | Monólito | Microsserviços |
|---:|---:|---:|
| 10 | 10,3 ms | 8,7 ms |
| 50 | 11,7 ms | 8,3 ms |
| 100 | 11,3 ms | 9,3 ms |

### Memória média agregada

| Usuários | Monólito | Microsserviços |
|---:|---:|---:|
| 10 | 112,97 MiB | 234,20 MiB |
| 50 | 118,93 MiB | 245,67 MiB |
| 100 | 121,53 MiB | 254,29 MiB |

Os microsserviços apresentaram menor latência nos cenários avaliados, porém utilizaram aproximadamente o dobro da memória agregada.

O throughput permaneceu praticamente equivalente.

---

## Kubernetes

A arquitetura de microsserviços também foi implantada em um cluster Kubernetes local utilizando `kind`.

Foram criados recursos de:

- Deployment;
- Service;
- ConfigMap;
- PersistentVolume;
- PersistentVolumeClaim.

A persistência do PostgreSQL foi validada por meio da exclusão deliberada do Pod do banco e posterior verificação da permanência dos dados após sua recriação automática.

---

## Estrutura do projeto

```text
tcc-microservices/
│
├── monolith/
│
├── microservices/
│   ├── product-service/
│   ├── customer-service/
│   └── order-service/
│
├── kubernetes/
│
├── tests/
│   ├── locustfile.py
│   ├── locustfile_microservices.py
│   ├── monitor_docker.py
│   └── analyze_resources.py
│
├── results/
│   └── final/
│
├── docker-compose.yml
├── requirements.txt
└── README.md
```

---

## Conclusão

Os resultados não demonstraram superioridade absoluta de uma arquitetura.

A decomposição em microsserviços manteve throughput semelhante e apresentou menores tempos de resposta nos cenários avaliados, porém aumentou significativamente o consumo agregado de memória.

O experimento evidenciou que a migração para microsserviços deve ser considerada como uma decisão arquitetural baseada em trade-offs entre:

- desempenho;
- consumo de recursos;
- modularidade;
- desacoplamento;
- independência de implantação;
- complexidade operacional.

---

## Autora

**Denise Mangabeira Grassi**

MBA em Engenharia de Software - USP/Esalq

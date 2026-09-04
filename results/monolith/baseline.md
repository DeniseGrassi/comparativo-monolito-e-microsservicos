# Baseline da Arquitetura Monolítica

## Testes de carga

Os testes foram executados com Locust sobre a aplicação monolítica desenvolvida com FastAPI e PostgreSQL.

Foram avaliados três cenários de carga com duração de aproximadamente 2 minutos cada.

| Cenário | Requisições | Falhas | Mediana | P90 | P99 | Média | Máximo | RPS |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 10 usuários | 771 | 0 | 9 ms | 10 ms | 17 ms | 9 ms | 44 ms | 6,9 |
| 50 usuários | 3.401 | 0 | 9 ms | 11 ms | 23 ms | 9 ms | 63 ms | 33 |
| 100 usuários | 7.727 | 0 | 9 ms | 16 ms | 50 ms | 11 ms | 110 ms | 66,6 |

## CPU e memória sob alta carga

Durante o cenário de 100 usuários simultâneos, foram coletadas três amostras do processo do Uvicorn utilizando o comando `top`.

| Amostra | CPU | MEM | RES |
|---|---:|---:|---:|
| 1 | 35,7% | 0,5% | 75.168 KB |
| 2 | 42,5% | 0,5% | 76.860 KB |
| 3 | 34,2% | 0,5% | 77.596 KB |

### Resumo

- CPU média observada: aproximadamente 37,5%
- Maior uso de CPU observado: 42,5%
- Memória residente média: aproximadamente 74,7 MB
- Maior memória residente observada: aproximadamente 75,8 MB
- Taxa de falhas: 0% em todos os cenários

## Endpoints utilizados nos testes

- GET `/products/`
- GET `/products/1`
- GET `/customers/`
- GET `/orders/`
- GET `/orders/1`

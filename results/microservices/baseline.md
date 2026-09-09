# Baseline de Desempenho — Arquitetura de Microsserviços

> Avaliação de desempenho da arquitetura de microsserviços em ambiente local, utilizando **Docker Compose** e **Locust**.

---

## 1. Ambiente de teste

A arquitetura de microsserviços foi executada em ambiente local utilizando **Docker Compose**.

### Serviços avaliados

- `product-service`
- `customer-service`
- `order-service`
- `PostgreSQL`

Os testes foram executados com **Locust**, utilizando os mesmos endpoints de leitura empregados na baseline da aplicação monolítica.

### Cenários avaliados

| Cenário | Usuários simultâneos | Spawn rate | Duração aproximada |
| :-----: | -------------------: | ---------: | -----------------: |
| 1 | 10 | 2 usuários/s | 2 minutos |
| 2 | 50 | 5 usuários/s | 2 minutos |
| 3 | 100 | 10 usuários/s | 2 minutos |

> **Nota:** os containers não relacionados ao experimento foram interrompidos antes da execução final dos testes.

---

## 2. Resultados dos testes

### 2.1 Cenário 1 — 10 usuários

#### Configuração

| Parâmetro | Valor |
| :-- | --: |
| Usuários | 10 |
| Spawn rate | 2 usuários/s |
| Duração | 2 minutos |

#### Resultados agregados

| Métrica | Resultado |
| :-- | --: |
| Requests | 791 |
| Falhas | 0 |
| Mediana | 9 ms |
| P90 | 11 ms |
| P99 | 13 ms |
| Média | 9 ms |
| Tempo mínimo | 4 ms |
| Tempo máximo | 67 ms |
| RPS | 6,5 |

---

### 2.2 Cenário 2 — 50 usuários

#### Configuração

| Parâmetro | Valor |
| :-- | --: |
| Usuários | 50 |
| Spawn rate | 5 usuários/s |
| Duração | 2 minutos |

#### Resultados agregados

| Métrica | Resultado |
| :-- | --: |
| Requests | 3.862 |
| Falhas | 0 |
| Mediana | 9 ms |
| P90 | 11 ms |
| P99 | 18 ms |
| Média | 9 ms |
| Tempo mínimo | 4 ms |
| Tempo máximo | 31 ms |
| RPS | 33,3 |

---

### 2.3 Cenário 3 — 100 usuários

#### Configuração

| Parâmetro | Valor |
| :-- | --: |
| Usuários | 100 |
| Spawn rate | 10 usuários/s |
| Duração | 2 minutos |

#### Resultados agregados

| Métrica | Resultado |
| :-- | --: |
| Requests | 8.693 |
| Falhas | 1 |
| Mediana | 10 ms |
| P90 | 17 ms |
| P99 | 38 ms |
| Média | 12 ms |
| Tempo mínimo | 3 ms |
| Tempo máximo | 119 ms |
| RPS | 65,7 |

#### Falha registrada

A única falha ocorreu no endpoint:

```http
GET /orders/
Host: order-service
```

Erro retornado:

```text
RemoteDisconnected(Remote end closed connection without response)
```

Taxa aproximada de falhas:

$$
\frac{1}{8.693} \times 100 \approx 0{,}012\%
$$

> **Taxa de sucesso:** superior a **99,98%**.

---

## 3. Consumo de recursos

### 3.1 Consumo de CPU — cenário de 100 usuários

Foram realizadas três capturas durante a execução do cenário de 100 usuários com o comando:

```bash
docker stats
```

| Captura | `order-service` | `product-service` | `customer-service` | Total dos serviços |
| :-----: | --------------: | ----------------: | -----------------: | -----------------: |
| 1 | 15,46% | 17,79% | 10,22% | 43,47% |
| 2 | 20,07% | 16,54% | 10,19% | 46,80% |
| 3 | 25,44% | 26,53% | 8,37% | 60,34% |

> **CPU média aproximada dos três microsserviços:** **50,2%**.

O PostgreSQL apresentou consumo variável entre aproximadamente **4,33% e 13,75%**. O consumo do banco de dados foi analisado separadamente do consumo dos serviços da aplicação.

### 3.2 Consumo de memória

Durante o cenário de 100 usuários, o consumo de memória permaneceu relativamente estável.

| Serviço | Memória aproximada |
| :-- | --: |
| `order-service` | 63,7 MiB |
| `product-service` | 62,7 MiB |
| `customer-service` | 67,2 MiB |

> **Consumo agregado aproximado dos três serviços:** **193,6 MiB**.

O PostgreSQL apresentou consumo aproximado entre **70,5 e 72 MiB**.

---

## 4. Resumo comparativo

| Cenário | Requests | Falhas | Mediana | P90 | P99 | RPS |
| :-- | --: | --: | --: | --: | --: | --: |
| 10 usuários | 791 | 0 | 9 ms | 11 ms | 13 ms | 6,5 |
| 50 usuários | 3.862 | 0 | 9 ms | 11 ms | 18 ms | 33,3 |
| 100 usuários | 8.693 | 1 | 10 ms | 17 ms | 38 ms | 65,7 |

---

## 5. Observações

- Os testes mostraram estabilidade de latência nos três cenários avaliados.
- Mesmo com o aumento de **10 para 100 usuários simultâneos**, a mediana variou apenas de **9 ms para 10 ms**.
- O throughput aumentou de **6,5 RPS para 65,7 RPS**.
- No cenário de maior carga, foi registrada uma única falha de desconexão remota.
- Os resultados indicam que a arquitetura de microsserviços manteve baixa latência e alta taxa de sucesso, embora com maior consumo agregado de CPU e memória decorrente da execução independente de múltiplos serviços.

---

## 6. Conclusão

A arquitetura de microsserviços apresentou comportamento estável nos três cenários avaliados. Mesmo sob a carga máxima de **100 usuários simultâneos**, manteve baixa latência, throughput crescente e taxa de sucesso superior a **99,98%**.

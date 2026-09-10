# Comparação de desempenho - Monólito x Microsserviços

## Metodologia

As duas arquiteturas foram submetidas a testes de carga utilizando Locust.

Foram avaliados três cenários:

- 10 usuários simultâneos, spawn rate de 2 usuários/s;
- 50 usuários simultâneos, spawn rate de 5 usuários/s;
- 100 usuários simultâneos, spawn rate de 10 usuários/s.

Cada execução teve duração aproximada de 2 minutos.

Foram utilizados endpoints equivalentes de leitura envolvendo os domínios:

- Products
- Customers
- Orders

Para a arquitetura de microsserviços, containers não relacionados ao experimento foram interrompidos antes da execução final dos testes.

---

# Comparação dos resultados

## Cenário 1 - 10 usuários

| Métrica | Monólito | Microsserviços |
|---|---:|---:|
| Requests | 771 | 791 |
| Falhas | 0 | 0 |
| Mediana | 9 ms | 9 ms |
| P90 | 10 ms | 11 ms |
| P99 | 17 ms | 13 ms |
| Média | 9 ms | 9 ms |
| Máximo | 44 ms | 67 ms |
| RPS | 6,9 | 6,5 |

### Observação

No cenário de baixa carga, as duas arquiteturas apresentaram comportamento bastante semelhante. A mediana e a latência média permaneceram em 9 ms em ambos os casos, sem ocorrência de falhas.

---

## Cenário 2 - 50 usuários

| Métrica | Monólito | Microsserviços |
|---|---:|---:|
| Requests | 3.401 | 3.862 |
| Falhas | 0 | 0 |
| Mediana | 9 ms | 9 ms |
| P90 | 11 ms | 11 ms |
| P99 | 23 ms | 18 ms |
| Média | 9 ms | 9 ms |
| Máximo | 63 ms | 31 ms |
| RPS | 33,0 | 33,3 |

### Observação

Com 50 usuários simultâneos, o comportamento das duas arquiteturas continuou próximo. Os microsserviços apresentaram menor P99 e menor tempo máximo de resposta nesta execução, enquanto o throughput permaneceu praticamente equivalente.

---

## Cenário 3 - 100 usuários

| Métrica | Monólito | Microsserviços |
|---|---:|---:|
| Requests | 7.727 | 8.693 |
| Falhas | 0 | 1 |
| Mediana | 9 ms | 10 ms |
| P90 | 16 ms | 17 ms |
| P99 | 50 ms | 38 ms |
| Média | 11 ms | 12 ms |
| Máximo | 110 ms | 119 ms |
| RPS | 66,6 | 65,7 |

### Observação

No cenário de maior carga, as duas arquiteturas mantiveram throughput semelhante.

O monólito apresentou:

- menor mediana;
- menor latência média;
- ausência de falhas.

Os microsserviços apresentaram:

- menor P99;
- throughput próximo ao monólito;
- uma única falha em 8.693 requisições.

A falha registrada ocorreu no endpoint:

`GET order-service /orders/`

com o erro:

`RemoteDisconnected(Remote end closed connection without response)`

A ocorrência representa aproximadamente 0,012% das requisições desse cenário.

---

# Consumo de recursos - cenário de 100 usuários

## CPU da aplicação

| Arquitetura | CPU média aproximada |
|---|---:|
| Monólito | 37,5% |
| Microsserviços | 50,2% |

No caso dos microsserviços, o valor corresponde à soma aproximada do consumo dos processos:

- product-service;
- customer-service;
- order-service.

O consumo do PostgreSQL foi mantido separado para evitar distorção da comparação entre os processos da aplicação.

---

## Memória da aplicação

| Arquitetura | Memória aproximada |
|---|---:|
| Monólito | 75 MiB |
| Microsserviços | 193,6 MiB |

Nos microsserviços, o consumo foi distribuído aproximadamente da seguinte forma:

| Serviço | Memória |
|---|---:|
| order-service | 63,7 MiB |
| product-service | 62,7 MiB |
| customer-service | 67,2 MiB |

O PostgreSQL containerizado utilizou aproximadamente 70,5 a 72 MiB adicionais, sendo analisado separadamente.

---

# Síntese comparativa

Os resultados indicam que a decomposição da aplicação monolítica em microsserviços não provocou degradação significativa de desempenho nos cenários avaliados.

A latência mediana permaneceu entre 9 e 10 ms em ambas as arquiteturas, enquanto o throughput no cenário de 100 usuários ficou próximo de 66 requisições por segundo.

A arquitetura de microsserviços apresentou menor P99 no cenário de maior carga, porém exigiu maior consumo agregado de CPU e memória.

Esse aumento de utilização de recursos é consistente com a execução de múltiplos processos independentes, cada um contendo sua própria instância da aplicação FastAPI e seus componentes associados.

Dessa forma, os resultados evidenciam um trade-off entre isolamento arquitetural e eficiência de recursos. A arquitetura monolítica mostrou-se mais econômica em termos computacionais, enquanto a arquitetura de microsserviços manteve desempenho semelhante ao distribuir os domínios em serviços independentes.

Os benefícios da decomposição devem, portanto, ser analisados não apenas pelo desempenho bruto, mas também pelas características arquiteturais obtidas, como:

- isolamento entre domínios;
- independência de implantação;
- separação de responsabilidades;
- possibilidade de escalabilidade individual dos serviços;
- redução do acoplamento entre módulos;
- maior flexibilidade de evolução da aplicação.
# TCC - Migração de Monólito para Microsserviços

## Baseline da aplicação monolítica

Aplicação experimental desenvolvida em Python com FastAPI e PostgreSQL para análise comparativa entre arquitetura monolítica e arquitetura baseada em microsserviços.

### Domínios implementados

- Products
- Customers
- Orders

### Tecnologias

- Python
- FastAPI
- SQLAlchemy
- PostgreSQL

### Banco de dados

PostgreSQL executado localmente na porta 5433.

### Funcionalidades

#### Products
- criação de produtos
- listagem de produtos
- consulta por ID
- atualização
- exclusão

#### Customers
- criação de clientes
- listagem de clientes
- consulta por ID
- atualização
- exclusão
- validação de e-mail duplicado

#### Orders
- criação de pedidos
- listagem de pedidos
- consulta por ID
- validação da existência do cliente
- validação da existência do produto
- validação de estoque
- cálculo do valor total
- atualização do estoque após criação do pedido

## Acoplamento da arquitetura monolítica

A criação de um pedido depende diretamente dos modelos CustomerModel e ProductModel.

O fluxo atual é:

Customer
    ↓
Order
    ↓
Product
    ↓
Stock

A operação de criação de pedido consulta cliente e produto no mesmo banco de dados e atualiza o estoque dentro da mesma aplicação.
from locust import HttpUser, task, between


class MicroservicesUser(HttpUser):
    wait_time = between(1, 2)

    @task(3)
    def list_products(self):
        self.client.get(
            "http://127.0.0.1:8001/products/",
            name="GET product-service /products/"
        )

    @task(2)
    def get_product(self):
        self.client.get(
            "http://127.0.0.1:8001/products/1",
            name="GET product-service /products/1"
        )

    @task(3)
    def list_customers(self):
        self.client.get(
            "http://127.0.0.1:8002/customers/",
            name="GET customer-service /customers/"
        )

    @task(3)
    def list_orders(self):
        self.client.get(
            "http://127.0.0.1:8003/orders/",
            name="GET order-service /orders/"
        )

    @task(2)
    def get_order(self):
        self.client.get(
            "http://127.0.0.1:8003/orders/1",
            name="GET order-service /orders/1"
        )
from locust import HttpUser, task, between


class MonolithUser(HttpUser):
    wait_time = between(1, 2)

    @task(3)
    def list_products(self):
        self.client.get("/products/")

    @task(2)
    def get_product(self):
        self.client.get("/products/1")

    @task(3)
    def list_customers(self):
        self.client.get("/customers/")

    @task(3)
    def list_orders(self):
        self.client.get("/orders/")

    @task(2)
    def get_order(self):
        self.client.get("/orders/1")
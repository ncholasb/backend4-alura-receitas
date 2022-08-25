from datetime import datetime
from rest_framework.test import APITestCase


class TestGetAllDespesas(APITestCase):
    URL = "/api/v1/despesas/"

    def test_retorna_todas_despesas(self):
        data = datetime.now().strftime("%Y-%m-%d")
        self.client.post(self.URL, data={
            "descricao": "Despesa 1",
            "valor": 1500.00,
            "data": data
        })
        response = self.client.get(self.URL, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data[0]["id"], 1)
        self.assertEqual(response.data[0]["descricao"], "Despesa 1")
        self.assertEqual(response.data[0]["valor"], 1500.0)
        self.assertEqual(response.data[0]["data"].replace("T", " ").replace("Z", ""), data)  # noqa

    def test_retorna_erro(self):
        response = self.client.get(self.URL, format='json')
        self.assertEqual(response.data, {"error": "Não há dados cadastrados"})

    def test_retorna_filtrada_descricao(self):
        data = datetime.now().strftime("%Y-%m-%d")
        self.client.post(self.URL, data={
            "descricao": "Despesa 1",
            "valor": 1500.00,
            "data": data
        })
        self.client.post(self.URL, data={
            "descricao": "Segunda despesa",
            "valor": 1500.00,
            "data": data
        })
        self.client.post(self.URL, data={
            "descricao": "Terceira despesa",
            "valor": 1500.00,
            "data": data
        })
        response = self.client.get(self.URL + "?descricao=Despesa 1", format='json')   # noqa
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)


class TestCreateDespesas(APITestCase):
    URL = "/api/v1/despesas/"

    def test_cria_despesa_retorna_ok(self):
        data = datetime.now().strftime("%Y-%m-%d")
        value = {"message": "Dados registrados!"}
        response = self.client.post(self.URL, data={
            "descricao": "Despesa 1",
            "valor": 1500.00,
            "data": data
        })
        self.assertEqual(value, response.data)
        self.assertEqual(response.status_code, 200)

    def test_retorna_erro_duplicado(self):
        self.client.post(self.URL, data={
            "descricao": "Despesa 1",
            "valor": 1500.00,
             "data": "2022-08-11 20:18:50"  # noqa
        })
        response = self.client.post(self.URL, data={
            "descricao": "Despesa 1",
            "valor": 1500.00,
             "data": "2022-08-12 20:18:50"  # noqa
        })
        value = {"error": "Os dados não foram registrados..."}
        self.assertEqual(value, response.data)
        self.assertEqual(response.status_code, 400)


class TestDespesasID(APITestCase):
    URL = "/api/v1/despesas/"

    def test_get_despesas_id(self):
        data = datetime.now().strftime("%Y-%m-%d")
        self.client.post(self.URL, data={
            "descricao": "Despesa 1",
            "valor": 1500.00,
            "data": data
        })
        response = self.client.get(self.URL + "1/", format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["id"], 1)
        self.assertEqual(response.data["descricao"], "Despesa 1")
        self.assertEqual(response.data["valor"], 1500.0)
        self.assertEqual(response.data["data"].replace("T", " ").replace("Z", ""), data)  # noqa

    def test_retorna_erro(self):
        response = self.client.get(self.URL + "1/", format='json')
        self.assertEqual({"error": f"Não foi encontrada nenhuma despesa com id: 1"}, response.data)  # noqa


class TestDelete(APITestCase):
    URL = "/api/v1/despesas/"

    def test_deleta_retorna_valor(self):
        data = datetime.now().strftime("%Y-%m-%d")
        self.client.post(self.URL, data={
            "descricao": "Despesa 1",
            "valor": 1500.00,
            "data": data
        })
        response = self.client.delete(self.URL + "1/", format='json')
        self.assertEqual({"message": "Despesa 1 removida com sucesso!"}, response.data)  # noqa

    def test_should_be_delete_return_error(self):
        response = self.client.delete(self.URL + "1/", format='json')
        self.assertEqual({"error": f"Não foi encontrada nenhuma despesa com id: 1"}, response.data)  # noqa


class TestUpdate(APITestCase):
    URL = "/api/v1/despesas/"

    def test_retorna_erro(self):
        response = self.client.put(self.URL + "1/", data={
            "id": 1,
            "descricao": "Despesa 1",
            "valor": 1500.00,
            "data": "2022-08-24 20:46:55"  # noqa
        })
        self.assertEqual({"error": f"Não foi encontrada nenhuma Despesa com id: 1"}, response.data)  # noqa

    def test_update_retorna_valor(self):
        data = datetime.now().strftime("%Y-%m-%d")
        self.client.post(self.URL, data={
            "descricao": "Despesa 1",
            "valor": 1500.00,
            "data": data
        })
        response = self.client.put(self.URL + "1/", data={
            "id": 1,
            "categoria": "Outras",
            "descricao": "Despesa 1",
            "valor": 1500.00,
            "data": "2022-08-25"  # noqa
        })
        self.assertEqual({"message": "Despesa atualizada com sucesso!"}, response.data)  # noqa


class TestFiltroAnoMes(APITestCase):
    URL = "/api/v1/despesas/"

    def test_retorna_list_ano_mes(self):
        self.add_valor_id_db()
        response = self.client.get(self.URL + "2022/01/", format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

    def add_valor_id_db(self) -> None:
        self.client.post(self.URL, data={
            "descricao": "Despesa 1 de agosto",
            "valor": 1500.00,
            "data": "2022-08-13 15:25:55"
        })
        self.client.post(self.URL, data={
            "descricao": "Despesa 1 de julho",
            "valor": 1500.00,
            "data": "2022-07-13 15:25:55"
        })
        self.client.post(self.URL, data={
            "descricao": "Segunda Despesa de julho",
            "valor": 1500.00,
            "data": "2022-07-13 15:25:55"
        })
        self.client.post(self.URL, data={
            "descricao": "Despesa 1 de janeiro",
            "valor": 1500.00,
            "data": "2022-01-13 15:25:55"
        })

    def test_retorna_erro(self):
        response = self.client.get(self.URL + "2022/01/", format='json')
        self.assertEqual(
            response.data,
            {"error": "Não foram encontradas despesas no mês: 1 e ano: 2022"}
        )

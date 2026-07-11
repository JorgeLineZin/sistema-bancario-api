import os
import sys
import unittest

from fastapi.testclient import TestClient

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

os.environ.setdefault("DATABASE_URL", "sqlite:///./test_bank.db")

from src.api.server.server import app
from src.core.db import init_db


class BankRoutesTest(unittest.TestCase):
    def setUp(self) -> None:
        if os.path.exists("test_bank.db"):
            os.remove("test_bank.db")
        init_db()
        self.client = TestClient(app)

    def test_create_user_and_account_flow(self) -> None:
        create_user_response = self.client.post(
            "/users",
            json={
                "name": "Ana",
                "age": 30,
                "email": "ana@example.com",
                "cpf": "52998224725",
            },
        )
        self.assertEqual(create_user_response.status_code, 201)

        users_response = self.client.get("/users")
        self.assertEqual(users_response.status_code, 200)
        self.assertGreaterEqual(len(users_response.json()["data"]), 1)

        create_account_response = self.client.post(
            "/accounts",
            json={"agency": "001", "user_id": 1},
        )
        self.assertEqual(create_account_response.status_code, 201)

        account_response = self.client.get("/accounts/1")
        self.assertEqual(account_response.status_code, 200)
        self.assertEqual(account_response.json()["data"]["user_id"], 1)

    def test_invalid_json_body_returns_clear_error(self) -> None:
        response = self.client.post(
            "/users",
            content='{"name": "Jorge Felipe", "age": 20, "email": "jorge@example.com", "cpf": "52998224725"',
            headers={"content-type": "application/json"},
        )

        self.assertEqual(response.status_code, 422)
        self.assertEqual(response.json()["message"], "JSON inválido")


if __name__ == "__main__":
    unittest.main()

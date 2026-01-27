from unittest.mock import patch, MagicMock
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from calculate.models import CreditParameters
from .factories import UserFactory, CreditParametersFactory


class CreditParametersViewSetTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.base_url = "/calculate/credit-parameters/"
        self.user = UserFactory()

        self.valid_data = {
            "name": "John Doe",
            "month": "January",
            "occupation": "Engineer",
            "delay_from_due_date": "0",
            "credit_mix": "Standard",
            "payment_of_minimum_amount": "Yes",
            "payment_behaviour": "low_spend_small_value_payments",
            "changed_credit_limit": "No",
            "credit_history_age": "5",
            "age": 30,
            "annual_income": "50000.00",
            "monthly_in_hand_salary": "4000.00",
            "number_of_bank_accounts": 2,
            "number_of_credit_cards": 1,
            "interest_rate": "12.50",
            "number_of_loans": 1,
            "number_of_delayed_payment": 0,
            "num_credit_inquiries": 0,
            "outstanding_debt": "1000.00",
            "credit_utilization_ratio": "10.50",
            "total_emi_per_month": "500.00",
            "amount_invested_monthly": "200.00",
            "monthly_balance": "3000.00"
        }


    @patch("calculate.api.viewsets.open", create=True)
    @patch("calculate.api.viewsets.pickle.load", create=True)
    def test_create_credit_parameters(self, mock_pickle_load, mock_open):
        mock_model = MagicMock()
        mock_model.predict.return_value = "good"
        mock_pickle_load.return_value = mock_model

        response = self.client.post(self.base_url, self.valid_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        obj = CreditParameters.objects.get(id=response.data["id"])
        self.assertEqual(obj.credit_score, "good")

    def test_retrieve_credit_parameters(self):
        obj = CreditParametersFactory(credit_score="good")
        response = self.client.get(f"{self.base_url}{obj.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["credit_score"], "good")

    def test_update_credit_parameters(self):
        obj = CreditParametersFactory(credit_score="good")
        updated_data = self.valid_data.copy()
        updated_data["name"] = "Jane Doe"

        response = self.client.put(f"{self.base_url}{obj.id}/", updated_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        obj.refresh_from_db()
        self.assertEqual(obj.name, "Jane Doe")

    def test_delete_credit_parameters(self):
        obj = CreditParametersFactory(credit_score="good")
        response = self.client.delete(f"{self.base_url}{obj.id}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        from django.core.exceptions import ObjectDoesNotExist
        with self.assertRaises(ObjectDoesNotExist):
            CreditParameters.objects.get(id=obj.id)

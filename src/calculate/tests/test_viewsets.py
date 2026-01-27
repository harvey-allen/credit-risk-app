from unittest.mock import patch, MagicMock
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from calculate.models import CreditParameters
from users.models import User
from .factories import UserFactory, CreditParametersFactory


class CreditParametersViewSetTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.base_url = "/calculate/credit-parameters/"
        self.user = UserFactory()

        self.valid_data = {
            "user": self.user.email,
            "name": "John Doe",
            "occupation": "Engineer",
            "delay_from_due_date": "0",
            "credit_mix": "Standard",
            "payment_of_minimum_amount": "Yes",
            "payment_behaviour": "low_spend_small_value_payments",
            "changed_credit_limit": "No",

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
    def test_create_credit_parameters_with_existing_user(self, mock_pickle_load, mock_open):
        """Test creating credit parameters with an existing user email"""
        mock_model = MagicMock()
        mock_model.predict.return_value = "good"
        mock_pickle_load.return_value = mock_model

        initial_user_count = User.objects.count()

        response = self.client.post(self.base_url, self.valid_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Verify user count hasn't changed (no new user created)
        self.assertEqual(User.objects.count(), initial_user_count)

        # Verify credit parameters were created
        obj = CreditParameters.objects.get(id=response.data["id"])
        self.assertEqual(obj.credit_score, "good")
        self.assertEqual(obj.user.email, self.user.email)
        self.assertEqual(obj.name, "John Doe")

    @patch("calculate.api.viewsets.open", create=True)
    @patch("calculate.api.viewsets.pickle.load", create=True)
    def test_create_credit_parameters_creates_new_user(self, mock_pickle_load, mock_open):
        """Test creating credit parameters with a new user email auto-creates the user"""
        mock_model = MagicMock()
        mock_model.predict.return_value = "standard"
        mock_pickle_load.return_value = mock_model

        initial_user_count = User.objects.count()
        new_email = "newuser@example.com"

        new_user_data = self.valid_data.copy()
        new_user_data["user"] = new_email
        new_user_data["name"] = "Jane Smith"

        response = self.client.post(self.base_url, new_user_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Verify a new user was created
        self.assertEqual(User.objects.count(), initial_user_count + 1)

        # Verify the new user exists with correct data
        new_user = User.objects.get(email=new_email)
        self.assertEqual(new_user.first_name, "Jane")
        self.assertEqual(new_user.last_name, "Smith")
        self.assertEqual(new_user.phone_number, "0000000000")

        # Verify credit parameters were created and linked to new user
        obj = CreditParameters.objects.get(id=response.data["id"])
        self.assertEqual(obj.credit_score, "standard")
        self.assertEqual(obj.user.email, new_email)
        self.assertEqual(obj.name, "Jane Smith")

    @patch("calculate.api.viewsets.open", create=True)
    @patch("calculate.api.viewsets.pickle.load", create=True)
    def test_create_credit_parameters_single_name(self, mock_pickle_load, mock_open):
        """Test creating credit parameters with single name creates user correctly"""
        mock_model = MagicMock()
        mock_model.predict.return_value = "poor"
        mock_pickle_load.return_value = mock_model

        new_email = "singlename@example.com"
        new_user_data = self.valid_data.copy()
        new_user_data["user"] = new_email
        new_user_data["name"] = "Madonna"

        response = self.client.post(self.base_url, new_user_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Verify the new user was created with first name only
        new_user = User.objects.get(email=new_email)
        self.assertEqual(new_user.first_name, "Madonna")
        self.assertEqual(new_user.last_name, "")

    @patch("calculate.api.viewsets.open", create=True)
    @patch("calculate.api.viewsets.pickle.load", create=True)
    def test_create_duplicate_user_uses_existing(self, mock_pickle_load, mock_open):
        """Test that creating parameters with existing email fails due to OneToOne constraint"""
        mock_model = MagicMock()
        mock_model.predict.return_value = "good"
        mock_pickle_load.return_value = mock_model

        # Create first credit parameters which creates a user
        email = "duplicate@example.com"
        data1 = self.valid_data.copy()
        data1["user"] = email
        data1["name"] = "First User"

        response1 = self.client.post(self.base_url, data1, format="json")
        self.assertEqual(response1.status_code, status.HTTP_201_CREATED)

        user_count_after_first = User.objects.count()

        # Try to create another with same email - should fail due to OneToOne constraint
        data2 = self.valid_data.copy()
        data2["user"] = email
        data2["name"] = "Second User"

        response2 = self.client.post(self.base_url, data2, format="json")
        
        # Should return 400 error due to unique constraint
        self.assertEqual(response2.status_code, status.HTTP_400_BAD_REQUEST)
        
        # User count should not increase
        self.assertEqual(User.objects.count(), user_count_after_first)

    def test_retrieve_credit_parameters(self):
        """Test retrieving credit parameters by ID"""
        obj = CreditParametersFactory(credit_score="good")
        response = self.client.get(f"{self.base_url}{obj.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["credit_score"], "good")

    def test_update_credit_parameters(self):
        """Test updating credit parameters with existing user"""
        obj = CreditParametersFactory(credit_score="good")
        updated_data = self.valid_data.copy()
        updated_data["user"] = obj.user.email
        updated_data["name"] = "Jane Doe"

        response = self.client.put(f"{self.base_url}{obj.id}/", updated_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        obj.refresh_from_db()
        self.assertEqual(obj.name, "Jane Doe")

    def test_delete_credit_parameters(self):
        """Test deleting credit parameters"""
        obj = CreditParametersFactory(credit_score="good")
        response = self.client.delete(f"{self.base_url}{obj.id}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        from django.core.exceptions import ObjectDoesNotExist
        with self.assertRaises(ObjectDoesNotExist):
            CreditParameters.objects.get(id=obj.id)

    def test_list_credit_parameters(self):
        """Test listing all credit parameters"""
        CreditParametersFactory.create_batch(3)
        response = self.client.get(self.base_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)

    @patch("calculate.api.viewsets.open", create=True)
    @patch("calculate.api.viewsets.pickle.load", create=True)
    def test_create_without_user_email_fails(self, mock_pickle_load, mock_open):
        """Test that creating without user email fails"""
        mock_model = MagicMock()
        mock_model.predict.return_value = "good"
        mock_pickle_load.return_value = mock_model

        invalid_data = self.valid_data.copy()
        invalid_data.pop("user")

        response = self.client.post(self.base_url, invalid_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


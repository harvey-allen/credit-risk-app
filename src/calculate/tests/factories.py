import factory
from factory.django import DjangoModelFactory
from users.models import User
from calculate.models import CreditParameters


class UserFactory(DjangoModelFactory):
    class Meta:
        model = User

    email = factory.Sequence(lambda n: f"user{n}@example.com")
    first_name = "Test"
    last_name = "User"
    phone_number = factory.Sequence(lambda n: f"07123456{str(n).zfill(3)}")
    password = factory.PostGenerationMethodCall('set_password', 'password123')


class CreditParametersFactory(DjangoModelFactory):
    class Meta:
        model = CreditParameters

    user = factory.SubFactory(UserFactory)
    name = "John Doe"
    occupation = "Engineer"
    delay_from_due_date = "0"
    credit_mix = "Standard"
    payment_of_minimum_amount = "Yes"
    payment_behaviour = "LSSV"
    changed_credit_limit = "No"
    age = 30
    annual_income = "50000.00"
    monthly_in_hand_salary = "4000.00"
    number_of_bank_accounts = 2
    number_of_credit_cards = 1
    interest_rate = "12.50"
    number_of_loans = 1
    number_of_delayed_payment = 0
    num_credit_inquiries = 0
    outstanding_debt = "1000.00"
    credit_utilization_ratio = "10.50"
    total_emi_per_month = "500.00"
    amount_invested_monthly = "200.00"
    monthly_balance = "3000.00"
    credit_score = None

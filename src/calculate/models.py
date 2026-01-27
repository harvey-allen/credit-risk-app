import uuid
import logging

from django.db import models
from django.utils.translation import gettext_lazy as _

from users.models import User

logger = logging.getLogger("credit_models")


class CreditStatus(models.TextChoices):
    POOR = "poor", _("Poor Credit")
    STANDARD = "standard", _("Standard Credit")
    GOOD = "good", _("Good Credit")


class PaymentBehaviour(models.TextChoices):
    LSSV = "low_spend_small_value_payments", _("Low Spend and small value payments")
    LSMV = "low_spend_medium_value_payments", _("Low Spend and medium value payments")
    LSLV = "low_spend_large_value_payments", _("Low Spend and large value payments")
    HSSV = "high_spend_small_value_payments", _("High Spend and small value payments")
    HSMV = "high_spend_medium_value_payments", _("High Spend and medium value payments")
    HSLV = "high_spend_large_value_payments", _("High Spend and large value payments")


class CreditParameters(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    # Categorical Features
    month = models.CharField(max_length=10)
    occupation = models.CharField(max_length=100)
    delay_from_due_date = models.CharField(max_length=10)
    credit_mix = models.CharField(max_length=100)
    payment_of_minimum_amount = models.CharField(max_length=10)
    payment_behaviour = models.CharField(
        max_length=50,
        choices=PaymentBehaviour.choices,
        verbose_name="payment behaviour",
    )
    changed_credit_limit = models.CharField(max_length=10)
    credit_history_age = models.CharField(max_length=100)
    # Numerical Features
    age = models.IntegerField()
    annual_income = models.DecimalField(max_digits=10, decimal_places=2)
    monthly_in_hand_salary = models.DecimalField(max_digits=10, decimal_places=2)
    number_of_bank_accounts = models.IntegerField()
    number_of_credit_cards = models.IntegerField()
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2)
    number_of_loans = models.IntegerField()
    number_of_delayed_payment = models.IntegerField()
    num_credit_inquiries = models.IntegerField()
    outstanding_debt = models.DecimalField(max_digits=10, decimal_places=2)
    credit_utilization_ratio = models.DecimalField(max_digits=5, decimal_places=2)
    total_emi_per_month = models.DecimalField(max_digits=10, decimal_places=2)
    amount_invested_monthly = models.DecimalField(max_digits=10, decimal_places=2)
    monthly_balance = models.DecimalField(max_digits=10, decimal_places=2)
    # Result
    credit_score = models.CharField(
        max_length=20,
        choices=CreditStatus.choices,
        verbose_name="qualification type",
        blank=True,
        null=True,
    )

    def save(self, *args, **kwargs):
        is_new = self._state.adding
        if is_new:
            logger.info(f"Creating new credit parameter record for user: {self.user}")
        else:
            logger.info(f"Updating credit parameter record {self.id}")
        
        try:
            super(CreditParameters, self).save(*args, **kwargs)
            if is_new:
                logger.info(f"Successfully created credit parameter {self.id}")
            else:
                logger.info(f"Successfully updated credit parameter {self.id}")
        except Exception as e:
            logger.error(f"Failed to save credit parameter: {str(e)}", exc_info=True)
            raise


class CreditLoans(models.Model):
    class LoanTypes(models.TextChoices):
        AUTO = "auto_loan", _("Auto Loan")
        CREDIT_BUILDER = "credit_builder_loan", _("Credit Builder Loan")
        PERSONAL = "personal_loan", _("Personal Loan")
        HOME_EQUITY = "home_equity_loan", _("Home Equity Loan")
        MORTGAGE = "mortgage_loan", _("Mortgage Loan")
        STUDENT = "student_loan", _("Student Loan")
        DEBT_CONSOLIDATION = "debt_consolidation_loan", _("Debt Consolidation Loan")
        PAYDAY = "payday_loan", _("Payday Loan")
        NOT_SPECIFIED = "non_specified_loan", _("Not Specified")

    credit_check = models.ForeignKey(CreditParameters, on_delete=models.CASCADE)
    loan_type = models.CharField(
        max_length=20,
        choices=CreditStatus.choices,
        verbose_name="loan type",
        default=LoanTypes.NOT_SPECIFIED,
    )

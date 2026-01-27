import logging

from rest_framework import serializers

from calculate.models import CreditParameters
from users.models import User

logger = logging.getLogger("credit_serializers")


class CreditParametersSerializer(serializers.ModelSerializer):
    user = serializers.EmailField(write_only=True, required=False, allow_blank=True)
    user_id = serializers.IntegerField(source='user.id', read_only=True)
    
    class Meta:
        model = CreditParameters
        fields = "__all__"
        extra_kwargs = {
            'credit_score': {'required': False}
        }

    categorical_fields = [
        "name",
        "occupation",
        "delay_from_due_date",
        "credit_mix",
        "payment_of_minimum_amount",
        "payment_behaviour",
        "changed_credit_limit",
    ]
    numerical_fields = [
        "age",
        "annual_income",
        "monthly_in_hand_salary",
        "number_of_bank_accounts",
        "number_of_credit_cards",
        "interest_rate",
        "number_of_loans",
        "number_of_delayed_payment",
        "num_credit_inquiries",
        "outstanding_debt",
        "credit_utilization_ratio",
        "total_emi_per_month",
        "amount_invested_monthly",
        "monthly_balance",
    ]

    def validate(self, data):
        logger.info("Validating credit parameters data")
        missing_categorical = [f for f in self.categorical_fields if f not in data]
        missing_numerical = [f for f in self.numerical_fields if f not in data]
        
        if missing_categorical:
            logger.warning(f"Missing categorical fields: {missing_categorical}")
            for field in missing_categorical:
                raise serializers.ValidationError(f"categorical {field} is required.")
        
        if missing_numerical:
            logger.warning(f"Missing numerical fields: {missing_numerical}")
            for field in missing_numerical:
                raise serializers.ValidationError(f"numerical {field} is required.")
        
        logger.info("Credit parameters validation successful")
        return data

    def to_internal_value(self, data):
        logger.debug("Converting internal values for numerical fields")
        
        # Store user email for later processing in viewset
        user_email = data.get('user')
        if user_email:
            # Check if user exists and set ID, otherwise remove from data
            try:
                user = User.objects.get(email=user_email)
                logger.info(f"Found existing user with email {user_email}, ID: {user.id}")
                # Remove the email field so it doesn't interfere with model validation
                data = data.copy()
                data.pop('user', None)
            except User.DoesNotExist:
                # Remove user field - will be handled by viewset
                logger.info(f"User with email {user_email} does not exist - will be created")
                data = data.copy()
                data.pop('user', None)
        
        for field in self.numerical_fields:
            if field in data:
                try:
                    original_value = data[field]
                    data[field] = round(float(data[field]), 2)
                    logger.debug(f"Converted {field}: {original_value} -> {data[field]}")
                except (ValueError, TypeError) as e:
                    logger.error(f"Failed to convert {field} to number: {data[field]} - {str(e)}")
                    raise serializers.ValidationError(
                        {field: "Must be a number."}
                    )
        logger.info("Successfully converted all numerical fields")
        return super().to_internal_value(data)


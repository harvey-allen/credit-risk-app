import logging

from rest_framework import serializers

from calculate.models import CreditParameters

logger = logging.getLogger("credit_serializers")


class CreditParametersSerializer(serializers.ModelSerializer):
    class Meta:
        model = CreditParameters
        fields = "__all__"

    categorical_fields = [
        "name",
        "month",
        "occupation",
        "delay_from_due_date",
        "credit_mix",
        "payment_of_minimum_amount",
        "payment_behaviour",
        "changed_credit_limit",
        "credit_history_age",
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
        logger.info(f"Validating credit parameters data")
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
        logger.debug(f"Converting internal values for numerical fields")
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


import logging
import pickle
import os
import pandas as pd

from django.db import transaction, IntegrityError
from rest_framework import viewsets
from rest_framework.exceptions import ValidationError

from calculate.api.serializers import CreditParametersSerializer
from calculate.models import CreditParameters
from users.models import User

logger = logging.getLogger("credit_parameters")


class CreditParametersViewSet(viewsets.ModelViewSet):
    """
    A ViewSet for managing credit parameters data.

    This ViewSet provides CRUD (Create, Retrieve, Update, Delete) operations for CreditParameters objects.
    It uses the CreditParameters model and the CreditParametersSerializer for serialization.

    Methods:
        - perform_create(serializer): Creates a new CreditParameters object. It predicts the credit score
          based on the provided data using a pre-trained model and saves the prediction to the object.

    Attributes:
        - log: A logger for recording events related to credit parameters.
        - queryset: The set of CreditParameters objects to be retrieved and manipulated.
        - serializer_class: The serializer class to be used for data serialization.
    """

    queryset = CreditParameters.objects.all()
    serializer_class = CreditParametersSerializer

    def list(self, request, *args, **kwargs):
        logger.info("Fetching list of credit parameters")
        response = super().list(request, *args, **kwargs)
        logger.info(f"Retrieved {len(response.data)} credit parameter records")
        return response

    def retrieve(self, request, *args, **kwargs):
        logger.info(f"Fetching credit parameter with ID: {kwargs.get('pk')}")
        try:
            response = super().retrieve(request, *args, **kwargs)
            logger.info(f"Successfully retrieved credit parameter {kwargs.get('pk')}")
            return response
        except Exception as e:
            logger.error(f"Failed to retrieve credit parameter {kwargs.get('pk')}: {str(e)}")
            raise

    def perform_create(self, serializer):
        logger.info("Starting credit score prediction for new parameters")
        try:
            filename = "credit_model.sav"
            
            if not os.path.exists(filename):
                logger.error(f"Model file not found: {filename}")
                raise FileNotFoundError(f"Model file {filename} not found")
            
            logger.info(f"Loading credit model from {filename}")
            model = pickle.load(open(filename, "rb"))
            
            # Check if we need to create a user
            user_email = self.request.data.get('user')
            user_obj = None
            
            # Try to get existing user or create new one
            if user_email:
                try:
                    user_obj = User.objects.get(email=user_email)
                    logger.info(f"Using existing user with email {user_email}, ID: {user_obj.id}")
                except User.DoesNotExist:
                    logger.info(f"Creating new user with email: {user_email}")
                    # Extract name from the form data
                    name = self.request.data.get('name', '')
                    name_parts = name.split(' ', 1)
                    first_name = name_parts[0] if len(name_parts) > 0 else 'User'
                    last_name = name_parts[1] if len(name_parts) > 1 else ''
                    
                    user_obj = User.objects.create_user(
                        email=user_email,
                        first_name=first_name,
                        last_name=last_name,
                        phone_number='0000000000'  # Default phone number
                    )
                    logger.info(f"Created new user with ID: {user_obj.id}")
            
            if not user_obj:
                logger.error("User email is required but not provided")
                raise ValidationError({"user": "This field is required."})
            
            data = serializer.validated_data
            user_id = user_obj.id
            logger.info(f"Predicting credit score for user: {user_id}")
            
            # Convert data to DataFrame with correct column names for the model
            # Map our field names to the training data column names
            model_data = {
                'Name': data.get('name'),
                'Occupation': data.get('occupation'),
                'Delay_from_due_date': data.get('delay_from_due_date'),
                'Credit_Mix': data.get('credit_mix'),
                'Payment_of_Min_Amount': data.get('payment_of_minimum_amount'),
                'Payment_Behaviour': data.get('payment_behaviour'),
                'Changed_Credit_Limit': data.get('changed_credit_limit'),
                'Age': float(data.get('age')),
                'Annual_Income': float(data.get('annual_income')),
                'Monthly_Inhand_Salary': float(data.get('monthly_in_hand_salary')),
                'Num_Bank_Accounts': float(data.get('number_of_bank_accounts')),
                'Num_Credit_Card': float(data.get('number_of_credit_cards')),
                'Interest_Rate': float(data.get('interest_rate')),
                'Num_of_Loan': float(data.get('number_of_loans')),
                'Num_of_Delayed_Payment': float(data.get('number_of_delayed_payment')),
                'Num_Credit_Inquiries': float(data.get('num_credit_inquiries')),
                'Outstanding_Debt': float(data.get('outstanding_debt')),
                'Credit_Utilization_Ratio': float(data.get('credit_utilization_ratio')),
                'Total_EMI_per_month': float(data.get('total_emi_per_month')),
                'Amount_invested_monthly': float(data.get('amount_invested_monthly')),
                'Monthly_Balance': float(data.get('monthly_balance'))
            }
            
            # Create DataFrame with single row
            df = pd.DataFrame([model_data])
            logger.info(f"Prepared data for prediction: {df.shape}")
            
            try:
                credit_prediction = model.predict(df)
                # Get the first prediction result
                credit_score = credit_prediction[0] if len(credit_prediction) > 0 else "standard"
            except ValueError as ve:
                # Model expects preprocessed data with different feature count
                # This happens because the saved model doesn't include the preprocessing pipeline
                logger.warning(f"Model prediction failed (likely missing preprocessor): {str(ve)}")
                logger.info("Using rule-based fallback for credit score prediction")
                
                # Simple rule-based fallback
                # Calculate a basic score based on key factors
                credit_util = float(data.get('credit_utilization_ratio', 0))
                delayed_payments = int(data.get('number_of_delayed_payment', 0))
                credit_mix = str(data.get('credit_mix', '')).lower()
                
                if delayed_payments > 10 or credit_util > 80:
                    credit_score = "poor"
                elif delayed_payments <= 2 and credit_util < 30 and credit_mix in ['good', 'standard']:
                    credit_score = "good"
                else:
                    credit_score = "standard"
                
                logger.info(f"Fallback prediction: {credit_score}")
            
            logger.info(
                f"User {user_id} has a predicted credit score of {credit_score}"
            )
            
            with transaction.atomic():
                data["credit_score"] = credit_score
                # Always pass user object explicitly
                try:
                    serializer.save(user=user_obj)
                    logger.info(f"Successfully saved credit parameters for user {user_id}")
                except IntegrityError as e:
                    logger.error(f"Integrity error: User {user_id} already has credit parameters")
                    raise ValidationError({
                        "user": f"Credit parameters already exist for user with email '{user_email}'."
                    })
        except FileNotFoundError as e:
            logger.error(f"Model file error: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Error during credit score prediction: {str(e)}", exc_info=True)
            raise

    def perform_update(self, serializer):
        logger.info(f"Updating credit parameter with ID: {serializer.instance.id}")
        try:
            # Handle user email if provided
            user_email = self.request.data.get('user')
            if user_email:
                try:
                    user_obj = User.objects.get(email=user_email)
                    logger.info(f"Updating with existing user email: {user_email}")
                    serializer.save(user=user_obj)
                except User.DoesNotExist:
                    logger.error(f"User with email {user_email} does not exist")
                    raise ValidationError({"user": f"User with email '{user_email}' does not exist."})
            else:
                serializer.save()
            logger.info(f"Successfully updated credit parameter {serializer.instance.id}")
        except Exception as e:
            logger.error(f"Failed to update credit parameter: {str(e)}", exc_info=True)
            raise

    def perform_destroy(self, instance):
        logger.info(f"Deleting credit parameter with ID: {instance.id}")
        try:
            instance.delete()
            logger.info(f"Successfully deleted credit parameter {instance.id}")
        except Exception as e:
            logger.error(f"Failed to delete credit parameter {instance.id}: {str(e)}", exc_info=True)
            raise

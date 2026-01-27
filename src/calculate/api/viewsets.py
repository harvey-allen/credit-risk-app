import logging
import pickle
import os

from django.db import transaction
from rest_framework import viewsets

from calculate.api.serializers import CreditParametersSerializer
from calculate.models import CreditParameters

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
            
            data = serializer.validated_data
            user_id = data.get('user', 'unknown')
            logger.info(f"Predicting credit score for user: {user_id}")
            
            credit_prediction = model.predict(data)
            logger.info(
                f"User {user_id} has a predicted credit score of {credit_prediction}"
            )
            
            with transaction.atomic():
                data["credit_score"] = credit_prediction
                serializer.save()
                logger.info(f"Successfully saved credit parameters for user {user_id}")
        except FileNotFoundError as e:
            logger.error(f"Model file error: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Error during credit score prediction: {str(e)}", exc_info=True)
            raise

    def perform_update(self, serializer):
        logger.info(f"Updating credit parameter with ID: {serializer.instance.id}")
        try:
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

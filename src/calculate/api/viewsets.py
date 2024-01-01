import logging
import pickle

from django.db import transaction
from rest_framework import viewsets

from calculate.api.serializers import CreditParametersSerializer
from calculate.models import CreditParameters


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

    log = logging.getLogger("credit_parameters")

    queryset = CreditParameters.objects.all()
    serializer_class = CreditParametersSerializer

    def perform_create(self, serializer):
        filename = "credit_model.sav"
        model = pickle.load(open(filename, "rb"))
        data = serializer.validated_data
        credit_prediction = model.predict(data)
        self.log.info(
            f"{data[id]} has a predicted credit score of {credit_prediction}."
        )
        with transaction.atomic():
            data["credit_score"] = credit_prediction
            serializer.save()

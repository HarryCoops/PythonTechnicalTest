import requests

from rest_framework import status
import django_filters.rest_framework
from rest_framework.generics import ListCreateAPIView
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import authentication_classes, permission_classes


from bonds import models
from bonds import serializers
from bonds.settings import GLEIF_LEILOOKUP_URL

@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class Bonds(ListCreateAPIView):
    serializer_class = serializers.BondSerializer
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    filter_fields = ["isin", "size", "lei", "legal_name", "maturity", "currency"]

    def get_queryset(self):
        # Only allow users to list bonds created by themself
        return models.Bond.objects.filter(user=self.request.user)

    def post(self, request):
        """
        Create a new bond
        """
        data = JSONParser().parse(request)
    
        if not "lei" in data:
            return Response(
                "LEI must be present in request", 
                status=status.HTTP_422_UNPROCESSABLE_ENTITY
            )

        # Get the legal_name via GLEIF API
        response = requests.get(
            f"{GLEIF_LEILOOKUP_URL}?lei={data['lei']}"
        )
        if response.status_code == status.HTTP_400_BAD_REQUEST:
            return Response(
                response.json()["message"], status=status.HTTP_400_BAD_REQUEST
            )
        elif response.status_code != 200:
            return Response(
                "Service temporarily unavailable", 
                status=status.HTTP_503_SERVICE_UNAVAILABLE
            )

        response_json = response.json()
        if not response_json:
            return Response(
                f"A legal entiry with LEI {data['lei']} does not exist",
                status = status.HTTP_422_UNPROCESSABLE_ENTITY
            )
        
        legal_name = response.json()[0]["Entity"]["LegalName"]["$"]
        data["legal_name"] = legal_name
        serializer = serializers.BondSerializer(data=data, context={"request": request})

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()
        return Response(status=status.HTTP_200_OK)


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import authentication_classes, permission_classes


@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class HelloWorld(APIView):
    def get(self, request):
        return Response("Hello World!")

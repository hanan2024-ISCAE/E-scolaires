from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .serializers import RegisterEtudiantSerializer


@api_view(['POST'])
def register_etudiant(request):

    serializer = RegisterEtudiantSerializer(data=request.data)

    if serializer.is_valid():

        serializer.save()

        return Response(
            {
                "success": True,
                "message": "Inscription réussie"
            },
            status=status.HTTP_201_CREATED
        )

    return Response(
        {
            "success": False,
            "errors": serializer.errors
        },
        status=status.HTTP_400_BAD_REQUEST
    )
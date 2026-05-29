from rest_framework.response import Response
from rest_framework import status
from datetime import datetime
from django.http import FileResponse
from rest_framework.decorators import api_view
from .models import Etudiant, Module, Attestation
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from .models import  Etudiant, Module
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
import json
from .serializers import RegisterEtudiantSerializer, EtudiantSerializer, LoginSerializer, AttestationSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import api_view
from rest_framework.decorators import permission_classes

from rest_framework.permissions import IsAuthenticated

from rest_framework.response import Response

from .models import Etudiant
from .models import Attestation

from django.core.files.base import ContentFile

from io import BytesIO

from reportlab.platypus import SimpleDocTemplate
from reportlab.platypus import Paragraph
from reportlab.platypus import Spacer

from reportlab.lib.styles import getSampleStyleSheet

from reportlab.lib.pagesizes import A4



# =====================================================
# LOGIN
# =====================================================
@api_view(['POST'])
def login_view(request):

    serializer = LoginSerializer(
        data=request.data
    )

    if serializer.is_valid():

        username = serializer.validated_data['username']

        password = serializer.validated_data['password']

        user = authenticate(
            username=username,
            password=password
        )

        if user is not None:

            refresh = RefreshToken.for_user(user)

            return Response({

                "access": str(refresh.access_token),

                "refresh": str(refresh),

                "role": user.role,

                "username": user.username
            })

        return Response({
            "error": "Nom ou mot de passe incorrect"
        }, status=401)

    return Response(
        serializer.errors,
        status=400
    )



@api_view(['POST'])
def register_etudiant(request):

    serializer = RegisterEtudiantSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()

        return Response(
            {
                "message": "Inscription réussie"
            },
            status=status.HTTP_201_CREATED
        )

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def liste_etudiants(request):

    etudiants = Etudiant.objects.select_related(
        'user'
    ).all()

    serializer = EtudiantSerializer(
        etudiants,
        many=True
    )

    return Response(serializer.data)


# =====================================================
# ADMIN GENERER ATTESTATION
# =====================================================
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def details_attestation(request):

    try:

        # =====================================
        # ETUDIANT CONNECTE
        # =====================================
        etudiant = Etudiant.objects.select_related(
            "user"
        ).get(
            user=request.user
        )

        # =====================================
        # MODULES
        # =====================================
        modules_s1 = Module.objects.filter(
            semestre="S1"
        )

        modules_s2 = Module.objects.filter(
            semestre="S2"
        )

        # =====================================
        # RESPONSE
        # =====================================
        return Response({

            "etudiant": {
                    "nom": etudiant.user.last_name,
                    "prenom": etudiant.user.first_name,
                    "username": etudiant.user.username,
                    "matricule": etudiant.matricule,
                    "filiere": etudiant.filiere,
                    "niveau": etudiant.niveau,
                },

            "modules_s1": [
                {
                    "intitule": m.intitule,
                    "coefficient": m.coefficient
                }
                for m in modules_s1
            ],

            "modules_s2": [
                {
                    "intitule": m.intitule,
                    "coefficient": m.coefficient
                }
                for m in modules_s2
            ]

        })

    except Exception as e:

        return Response({
            "error": str(e)
        }, status=500)
    


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def mes_attestations(request):

    try:

        # =====================================
        # VERIFIER ROLE
        # =====================================
        if request.user.role != "etudiant":

            return Response({
                "error": "Accès refusé"
            }, status=403)

        # =====================================
        # RECUPERATION ETUDIANT
        # =====================================
        etudiant = Etudiant.objects.get(
            user=request.user
        )

        # =====================================
        # RECUPERATION ATTESTATIONS
        # =====================================
        attestations = Attestation.objects.filter(
            etudiant=etudiant
        ).order_by("-date_creation")

        # =====================================
        # SERIALIZER
        # =====================================
        serializer = AttestationSerializer(
            attestations,
            many=True,
            context={
                "request": request
            }
        )

        return Response(serializer.data)

    except Exception as e:

        return Response({
            "error": str(e)
        }, status=500)    

# =====================================================
# GENERER ATTESTATION
# =====================================================
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def generer_attestation(request):

    try:

        # =====================================
        # VERIFIER ADMIN
        # =====================================
        if request.user.role != "admin":

            return Response({
                "error": "Accès refusé"
            }, status=403)

        # =====================================
        # MATRICULE
        # =====================================
        matricule = request.data.get(
            "matricule"
        )

        # =====================================
        # ETUDIANT
        # =====================================
        etudiant = Etudiant.objects.select_related(
            "user"
        ).get(
            matricule=matricule
        )

        # =====================================
        # PDF
        # =====================================
        buffer = BytesIO()

        pdf = SimpleDocTemplate(
            buffer,
            pagesize=A4
        )

        styles = getSampleStyleSheet()

        elements = []

        # =====================================
        # TITRE
        # =====================================
        elements.append(
            Paragraph(
                """
                <b>
                ATTESTATION D'INSCRIPTION
                </b>
                """,
                styles['Title']
            )
        )

        elements.append(
            Spacer(1, 30)
        )

        # =====================================
        # TEXTE
        # =====================================
        texte = f"""
        Le chef du service de la scolarité
        atteste par la présente que :

        <br/><br/>

        <b>
        {etudiant.user.first_name}
        {etudiant.user.last_name}
        </b>

        <br/><br/>

        Matricule :
        <b>{etudiant.matricule}</b>

        <br/><br/>

        Filière :
        <b>{etudiant.filiere}</b>

        <br/><br/>

        Niveau :
        <b>{etudiant.niveau}</b>

        <br/><br/>

        est régulièrement inscrit(e)
        au sein de l’établissement.
        """

        elements.append(
            Paragraph(
                texte,
                styles['BodyText']
            )
        )

        elements.append(
            Spacer(1, 30)
        )

        # =====================================
        # FIN
        # =====================================
        elements.append(
            Paragraph(
                """
                Cette attestation est délivrée
                pour servir et valoir ce que de droit.
                """,
                styles['BodyText']
            )
        )

        # =====================================
        # BUILD PDF
        # =====================================
        pdf.build(elements)

        # =====================================
        # SAVE PDF
        # =====================================
        buffer.seek(0)

        contenu_pdf = ContentFile(
            buffer.read()
        )

        nom_fichier = (
            f"attestation_{etudiant.matricule}.pdf"
        )

        # =====================================
        # ENREGISTREMENT
        # =====================================
        attestation = Attestation.objects.create(
            etudiant=etudiant,
            type_attestation="inscription"
        )

        attestation.fichier.save(
            nom_fichier,
            contenu_pdf
        )

        attestation.save()

        # =====================================
        # RESPONSE
        # =====================================
        return Response({

            "message":
            "Attestation générée avec succès",

            "fichier":
            attestation.fichier.url

        })

    except Etudiant.DoesNotExist:

        return Response({
            "error": "Étudiant introuvable"
        }, status=404)

    except Exception as e:

        return Response({
            "error": str(e)
        }, status=500)
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAuthenticated

from .serializers import (
    RegisterEtudiantSerializer,
    NoteSerializer,
    PublierNoteSerializer,
    StudentSerializer,
    ModuleSerializer,
)
from notes.models import Note, Module
from users.permissions import IsAdmin, IsStudent

User = get_user_model()


# ============ EXISTING CODE ============

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


# ============ NEW NOTES ENDPOINTS ============

# ✅ Get dropdown options (students and modules)
@api_view(['GET'])
@permission_classes([IsAdmin])
def dropdown_options(request):
    """Get all students and modules for dropdown menus"""
    try:
        students = User.objects.filter(role='student').order_by('first_name', 'last_name')
        modules = Module.objects.all().order_by('intitule')
        
        return Response(
            {
                "success": True,
                "students": StudentSerializer(students, many=True).data,
                "modules": ModuleSerializer(modules, many=True).data,
            },
            status=status.HTTP_200_OK
        )
    except Exception as e:
        return Response(
            {
                "success": False,
                "error": str(e)
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


# ✅ List all notes
@api_view(['GET'])
@permission_classes([IsAdmin])
def notes_list(request):
    """List all notes with optional filtering"""
    try:
        queryset = Note.objects.select_related("etudiant", "module", "publie_par")
        
        # Optional filters
        student_id = request.query_params.get('student_id')
        if student_id:
            queryset = queryset.filter(etudiant_id=student_id)
        
        module_id = request.query_params.get('module_id')
        if module_id:
            queryset = queryset.filter(module_id=module_id)
        
        serializer = NoteSerializer(queryset, many=True)
        return Response(
            {
                "success": True,
                "data": serializer.data
            },
            status=status.HTTP_200_OK
        )
    except Exception as e:
        return Response(
            {
                "success": False,
                "error": str(e)
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


# ✅ Publish/Create a note
@api_view(['POST'])
@permission_classes([IsAdmin])
def publier_note(request):
    """Create and publish a new note"""
    try:
        serializer = PublierNoteSerializer(
            data=request.data,
            context={'request': request}
        )
        
        if serializer.is_valid():
            # Auto-set the admin who published it
            note = serializer.save(publie_par=request.user)
            
            # Return full note data with nested student/module info
            note_data = NoteSerializer(note).data
            
            return Response(
                {
                    "success": True,
                    "message": "Note publiée avec succès",
                    "data": note_data
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
    except Exception as e:
        return Response(
            {
                "success": False,
                "error": str(e)
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


# ✅ List modules
@api_view(['GET'])
@permission_classes([IsAdmin])
def modules_list(request):
    """List all modules"""
    try:
        modules = Module.objects.all().order_by('intitule')
        serializer = ModuleSerializer(modules, many=True)
        return Response(
            {
                "success": True,
                "data": serializer.data
            },
            status=status.HTTP_200_OK
        )
    except Exception as e:
        return Response(
            {
                "success": False,
                "error": str(e)
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


# ✅ Student's own notes
@api_view(['GET'])
@permission_classes([IsStudent])
def mes_notes(request):
    """Get the authenticated student's notes"""
    try:
        notes = Note.objects.filter(etudiant=request.user).select_related("etudiant", "module", "publie_par")
        serializer = NoteSerializer(notes, many=True)
        return Response(
            {
                "success": True,
                "data": serializer.data
            },
            status=status.HTTP_200_OK
        )
    except Exception as e:
        return Response(
            {
                "success": False,
                "error": str(e)
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )








# from rest_framework.decorators import api_view
# from rest_framework.response import Response
# from rest_framework import status

# from .serializers import RegisterEtudiantSerializer


# @api_view(['POST'])
# def register_etudiant(request):

#     serializer = RegisterEtudiantSerializer(data=request.data)

#     if serializer.is_valid():

#         serializer.save()

#         return Response(
#             {
#                 "success": True,
#                 "message": "Inscription réussie"
#             },
#             status=status.HTTP_201_CREATED
#         )

#     return Response(
#         {
#             "success": False,
#             "errors": serializer.errors
#         },
#         status=status.HTTP_400_BAD_REQUEST
#     )





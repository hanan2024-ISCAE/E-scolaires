from django.db import connection
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from users.permissions import IsAdmin, IsStudent
from django.contrib.auth import get_user_model

from .models import Note, Module
from .serializers import (
    NoteSerializer, 
    PublierNoteSerializer, 
    ModuleSerializer,
    StudentSerializer,
    DropdownOptionsSerializer
)

User = get_user_model()


# ✅ GET dropdown options (students and modules)
class DropdownOptionsView(APIView):
    permission_classes = [IsAdmin]
    
    def get(self, request):
        students = User.objects.filter(role='student').order_by('first_name', 'last_name')
        modules = Module.objects.all().order_by('intitule')
        
        return Response({
            'students': StudentSerializer(students, many=True).data,
            'modules': ModuleSerializer(modules, many=True).data,
        })


# ✅ List all notes
class NotesListView(ListAPIView):
    serializer_class = NoteSerializer
    permission_classes = [IsAdmin]
    queryset = Note.objects.select_related("etudiant", "module", "publie_par")
    
    def get_queryset(self):
        # Optional: filter by student_id or module_id if provided
        queryset = Note.objects.select_related("etudiant", "module", "publie_par")
        
        student_id = self.request.query_params.get('student_id')
        if student_id:
            queryset = queryset.filter(etudiant_id=student_id)
        
        module_id = self.request.query_params.get('module_id')
        if module_id:
            queryset = queryset.filter(module_id=module_id)
        
        return queryset


# ✅ Publish/Create a note
class PublierNoteView(CreateAPIView):
    serializer_class = PublierNoteSerializer
    permission_classes = [IsAdmin]
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(publie_par=request.user)  # ✅ Auto-set the admin
            return Response(
                {'message': 'Note publiée avec succès', 'data': NoteSerializer(serializer.instance).data},
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ✅ List modules (for dropdown)
class ModulesListView(ListAPIView):
    serializer_class = ModuleSerializer
    permission_classes = [IsAdmin]
    queryset = Module.objects.all().order_by('intitule')


# ✅ Student's own notes
class MesNotesListView(ListAPIView):
    serializer_class = NoteSerializer
    permission_classes = [IsStudent]

    def get_queryset(self):
        return Note.objects.filter(etudiant=self.request.user).select_related("etudiant", "module", "publie_par")








# from django.db import connection
# from rest_framework.generics import CreateAPIView, ListAPIView
# from rest_framework.response import Response
# from rest_framework.views import APIView

# from users.permissions import IsAdmin, IsStudent

# from .models import Note
# from .serializers import NoteSerializer, PublierNoteSerializer


# class NotesListView(ListAPIView):
#     serializer_class = NoteSerializer
#     permission_classes = [IsAdmin]
#     queryset = Note.objects.select_related("etudiant", "publie_par")


# class PublierNoteView(CreateAPIView):
#     serializer_class = PublierNoteSerializer
#     permission_classes = [IsAdmin]


# class ModulesListView(APIView):
#     permission_classes = [IsAdmin]

#     def get(self, request):
#         with connection.cursor() as cursor:
#             cursor.execute("SELECT id, intitule, coefficient, semestre FROM api_module ORDER BY intitule")
#             rows = cursor.fetchall()
#         return Response([
#             {"id": row[0], "intitule": row[1], "coefficient": row[2], "semestre": row[3]}
#             for row in rows
#         ])


# class MesNotesListView(ListAPIView):
#     serializer_class = NoteSerializer
#     permission_classes = [IsStudent]

#     def get_queryset(self):
#         return Note.objects.filter(etudiant=self.request.user).select_related("etudiant", "publie_par")

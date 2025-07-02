from django.shortcuts import render, redirect
from .models import UploadedFile
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden, FileResponse

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from .serializers import UploadedFileSerializer
from users.permissions import IsOpsUser, IsClientUser

import uuid
import mimetypes


class FileUploadView(APIView):
    parser_classes = [MultiPartParser]
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated, IsOpsUser]

    def post(self, request):
        file_obj = request.data.get('file')

        # Extension Check
        if not file_obj.name.endswith(('.pptx', '.docx', '.xlsx')):
            return Response({"error": "Only .pptx, .docx, .xlsx files allowed"}, status=400)

        # MIME Type Check (additional security)
        valid_mime_types = [
            'application/vnd.openxmlformats-officedocument.presentationml.presentation',
            'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
            'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        ]
        if file_obj.content_type not in valid_mime_types:
            return Response({"error": "Invalid file MIME type"}, status=400)

        uploaded_file = UploadedFile.objects.create(
            uploader=request.user,
            file=file_obj,
            secure_token=str(uuid.uuid4())
        )
        return Response(UploadedFileSerializer(uploaded_file).data)


class FileListView(APIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated, IsClientUser]

    def get(self, request):
        files = UploadedFile.objects.all()
        return Response(UploadedFileSerializer(files, many=True).data)


class FileDownloadLinkView(APIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated, IsClientUser]

    def get(self, request, file_id):
        try:
            file = UploadedFile.objects.get(id=file_id)
            return Response({
                "download-link": f"http://localhost:8000/api/secure-download/{file.secure_token}/",
                "message": "success"
            })
        except UploadedFile.DoesNotExist:
            return Response({"error": "File not found"}, status=404)


class SecureDownloadView(APIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated, IsClientUser]

    def get(self, request, token):
        try:
            file = UploadedFile.objects.get(secure_token=token)
            return FileResponse(file.file, as_attachment=True, filename=file.file.name)
        except UploadedFile.DoesNotExist:
            return Response({"error": "Invalid or expired link"}, status=404)


@login_required
def generate_secure_link(request, file_id):
    if not request.user.is_client:
        return HttpResponseForbidden()

    try:
        file = UploadedFile.objects.get(id=file_id)
    except UploadedFile.DoesNotExist:
        return redirect('dashboard_client')  # Could also render with error

    link = request.build_absolute_uri(f"/api/secure-download/{file.secure_token}/")
    files = UploadedFile.objects.all()
    return render(request, 'dashboard_client.html', {'files': files, 'link': link})

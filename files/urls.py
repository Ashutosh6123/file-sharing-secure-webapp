from django.urls import path
from .views import FileUploadView, FileListView, FileDownloadLinkView, SecureDownloadView

urlpatterns = [
    path('upload/', FileUploadView.as_view()),
    path('list/', FileListView.as_view()),
    path('download-file/<int:file_id>/', FileDownloadLinkView.as_view()),
    path('secure-download/<str:token>/', SecureDownloadView.as_view()),
]

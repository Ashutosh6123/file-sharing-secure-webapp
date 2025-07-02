from django.db import models
from users.models import CustomUser
import uuid

class UploadedFile(models.Model):
    uploader = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    file = models.FileField(upload_to='uploads/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    secure_token = models.CharField(max_length=100, unique=True, default=uuid.uuid4)

    def __str__(self):
        return self.file.name

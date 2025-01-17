# models.py in the 'files' app
from django.db import models
import gridfs
from django.conf import settings

# MongoDB GridFS storage
class File(models.Model):
    file_name = models.CharField(max_length=255)
    file = models.FileField(upload_to='uploads/')  # Will not actually store in PostgreSQL
    uploaded_by = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def save_file_to_gridfs(self):
        """Save file to GridFS."""
        with open(self.file.path, 'rb') as f:
            fs.put(f, filename=self.file_name)

    def get_file_from_gridfs(self):
        """Retrieve file from GridFS."""
        file_data = fs.find_one({'filename': self.file_name})
        return file_data.read()

    def delete_file_from_gridfs(self):
        """Delete file from GridFS."""
        fs.delete({'filename': self.file_name})



from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .forms import FileUploadForm
from google.oauth2 import service_account
from googleapiclient.discovery import build
from .models import UploadedFile
from googleapiclient.http import MediaFileUpload
import os

def initialize_drive_service():
    credentials = service_account.Credentials.from_service_account_file(
        'credentials/named-embassy-432505-j4-f07c5344a234.json'  # Update with your actual path
    )
    return build('drive', 'v3', credentials=credentials)

def upload_file(request):
    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                uploaded_file = form.save(commit=False)
                uploaded_file.save()

                drive_service = initialize_drive_service()
                file_metadata = {
                    'name': uploaded_file.file.name,
                    'parents': ['1HVveRLTMwkPj0CahinfLSwi4wuO_9sTv']  # Replace with your Google Drive folder ID
                }

                if not os.path.exists(uploaded_file.file.path):
                    raise FileNotFoundError(f"The file {uploaded_file.file.path} does not exist.")

                media = MediaFileUpload(uploaded_file.file.path)
                gfile = drive_service.files().create(body=file_metadata, media_body=media, fields='id').execute()
                uploaded_file.drive_id = gfile['id']
                uploaded_file.save()

                messages.success(request, 'File uploaded successfully!')
                return redirect('upload_file')
            except Exception as e:
                messages.error(request, f'Error uploading file: {str(e)}')
    else:
        form = FileUploadForm()

    uploaded_files = UploadedFile.objects.all()  # Retrieve all uploaded files
    return render(request, 'upload_file.html', {'form': form, 'uploaded_files': uploaded_files})

def delete_file(request, file_id):
    uploaded_file = get_object_or_404(UploadedFile, id=file_id)
    try:
        # Optionally delete the file from Google Drive if you have a drive_id
        drive_service = initialize_drive_service()
        if uploaded_file.drive_id:
            drive_service.files().delete(fileId=uploaded_file.drive_id).execute()
        
        # Delete the file from the local filesystem
        if os.path.exists(uploaded_file.file.path):
            os.remove(uploaded_file.file.path)

        # Delete the file record from the database
        uploaded_file.delete()
        messages.success(request, 'File deleted successfully!')
    except Exception as e:
        messages.error(request, f'Error deleting file: {str(e)}')

    return redirect('upload_file')

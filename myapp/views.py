from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .forms import FileUploadForm  # Updated form name
from google.oauth2 import service_account 
from googleapiclient.discovery import build
from .models import UploadedFile  # Updated model name
from googleapiclient.http import MediaFileUpload
from django.conf import settings
import os

# Initialize Google Drive API client
def initialize_drive_service():
    credentials = service_account.Credentials.from_service_account_file(
        settings.SERVICE_ACCOUNT_KEY
    )
    return build('drive', 'v3', credentials=credentials)

def upload_file(request):
    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                # Save the file instance
                uploaded_file = form.save(commit=False)

                # Get the file name from the form
                file_name = request.POST.get('file_name')
                uploaded_file.file.name = f"{file_name}.{uploaded_file.file.name.split('.')[-1]}"

                # Save the file instance to the database
                uploaded_file.save()

                # Initialize Google Drive API client
                drive_service = initialize_drive_service()

                # Print the file path for upload
                print("File path for upload:", uploaded_file.file.path)

                # Prepare file metadata
                file_metadata = {
                    'name': uploaded_file.file.name,
                    'parents': ['1HVveRLTMwkPj0CahinfLSwi4wuO_9sTv']  # Replace with your folder ID
                }

                # Ensure the file exists before attempting to upload
                if not os.path.exists(uploaded_file.file.path):
                    raise FileNotFoundError(f"The file {uploaded_file.file.path} does not exist.")

                media = MediaFileUpload(uploaded_file.file.path)

                # Upload the file
                gfile = drive_service.files().create(body=file_metadata, media_body=media, fields='id').execute()

                # Print the uploaded file ID
                print("Uploaded file ID:", gfile['id'])

                # Save the Google Drive ID to the file instance
                uploaded_file.drive_id = gfile['id']
                uploaded_file.save()

                messages.success(request, 'File uploaded successfully!')
                return redirect('upload_file')
            except Exception as e:
                messages.error(request, f'Error uploading file: {str(e)}')
                print(f"Detailed error: {e}")  # Log the detailed error for debugging
    else:
        form = FileUploadForm()

    # Retrieve all uploaded files
    uploaded_files = UploadedFile.objects.all()

    return render(request, 'upload_file.html', {'form': form, 'uploaded_files': uploaded_files})

def delete_file(request, file_id):
    uploaded_file = get_object_or_404(UploadedFile, id=file_id)
    try:
        # Initialize Google Drive API client
        drive_service = initialize_drive_service()

        # Check if the file has a drive_id
        if uploaded_file.drive_id:
            # Print the file ID being deleted
            print("Attempting to delete file with ID:", uploaded_file.drive_id)

            # Delete the file from Google Drive
            drive_service.files().delete(fileId=uploaded_file.drive_id).execute()
        else:
            # If drive_id is missing, log a message
            print(f"No drive_id found for file with ID: {uploaded_file.id}")

        # Delete the file instance from the database
        uploaded_file.delete()

        messages.success(request, 'File deleted successfully!')
    except Exception as e:
        messages.error(request, f'Error deleting file: {str(e)}')
        print(f"Detailed error: {e}")  # Log the detailed error for debugging

    return redirect('upload_file')

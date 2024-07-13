from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status
from django.core.files.storage import default_storage
from myproject.settings import MEDIA_ROOT
from test import process_image_with_model  # Import the function from test.py
import os
class UploadImageView(APIView):
    # parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        try:
            file_obj = request.data['file']
            print(f"Received file: {file_obj.name}")  # Debug statement to print file name
            
            # Save the file to default storage (media directory)
            file_path = default_storage.save(file_obj.name, file_obj)
            print(f"File saved at: {file_path}")  # Debug statement to print file path
            
            # Process the image with your ML model
            full_file_path = os.path.join(MEDIA_ROOT, file_path)
            result = process_image_with_model(full_file_path)
            
            # Return the result
            return Response(result, status=status.HTTP_200_OK)
        except Exception as e:
            print(f"Error processing file upload: {e}")  # Print error for debugging
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
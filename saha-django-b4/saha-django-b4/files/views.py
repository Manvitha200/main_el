import os
from django.http import JsonResponse, HttpResponse
# from django.views.decorators.csrf import csrf_exempt
# from common.db_utils import get_db_connection
from pymongo import MongoClient
from gridfs import GridFS
from bson import ObjectId
from datetime import datetime

# MongoDB connection settings
MONGO_SETTINGS = {
    "host": "mongodb+srv://manaswiniks:vqii1tiSe638hpj3@saha.pop2i.mongodb.net/",
    "port": None,  # Port is not required for SRV URIs
    "database": "saha_file" # Specify your MongoDB database name here
}

# Helper to get MongoDB GridFS
def get_gridfs():
    client = MongoClient(MONGO_SETTINGS["host"], MONGO_SETTINGS["port"])
    db = client[MONGO_SETTINGS["database"]]
    fs=GridFS(db)
    return fs,db

# # Helper to check user access to a project in PostgreSQL
# def user_has_project_access(user_id, role, project_id):
#     conn = get_db_connection()
#     cursor = conn.cursor()
#     try:
#         if role == "Manager":
#             # Managers have access to their projects
#             cursor.execute(
#                 'SELECT 1 FROM "Project" WHERE project_id = %s AND manager_id = %s',
#                 (project_id, user_id),
#             )
#         else:
#             # Employees must be part of the project team
#             cursor.execute(
#                 'SELECT 1 FROM "Project_Team" WHERE project_id = %s AND user_id = %s',
#                 (project_id, user_id),
#             )
#         result = cursor.fetchone()
#         return bool(result)
#     finally:
#         cursor.close()
#         conn.close()

def get_gridfs():
    try:
        client = MongoClient(MONGO_SETTINGS["host"], MONGO_SETTINGS["port"])
        db = client[MONGO_SETTINGS["database"]]
        print(f"Connected to MongoDB database: {MONGO_SETTINGS['database']}")
        fs = GridFS(db)
        return fs, db
    except Exception as e:
        print(f"Error connecting to MongoDB: {e}")
        raise


def test_mongo_connection(request):
    try:
        fs, db = get_gridfs()
        # Test fetching any file from fs.files
        test_files = db['fs.files'].find_one()
        if test_files:
            return JsonResponse({"message": "MongoDB connection successful", "example_file": str(test_files)}, status=200)
        else:
            return JsonResponse({"message": "MongoDB connection successful, but no files found"}, status=200)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


def list_project_files(request):
    if request.method == 'GET':
        try:
            # Get user session
            user_id = request.session.get('user_id')
            role = request.session.get('role')
            project_id = request.session.get('project_id')

            if not project_id:
                return JsonResponse({'error': 'Project ID is required'}, status=400)

            print(f"User ID: {user_id}, Role: {role}, Queried Project ID: {project_id}")

            # Fetch files for the project
            fs, db = get_gridfs()

            # Fetch files matching the project ID
            files_cursor = db['fs.files'].find({'metadata.project_id': str(project_id)})

            # Convert cursor to a list to avoid exhaustion
            files_list = list(files_cursor)
            print(f"MongoDB query results: {files_list}")  # DEBUG: Check retrieved files

            # Format response
            file_list = [
                {
                    'file_id': str(file['_id']),
                    'filename': file['filename'],
                    'uploaded_by_user_id': file['metadata'].get('uploaded_by_user_id'),
                    'uploadDate': file['uploadDate'],
                }
                for file in files_list
            ]

            print(f"Formatted file list: {file_list}")  # DEBUG: Check formatted list

            # Return JSON response
            return JsonResponse({'files': file_list}, status=200)
        except Exception as e:
            print(f"Error in list_project_files: {e}")  # Log error
            return JsonResponse({'error': str(e)}, status=500)

# Upload a file to a specific project

def upload_project_file(request):
    if request.method == 'POST':
        try:
            user_id = request.session.get('user_id')
            role = request.session.get('role')
            session_project_id=request.session.get('project_id')
            # Get file from request
            uploaded_file = request.FILES['file']
            fs, db = get_gridfs()

            # Save file in MongoDB GridFS with metadata
            file_id = fs.put(
                uploaded_file,
                filename=uploaded_file.name,
                metadata={
                    "project_id": str(session_project_id),
                    "uploaded_by_user_id": user_id,
                },
            )   
            return JsonResponse({'message': 'File uploaded successfully', 'file_id': str(file_id)}, status=201)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

# Download a file for a specific project

def download_project_file(request,file_id):
    if request.method == 'GET':
        try:
            user_id = request.session.get('user_id')
            role = request.session.get('role')
            project_id=request.session.get('project_id')

            # Fetch file metadata
            fs, db = get_gridfs()
            file_metadata = db['fs.files'].find_one({'_id': ObjectId(file_id), 'metadata.project_id': str(project_id)})

            if not file_metadata:
                return JsonResponse({'error': 'File not found or access denied'}, status=404)

            # Stream file content
            file_data = fs.get(ObjectId(file_id))
            response = HttpResponse(file_data.read(), content_type=file_metadata['contentType'])
            response['Content-Disposition'] = f'attachment; filename="{file_metadata["filename"]}"'
            return response
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

# from django.shortcuts import render
# from django.http import JsonResponse, HttpResponse
# from pymongo import MongoClient
# import gridfs
# from bson import ObjectId  # Import ObjectId from bson module
# from psycopg2.extras import RealDictCursor

# # MongoDB connection
# client = MongoClient('mongodb+srv://manaswiniks:vqii1tiSe638hpj3@saha.pop2i.mongodb.net/')
# db = client['saha_file']  # Replace with your MongoDB database name
# fs = gridfs.GridFS(db)

# # Upload file functionality
# def upload_file(request):
#     if request.method == 'POST' and 'file' in request.FILES:
#         file = request.FILES['file']
#         project_id = request.POST.get("project_id")

#         # Check if Project ID is provided
#         if not project_id:
#             return JsonResponse({"error": "Project ID is required"}, status=400)

#         try:
#             # Save the file to GridFS
#             file_id = fs.put(
#                 file.read(),
#                 filename=file.name,
#                 content_type=file.content_type,
#                 metadata={
#                     "project_id": project_id,
#                     "uploaded_by_user_id": request.user.id,
#                 },
#             )
#             return JsonResponse({"message": "File uploaded successfully", "file_id": str(file_id)})

#         except Exception as e:
#             return JsonResponse({"error": str(e)}, status=500)

#     # Render the upload form on GET request
#     return render(request, 'files/upload_file.html')


# def download_file(request, file_id):
#     try:
#         # Convert string file_id to ObjectId
#         file_id = ObjectId(file_id)
        
#         # Fetch the file from GridFS
#         file_data = fs.get(file_id)
        
#         # Create a response with the file content
#         response = HttpResponse(file_data.read(), content_type=file_data.content_type)
#         response['Content-Disposition'] = f'attachment; filename={file_data.filename}'
        
#         return response
#     except Exception as e:
#         return HttpResponse(f"File not found: {str(e)}", status=404)

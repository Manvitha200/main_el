# MongoDB connection
from pymongo import MongoClient
import gridfs

client = MongoClient('mongodb+srv://manaswiniks:vqii1tiSe638hpj3@saha.pop2i.mongodb.net/')
db = client['saha_file']
fs = gridfs.GridFS(db)

# Fetch the file by its file_id
file_id = 'your_file_id_here'  # Replace this with the file ID you got after upload
file_data = fs.get(file_id)

# Example: Write the file content to disk
with open('downloaded_file.ext', 'wb') as f:
    f.write(file_data.read())

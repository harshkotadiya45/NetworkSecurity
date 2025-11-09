from pymongo import MongoClient
from pymongo.server_api import ServerApi
from urllib.parse import quote_plus

# Encode the password
username = "Harsh123"
password = "Harsh@2610"
encoded_password = quote_plus(password)

# Construct the URI
uri = f"mongodb+srv://{username}:{encoded_password}@cluster0.advttzc.mongodb.net/?appName=Cluster0"

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

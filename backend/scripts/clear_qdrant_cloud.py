from qdrant_client import QdrantClient

CLOUD_URL = "https://ea009ac6-4a47-47d7-9044-91b334d2a5d3.sa-east-1-0.aws.cloud.qdrant.io:6333"
CLOUD_API_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3MiOiJtIiwic3ViamVjdCI6ImFwaS1rZXk6NTNjNWQ1MzQtY2ZjZS00ZWRkLTg4NTYtMDUzNTZkODYzMDI1In0.o7h97FvZeWHmGSwaJH2qTK0dObx7j0mAKmLmmBUlyY0"

client = QdrantClient(url=CLOUD_URL, api_key=CLOUD_API_KEY)
client.delete_collection("sec_filings")
print("Cloud collection deleted.")
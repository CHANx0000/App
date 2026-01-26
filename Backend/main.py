from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Create a FastAPI instance
app = FastAPI()

# Configure CORS to allow Angular frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define a route (endpoint)
@app.get("/")
def read_root():
    return {"message": "Hello from FastAPI!"}


@app.get("/api/health")
def health_check():
    return {"status": "healthy", "message": "API is running"}
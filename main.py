from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import users, lancers

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

print("aaaaaa")
app.include_router(users.router, tags=["Users"])
app.include_router(lancers.router, tags=["Lancers"])

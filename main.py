from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import users, lancers
import os

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

# For Render deployment
if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)

# For Vercel deployment
handler = app

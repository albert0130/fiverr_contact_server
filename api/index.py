from main import app
from mangum import Mangum

# This is the entry point for Vercel
handler = Mangum(app)

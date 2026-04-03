"""
FastAPI Microservice Example for DIGIPIN

This script runs a complete high-performance geocoding server.
Run it with: uvicorn examples.fastapi_server:app --reload

Requirements:
    pip install digipinpy[fastapi]
"""

import uvicorn
from fastapi import FastAPI
from fastapi.responses import RedirectResponse

# Import the pre-built router
try:
    from digipin.fastapi_ext import router as digipin_router
except ImportError:
    print("FastAPI not installed. Run `pip install digipinpy[fastapi]`")
    exit(1)

app = FastAPI(
    title="DIGIPIN Microservice",
    description="High-performance geocoding API for India",
    version="1.3.0",
)

# Mount the router
app.include_router(digipin_router, prefix="/api/v1")


@app.get("/")
async def root():
    """Redirect to interactive docs."""
    return RedirectResponse(url="/docs")


if __name__ == "__main__":
    print("Starting DIGIPIN Server on http://127.0.0.1:8000")
    uvicorn.run(app, host="127.0.0.1", port=8000)

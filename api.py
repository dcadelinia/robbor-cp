from fastapi import FastAPI
import billing  # Import your new billing module

app = FastAPI(title="ManTAGU Spatial Telemetry Engine API")

# Register billing endpoint router layers
app.include_router(billing.router)

@app.get("/health")
def health_check():
    return {"status": "healthy"}

import mlflow
import os

def init_mlflow():
    # Store MLflow runs locally
    mlflow.set_tracking_uri("file:./mlruns")

    # Logical grouping of runs
    mlflow.set_experiment("ai_business_analyst")
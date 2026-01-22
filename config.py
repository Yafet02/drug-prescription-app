from pathlib import Path

# Project directory
PROJECT_DIR = Path(__file__).parent.absolute()

# Model path
MODEL_PATH = PROJECT_DIR / "model_saved"

# Data files
DATA_DIR = PROJECT_DIR

# CSV files
HISTORICAL_DATA_PATH = DATA_DIR / "Historical_Data_7_Aug_2024.csv"
MEDICINE_CSV_PATH = DATA_DIR / "medicine.csv"

# Image path
_LOCAL_IMAGE = PROJECT_DIR / "login_image.png"
IMAGE_PATH = _LOCAL_IMAGE if _LOCAL_IMAGE.exists() else None

# Medicine disease mapping
MEDICINE_DISEASE_MAP = {
    "Aspirin": "Fever",
    "Ibuprofen": "Headache",
    "Paracetamol": "Pain",
    "Amoxicillin": "Infection",
    "Cetirizine": "Allergy",
    "Loratadine": "Allergy",
    "Atorvastatin": "Cholesterol",
    "Metformin": "Diabetes",
    "Lisinopril": "Hypertension",
    "Omeprazole": "Acid Reflux",
    "Sertraline": "Depression"
}

def verify_files():
    """Verify all required files exist."""
    print(f"Project Directory: {PROJECT_DIR}")
    print(f"Model exists: {MODEL_PATH.exists()}")
    print(f"Image exists: {IMAGE_PATH is not None}")

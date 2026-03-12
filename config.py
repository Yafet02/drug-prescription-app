# config.py
from pathlib import Path

# Resolve to an absolute path to avoid any ambiguity
BASE_DIR = Path(__file__).parent.resolve()

# Database paths
DB_PATH_USERS = BASE_DIR / "users.db"
DB_PATH_MEDICINE = BASE_DIR / "Historical_Data_Medicine.db"

# Model & feature files
MODEL_PATH = BASE_DIR / "Model/best_rf_model.pkl"
FEATURES_PATH = BASE_DIR / "Model/feature_columns.pkl"

# Default session state values
SESSION_KEYS = {
    "authenticated": False,
    "user": "",
    "role": "",
    "login_error": "",
    "section": "General",
    "page": "Predict",
    "records_page": "View Records",
}
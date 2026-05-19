import os
from dotenv import load_dotenv

load_dotenv()

# Flask Config
FLASK_HOST = os.getenv("FLASK_HOST", "localhost")
FLASK_PORT = os.getenv("FLASK_PORT", 5000)
FLASK_DEBUG = os.getenv("FLASK_DEBUG", True)

# Streamlit Config
STREAMLIT_PORT = os.getenv("STREAMLIT_PORT", 8501)

# Model Config
MODEL_PATH = os.getenv("MODEL_PATH", "ml_model/plant_disease_model.h5")
MODEL_WEIGHT_PATH = os.getenv("MODEL_WEIGHT_PATH", "ml_model/model_weights.h5")

# API Keys
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY", "dummy_key")
MARKET_API_KEY = os.getenv("MARKET_API_KEY", "dummy_key")

# Paths
UPLOAD_FOLDER = os.getenv("UPLOAD_FOLDER", "uploads")
DATA_FOLDER = os.getenv("DATA_FOLDER", "data")

# Create folders if not exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(DATA_FOLDER, exist_ok=True)

# Disease Database
DISEASE_DB_PATH = os.path.join(DATA_FOLDER, "disease_data.json")

# Supported crops and diseases
SUPPORTED_CROPS = ["tomato", "potato", "wheat", "rice", "corn", "cotton"]
SUPPORTED_DISEASES = [
    "Tomato___Bacterial_spot",
    "Tomato___Early_blight",
    "Tomato___Late_blight",
    "Tomato___Leaf_Mold",
    "Tomato___Septoria_leaf_spot",
    "Potato___Early_blight",
    "Potato___Late_blight",
    "Wheat___Brown_rust",
    "Wheat___Yellow_rust",
    "Healthy"
]
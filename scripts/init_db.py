import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from run import app
from app.extensions import db
from app import models

with app.app_context():
    db.create_all()
    print("CyberSOC database tables created.")

import json
import os

def load_db():
    """Load database from db.json file"""
    db_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'db.json')
    with open(db_path, 'r') as f:
        return json.load(f)
    
def save_db(db):
    """Save database to db.json file"""
    db_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'db.json')
    with open(db_path, 'w') as f:
        json.dump(db, f, indent=4)

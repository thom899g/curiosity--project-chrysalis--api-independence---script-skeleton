"""
Initialize Firebase Firestore with required collections and security rules
"""
import json
import time
from firebase_admin import firestore, credentials, initialize_app
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def initialize_firestore_db():
    """Set up Firestore with required collections and initial documents"""
    try:
        # Initialize Firebase Admin
        cred = credentials.Certificate("firebase-credentials.json")
        app = initialize_app(cred)
        db = firestore.client()
        
        logger.info("Firebase Admin SDK initialized successfully")
        
        # Create collections with initial structure
        collections = [
            "chrysalis_queues/actions",
            "chrysalis_state/system",
            "chrysalis_memories/reflections",
            "chrysalis_circuits/breakers"
        ]
        
        for collection_path in collections:
            # Firestore doesn't require explicit collection creation
            # We'll create a dummy document to ensure collection exists
            parts = collection_path.split("/")
            collection_name = parts[0]
            subcollection = parts[1] if len(parts) > 1 else None
            
            if subcollection:
                # Create parent document with timestamp
                parent_doc_ref = db.collection(collection_name).document("system")
                parent_doc_ref.set({
                    "initialized_at": firestore.SERVER_TIMESTAMP,
                    "version": "1.0.0"
                })
                
                # Create subcollection document
                subcoll_ref = parent_doc_ref.collection(subcollection).document("init")
                subcoll_ref.set({
                    "created_at": firestore.SERVER_TIMESTAMP,
                    "status": "active"
                })
            else:
                # Create regular collection document
                doc_ref = db.collection(collection_name).document("system")
                doc_ref.set({
                    "initialized_at": firestore.SERVER_TIMESTAMP,
                    "version": "1.0.0"
                })
        
        logger.info("Firestore collections initialized successfully")
        
        # Initialize circuit breaker states
        circuits_ref = db.collection("chrysalis_circuits").document("main")
        circuits_ref.set({
            "status": "CLOSED",
            "failure_count": 0,
            "last_failure": None,
            "tripped_at": None,
            "created_at": firestore.SERVER_TIMESTAMP
        })
        
        # Initialize system state
        system_ref = db.collection("chrysalis_state").document("config")
        system_ref.set({
            "max_position_size": 100,
            "safety_enabled": True,
            "llm_provider": "anthropic",  # or "deepseek"
            "current_mode": "conservative",
            "updated_at": firestore.SERVER_TIMESTAMP
        })
        
        logger.info("Initial documents created successfully")
        
        # Create security rules document (for reference)
        security_rules = {
            "rules_version": "2",
            "rules": {
                "chrysalis_queues": {
                    "$queue": {
                        ".read": "auth != null",
                        ".write": "auth != null"
                    }
                },
                "chrysalis_state": {
                    ".read": "auth != null",
                    ".write": "auth != null"
                },
                "chrysalis_memories": {
                    ".read": "auth != null",
                    ".write": "auth != null"
                },
                "chrysalis_circuits": {
                    ".read": "auth != null",
                    ".write": "auth != null"
                }
            }
        }
        
        with open("firestore-security-rules.json", "w") as f:
            json.dump(security_rules, f, indent=2)
        
        logger.info("Security rules template saved to firestore-security-rules.json")
        logger.info("Initialization complete. Remember to deploy rules in Firebase Console.")
        
        return True
        
    except Exception as e:
        logger.error(f"Failed to initialize Firestore: {e}")
        return False


if __name__ == "__main__":
    success = initialize_firestore_db()
    if success:
        print("✅ Firestore initialization completed successfully")
    else:
        print("❌ Firestore initialization failed")
        exit(1)
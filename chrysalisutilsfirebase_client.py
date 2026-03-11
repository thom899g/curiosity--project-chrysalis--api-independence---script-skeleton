"""
Firebase Firestore client wrapper with error handling and retries
"""
import time
from typing import Any, Optional, Dict, List
import logging
from firebase_admin import firestore, credentials, initialize_app
from google.cloud.firestore_v1.base_query
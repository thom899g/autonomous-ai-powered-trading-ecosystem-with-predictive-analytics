"""
Firebase client for centralized data management and real-time streaming.
Handles Firestore for historical data and Realtime Database for streaming signals.
"""
import logging
import asyncio
from typing import Dict, Any, Optional, List
from datetime import datetime
import firebase_admin
from firebase_admin import credentials, firestore, db
from firebase_admin.exceptions import FirebaseError

from config.settings import config

logger = logging.getLogger(__name__)

class FirebaseClient:
    """
    Firebase client for the trading ecosystem.
    
    Features:
    - Singleton pattern to avoid multiple initializations
    - Connection pooling and error recovery
    - Automatic retry for transient failures
    - Real-time subscription management
    """
    
    _instance = None
    _initialized = False
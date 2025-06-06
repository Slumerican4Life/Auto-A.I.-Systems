#!/usr/bin/env python3
"""
Database Restore Script

This script restores the database for the Business Automation System from a backup.
It supports both Firebase and PostgreSQL databases.
"""

import os
import sys
import argparse
import logging
import subprocess
import json
import firebase_admin
from firebase_admin import credentials, firestore
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Base directory
BASE_DIR = Path(__file__).parent
BACKUP_DIR = BASE_DIR / 'backups'

def restore_firebase(backup_file):
    """Restore Firebase database from backup."""
    logger.info(f"Restoring Firebase database from {backup_file}")
    
    # Check if Firebase credentials are set
    firebase_creds = os.getenv('FIREBASE_SERVICE_ACCOUNT_PATH')
    firebase_project_id = os.getenv('FIREBASE_PROJECT_ID')
    firebase_private_key = os.getenv('FIREBASE_PRIVATE_KEY')
    firebase_client_email = os.getenv('FIREBASE_CLIENT_EMAIL')
    
    if not firebase_creds and not all([firebase_project_id, firebase_private_key, firebase_client_email]):
        logger.error("Firebase credentials not provided. Set FIREBASE_SERVICE_ACCOUNT_PATH or all of FIREBASE_PROJECT_ID, FIREBASE_PRIVATE_KEY, FIREBASE_CLIENT_EMAIL")
        sys.exit(1)
    
    try:
        # Initialize Firebase
        if not firebase_admin._apps:
            if firebase_creds:
                cred = credentials.Certificate(firebase_creds)
            else:
                service_account_info = {
                    "type": "service_account",
                    "project_id": firebase_project_id,
                    "private_key": firebase_private_key.replace("\\n", "\n"),
                    "client_email": firebase_client_email,
                    "token_uri": "https://oauth2.googleapis.com/token"
                }
                cred = credentials.Certificate(service_account_info)
            
            firebase_admin.initialize_app(cred)
        
        db = firestore.client()
        
        # Load backup data
        with open(backup_file, 'r') as f:
            backup_data = json.load(f)
        
        # Restore data
        batch_size = 500
        for collection_name, documents in backup_data.items():
            logger.info(f"Restoring collection {collection_name} with {len(documents)} documents")
            
            # Process in batches to avoid Firestore limits
            for i in range(0, len(documents), batch_size):
                batch = db.batch()
                batch_docs = documents[i:i+batch_size]
                
                for doc_data in batch_docs:
                    doc_id = doc_data.pop('id')
                    doc_ref = db.collection(collection_name).document(doc_id)
                    batch.set(doc_ref, doc_data)
                
                # Commit batch
                batch.commit()
                logger.info(f"Restored batch of {len(batch_docs)} documents to collection {collection_name}")
        
        logger.info("Firebase restore completed successfully")
    except Exception as e:
        logger.error(f"Error restoring Firebase database: {e}")
        sys.exit(1)

def restore_postgresql(backup_file):
    """Restore PostgreSQL database from backup."""
    logger.info(f"Restoring PostgreSQL database from {backup_file}")
    
    # Check if PostgreSQL credentials are set
    pg_user = os.getenv('POSTGRES_USER')
    pg_password = os.getenv('POSTGRES_PASSWORD')
    pg_host = os.getenv('POSTGRES_HOST')
    pg_port = os.getenv('POSTGRES_PORT')
    pg_db = os.getenv('POSTGRES_DB')
    
    if not all([pg_user, pg_password, pg_host, pg_port, pg_db]):
        logger.error("PostgreSQL credentials not provided. Set POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_HOST, POSTGRES_PORT, and POSTGRES_DB")
        sys.exit(1)
    
    try:
        # Set PGPASSWORD environment variable for psql
        env = os.environ.copy()
        env['PGPASSWORD'] = pg_password
        
        # Run psql to restore
        cmd = [
            'psql',
            '-h', pg_host,
            '-p', pg_port,
            '-U', pg_user,
            '-d', pg_db,
            '-f', str(backup_file)
        ]
        
        subprocess.run(cmd, env=env, check=True)
        
        logger.info("PostgreSQL restore completed successfully")
    except subprocess.CalledProcessError as e:
        logger.error(f"Error restoring PostgreSQL database: {e}")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Error restoring PostgreSQL database: {e}")
        sys.exit(1)

def main():
    """Main function."""
    parser = argparse.ArgumentParser(description='Restore the database for the Business Automation System')
    parser.add_argument('--db-type', choices=['firebase', 'postgresql'], required=True, help='Database type to restore')
    parser.add_argument('--backup-file', required=True, help='Path to backup file')
    
    args = parser.parse_args()
    
    # Check if backup file exists
    backup_file = Path(args.backup_file)
    if not backup_file.exists():
        logger.error(f"Backup file not found: {backup_file}")
        sys.exit(1)
    
    if args.db_type == 'firebase':
        restore_firebase(backup_file)
    elif args.db_type == 'postgresql':
        restore_postgresql(backup_file)
    else:
        logger.error(f"Unsupported database type: {args.db_type}")
        sys.exit(1)
    
    logger.info("Restore completed successfully")

if __name__ == '__main__':
    main()


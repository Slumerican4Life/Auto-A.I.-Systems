#!/usr/bin/env python3
"""
Database Backup Script

This script creates backups of the database for the Business Automation System.
It supports both Firebase and PostgreSQL databases.
"""

import os
import sys
import argparse
import logging
import subprocess
import json
import datetime
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

def ensure_backup_dir():
    """Ensure backup directory exists."""
    BACKUP_DIR.mkdir(exist_ok=True)
    logger.info(f"Using backup directory: {BACKUP_DIR}")

def backup_firebase():
    """Backup Firebase database."""
    logger.info("Backing up Firebase database")
    
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
        
        # Get all collections
        collections = db.collections()
        
        # Create timestamp for backup filename
        timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_file = BACKUP_DIR / f"firebase_backup_{timestamp}.json"
        
        # Backup data
        backup_data = {}
        for collection in collections:
            collection_name = collection.id
            backup_data[collection_name] = []
            
            # Get all documents in collection
            docs = collection.stream()
            for doc in docs:
                doc_data = doc.to_dict()
                doc_data['id'] = doc.id
                backup_data[collection_name].append(doc_data)
            
            logger.info(f"Backed up {len(backup_data[collection_name])} documents from collection {collection_name}")
        
        # Write backup to file
        with open(backup_file, 'w') as f:
            json.dump(backup_data, f, default=str, indent=2)
        
        logger.info(f"Firebase backup completed successfully: {backup_file}")
        return str(backup_file)
    except Exception as e:
        logger.error(f"Error backing up Firebase database: {e}")
        sys.exit(1)

def backup_postgresql():
    """Backup PostgreSQL database."""
    logger.info("Backing up PostgreSQL database")
    
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
        # Create timestamp for backup filename
        timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_file = BACKUP_DIR / f"postgresql_backup_{timestamp}.sql"
        
        # Set PGPASSWORD environment variable for pg_dump
        env = os.environ.copy()
        env['PGPASSWORD'] = pg_password
        
        # Run pg_dump
        cmd = [
            'pg_dump',
            '-h', pg_host,
            '-p', pg_port,
            '-U', pg_user,
            '-d', pg_db,
            '-f', str(backup_file),
            '--format=p',  # plain text format
            '--no-owner',
            '--no-acl'
        ]
        
        subprocess.run(cmd, env=env, check=True)
        
        logger.info(f"PostgreSQL backup completed successfully: {backup_file}")
        return str(backup_file)
    except subprocess.CalledProcessError as e:
        logger.error(f"Error backing up PostgreSQL database: {e}")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Error backing up PostgreSQL database: {e}")
        sys.exit(1)

def main():
    """Main function."""
    parser = argparse.ArgumentParser(description='Backup the database for the Business Automation System')
    parser.add_argument('--db-type', choices=['firebase', 'postgresql'], required=True, help='Database type to backup')
    
    args = parser.parse_args()
    
    # Ensure backup directory exists
    ensure_backup_dir()
    
    if args.db_type == 'firebase':
        backup_file = backup_firebase()
    elif args.db_type == 'postgresql':
        backup_file = backup_postgresql()
    else:
        logger.error(f"Unsupported database type: {args.db_type}")
        sys.exit(1)
    
    logger.info(f"Backup completed: {backup_file}")

if __name__ == '__main__':
    main()


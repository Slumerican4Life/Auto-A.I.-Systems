#!/usr/bin/env python3
"""
Database Setup Script

This script sets up the database for the Business Automation System.
It supports both Firebase and PostgreSQL databases.
"""

import os
import sys
import argparse
import logging
import subprocess
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Base directory
BASE_DIR = Path(__file__).parent

def setup_firebase():
    """Set up Firebase database."""
    logger.info("Setting up Firebase database")
    
    # Check if Firebase credentials are set
    firebase_creds = os.getenv('FIREBASE_SERVICE_ACCOUNT_PATH')
    firebase_project_id = os.getenv('FIREBASE_PROJECT_ID')
    firebase_private_key = os.getenv('FIREBASE_PRIVATE_KEY')
    firebase_client_email = os.getenv('FIREBASE_CLIENT_EMAIL')
    
    if not firebase_creds and not all([firebase_project_id, firebase_private_key, firebase_client_email]):
        logger.error("Firebase credentials not provided. Set FIREBASE_SERVICE_ACCOUNT_PATH or all of FIREBASE_PROJECT_ID, FIREBASE_PRIVATE_KEY, FIREBASE_CLIENT_EMAIL")
        sys.exit(1)
    
    # Run Firebase initialization script
    firebase_script = BASE_DIR / 'firebase' / 'init_firebase.py'
    try:
        subprocess.run(['python', str(firebase_script)], check=True)
        logger.info("Firebase database setup completed successfully")
    except subprocess.CalledProcessError as e:
        logger.error(f"Error setting up Firebase database: {e}")
        sys.exit(1)

def setup_postgresql():
    """Set up PostgreSQL database."""
    logger.info("Setting up PostgreSQL database")
    
    # Check if PostgreSQL credentials are set
    pg_user = os.getenv('POSTGRES_USER')
    pg_password = os.getenv('POSTGRES_PASSWORD')
    pg_host = os.getenv('POSTGRES_HOST')
    pg_port = os.getenv('POSTGRES_PORT')
    pg_db = os.getenv('POSTGRES_DB')
    
    if not all([pg_user, pg_password, pg_host, pg_port, pg_db]):
        logger.error("PostgreSQL credentials not provided. Set POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_HOST, POSTGRES_PORT, and POSTGRES_DB")
        sys.exit(1)
    
    # Run PostgreSQL migration script
    migration_script = BASE_DIR / 'postgresql' / 'run_migrations.py'
    try:
        subprocess.run(['python', str(migration_script)], check=True)
        logger.info("PostgreSQL database setup completed successfully")
    except subprocess.CalledProcessError as e:
        logger.error(f"Error setting up PostgreSQL database: {e}")
        sys.exit(1)

def main():
    """Main function."""
    parser = argparse.ArgumentParser(description='Set up the database for the Business Automation System')
    parser.add_argument('--db-type', choices=['firebase', 'postgresql'], required=True, help='Database type to set up')
    
    args = parser.parse_args()
    
    if args.db_type == 'firebase':
        setup_firebase()
    elif args.db_type == 'postgresql':
        setup_postgresql()
    else:
        logger.error(f"Unsupported database type: {args.db_type}")
        sys.exit(1)

if __name__ == '__main__':
    main()


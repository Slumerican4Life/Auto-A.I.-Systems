#!/usr/bin/env python3
"""
PostgreSQL Database Migration Script

This script runs the SQL migration files in the migrations directory in order.
It keeps track of which migrations have been run in a migrations table.
"""

import os
import sys
import asyncio
import asyncpg
import logging
from datetime import datetime
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Get database connection parameters from environment variables
DB_USER = os.getenv('POSTGRES_USER', 'postgres')
DB_PASSWORD = os.getenv('POSTGRES_PASSWORD', 'password')
DB_HOST = os.getenv('POSTGRES_HOST', 'localhost')
DB_PORT = os.getenv('POSTGRES_PORT', '5432')
DB_NAME = os.getenv('POSTGRES_DB', 'business_automation')

# Migrations directory
MIGRATIONS_DIR = Path(__file__).parent / 'migrations'

async def create_migrations_table(conn):
    """Create the migrations table if it doesn't exist."""
    await conn.execute('''
        CREATE TABLE IF NOT EXISTS migrations (
            id SERIAL PRIMARY KEY,
            name VARCHAR(255) NOT NULL UNIQUE,
            applied_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
        )
    ''')

async def get_applied_migrations(conn):
    """Get a list of migrations that have already been applied."""
    return [row['name'] for row in await conn.fetch('SELECT name FROM migrations ORDER BY id')]

async def apply_migration(conn, migration_file):
    """Apply a single migration file."""
    migration_path = MIGRATIONS_DIR / migration_file
    
    # Read migration file
    with open(migration_path, 'r') as f:
        migration_sql = f.read()
    
    # Start a transaction
    async with conn.transaction():
        # Apply migration
        logger.info(f"Applying migration: {migration_file}")
        await conn.execute(migration_sql)
        
        # Record migration
        await conn.execute(
            'INSERT INTO migrations (name) VALUES ($1)',
            migration_file
        )
    
    logger.info(f"Migration applied successfully: {migration_file}")

async def run_migrations():
    """Run all pending migrations."""
    # Connect to database
    try:
        conn = await asyncpg.connect(
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT,
            database=DB_NAME
        )
    except Exception as e:
        logger.error(f"Failed to connect to database: {e}")
        sys.exit(1)
    
    try:
        # Create migrations table
        await create_migrations_table(conn)
        
        # Get applied migrations
        applied_migrations = await get_applied_migrations(conn)
        logger.info(f"Found {len(applied_migrations)} previously applied migrations")
        
        # Get all migration files
        migration_files = sorted([f for f in os.listdir(MIGRATIONS_DIR) if f.endswith('.sql')])
        logger.info(f"Found {len(migration_files)} migration files")
        
        # Apply pending migrations
        pending_migrations = [f for f in migration_files if f not in applied_migrations]
        logger.info(f"Found {len(pending_migrations)} pending migrations")
        
        for migration_file in pending_migrations:
            await apply_migration(conn, migration_file)
        
        logger.info("All migrations applied successfully")
    except Exception as e:
        logger.error(f"Error running migrations: {e}")
        sys.exit(1)
    finally:
        await conn.close()

if __name__ == '__main__':
    logger.info("Starting database migrations")
    asyncio.run(run_migrations())
    logger.info("Database migrations completed")


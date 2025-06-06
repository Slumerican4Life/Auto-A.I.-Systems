#!/usr/bin/env python3
"""
Firebase Database Initialization Script

This script initializes the Firebase Firestore database with the required collections and documents.
It also sets up security rules and indexes.
"""

import os
import sys
import json
import logging
import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime, timezone
import uuid

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Get Firebase credentials from environment variables
FIREBASE_PROJECT_ID = os.getenv('FIREBASE_PROJECT_ID')
FIREBASE_PRIVATE_KEY = os.getenv('FIREBASE_PRIVATE_KEY')
FIREBASE_CLIENT_EMAIL = os.getenv('FIREBASE_CLIENT_EMAIL')
FIREBASE_SERVICE_ACCOUNT_PATH = os.getenv('FIREBASE_SERVICE_ACCOUNT_PATH')

def initialize_firebase():
    """Initialize Firebase Admin SDK."""
    try:
        # Check if already initialized
        if not firebase_admin._apps:
            # Initialize with service account
            if FIREBASE_SERVICE_ACCOUNT_PATH:
                cred = credentials.Certificate(FIREBASE_SERVICE_ACCOUNT_PATH)
            else:
                # Use environment variables
                if not all([FIREBASE_PROJECT_ID, FIREBASE_PRIVATE_KEY, FIREBASE_CLIENT_EMAIL]):
                    logger.error("Firebase credentials not provided. Set FIREBASE_SERVICE_ACCOUNT_PATH or all of FIREBASE_PROJECT_ID, FIREBASE_PRIVATE_KEY, FIREBASE_CLIENT_EMAIL")
                    sys.exit(1)
                
                service_account_info = {
                    "type": "service_account",
                    "project_id": FIREBASE_PROJECT_ID,
                    "private_key": FIREBASE_PRIVATE_KEY.replace("\\n", "\n"),
                    "client_email": FIREBASE_CLIENT_EMAIL,
                    "token_uri": "https://oauth2.googleapis.com/token"
                }
                cred = credentials.Certificate(service_account_info)
            
            firebase_admin.initialize_app(cred)
        
        db = firestore.client()
        logger.info("Firebase initialized successfully")
        return db
    except Exception as e:
        logger.error(f"Failed to initialize Firebase: {e}")
        sys.exit(1)

def create_demo_data(db):
    """Create demo data in Firestore."""
    try:
        # Generate IDs
        company_id = "company_" + str(uuid.uuid4())
        admin_id = "user_" + str(uuid.uuid4())
        user_id = "user_" + str(uuid.uuid4())
        
        # Create company
        company_ref = db.collection('companies').document(company_id)
        company_ref.set({
            'name': 'Demo Company',
            'industry': 'Technology',
            'website': 'https://demo-company.example.com',
            'created_at': firestore.SERVER_TIMESTAMP,
            'updated_at': firestore.SERVER_TIMESTAMP,
            'settings': {
                'timezone': 'America/New_York',
                'business_hours': {
                    'start': '09:00',
                    'end': '17:00'
                },
                'branding': {
                    'primary_color': '#4f46e5',
                    'secondary_color': '#10b981'
                }
            }
        })
        logger.info(f"Created demo company with ID: {company_id}")
        
        # Create admin user
        admin_ref = db.collection('users').document(admin_id)
        admin_ref.set({
            'email': 'admin@demo-company.example.com',
            'name': 'Admin User',
            'role': 'admin',
            'company_id': company_id,
            'created_at': firestore.SERVER_TIMESTAMP,
            'updated_at': firestore.SERVER_TIMESTAMP,
            'settings': {
                'notifications': True,
                'theme': 'light'
            }
        })
        logger.info(f"Created admin user with ID: {admin_id}")
        
        # Create regular user
        user_ref = db.collection('users').document(user_id)
        user_ref.set({
            'email': 'user@demo-company.example.com',
            'name': 'Regular User',
            'role': 'user',
            'company_id': company_id,
            'created_at': firestore.SERVER_TIMESTAMP,
            'updated_at': firestore.SERVER_TIMESTAMP,
            'settings': {
                'notifications': True,
                'theme': 'light'
            }
        })
        logger.info(f"Created regular user with ID: {user_id}")
        
        # Create leads
        leads = [
            {
                'name': 'John Doe',
                'email': 'john.doe@example.com',
                'phone': '+1-555-123-4567',
                'source': 'website_form',
                'status': 'new',
                'notes': 'Interested in our services',
                'tags': ['website', 'new_lead'],
                'company_id': company_id,
                'assigned_to': admin_id,
                'created_at': firestore.SERVER_TIMESTAMP,
                'updated_at': firestore.SERVER_TIMESTAMP,
                'custom_fields': {}
            },
            {
                'name': 'Jane Smith',
                'email': 'jane.smith@example.com',
                'phone': '+1-555-987-6543',
                'source': 'referral',
                'status': 'contacted',
                'notes': 'Referred by existing customer',
                'tags': ['referral', 'high_priority'],
                'company_id': company_id,
                'assigned_to': user_id,
                'created_at': firestore.SERVER_TIMESTAMP,
                'updated_at': firestore.SERVER_TIMESTAMP,
                'custom_fields': {}
            },
            {
                'name': 'Bob Johnson',
                'email': 'bob.johnson@example.com',
                'phone': '+1-555-456-7890',
                'source': 'google_ads',
                'status': 'qualified',
                'notes': 'Looking for enterprise solution',
                'tags': ['google_ads', 'enterprise'],
                'company_id': company_id,
                'assigned_to': admin_id,
                'created_at': firestore.SERVER_TIMESTAMP,
                'updated_at': firestore.SERVER_TIMESTAMP,
                'custom_fields': {}
            }
        ]
        
        lead_refs = []
        for lead in leads:
            lead_id = "lead_" + str(uuid.uuid4())
            lead_ref = db.collection('leads').document(lead_id)
            lead_ref.set(lead)
            lead_refs.append((lead_id, lead))
            logger.info(f"Created lead with ID: {lead_id}")
        
        # Create workflow configs
        workflow_configs = [
            {
                'company_id': company_id,
                'workflow_type': 'lead_nurturing',
                'name': 'Website Lead Follow-up',
                'active': True,
                'triggers': {
                    'lead_source': ['website_form', 'landing_page']
                },
                'actions': {
                    'initial_delay_minutes': 5,
                    'channel': 'email',
                    'message_template': 'welcome_template',
                    'follow_up': [
                        {
                            'delay_hours': 24,
                            'message_template': 'follow_up_1'
                        },
                        {
                            'delay_hours': 72,
                            'message_template': 'follow_up_2'
                        }
                    ]
                },
                'templates': {
                    'welcome_template': 'Hi {{name}},\n\nThank you for your interest in our services. How can we help you today?\n\nBest regards,\nDemo Company',
                    'follow_up_1': 'Hi {{name}},\n\nJust following up on your recent inquiry. Do you have any questions I can answer?\n\nBest regards,\nDemo Company',
                    'follow_up_2': 'Hi {{name}},\n\nI wanted to check in one more time to see if you have any questions about our services.\n\nBest regards,\nDemo Company'
                },
                'created_at': firestore.SERVER_TIMESTAMP,
                'updated_at': firestore.SERVER_TIMESTAMP,
                'created_by': admin_id
            },
            {
                'company_id': company_id,
                'workflow_type': 'review_referral',
                'name': 'Post-Sale Review Request',
                'active': True,
                'triggers': {
                    'sale_status': ['completed']
                },
                'actions': {
                    'initial_delay_hours': 48,
                    'review_platforms': ['google', 'yelp'],
                    'referral_offer': {
                        'type': 'discount',
                        'value': 50,
                        'description': '50% off first month'
                    }
                },
                'templates': {
                    'review_request': 'Hi {{name}},\n\nThank you for your recent purchase! We hope you're enjoying our product/service. Would you mind taking a moment to leave us a review?\n\nBest regards,\nDemo Company',
                    'referral_offer': 'Hi {{name}},\n\nThank you for your review! As a token of our appreciation, we'd like to offer you a referral code to share with friends and family. They'll get 50% off their first month, and you'll receive a $25 credit when they sign up.\n\nYour referral code: {{code}}\n\nBest regards,\nDemo Company'
                },
                'created_at': firestore.SERVER_TIMESTAMP,
                'updated_at': firestore.SERVER_TIMESTAMP,
                'created_by': admin_id
            },
            {
                'company_id': company_id,
                'workflow_type': 'content_generation',
                'name': 'Weekly Blog Post',
                'active': True,
                'triggers': {
                    'schedule': '0 9 * * 1'
                },
                'actions': {
                    'content_type': 'blog',
                    'topics': ['industry_news', 'tips_and_tricks', 'case_studies'],
                    'word_count': 1000,
                    'publish': True,
                    'platforms': ['wordpress']
                },
                'templates': {
                    'blog_template': '# {{title}}\n\n{{content}}\n\n## Conclusion\n\nThank you for reading our blog post. If you have any questions, please contact us.'
                },
                'created_at': firestore.SERVER_TIMESTAMP,
                'updated_at': firestore.SERVER_TIMESTAMP,
                'created_by': admin_id
            }
        ]
        
        for config in workflow_configs:
            config_id = "wf_" + str(uuid.uuid4())
            config_ref = db.collection('workflow_configs').document(config_id)
            config_ref.set(config)
            logger.info(f"Created workflow config with ID: {config_id}")
        
        logger.info("Demo data created successfully")
    except Exception as e:
        logger.error(f"Error creating demo data: {e}")
        sys.exit(1)

def main():
    """Main function."""
    logger.info("Starting Firebase initialization")
    
    # Initialize Firebase
    db = initialize_firebase()
    
    # Create demo data
    create_demo_data(db)
    
    logger.info("Firebase initialization completed")

if __name__ == '__main__':
    main()


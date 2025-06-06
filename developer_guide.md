# Business Automation System Developer Guide

## Introduction

This developer guide provides comprehensive documentation for developers working with the Business Automation System. Whether you're maintaining the existing codebase, extending functionality, or integrating with other systems, this guide will help you understand the system architecture, components, and development practices.

The Business Automation System is built with a modular architecture that allows for easy extension and customization. The system consists of three main components:

1. **Backend API**: A FastAPI application that provides RESTful endpoints for all system functionality
2. **Frontend Dashboard**: A React application with TailwindCSS that provides the user interface
3. **Database**: Support for both PostgreSQL and Firebase Firestore

## Table of Contents

1. [System Architecture](#system-architecture)
   - [Overview](#architecture-overview)
   - [Component Diagram](#component-diagram)
   - [Data Flow](#data-flow)

2. [Backend Development](#backend-development)
   - [Project Structure](#backend-project-structure)
   - [Core Components](#backend-core-components)
   - [API Endpoints](#api-endpoints)
   - [Workflow Implementation](#workflow-implementation)
   - [Database Access](#database-access)
   - [Authentication and Authorization](#authentication-and-authorization)
   - [Background Tasks](#background-tasks)

3. [Frontend Development](#frontend-development)
   - [Project Structure](#frontend-project-structure)
   - [Component Hierarchy](#component-hierarchy)
   - [State Management](#state-management)
   - [API Integration](#api-integration)
   - [Styling and Theming](#styling-and-theming)
   - [Responsive Design](#responsive-design)

4. [Database](#database)
   - [Schema Design](#schema-design)
   - [PostgreSQL Implementation](#postgresql-implementation)
   - [Firebase Implementation](#firebase-implementation)
   - [Migration Strategy](#migration-strategy)

5. [AI Integration](#ai-integration)
   - [OpenAI API Usage](#openai-api-usage)
   - [Prompt Engineering](#prompt-engineering)
   - [Response Processing](#response-processing)
   - [Error Handling](#ai-error-handling)

6. [External Integrations](#external-integrations)
   - [Email Services](#email-services)
   - [SMS Services](#sms-services)
   - [CRM Integration](#crm-integration)
   - [Social Media Integration](#social-media-integration)
   - [Content Management Systems](#content-management-systems)

7. [Testing](#testing)
   - [Unit Testing](#unit-testing)
   - [Integration Testing](#integration-testing)
   - [End-to-End Testing](#end-to-end-testing)
   - [Performance Testing](#performance-testing)

8. [Deployment](#deployment)
   - [Docker Deployment](#docker-deployment)
   - [Cloud Deployment](#cloud-deployment)
   - [CI/CD Pipeline](#cicd-pipeline)

9. [Extending the System](#extending-the-system)
   - [Adding New Workflows](#adding-new-workflows)
   - [Creating Custom Integrations](#creating-custom-integrations)
   - [Implementing New Features](#implementing-new-features)

10. [API Reference](#api-reference)
    - [Authentication](#api-authentication)
    - [Lead Nurturing API](#lead-nurturing-api)
    - [Review & Referral API](#review--referral-api)
    - [Content Generation API](#content-generation-api)
    - [User Management API](#user-management-api)
    - [System API](#system-api)

## System Architecture

### Architecture Overview

The Business Automation System follows a modern, microservices-inspired architecture with clear separation of concerns:

- **Presentation Layer**: React frontend with TailwindCSS
- **Application Layer**: FastAPI backend with business logic
- **Data Layer**: PostgreSQL or Firebase Firestore
- **Integration Layer**: External service connectors (OpenAI, SendGrid, Twilio, etc.)

The system is designed to be:

- **Scalable**: Components can be scaled independently
- **Maintainable**: Clear separation of concerns and modular design
- **Extensible**: Easy to add new workflows and integrations
- **Secure**: Authentication, authorization, and data protection

### Component Diagram

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│                 │     │                 │     │                 │
│  React Frontend │────▶│  FastAPI Backend│────▶│    Database     │
│                 │◀────│                 │◀────│                 │
└─────────────────┘     └─────────────────┘     └─────────────────┘
                               │  ▲
                               │  │
                               ▼  │
                        ┌─────────────────┐
                        │                 │
                        │External Services│
                        │                 │
                        └─────────────────┘
```

### Data Flow

1. **User Interaction Flow**:
   - User interacts with the React frontend
   - Frontend makes API calls to the backend
   - Backend processes the request and interacts with the database
   - Backend returns response to the frontend
   - Frontend updates the UI

2. **Automated Workflow Flow**:
   - Trigger event occurs (e.g., new lead, completed sale)
   - Backend creates a workflow run
   - Background task processes the workflow
   - External services are called as needed (AI, email, SMS)
   - Results are stored in the database
   - Dashboard is updated with new data

## Backend Development

### Backend Project Structure

The backend is organized into the following directory structure:

```
backend/
├── api/                  # API routes
│   ├── lead_nurturing.py
│   ├── review_referral.py
│   ├── content_generation.py
│   └── ...
├── core/                 # Core functionality
│   ├── config.py         # Configuration
│   ├── security.py       # Authentication and authorization
│   ├── database.py       # Database abstraction
│   └── celery_app.py     # Background task queue
├── services/             # Service integrations
│   ├── ai/               # AI service
│   ├── email/            # Email service
│   ├── sms/              # SMS service
│   └── ...
├── workflows/            # Workflow implementations
│   ├── lead_nurturing/
│   ├── review_referral/
│   ├── content_generation/
│   └── ...
├── tests/                # Test cases
├── main.py               # Application entry point
└── requirements.txt      # Dependencies
```

### Backend Core Components

#### Configuration (core/config.py)

The configuration module handles environment variables and settings:

```python
from pydantic import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str = "Business Automation System"
    API_V1_STR: str = "/api"
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    DATABASE_URL: str
    OPENAI_API_KEY: str
    # Other settings...
    
    class Config:
        env_file = ".env"

settings = Settings()
```

#### Security (core/security.py)

The security module handles authentication and authorization:

```python
from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from core.config import settings

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

async def get_current_user(token: str = Depends(oauth2_scheme)):
    # Implementation...
```

#### Database (core/database.py)

The database module provides a unified interface for both PostgreSQL and Firebase:

```python
import os
from typing import List, Dict, Any, Optional
from databases import Database
import firebase_admin
from firebase_admin import credentials, firestore

from core.config import settings

class DatabaseClient:
    def __init__(self):
        self.db_type = os.getenv("DATABASE_TYPE", "postgres")
        
        if self.db_type == "postgres":
            self.db = Database(settings.DATABASE_URL)
        elif self.db_type == "firebase":
            cred = credentials.Certificate({
                "type": "service_account",
                "project_id": settings.FIREBASE_PROJECT_ID,
                "private_key": settings.FIREBASE_PRIVATE_KEY.replace("\\n", "\n"),
                "client_email": settings.FIREBASE_CLIENT_EMAIL
            })
            firebase_admin.initialize_app(cred)
            self.db = firestore.client()
    
    async def get_document(self, collection: str, doc_id: str) -> Optional[Dict[str, Any]]:
        # Implementation...
    
    async def query_collection(self, collection: str, filters: List[Dict[str, Any]] = None, 
                              order_by: str = None, limit: int = None) -> List[Dict[str, Any]]:
        # Implementation...
    
    async def create_document(self, collection: str, data: Dict[str, Any]) -> Dict[str, Any]:
        # Implementation...
    
    async def update_document(self, collection: str, doc_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        # Implementation...
    
    async def delete_document(self, collection: str, doc_id: str) -> bool:
        # Implementation...

# Create a global database client
db = DatabaseClient()
```

### API Endpoints

The API endpoints are organized by workflow and functionality:

#### Lead Nurturing API (api/lead_nurturing.py)

```python
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from typing import Dict, Any, List

from core.security import get_current_user
from workflows.lead_nurturing.service import lead_nurturing_service

router = APIRouter(
    prefix="/api/lead-nurturing",
    tags=["lead-nurturing"],
    responses={404: {"description": "Not found"}},
)

@router.post("/leads")
async def create_lead(
    lead_data: Dict[str, Any],
    background_tasks: BackgroundTasks,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    # Implementation...

@router.get("/leads")
async def get_leads(
    status: str = None,
    source: str = None,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    # Implementation...

# Other endpoints...
```

### Workflow Implementation

Each workflow is implemented as a service with models, repository, and business logic:

#### Lead Nurturing Service (workflows/lead_nurturing/service.py)

```python
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional

from core.database import db
from services.ai.openai_service import OpenAIService
from services.email.email_service import EmailService
from services.sms.sms_service import SMSService

class LeadNurturingService:
    def __init__(self):
        self.ai_service = OpenAIService()
        self.email_service = EmailService()
        self.sms_service = SMSService()
    
    async def process_new_lead(self, lead_id: str) -> Dict[str, Any]:
        # Implementation...
    
    async def process_follow_up(self, lead_id: str, follow_up_index: int, workflow_run_id: str) -> Dict[str, Any]:
        # Implementation...
    
    async def process_lead_reply(self, interaction_id: str) -> Dict[str, Any]:
        # Implementation...

# Create service instance
lead_nurturing_service = LeadNurturingService()
```

### Database Access

Database access is handled through the database abstraction layer:

```python
# Get a document
lead = await db.get_document('leads', lead_id)

# Query a collection
active_workflows = await db.query_collection(
    'workflow_configs',
    filters=[
        {'field': 'company_id', 'op': '==', 'value': company_id},
        {'field': 'workflow_type', 'op': '==', 'value': 'lead_nurturing'},
        {'field': 'active', 'op': '==', 'value': True}
    ]
)

# Create a document
workflow_run = await db.create_document('workflow_runs', {
    'company_id': company_id,
    'workflow_config_id': workflow_config['id'],
    'status': 'running',
    'started_at': datetime.now(),
    'trigger_type': 'new_lead',
    'trigger_id': lead_id,
    'actions_performed': [],
    'results': {}
})

# Update a document
await db.update_document('leads', lead_id, {
    'status': 'contacted',
    'updated_at': datetime.now()
})
```

### Authentication and Authorization

Authentication is implemented using JWT tokens:

```python
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

@app.post("/token")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = create_access_token(
        data={"sub": user["username"]}
    )
    
    return {"access_token": access_token, "token_type": "bearer"}
```

### Background Tasks

Background tasks are implemented using Celery:

```python
from celery import Celery
from core.config import settings

celery_app = Celery(
    "worker",
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND
)

celery_app.conf.task_routes = {
    "workflows.lead_nurturing.tasks.*": {"queue": "lead_nurturing"},
    "workflows.review_referral.tasks.*": {"queue": "review_referral"},
    "workflows.content_generation.tasks.*": {"queue": "content_generation"},
}
```

## Frontend Development

### Frontend Project Structure

The frontend is organized into the following directory structure:

```
frontend/
├── public/              # Static assets
├── src/
│   ├── components/      # React components
│   │   ├── auth/        # Authentication components
│   │   ├── dashboard/   # Dashboard components
│   │   ├── layout/      # Layout components
│   │   ├── ui/          # UI components
│   │   └── ...
│   ├── context/         # React context providers
│   ├── hooks/           # Custom React hooks
│   ├── pages/           # Page components
│   │   ├── auth/        # Authentication pages
│   │   ├── dashboard/   # Dashboard pages
│   │   ├── lead-nurturing/ # Lead nurturing pages
│   │   └── ...
│   ├── services/        # API services
│   ├── utils/           # Utility functions
│   ├── App.jsx          # Main application component
│   └── main.jsx         # Application entry point
├── .env                 # Environment variables
├── index.html           # HTML template
├── package.json         # Dependencies
├── tailwind.config.js   # Tailwind CSS configuration
└── vite.config.js       # Vite configuration
```

### Component Hierarchy

The frontend follows a component-based architecture:

```
App
├── AuthProvider
│   └── Router
│       ├── MainLayout
│       │   ├── Sidebar
│       │   ├── Header
│       │   └── Content
│       │       ├── DashboardPage
│       │       ├── LeadNurturingPage
│       │       ├── ReviewReferralPage
│       │       └── ContentGenerationPage
│       └── AuthLayout
│           ├── LoginPage
│           └── RegisterPage
```

### State Management

State management is implemented using React Context:

```jsx
// src/context/AuthContext.jsx
import React, { createContext, useState, useEffect, useContext } from 'react';
import api from '../services/api';

const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  
  useEffect(() => {
    // Check if user is logged in
    const checkAuth = async () => {
      try {
        const token = localStorage.getItem('token');
        if (token) {
          const response = await api.get('/users/me');
          setUser(response.data);
        }
      } catch (error) {
        localStorage.removeItem('token');
      } finally {
        setLoading(false);
      }
    };
    
    checkAuth();
  }, []);
  
  const login = async (username, password) => {
    // Implementation...
  };
  
  const logout = () => {
    // Implementation...
  };
  
  return (
    <AuthContext.Provider value={{ user, loading, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => useContext(AuthContext);
```

### API Integration

API integration is implemented using Axios:

```jsx
// src/services/api.js
import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add request interceptor for authentication
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// Add response interceptor for error handling
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response && error.response.status === 401) {
      // Handle unauthorized error
      localStorage.removeItem('token');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

export default api;
```

### Styling and Theming

Styling is implemented using TailwindCSS with a custom theme:

```js
// tailwind.config.js
module.exports = {
  content: [
    "./index.html",
    "./src/**/*.{js,jsx,ts,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: {
          50: '#f0f9ff',
          100: '#e0f2fe',
          200: '#bae6fd',
          300: '#7dd3fc',
          400: '#38bdf8',
          500: '#0ea5e9',
          600: '#0284c7',
          700: '#0369a1',
          800: '#075985',
          900: '#0c4a6e',
        },
        // Other colors...
      },
      fontFamily: {
        sans: ['Inter', 'sans-serif'],
      },
    },
  },
  plugins: [
    require('@tailwindcss/forms'),
  ],
}
```

### Responsive Design

The frontend is designed to be responsive using Tailwind's responsive utilities:

```jsx
// src/components/layout/MainLayout.jsx
import React, { useState } from 'react';
import { useMediaQuery } from '../../hooks/use-media-query';

export const MainLayout = ({ children }) => {
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const isDesktop = useMediaQuery('(min-width: 1024px)');
  
  return (
    <div className="flex h-screen bg-gray-100">
      {/* Sidebar for mobile */}
      {!isDesktop && (
        <div
          className={`fixed inset-0 z-40 bg-black bg-opacity-50 transition-opacity ${
            sidebarOpen ? 'opacity-100' : 'opacity-0 pointer-events-none'
          }`}
          onClick={() => setSidebarOpen(false)}
        />
      )}
      
      {/* Sidebar */}
      <div
        className={`fixed inset-y-0 left-0 z-50 w-64 bg-white shadow-lg transform transition-transform ${
          sidebarOpen || isDesktop ? 'translate-x-0' : '-translate-x-full'
        } ${isDesktop ? 'relative' : 'absolute'}`}
      >
        {/* Sidebar content */}
      </div>
      
      {/* Main content */}
      <div className="flex-1 flex flex-col overflow-hidden">
        {/* Header */}
        <header className="bg-white shadow-sm z-10">
          {/* Header content */}
        </header>
        
        {/* Content */}
        <main className="flex-1 overflow-auto p-4 md:p-6">
          {children}
        </main>
      </div>
    </div>
  );
};
```

## Database

### Schema Design

The database schema is designed to support all system workflows:

#### Users

```
users
├── id: string (primary key)
├── username: string
├── email: string
├── hashed_password: string
├── full_name: string
├── company_id: string (foreign key)
├── role: string (admin, manager, user)
├── is_active: boolean
├── created_at: timestamp
└── updated_at: timestamp
```

#### Companies

```
companies
├── id: string (primary key)
├── name: string
├── industry: string
├── website: string
├── settings: json
├── created_at: timestamp
└── updated_at: timestamp
```

#### Leads

```
leads
├── id: string (primary key)
├── company_id: string (foreign key)
├── name: string
├── email: string
├── phone: string
├── source: string
├── status: string
├── notes: string
├── created_at: timestamp
└── updated_at: timestamp
```

#### Interactions

```
interactions
├── id: string (primary key)
├── company_id: string (foreign key)
├── lead_id: string (foreign key)
├── type: string (email, sms)
├── direction: string (inbound, outbound)
├── content: string
├── channel: string
├── status: string
├── created_at: timestamp
├── metadata: json
```

#### Workflow Configs

```
workflow_configs
├── id: string (primary key)
├── company_id: string (foreign key)
├── workflow_type: string
├── active: boolean
├── actions: json
├── settings: json
├── templates: json
├── triggers: json
├── created_at: timestamp
└── updated_at: timestamp
```

#### Workflow Runs

```
workflow_runs
├── id: string (primary key)
├── company_id: string (foreign key)
├── workflow_config_id: string (foreign key)
├── status: string
├── started_at: timestamp
├── completed_at: timestamp
├── trigger_type: string
├── trigger_id: string
├── actions_performed: json
└── results: json
```

### PostgreSQL Implementation

The PostgreSQL implementation uses SQL migrations:

```sql
-- Initial Schema Migration
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    username VARCHAR(255) NOT NULL UNIQUE,
    email VARCHAR(255) NOT NULL UNIQUE,
    hashed_password VARCHAR(255) NOT NULL,
    full_name VARCHAR(255),
    company_id UUID REFERENCES companies(id),
    role VARCHAR(50) NOT NULL DEFAULT 'user',
    is_active BOOLEAN NOT NULL DEFAULT true,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Other tables...
```

### Firebase Implementation

The Firebase implementation uses Firestore collections:

```javascript
// Firebase schema initialization
const collections = [
  {
    name: 'users',
    indexes: [
      { field: 'email', type: 'ASC' },
      { field: 'company_id', type: 'ASC' }
    ]
  },
  // Other collections...
];

async function initializeFirebase() {
  const db = firestore.client();
  
  for (const collection of collections) {
    // Create collection if it doesn't exist
    const collectionRef = db.collection(collection.name);
    
    // Create indexes
    for (const index of collection.indexes) {
      // Firebase indexes are created in the Firebase console
      console.log(`Create index on ${collection.name}.${index.field}`);
    }
  }
}
```

### Migration Strategy

The system supports migrating between database types:

```python
async def migrate_data(source_type, target_type):
    """Migrate data from one database type to another."""
    # Implementation...
```

## AI Integration

### OpenAI API Usage

The system integrates with the OpenAI API for AI-powered workflows:

```python
import openai
from core.config import settings

class OpenAIService:
    def __init__(self):
        openai.api_key = settings.OPENAI_API_KEY
    
    async def generate_text(self, prompt: str, max_tokens: int = 1000) -> str:
        """Generate text using OpenAI API."""
        try:
            response = await openai.ChatCompletion.acreate(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=max_tokens,
                temperature=0.7
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            logger.error(f"Error generating text with OpenAI: {e}")
            return ""
```

### Prompt Engineering

The system uses carefully crafted prompts for each workflow:

```python
# Lead Nurturing Prompts
INITIAL_CONTACT_PROMPT = """
You are an AI assistant helping to craft a personalized initial contact message to a potential lead.

Business Information:
- Business Name: {business_name}
- Industry: {industry}
- Products/Services: {products_services}
- Value Proposition: {value_proposition}

Lead Information:
- Name: {lead_name}
- Source: {lead_source}
- Interest: {lead_interest}

Guidelines:
- Be friendly and professional
- Briefly introduce the business
- Reference how the lead found the business
- Address their specific interest
- Include a clear call to action
- Keep the message concise (100-150 words)
- Use a {tone} tone

Please write a personalized initial contact message:
"""

# Other prompts...
```

### Response Processing

AI responses are processed and formatted before use:

```python
async def process_ai_response(response: str, template_variables: Dict[str, str]) -> str:
    """Process and format AI response."""
    # Replace template variables
    for key, value in template_variables.items():
        response = response.replace(f"{{{{{key}}}}}", value)
    
    # Clean up formatting
    response = response.strip()
    
    return response
```

### AI Error Handling

The system includes robust error handling for AI services:

```python
async def generate_text_with_fallback(prompt: str, fallback_template: str, variables: Dict[str, str]) -> str:
    """Generate text with fallback to template if AI fails."""
    try:
        response = await ai_service.generate_text(prompt)
        if not response:
            raise ValueError("Empty response from AI service")
        return await process_ai_response(response, variables)
    except Exception as e:
        logger.error(f"Error generating text with AI: {e}")
        # Fall back to template
        return await process_ai_response(fallback_template, variables)
```

## External Integrations

### Email Services

The system integrates with email services like SendGrid and Gmail:

```python
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from core.config import settings

class EmailService:
    def __init__(self):
        self.service_type = settings.EMAIL_SERVICE
        
        if self.service_type == "sendgrid":
            self.client = SendGridAPIClient(settings.SENDGRID_API_KEY)
        elif self.service_type == "gmail":
            # Gmail setup
            pass
    
    async def send_email(self, to_email: str, subject: str, content: str, from_email: str = None) -> Dict[str, Any]:
        """Send an email."""
        try:
            if self.service_type == "sendgrid":
                message = Mail(
                    from_email=from_email or settings.DEFAULT_FROM_EMAIL,
                    to_emails=to_email,
                    subject=subject,
                    html_content=content
                )
                response = self.client.send(message)
                return {
                    "success": True,
                    "status_code": response.status_code,
                    "message": "Email sent successfully"
                }
            elif self.service_type == "gmail":
                # Gmail implementation
                pass
        except Exception as e:
            logger.error(f"Error sending email: {e}")
            return {
                "success": False,
                "message": str(e)
            }
```

### SMS Services

The system integrates with SMS services like Twilio:

```python
from twilio.rest import Client
from core.config import settings

class SMSService:
    def __init__(self):
        self.client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
        self.from_number = settings.TWILIO_PHONE_NUMBER
    
    async def send_sms(self, to_number: str, message: str) -> Dict[str, Any]:
        """Send an SMS."""
        try:
            message = self.client.messages.create(
                body=message,
                from_=self.from_number,
                to=to_number
            )
            return {
                "success": True,
                "message_id": message.sid,
                "message": "SMS sent successfully"
            }
        except Exception as e:
            logger.error(f"Error sending SMS: {e}")
            return {
                "success": False,
                "message": str(e)
            }
```

### CRM Integration

The system integrates with CRM systems:

```python
class CRMService:
    def __init__(self, crm_type: str, config: Dict[str, Any]):
        self.crm_type = crm_type
        self.config = config
        
        if crm_type == "hubspot":
            # HubSpot setup
            pass
        elif crm_type == "salesforce":
            # Salesforce setup
            pass
    
    async def sync_lead(self, lead: Dict[str, Any]) -> Dict[str, Any]:
        """Sync a lead with the CRM."""
        # Implementation...
    
    async def sync_interaction(self, interaction: Dict[str, Any]) -> Dict[str, Any]:
        """Sync an interaction with the CRM."""
        # Implementation...
```

### Social Media Integration

The system integrates with social media platforms:

```python
class SocialMediaService:
    def __init__(self, platform: str, config: Dict[str, Any]):
        self.platform = platform
        self.config = config
        
        if platform == "facebook":
            # Facebook setup
            pass
        elif platform == "twitter":
            # Twitter setup
            pass
        elif platform == "linkedin":
            # LinkedIn setup
            pass
    
    async def post_content(self, content: str, media_urls: List[str] = None) -> Dict[str, Any]:
        """Post content to social media."""
        # Implementation...
```

### Content Management Systems

The system integrates with content management systems:

```python
class CMSService:
    def __init__(self, cms_type: str, config: Dict[str, Any]):
        self.cms_type = cms_type
        self.config = config
        
        if cms_type == "wordpress":
            # WordPress setup
            pass
        elif cms_type == "shopify":
            # Shopify setup
            pass
    
    async def publish_post(self, title: str, content: str, categories: List[str] = None, tags: List[str] = None) -> Dict[str, Any]:
        """Publish a post to the CMS."""
        # Implementation...
```

## Testing

### Unit Testing

Unit tests are implemented using pytest:

```python
import pytest
from unittest.mock import patch, MagicMock

from workflows.lead_nurturing.service import LeadNurturingService

@pytest.fixture
def lead_nurturing_service():
    """Create a LeadNurturingService instance with mocked dependencies."""
    service = LeadNurturingService()
    service.ai_service = MagicMock()
    service.email_service = MagicMock()
    service.sms_service = MagicMock()
    return service

@pytest.mark.asyncio
async def test_process_new_lead_success(lead_nurturing_service):
    """Test processing a new lead successfully."""
    # Test implementation...
```

### Integration Testing

Integration tests verify the interaction between components:

```python
@pytest.mark.asyncio
async def test_lead_nurturing_workflow_integration():
    """Test the complete lead nurturing workflow."""
    # Test implementation...
```

### End-to-End Testing

End-to-end tests verify the complete system:

```python
from playwright.async_api import async_playwright

@pytest.mark.asyncio
async def test_lead_form_submission():
    """Test submitting a lead form and verifying the workflow."""
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        
        # Navigate to the lead form
        await page.goto("http://localhost:3000/contact")
        
        # Fill out the form
        await page.fill("input[name='name']", "Test User")
        await page.fill("input[name='email']", "test@example.com")
        await page.fill("textarea[name='message']", "I'm interested in your services")
        
        # Submit the form
        await page.click("button[type='submit']")
        
        # Verify success message
        assert await page.inner_text(".success-message") == "Thank you for your message!"
        
        # Verify lead was created in the database
        # Implementation...
        
        await browser.close()
```

### Performance Testing

Performance tests verify system performance under load:

```python
import asyncio
from locust import HttpUser, task, between

class BusinessAutomationUser(HttpUser):
    wait_time = between(1, 5)
    
    def on_start(self):
        """Log in before starting tests."""
        response = self.client.post("/token", {
            "username": "test@example.com",
            "password": "password"
        })
        self.token = response.json()["access_token"]
        self.client.headers = {"Authorization": f"Bearer {self.token}"}
    
    @task
    def view_dashboard(self):
        """Test viewing the dashboard."""
        self.client.get("/api/dashboard")
    
    @task
    def create_lead(self):
        """Test creating a lead."""
        self.client.post("/api/lead-nurturing/leads", json={
            "name": "Test Lead",
            "email": "lead@example.com",
            "source": "website_form"
        })
```

## Deployment

### Docker Deployment

The system can be deployed using Docker:

```yaml
# docker-compose.yml
version: '3.8'

services:
  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://postgres:postgres@db:5432/business_automation
      - OPENAI_API_KEY=${OPENAI_API_KEY}
    depends_on:
      - db
    volumes:
      - ./backend:/app
    restart: unless-stopped

  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile
    ports:
      - "3000:80"
    depends_on:
      - backend
    restart: unless-stopped

  db:
    image: postgres:15-alpine
    ports:
      - "5432:5432"
    environment:
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=postgres
      - POSTGRES_DB=business_automation
    volumes:
      - postgres_data:/var/lib/postgresql/data
    restart: unless-stopped

volumes:
  postgres_data:
```

### Cloud Deployment

The system can be deployed to cloud platforms:

#### Railway Deployment

```yaml
# railway.json
{
  "build": {
    "builder": "nixpacks",
    "buildCommand": "cd backend && pip install -r requirements.txt"
  },
  "deploy": {
    "startCommand": "cd backend && uvicorn main:app --host 0.0.0.0 --port $PORT",
    "healthcheckPath": "/",
    "healthcheckTimeout": 300,
    "restartPolicyType": "on_failure"
  }
}
```

#### Render Deployment

```yaml
# render.yaml
services:
  - name: backend
    type: web
    env: python
    buildCommand: cd backend && pip install -r requirements.txt
    startCommand: cd backend && uvicorn main:app --host 0.0.0.0 --port $PORT
    envVars:
      - key: OPENAI_API_KEY
        sync: false
      # Other environment variables...
  
  - name: frontend
    type: web
    env: node
    buildCommand: cd frontend && npm install && npm run build
    startCommand: cd frontend && npx serve -s dist -l $PORT
    envVars:
      - key: VITE_API_URL
        value: https://backend.onrender.com
```

### CI/CD Pipeline

The system includes a CI/CD pipeline using GitHub Actions:

```yaml
# .github/workflows/ci-cd.yml
name: CI/CD Pipeline

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - name: Install dependencies
        run: |
          cd backend
          pip install -r requirements.txt
      - name: Run tests
        run: |
          cd backend
          pytest
  
  deploy:
    needs: test
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Deploy to Railway
        uses: railwayapp/cli@master
        with:
          args: up
        env:
          RAILWAY_TOKEN: ${{ secrets.RAILWAY_TOKEN }}
```

## Extending the System

### Adding New Workflows

To add a new workflow:

1. Create a new directory in `backend/workflows/`
2. Implement the workflow components:
   - `models.py`: Data models
   - `repository.py`: Database access
   - `service.py`: Business logic
   - `tasks.py`: Background tasks
   - `prompts.py`: AI prompts
3. Create API routes in `backend/api/`
4. Add frontend components in `frontend/src/components/`
5. Add frontend pages in `frontend/src/pages/`
6. Update the navigation menu

Example of a new workflow:

```python
# backend/workflows/customer_onboarding/service.py
class CustomerOnboardingService:
    def __init__(self):
        self.ai_service = OpenAIService()
        self.email_service = EmailService()
    
    async def process_new_customer(self, customer_id: str) -> Dict[str, Any]:
        # Implementation...
    
    async def send_welcome_materials(self, customer_id: str) -> Dict[str, Any]:
        # Implementation...
    
    async def schedule_onboarding_call(self, customer_id: str) -> Dict[str, Any]:
        # Implementation...

# Create service instance
customer_onboarding_service = CustomerOnboardingService()
```

### Creating Custom Integrations

To create a custom integration:

1. Create a new service in `backend/services/`
2. Implement the service interface
3. Add configuration options
4. Update the API to expose the integration

Example of a custom integration:

```python
# backend/services/crm/hubspot_service.py
import hubspot
from core.config import settings

class HubSpotService:
    def __init__(self):
        self.client = hubspot.Client.create(api_key=settings.HUBSPOT_API_KEY)
    
    async def create_contact(self, contact_data: Dict[str, Any]) -> Dict[str, Any]:
        # Implementation...
    
    async def update_contact(self, contact_id: str, contact_data: Dict[str, Any]) -> Dict[str, Any]:
        # Implementation...
    
    async def create_deal(self, deal_data: Dict[str, Any]) -> Dict[str, Any]:
        # Implementation...

# Create service instance
hubspot_service = HubSpotService()
```

### Implementing New Features

To implement a new feature:

1. Define the feature requirements
2. Update the database schema if needed
3. Implement the backend logic
4. Create or update API endpoints
5. Implement the frontend components
6. Add tests for the new feature

Example of a new feature:

```python
# backend/api/analytics.py
from fastapi import APIRouter, Depends
from typing import Dict, Any, List

from core.security import get_current_user
from services.analytics.service import analytics_service

router = APIRouter(
    prefix="/api/analytics",
    tags=["analytics"],
    responses={404: {"description": "Not found"}},
)

@router.get("/dashboard")
async def get_dashboard_analytics(
    start_date: str = None,
    end_date: str = None,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """Get analytics data for the dashboard."""
    company_id = current_user["company_id"]
    return await analytics_service.get_dashboard_analytics(company_id, start_date, end_date)

@router.get("/lead-nurturing")
async def get_lead_nurturing_analytics(
    start_date: str = None,
    end_date: str = None,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """Get analytics data for lead nurturing."""
    company_id = current_user["company_id"]
    return await analytics_service.get_lead_nurturing_analytics(company_id, start_date, end_date)

# Other endpoints...
```

## API Reference

### API Authentication

All API endpoints (except authentication endpoints) require authentication:

```
POST /token
```

Request:
```json
{
  "username": "user@example.com",
  "password": "password"
}
```

Response:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

### Lead Nurturing API

```
POST /api/lead-nurturing/leads
GET /api/lead-nurturing/leads
GET /api/lead-nurturing/leads/{lead_id}
PUT /api/lead-nurturing/leads/{lead_id}
DELETE /api/lead-nurturing/leads/{lead_id}
POST /api/lead-nurturing/interactions
GET /api/lead-nurturing/interactions
GET /api/lead-nurturing/analytics
```

### Review & Referral API

```
POST /api/review-referral/reviews
GET /api/review-referral/reviews
GET /api/review-referral/reviews/{review_id}
PUT /api/review-referral/reviews/{review_id}
POST /api/review-referral/referrals
GET /api/review-referral/referrals
GET /api/review-referral/referrals/{referral_id}
GET /api/review-referral/analytics
```

### Content Generation API

```
POST /api/content-generation/blog-post
POST /api/content-generation/social-media
POST /api/content-generation/email-newsletter
POST /api/content-generation/product-description
POST /api/content-generation/schedule
POST /api/content-generation/publish/{content_id}
GET /api/content-generation/content/{content_id}
GET /api/content-generation/schedules
GET /api/content-generation/analytics
```

### User Management API

```
POST /api/users
GET /api/users
GET /api/users/{user_id}
PUT /api/users/{user_id}
DELETE /api/users/{user_id}
GET /api/users/me
```

### System API

```
GET /api/system/health
GET /api/system/stats
POST /api/system/backup
POST /api/system/restore
```

For detailed API documentation, see the OpenAPI documentation at `/docs` when running the backend server.


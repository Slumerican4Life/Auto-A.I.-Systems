# Business Automation System - Deployment Instructions

This document provides instructions for deploying the Business Automation System to various environments.

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Environment Setup](#environment-setup)
3. [Backend Deployment](#backend-deployment)
4. [Frontend Deployment](#frontend-deployment)
5. [Database Setup](#database-setup)
6. [Environment Variables](#environment-variables)
7. [Deployment Options](#deployment-options)
8. [Monitoring and Maintenance](#monitoring-and-maintenance)

## Prerequisites

Before deploying the system, ensure you have the following:

- Node.js 16+ and npm 8+
- Python 3.9+
- PostgreSQL 13+ or Firebase account
- SendGrid or SMTP email provider account
- Twilio account for SMS functionality
- OpenAI API key for AI-powered features
- Domain name (for production deployment)

## Environment Setup

### Development Environment

1. Clone the repository:
   ```bash
   git clone https://github.com/your-org/business-automation-system.git
   cd business-automation-system
   ```

2. Set up backend:
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. Set up frontend:
   ```bash
   cd ../frontend
   npm install
   ```

4. Create a `.env` file in both the backend and frontend directories using the provided `.env.example` templates.

## Backend Deployment

### Option 1: Railway

1. Create a new project in Railway
2. Connect your GitHub repository
3. Add the required environment variables
4. Deploy the backend service

```bash
# From the backend directory
railway up
```

### Option 2: Render

1. Create a new Web Service in Render
2. Connect your GitHub repository
3. Configure the service:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn main:app --host 0.0.0.0 --port $PORT`
4. Add the required environment variables
5. Deploy the service

### Option 3: Docker

1. Build the Docker image:
   ```bash
   docker build -t business-automation-backend ./backend
   ```

2. Run the container:
   ```bash
   docker run -p 8000:8000 --env-file ./backend/.env business-automation-backend
   ```

## Frontend Deployment

### Option 1: Vercel

1. Connect your GitHub repository to Vercel
2. Configure the build settings:
   - Build Command: `npm run build`
   - Output Directory: `build`
3. Add the required environment variables
4. Deploy the frontend

```bash
# From the frontend directory
vercel
```

### Option 2: Netlify

1. Connect your GitHub repository to Netlify
2. Configure the build settings:
   - Build Command: `npm run build`
   - Publish Directory: `build`
3. Add the required environment variables
4. Deploy the frontend

### Option 3: Docker

1. Build the Docker image:
   ```bash
   docker build -t business-automation-frontend ./frontend
   ```

2. Run the container:
   ```bash
   docker run -p 3000:80 business-automation-frontend
   ```

## Database Setup

### PostgreSQL

1. Create a new PostgreSQL database:
   ```sql
   CREATE DATABASE business_automation;
   CREATE USER business_automation_user WITH PASSWORD 'your_password';
   GRANT ALL PRIVILEGES ON DATABASE business_automation TO business_automation_user;
   ```

2. Run the database migrations:
   ```bash
   cd backend
   alembic upgrade head
   ```

### Firebase

1. Create a new Firebase project
2. Set up Firestore database
3. Create a service account and download the credentials JSON file
4. Add the Firebase credentials to your environment variables

## Environment Variables

### Backend Environment Variables

Create a `.env` file in the backend directory with the following variables:

```
# API settings
SECRET_KEY=your_secret_key
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Database settings
DATABASE_TYPE=postgres  # or firebase
POSTGRES_SERVER=localhost
POSTGRES_USER=business_automation_user
POSTGRES_PASSWORD=your_password
POSTGRES_DB=business_automation

# Firebase settings (if using Firebase)
FIREBASE_PROJECT_ID=your_project_id
FIREBASE_PRIVATE_KEY=your_private_key
FIREBASE_CLIENT_EMAIL=your_client_email

# Email settings
EMAIL_PROVIDER=sendgrid  # or smtp
SENDGRID_API_KEY=your_sendgrid_api_key
SENDGRID_FROM_EMAIL=noreply@yourdomain.com

# SMTP settings (if using SMTP)
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your_email@gmail.com
SMTP_PASSWORD=your_password
SMTP_USE_TLS=true
SMTP_FROM_EMAIL=noreply@yourdomain.com

# SMS settings
SMS_PROVIDER=twilio
TWILIO_ACCOUNT_SID=your_twilio_account_sid
TWILIO_AUTH_TOKEN=your_twilio_auth_token
TWILIO_FROM_NUMBER=your_twilio_phone_number

# OpenAI settings
OPENAI_API_KEY=your_openai_api_key
OPENAI_MODEL=gpt-4

# Celery settings
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/0
```

### Frontend Environment Variables

Create a `.env` file in the frontend directory with the following variables:

```
REACT_APP_API_URL=http://localhost:8000/api
REACT_APP_ENVIRONMENT=development
```

For production, update the API URL to your production backend URL.

## Deployment Options

### Option 1: All-in-One Deployment with Docker Compose

1. Create a `docker-compose.yml` file in the root directory:
   ```yaml
   version: '3'
   
   services:
     backend:
       build: ./backend
       ports:
         - "8000:8000"
       env_file:
         - ./backend/.env
       depends_on:
         - postgres
         - redis
   
     frontend:
       build: ./frontend
       ports:
         - "3000:80"
       env_file:
         - ./frontend/.env
       depends_on:
         - backend
   
     postgres:
       image: postgres:13
       environment:
         POSTGRES_USER: business_automation_user
         POSTGRES_PASSWORD: your_password
         POSTGRES_DB: business_automation
       volumes:
         - postgres_data:/var/lib/postgresql/data
   
     redis:
       image: redis:6
       volumes:
         - redis_data:/data
   
     celery_worker:
       build: ./backend
       command: celery -A worker worker --loglevel=info
       env_file:
         - ./backend/.env
       depends_on:
         - postgres
         - redis
   
     celery_beat:
       build: ./backend
       command: celery -A worker beat --loglevel=info
       env_file:
         - ./backend/.env
       depends_on:
         - postgres
         - redis
   
   volumes:
     postgres_data:
     redis_data:
   ```

2. Start the services:
   ```bash
   docker-compose up -d
   ```

### Option 2: Separate Services Deployment

1. Deploy the backend to Railway, Render, or Heroku
2. Deploy the frontend to Vercel, Netlify, or Firebase Hosting
3. Set up a managed PostgreSQL database (e.g., Railway, Render, AWS RDS)
4. Set up a managed Redis instance (e.g., Railway, Render, AWS ElastiCache)

## Monitoring and Maintenance

### Monitoring

1. Set up logging with CloudWatch, Datadog, or Sentry
2. Configure health check endpoints
3. Set up alerts for critical errors

### Backups

1. Configure regular database backups
2. Store backups in a secure location (e.g., AWS S3, Google Cloud Storage)

### Updates

1. Regularly update dependencies
2. Follow a CI/CD pipeline for automated testing and deployment
3. Implement a blue-green deployment strategy for zero-downtime updates

## Scaling

### Horizontal Scaling

1. Deploy multiple instances of the backend behind a load balancer
2. Scale the database with read replicas
3. Use a CDN for the frontend

### Vertical Scaling

1. Increase resources (CPU, memory) for the backend and database
2. Optimize database queries and add indexes
3. Implement caching for frequently accessed data


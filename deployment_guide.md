# Business Automation System Deployment Guide

This guide provides detailed instructions for deploying the Business Automation System in various environments.

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Local Development Setup](#local-development-setup)
3. [Docker Deployment](#docker-deployment)
4. [Cloud Deployment](#cloud-deployment)
   - [Railway Deployment](#railway-deployment)
   - [Render Deployment](#render-deployment)
5. [Database Configuration](#database-configuration)
   - [PostgreSQL Setup](#postgresql-setup)
   - [Firebase Setup](#firebase-setup)
6. [Environment Variables](#environment-variables)
7. [Scaling Considerations](#scaling-considerations)
8. [Monitoring and Maintenance](#monitoring-and-maintenance)
9. [Troubleshooting](#troubleshooting)

## Prerequisites

Before deploying the Business Automation System, ensure you have the following:

- **API Keys**:
  - OpenAI API key for AI-powered workflows
  - SendGrid or Gmail credentials for email functionality
  - Twilio credentials for SMS functionality (optional)

- **Development Tools**:
  - Node.js 16+ and npm
  - Python 3.9+
  - Docker and Docker Compose (for containerized deployment)

- **Database**:
  - PostgreSQL 13+ or
  - Firebase account with Firestore

## Local Development Setup

To set up the system for local development:

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd business-automation-system
   ```

2. **Set up the backend**:
   ```bash
   cd backend
   pip install -r requirements.txt
   cp .env.example .env
   # Edit .env with your configuration
   ```

3. **Set up the frontend**:
   ```bash
   cd ../frontend
   npm install
   cp .env.example .env
   # Edit .env with your configuration
   ```

4. **Initialize the database**:
   ```bash
   cd ../backend
   # For PostgreSQL
   python -m database.postgresql.run_migrations
   # For Firebase
   python -m database.firebase.init_firebase
   ```

5. **Start the development servers**:
   ```bash
   # Terminal 1 - Backend
   cd backend
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   
   # Terminal 2 - Frontend
   cd frontend
   npm run dev
   ```

6. **Access the application**:
   - Backend API: http://localhost:8000
   - Frontend: http://localhost:3000

## Docker Deployment

The easiest way to deploy the entire system is using Docker Compose:

1. **Create environment file**:
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

2. **Build and start the containers**:
   ```bash
   docker-compose up -d
   ```

3. **Run database migrations**:
   ```bash
   # For PostgreSQL
   docker-compose exec backend python -m database.postgresql.run_migrations
   # For Firebase
   docker-compose exec backend python -m database.firebase.init_firebase
   ```

4. **Access the application**:
   - Backend API: http://localhost:8000
   - Frontend: http://localhost:3000

5. **Stop the containers**:
   ```bash
   docker-compose down
   ```

Alternatively, you can use the deployment script:

```bash
chmod +x deploy.sh
./deploy.sh --mode docker --database postgres
```

## Cloud Deployment

### Railway Deployment

To deploy the system on Railway:

1. **Install Railway CLI**:
   ```bash
   npm i -g @railway/cli
   railway login
   ```

2. **Initialize Railway project**:
   ```bash
   railway init
   ```

3. **Set environment variables**:
   ```bash
   railway variables set OPENAI_API_KEY=your_openai_api_key
   railway variables set JWT_SECRET=your_jwt_secret
   # Set other required variables
   ```

4. **Deploy the application**:
   ```bash
   railway up
   ```

5. **Run database migrations**:
   ```bash
   railway run python -m database.postgresql.run_migrations
   ```

Alternatively, use the deployment script:

```bash
./deploy.sh --mode railway --database postgres
```

### Render Deployment

To deploy the system on Render:

1. **Create a render.yaml file**:
   ```yaml
   services:
     - name: backend
       type: web
       env: python
       buildCommand: pip install -r requirements.txt
       startCommand: uvicorn main:app --host 0.0.0.0 --port $PORT
       envVars:
         - key: OPENAI_API_KEY
           sync: false
         # Add other environment variables
     
     - name: frontend
       type: web
       env: node
       buildCommand: npm install && npm run build
       startCommand: npx serve -s dist -l $PORT
       envVars:
         - key: VITE_API_URL
           value: https://backend.onrender.com
   
     - name: db
       type: pserv
       env: docker
       image: postgres:15-alpine
       envVars:
         - key: POSTGRES_USER
           value: postgres
         - key: POSTGRES_PASSWORD
           sync: false
         - key: POSTGRES_DB
           value: business_automation
   ```

2. **Deploy to Render**:
   ```bash
   render deploy
   ```

Alternatively, use the deployment script:

```bash
./deploy.sh --mode render --database postgres
```

## Database Configuration

### PostgreSQL Setup

To configure PostgreSQL:

1. **Create a database**:
   ```sql
   CREATE DATABASE business_automation;
   ```

2. **Set environment variables**:
   ```
   DATABASE_URL=postgresql://username:password@host:port/business_automation
   ```

3. **Run migrations**:
   ```bash
   python -m database.postgresql.run_migrations
   ```

### Firebase Setup

To configure Firebase:

1. **Create a Firebase project** in the Firebase Console

2. **Generate a service account key**:
   - Go to Project Settings > Service Accounts
   - Click "Generate New Private Key"
   - Save the JSON file securely

3. **Set environment variables**:
   ```
   FIREBASE_PROJECT_ID=your_project_id
   FIREBASE_PRIVATE_KEY=your_private_key
   FIREBASE_CLIENT_EMAIL=your_client_email
   ```

4. **Initialize Firebase**:
   ```bash
   python -m database.firebase.init_firebase
   ```

## Environment Variables

The system requires the following environment variables:

```
# OpenAI API Key (required)
OPENAI_API_KEY=your_openai_api_key

# JWT Secret for authentication
JWT_SECRET=your_jwt_secret_change_this_in_production

# Database Configuration
DATABASE_URL=postgresql://postgres:postgres@db:5432/business_automation

# Email Service Configuration
EMAIL_SERVICE=sendgrid  # or gmail
SENDGRID_API_KEY=your_sendgrid_api_key
GMAIL_USER=your_gmail_user
GMAIL_PASSWORD=your_gmail_app_password

# SMS Service Configuration
TWILIO_ACCOUNT_SID=your_twilio_account_sid
TWILIO_AUTH_TOKEN=your_twilio_auth_token
TWILIO_PHONE_NUMBER=your_twilio_phone_number

# Firebase Configuration (if using Firebase)
FIREBASE_PROJECT_ID=your_firebase_project_id
FIREBASE_PRIVATE_KEY=your_firebase_private_key
FIREBASE_CLIENT_EMAIL=your_firebase_client_email

# Deployment Configuration
PORT=8000
NODE_ENV=production
```

## Scaling Considerations

To scale the system for higher loads:

1. **Horizontal Scaling**:
   - Deploy multiple instances of the backend service
   - Use a load balancer to distribute traffic
   - Scale the database with read replicas

2. **Vertical Scaling**:
   - Increase resources (CPU, memory) for the backend services
   - Optimize database performance with proper indexing

3. **Caching**:
   - Implement Redis caching for frequently accessed data
   - Use CDN for static frontend assets

4. **Background Processing**:
   - Scale Celery workers horizontally for more processing power
   - Use dedicated queues for different types of tasks

## Monitoring and Maintenance

To monitor and maintain the system:

1. **Logging**:
   - Configure centralized logging with ELK stack or similar
   - Set up log rotation to manage disk space

2. **Monitoring**:
   - Implement health check endpoints
   - Set up alerts for critical errors
   - Monitor API usage and costs

3. **Backups**:
   - Schedule regular database backups
   - Test backup restoration periodically

4. **Updates**:
   - Keep dependencies updated
   - Follow a CI/CD pipeline for safe deployments

## Troubleshooting

Common issues and solutions:

1. **API Connection Issues**:
   - Check API keys and permissions
   - Verify network connectivity
   - Check for rate limiting

2. **Database Connection Issues**:
   - Verify connection string
   - Check database server status
   - Ensure proper credentials

3. **Workflow Failures**:
   - Check logs for specific error messages
   - Verify AI service availability
   - Check for malformed data

4. **Deployment Failures**:
   - Verify environment variables
   - Check for disk space issues
   - Ensure proper permissions

For additional help, refer to the project documentation or contact support.


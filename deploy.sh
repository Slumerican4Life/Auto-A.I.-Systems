#!/bin/bash

# Deployment script for Business Automation System
# This script automates the deployment process for the system

# Exit on error
set -e

# Display help message
function show_help {
    echo "Business Automation System Deployment Script"
    echo ""
    echo "Usage: ./deploy.sh [options]"
    echo ""
    echo "Options:"
    echo "  -h, --help                 Show this help message"
    echo "  -e, --env <file>           Specify environment file (default: .env)"
    echo "  -m, --mode <mode>          Deployment mode: docker, railway, render (default: docker)"
    echo "  -d, --database <type>      Database type: postgres, firebase (default: postgres)"
    echo "  --skip-build               Skip building the application"
    echo "  --skip-tests               Skip running tests"
    echo ""
}

# Default values
ENV_FILE=".env"
DEPLOY_MODE="docker"
DATABASE_TYPE="postgres"
SKIP_BUILD=false
SKIP_TESTS=false

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    key="$1"
    case $key in
        -h|--help)
            show_help
            exit 0
            ;;
        -e|--env)
            ENV_FILE="$2"
            shift
            shift
            ;;
        -m|--mode)
            DEPLOY_MODE="$2"
            shift
            shift
            ;;
        -d|--database)
            DATABASE_TYPE="$2"
            shift
            shift
            ;;
        --skip-build)
            SKIP_BUILD=true
            shift
            ;;
        --skip-tests)
            SKIP_TESTS=true
            shift
            ;;
        *)
            echo "Unknown option: $1"
            show_help
            exit 1
            ;;
    esac
done

# Check if environment file exists
if [ ! -f "$ENV_FILE" ]; then
    echo "Environment file $ENV_FILE not found!"
    echo "Creating a sample environment file..."
    cat > "$ENV_FILE" << EOL
# Business Automation System Environment Variables

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
EOL
    echo "Please edit $ENV_FILE with your actual configuration values."
    exit 1
fi

# Load environment variables
echo "Loading environment variables from $ENV_FILE..."
export $(grep -v '^#' "$ENV_FILE" | xargs)

# Run tests if not skipped
if [ "$SKIP_TESTS" = false ]; then
    echo "Running tests..."
    cd backend
    python run_tests.py
    cd ..
    
    echo "Tests completed successfully!"
fi

# Build the application if not skipped
if [ "$SKIP_BUILD" = false ]; then
    echo "Building the application..."
    
    # Build frontend
    echo "Building frontend..."
    cd frontend
    npm install
    npm run build
    cd ..
    
    echo "Build completed successfully!"
fi

# Deploy based on selected mode
echo "Deploying in $DEPLOY_MODE mode with $DATABASE_TYPE database..."

case $DEPLOY_MODE in
    docker)
        echo "Deploying with Docker Compose..."
        docker-compose down
        docker-compose build
        docker-compose up -d
        
        echo "Running database migrations..."
        if [ "$DATABASE_TYPE" = "postgres" ]; then
            docker-compose exec backend python -m database.postgresql.run_migrations
        elif [ "$DATABASE_TYPE" = "firebase" ]; then
            docker-compose exec backend python -m database.firebase.init_firebase
        fi
        
        echo "Deployment completed successfully!"
        echo "The application is now running at:"
        echo "- Backend API: http://localhost:8000"
        echo "- Frontend: http://localhost:3000"
        ;;
        
    railway)
        echo "Deploying to Railway..."
        # Check if Railway CLI is installed
        if ! command -v railway &> /dev/null; then
            echo "Railway CLI not found. Please install it first:"
            echo "npm i -g @railway/cli"
            exit 1
        fi
        
        # Deploy to Railway
        railway up
        
        echo "Deployment to Railway completed successfully!"
        ;;
        
    render)
        echo "Deploying to Render..."
        # Check if Render CLI is installed
        if ! command -v render &> /dev/null; then
            echo "Render CLI not found. Please install it first."
            exit 1
        fi
        
        # Deploy to Render
        render deploy
        
        echo "Deployment to Render completed successfully!"
        ;;
        
    *)
        echo "Unknown deployment mode: $DEPLOY_MODE"
        exit 1
        ;;
esac

echo "Deployment process completed!"


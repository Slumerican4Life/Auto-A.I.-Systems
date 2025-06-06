# Business Automation System - File Structure

This document provides an overview of the key files and directories in the Business Automation System project.

## Project Root

```
business-automation-system/
├── backend/           # Backend FastAPI application
├── frontend/          # Frontend React application
├── docs/              # Project documentation
├── database/          # Database scripts and migrations
├── scripts/           # Utility scripts
└── README.md          # Project overview
```

## Backend Structure

```
backend/
├── api/                           # API routes
│   ├── __init__.py
│   ├── auth.py                    # Authentication endpoints
│   ├── leads.py                   # Lead management endpoints
│   ├── reviews.py                 # Review and referral endpoints
│   ├── content.py                 # Content management endpoints
│   └── analytics.py               # Analytics endpoints
│
├── core/                          # Core functionality
│   ├── __init__.py
│   ├── config.py                  # Configuration settings
│   └── security.py                # Authentication and security
│
├── models/                        # Data models
│   ├── __init__.py
│   ├── user.py                    # User models
│   ├── company.py                 # Company models
│   ├── lead.py                    # Lead models
│   ├── review_referral.py         # Review and referral models
│   ├── content.py                 # Content models
│   ├── workflow.py                # Workflow models
│   └── analytics.py               # Analytics models
│
├── services/                      # Business logic services
│   ├── __init__.py
│   ├── lead_service.py            # Lead management service
│   ├── review_service.py          # Review and referral service
│   ├── content_service.py         # Content management service
│   │
│   ├── ai/                        # AI services
│   │   ├── __init__.py
│   │   ├── ai_service.py          # AI service implementation
│   │   └── prompt_templates.py    # AI prompt templates
│   │
│   ├── analytics/                 # Analytics services
│   │   ├── __init__.py
│   │   └── analytics_service.py   # Analytics service implementation
│   │
│   ├── email/                     # Email services
│   │   ├── __init__.py
│   │   └── email_service.py       # Email service implementation
│   │
│   ├── scheduler/                 # Scheduler services
│   │   ├── __init__.py
│   │   └── scheduler_service.py   # Scheduler service implementation
│   │
│   └── sms/                       # SMS services
│       ├── __init__.py
│       └── sms_service.py         # SMS service implementation
│
├── main.py                        # FastAPI application entry point
├── requirements.txt               # Python dependencies
└── alembic.ini                    # Database migration configuration
```

## Frontend Structure

```
frontend/
├── public/                        # Static files
│   ├── index.html                 # HTML template
│   ├── favicon.ico                # Favicon
│   └── logo.svg                   # Logo
│
├── src/                           # Source code
│   ├── components/                # React components
│   │   ├── common/                # Common components
│   │   │   ├── Button.js
│   │   │   ├── Card.js
│   │   │   ├── DateRangePicker.js
│   │   │   ├── ErrorAlert.js
│   │   │   ├── LoadingSpinner.js
│   │   │   └── Table.js
│   │   │
│   │   ├── dashboard/             # Dashboard components
│   │   │   ├── ActivityFeed.js
│   │   │   ├── DashboardCard.js
│   │   │   ├── MetricCard.js
│   │   │   └── ValueSummaryCard.js
│   │   │
│   │   ├── leads/                 # Lead components
│   │   │   ├── LeadForm.js
│   │   │   ├── LeadList.js
│   │   │   └── InteractionList.js
│   │   │
│   │   ├── reviews/               # Review components
│   │   │   ├── ReviewForm.js
│   │   │   ├── ReviewList.js
│   │   │   └── ReferralList.js
│   │   │
│   │   └── content/               # Content components
│   │       ├── ContentForm.js
│   │       ├── ContentList.js
│   │       └── ContentPreview.js
│   │
│   ├── contexts/                  # React contexts
│   │   ├── AuthContext.js         # Authentication context
│   │   └── NotificationContext.js # Notification context
│   │
│   ├── layouts/                   # Page layouts
│   │   ├── DashboardLayout.js     # Dashboard layout
│   │   └── AuthLayout.js          # Authentication layout
│   │
│   ├── pages/                     # Page components
│   │   ├── Login.js               # Login page
│   │   ├── Register.js            # Registration page
│   │   ├── Dashboard.js           # Dashboard page
│   │   ├── NotFound.js            # 404 page
│   │   │
│   │   ├── leads/                 # Lead pages
│   │   │   ├── LeadsList.js
│   │   │   └── LeadDetail.js
│   │   │
│   │   ├── reviews/               # Review pages
│   │   │   ├── ReviewsList.js
│   │   │   ├── ReviewDetail.js
│   │   │   └── ReferralsList.js
│   │   │
│   │   ├── content/               # Content pages
│   │   │   ├── ContentList.js
│   │   │   ├── ContentDetail.js
│   │   │   └── ContentGenerator.js
│   │   │
│   │   ├── analytics/             # Analytics pages
│   │   │   └── Analytics.js
│   │   │
│   │   └── settings/              # Settings pages
│   │       └── Settings.js
│   │
│   ├── services/                  # API services
│   │   └── api.js                 # API client
│   │
│   ├── utils/                     # Utility functions
│   │   ├── date.js                # Date utilities
│   │   └── format.js              # Formatting utilities
│   │
│   ├── App.js                     # Main React component
│   ├── index.js                   # React entry point
│   └── index.css                  # Global styles
│
├── package.json                   # NPM dependencies
├── tailwind.config.js             # Tailwind CSS configuration
└── .env.example                   # Environment variables example
```

## Documentation Structure

```
docs/
├── api/                           # API documentation
│   └── api_endpoints.md           # API endpoints documentation
│
├── architecture/                  # Architecture documentation
│   ├── system_architecture.md     # System architecture overview
│   └── database_schema.md         # Database schema documentation
│
├── deployment/                    # Deployment documentation
│   └── deployment_instructions.md # Deployment instructions
│
├── file_structure.md              # This file
└── project_summary.md             # Project summary
```

## Database Structure

```
database/
├── migrations/                    # Database migrations
│   └── versions/                  # Migration versions
│
├── init.sql                       # Initial database setup
└── seed.sql                       # Seed data for development
```

## Scripts Structure

```
scripts/
├── setup.sh                       # Setup script
├── deploy.sh                      # Deployment script
└── backup.sh                      # Database backup script
```

## Key Files

### Backend Key Files

- `backend/main.py`: The entry point for the FastAPI application
- `backend/core/config.py`: Configuration settings for the application
- `backend/core/security.py`: Authentication and security functionality
- `backend/api/*.py`: API endpoints for different features
- `backend/models/*.py`: Data models for the application
- `backend/services/*_service.py`: Business logic services

### Frontend Key Files

- `frontend/src/App.js`: The main React component
- `frontend/src/index.js`: The React entry point
- `frontend/src/contexts/AuthContext.js`: Authentication context
- `frontend/src/services/api.js`: API client for backend communication
- `frontend/src/layouts/DashboardLayout.js`: Dashboard layout component
- `frontend/src/pages/Dashboard.js`: Dashboard page component

### Documentation Key Files

- `README.md`: Project overview
- `docs/project_summary.md`: Detailed project summary
- `docs/architecture/system_architecture.md`: System architecture documentation
- `docs/deployment/deployment_instructions.md`: Deployment instructions


# Business Automation System

A modular business automation system with AI-powered workflows for small businesses. This system automates high-leverage business processes, tracks performance in real-time, and displays results in a beautiful UI dashboard.

![Dashboard Preview](https://private-us-east-1.manuscdn.com/sessionFile/SBogVJVAllsFhCdm4pZVQq/sandbox/r08mqAWGNSOWy8Shu8ozmU-images_1749161192944_na1fn_L2hvbWUvdWJ1bnR1L3VwbG9hZC97MjVCNTkyRDQtMTAwNS00Njc4LUI1NzktQjAwMzVDMjY5REQyfQ.png?Policy=eyJTdGF0ZW1lbnQiOlt7IlJlc291cmNlIjoiaHR0cHM6Ly9wcml2YXRlLXVzLWVhc3QtMS5tYW51c2Nkbi5jb20vc2Vzc2lvbkZpbGUvU0JvZ1ZKVkFsbHNGaENkbTRwWlZRcS9zYW5kYm94L3IwOG1xQVdHTlNPV3k4U2h1OG96bVUtaW1hZ2VzXzE3NDkxNjExOTI5NDRfbmExZm5fTDJodmJXVXZkV0oxYm5SMUwzVndiRzloWkM5N01qVkNOVGt5UkRRdE1UQXdOUzAwTmpjNExVSTFOemt0UWpBd016VkRNalk1UkVReWZRLnBuZyIsIkNvbmRpdGlvbiI6eyJEYXRlTGVzc1RoYW4iOnsiQVdTOkVwb2NoVGltZSI6MTc2NzIyNTYwMH19fV19&Key-Pair-Id=K2HSFNDJXOU9YS&Signature=Uth87Yk-BimAHAgltYZDtD2tZSwqCCjEY753BmdS65ivw2kdlAzegFNA3YPtffMU~nOzLaipkheabeS~mlH5PgAxQ8nBsbEAfEOseFWOGFhovfiON2Ia-0WBAX-yGUvJVnfddnvX7yb~UUZE2Nj0hxtVmrsMNxOnRb9~ugoOJTkTN2idr3XPajU2GFgPGv8zuBG45nyM6qdMmW4Mp0pI3Aw5RCRjPBDEzXpdcEGsmUvmqpr3d0NseCum4WtPfnpn~YmRvsjl4NRU0P7OiQL5pRUIYW6m6x2HhzhHU2ES6ZaRyxpByGD3~hOZ3KThpNB~tmh-EvSBwWZem3hMcf170w__)

## Features

### 1. AI Lead Nurturing Agent
- Automatically responds to new leads from various sources
- Generates personalized messages using GPT
- Sends follow-up messages via email or SMS
- Tracks lead status, reply rates, and conversions

### 2. Review & Referral Generator
- Sends thank-you messages and review requests after completed services
- Generates trackable referral offers upon review completion
- Monitors review completion and referral usage
- Tracks new client conversions from referrals

### 3. Content Generation Bot
- Automatically creates blog posts, social media captions, and email newsletters
- Publishes content to WordPress, social media platforms, or email services
- Schedules content creation and publishing
- Tracks engagement metrics for all content

### Dashboard UI
- Real-time KPIs for leads, reviews, referrals, and content
- Interactive charts showing performance over time
- Activity feed with recent actions and events
- Value summary showing estimated revenue impact and time saved

## Tech Stack

### Backend
- FastAPI (Python)
- PostgreSQL or Firebase Firestore
- OpenAI API for AI-powered content generation
- SendGrid/SMTP for email delivery
- Twilio for SMS messaging
- Celery for task scheduling

### Frontend
- React with React Router
- TailwindCSS for styling
- Recharts for data visualization
- React Query for data fetching
- Context API for state management

## Getting Started

### Prerequisites
- Node.js 16+ and npm 8+
- Python 3.9+
- PostgreSQL 13+ or Firebase account
- SendGrid or SMTP email provider account
- Twilio account for SMS functionality
- OpenAI API key for AI-powered features

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-org/business-automation-system.git
   cd business-automation-system
   ```

2. Set up the backend:
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. Set up the frontend:
   ```bash
   cd ../frontend
   npm install
   ```

4. Create a `.env` file in both the backend and frontend directories using the provided `.env.example` templates.

5. Start the backend server:
   ```bash
   cd ../backend
   uvicorn main:app --reload
   ```

6. Start the frontend development server:
   ```bash
   cd ../frontend
   npm start
   ```

7. Open your browser and navigate to `http://localhost:3000`

## Project Structure

```
business-automation-system/
├── backend/
│   ├── api/                 # API routes
│   ├── core/                # Core functionality
│   ├── models/              # Data models
│   ├── services/            # Business logic
│   │   ├── ai/              # AI services
│   │   ├── analytics/       # Analytics services
│   │   ├── email/           # Email services
│   │   ├── scheduler/       # Scheduler services
│   │   └── sms/             # SMS services
│   └── main.py              # FastAPI application
├── frontend/
│   ├── public/              # Static files
│   └── src/
│       ├── components/      # React components
│       ├── contexts/        # React contexts
│       ├── layouts/         # Page layouts
│       ├── pages/           # Page components
│       ├── services/        # API services
│       └── App.js           # Main React component
├── docs/                    # Documentation
│   ├── api/                 # API documentation
│   ├── architecture/        # Architecture documentation
│   └── deployment/          # Deployment instructions
└── README.md                # Project overview
```

## Workflows

### Lead Nurturing Workflow
1. New lead is received via form, ad, DM, or manual entry
2. System generates personalized response using GPT
3. Response is sent via email or SMS
4. Follow-up messages are scheduled if no reply
5. All interactions are logged for tracking

### Review & Referral Workflow
1. After service completion, thank-you message is sent with review request
2. When review is completed, referral offer is generated
3. Referral offer is sent to customer
4. Referral usage is tracked for new client conversion

### Content Generation Workflow
1. Content generation is triggered on schedule
2. System generates content using GPT based on configured topics
3. Content is published to configured platforms
4. Engagement metrics are tracked and reported

## Customization

The system is designed to be modular and customizable for different industries:

- **Service Businesses**: Customize lead nurturing sequences and review requests
- **E-commerce**: Focus on post-purchase follow-ups and referral programs
- **Professional Services**: Emphasize content generation and thought leadership
- **Local Businesses**: Prioritize review generation and local SEO content

## Deployment

See [Deployment Instructions](docs/deployment/deployment_instructions.md) for detailed deployment options.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgements

- [OpenAI](https://openai.com/) for the GPT API
- [FastAPI](https://fastapi.tiangolo.com/) for the backend framework
- [React](https://reactjs.org/) for the frontend framework
- [TailwindCSS](https://tailwindcss.com/) for the styling framework


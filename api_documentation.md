# Business Automation System API Documentation

## Introduction

This document provides comprehensive documentation for the Business Automation System API. The API is built using FastAPI and follows RESTful principles. It provides endpoints for managing leads, reviews, referrals, content generation, and system administration.

## Base URL

```
https://api.businessautomationsystem.com
```

For local development:

```
http://localhost:8000
```

## Authentication

The API uses JWT (JSON Web Token) for authentication. To authenticate, you need to obtain an access token by sending a POST request to the `/token` endpoint with your credentials.

### Obtain Access Token

```
POST /token
```

Request body:
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

### Using the Access Token

Include the access token in the `Authorization` header of all API requests:

```
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

## Error Handling

The API returns standard HTTP status codes to indicate the success or failure of a request:

- `200 OK`: The request was successful
- `201 Created`: The resource was successfully created
- `400 Bad Request`: The request was invalid
- `401 Unauthorized`: Authentication failed
- `403 Forbidden`: The authenticated user doesn't have permission
- `404 Not Found`: The requested resource was not found
- `500 Internal Server Error`: An error occurred on the server

Error responses include a JSON body with details:

```json
{
  "detail": "Error message"
}
```

## Rate Limiting

The API implements rate limiting to prevent abuse. The limits are:

- 100 requests per minute per IP address
- 1000 requests per hour per user

When the rate limit is exceeded, the API returns a `429 Too Many Requests` status code.

## Endpoints

### Lead Nurturing API

#### Create a Lead

```
POST /api/lead-nurturing/leads
```

Create a new lead in the system.

Request body:
```json
{
  "name": "John Doe",
  "email": "john.doe@example.com",
  "phone": "+1234567890",
  "source": "website_form",
  "notes": "Interested in our services"
}
```

Response:
```json
{
  "id": "lead-123",
  "name": "John Doe",
  "email": "john.doe@example.com",
  "phone": "+1234567890",
  "company_id": "company-123",
  "source": "website_form",
  "status": "new",
  "notes": "Interested in our services",
  "created_at": "2025-06-01T12:00:00Z",
  "updated_at": "2025-06-01T12:00:00Z"
}
```

#### Get Leads

```
GET /api/lead-nurturing/leads
```

Get a list of leads.

Query parameters:
- `status` (optional): Filter by status (new, contacted, engaged, qualified, converted, lost)
- `source` (optional): Filter by source (website_form, ad_campaign, manual_entry, crm)
- `page` (optional): Page number for pagination (default: 1)
- `limit` (optional): Number of items per page (default: 20)

Response:
```json
{
  "items": [
    {
      "id": "lead-123",
      "name": "John Doe",
      "email": "john.doe@example.com",
      "phone": "+1234567890",
      "company_id": "company-123",
      "source": "website_form",
      "status": "new",
      "notes": "Interested in our services",
      "created_at": "2025-06-01T12:00:00Z",
      "updated_at": "2025-06-01T12:00:00Z"
    },
    // More leads...
  ],
  "total": 42,
  "page": 1,
  "limit": 20
}
```

#### Get Lead by ID

```
GET /api/lead-nurturing/leads/{lead_id}
```

Get a specific lead by ID.

Response:
```json
{
  "id": "lead-123",
  "name": "John Doe",
  "email": "john.doe@example.com",
  "phone": "+1234567890",
  "company_id": "company-123",
  "source": "website_form",
  "status": "new",
  "notes": "Interested in our services",
  "created_at": "2025-06-01T12:00:00Z",
  "updated_at": "2025-06-01T12:00:00Z"
}
```

#### Update Lead

```
PUT /api/lead-nurturing/leads/{lead_id}
```

Update a specific lead.

Request body:
```json
{
  "name": "John Doe",
  "email": "john.doe@example.com",
  "phone": "+1234567890",
  "status": "contacted",
  "notes": "Interested in our services, sent initial email"
}
```

Response:
```json
{
  "id": "lead-123",
  "name": "John Doe",
  "email": "john.doe@example.com",
  "phone": "+1234567890",
  "company_id": "company-123",
  "source": "website_form",
  "status": "contacted",
  "notes": "Interested in our services, sent initial email",
  "created_at": "2025-06-01T12:00:00Z",
  "updated_at": "2025-06-01T12:30:00Z"
}
```

#### Delete Lead

```
DELETE /api/lead-nurturing/leads/{lead_id}
```

Delete a specific lead.

Response:
```json
{
  "success": true,
  "message": "Lead deleted successfully"
}
```

#### Create Interaction

```
POST /api/lead-nurturing/interactions
```

Create a new interaction with a lead.

Request body:
```json
{
  "lead_id": "lead-123",
  "type": "email",
  "direction": "outbound",
  "content": "Hi John, thank you for your interest in our services.",
  "channel": "manual",
  "metadata": {
    "subject": "Thank you for your interest"
  }
}
```

Response:
```json
{
  "id": "interaction-123",
  "company_id": "company-123",
  "lead_id": "lead-123",
  "type": "email",
  "direction": "outbound",
  "content": "Hi John, thank you for your interest in our services.",
  "channel": "manual",
  "status": "delivered",
  "created_at": "2025-06-01T12:30:00Z",
  "metadata": {
    "subject": "Thank you for your interest"
  }
}
```

#### Get Interactions

```
GET /api/lead-nurturing/interactions
```

Get a list of interactions.

Query parameters:
- `lead_id` (optional): Filter by lead ID
- `type` (optional): Filter by type (email, sms)
- `direction` (optional): Filter by direction (inbound, outbound)
- `page` (optional): Page number for pagination (default: 1)
- `limit` (optional): Number of items per page (default: 20)

Response:
```json
{
  "items": [
    {
      "id": "interaction-123",
      "company_id": "company-123",
      "lead_id": "lead-123",
      "type": "email",
      "direction": "outbound",
      "content": "Hi John, thank you for your interest in our services.",
      "channel": "manual",
      "status": "delivered",
      "created_at": "2025-06-01T12:30:00Z",
      "metadata": {
        "subject": "Thank you for your interest"
      }
    },
    // More interactions...
  ],
  "total": 15,
  "page": 1,
  "limit": 20
}
```

#### Get Lead Nurturing Analytics

```
GET /api/lead-nurturing/analytics
```

Get analytics data for lead nurturing.

Query parameters:
- `start_date` (optional): Start date for analytics (format: YYYY-MM-DD)
- `end_date` (optional): End date for analytics (format: YYYY-MM-DD)

Response:
```json
{
  "total_leads": 42,
  "leads_by_source": {
    "website_form": 25,
    "ad_campaign": 10,
    "manual_entry": 5,
    "crm": 2
  },
  "leads_by_status": {
    "new": 10,
    "contacted": 15,
    "engaged": 8,
    "qualified": 5,
    "converted": 3,
    "lost": 1
  },
  "response_rate": 0.85,
  "engagement_rate": 0.65,
  "conversion_rate": 0.12,
  "average_time_to_conversion": 7.5,
  "interactions_by_type": {
    "email": 75,
    "sms": 25
  }
}
```

### Review & Referral API

#### Create a Review Request

```
POST /api/review-referral/reviews
```

Create a new review request.

Request body:
```json
{
  "customer_id": "customer-123",
  "sale_id": "sale-123"
}
```

Response:
```json
{
  "id": "review-123",
  "company_id": "company-123",
  "customer_id": "customer-123",
  "sale_id": "sale-123",
  "rating": null,
  "content": null,
  "platform": null,
  "status": "requested",
  "request_sent_at": null,
  "submitted_at": null,
  "verified_at": null,
  "created_at": "2025-06-01T12:00:00Z",
  "updated_at": "2025-06-01T12:00:00Z"
}
```

#### Get Reviews

```
GET /api/review-referral/reviews
```

Get a list of reviews.

Query parameters:
- `status` (optional): Filter by status (requested, submitted, verified)
- `platform` (optional): Filter by platform (google, yelp)
- `page` (optional): Page number for pagination (default: 1)
- `limit` (optional): Number of items per page (default: 20)

Response:
```json
{
  "items": [
    {
      "id": "review-123",
      "company_id": "company-123",
      "customer_id": "customer-123",
      "sale_id": "sale-123",
      "rating": 5,
      "content": "Great service!",
      "platform": "google",
      "status": "submitted",
      "request_sent_at": "2025-06-01T12:00:00Z",
      "submitted_at": "2025-06-02T10:00:00Z",
      "verified_at": null,
      "created_at": "2025-06-01T12:00:00Z",
      "updated_at": "2025-06-02T10:00:00Z"
    },
    // More reviews...
  ],
  "total": 18,
  "page": 1,
  "limit": 20
}
```

#### Get Review by ID

```
GET /api/review-referral/reviews/{review_id}
```

Get a specific review by ID.

Response:
```json
{
  "id": "review-123",
  "company_id": "company-123",
  "customer_id": "customer-123",
  "sale_id": "sale-123",
  "rating": 5,
  "content": "Great service!",
  "platform": "google",
  "status": "submitted",
  "request_sent_at": "2025-06-01T12:00:00Z",
  "submitted_at": "2025-06-02T10:00:00Z",
  "verified_at": null,
  "created_at": "2025-06-01T12:00:00Z",
  "updated_at": "2025-06-02T10:00:00Z"
}
```

#### Update Review

```
PUT /api/review-referral/reviews/{review_id}
```

Update a specific review.

Request body:
```json
{
  "rating": 5,
  "content": "Great service!",
  "platform": "google",
  "status": "submitted",
  "submitted_at": "2025-06-02T10:00:00Z"
}
```

Response:
```json
{
  "id": "review-123",
  "company_id": "company-123",
  "customer_id": "customer-123",
  "sale_id": "sale-123",
  "rating": 5,
  "content": "Great service!",
  "platform": "google",
  "status": "submitted",
  "request_sent_at": "2025-06-01T12:00:00Z",
  "submitted_at": "2025-06-02T10:00:00Z",
  "verified_at": null,
  "created_at": "2025-06-01T12:00:00Z",
  "updated_at": "2025-06-02T10:00:00Z"
}
```

#### Create Referral

```
POST /api/review-referral/referrals
```

Create a new referral.

Request body:
```json
{
  "customer_id": "customer-123",
  "review_id": "review-123"
}
```

Response:
```json
{
  "id": "referral-123",
  "company_id": "company-123",
  "customer_id": "customer-123",
  "review_id": "review-123",
  "code": "ACME123",
  "status": "created",
  "offer": {
    "referrer_offer": "10% off next purchase",
    "description": "$20 off for new customers"
  },
  "created_at": "2025-06-02T11:00:00Z",
  "updated_at": "2025-06-02T11:00:00Z",
  "expires_at": "2025-07-02T11:00:00Z"
}
```

#### Get Referrals

```
GET /api/review-referral/referrals
```

Get a list of referrals.

Query parameters:
- `status` (optional): Filter by status (created, sent, used, expired)
- `page` (optional): Page number for pagination (default: 1)
- `limit` (optional): Number of items per page (default: 20)

Response:
```json
{
  "items": [
    {
      "id": "referral-123",
      "company_id": "company-123",
      "customer_id": "customer-123",
      "review_id": "review-123",
      "code": "ACME123",
      "status": "created",
      "offer": {
        "referrer_offer": "10% off next purchase",
        "description": "$20 off for new customers"
      },
      "created_at": "2025-06-02T11:00:00Z",
      "updated_at": "2025-06-02T11:00:00Z",
      "expires_at": "2025-07-02T11:00:00Z"
    },
    // More referrals...
  ],
  "total": 12,
  "page": 1,
  "limit": 20
}
```

#### Get Referral by ID

```
GET /api/review-referral/referrals/{referral_id}
```

Get a specific referral by ID.

Response:
```json
{
  "id": "referral-123",
  "company_id": "company-123",
  "customer_id": "customer-123",
  "review_id": "review-123",
  "code": "ACME123",
  "status": "created",
  "offer": {
    "referrer_offer": "10% off next purchase",
    "description": "$20 off for new customers"
  },
  "created_at": "2025-06-02T11:00:00Z",
  "updated_at": "2025-06-02T11:00:00Z",
  "expires_at": "2025-07-02T11:00:00Z"
}
```

#### Process Referral Use

```
POST /api/review-referral/referrals/use
```

Process the use of a referral code.

Request body:
```json
{
  "code": "ACME123",
  "lead_id": "lead-456"
}
```

Response:
```json
{
  "success": true,
  "referral_id": "referral-123",
  "lead_id": "lead-456",
  "offer": {
    "description": "$20 off for new customers"
  }
}
```

#### Get Review & Referral Analytics

```
GET /api/review-referral/analytics
```

Get analytics data for reviews and referrals.

Query parameters:
- `start_date` (optional): Start date for analytics (format: YYYY-MM-DD)
- `end_date` (optional): End date for analytics (format: YYYY-MM-DD)

Response:
```json
{
  "review_requests": {
    "sent": 50,
    "completed": 35
  },
  "average_rating": 4.7,
  "rating_distribution": {
    "1": 0,
    "2": 1,
    "3": 3,
    "4": 10,
    "5": 21
  },
  "platform_distribution": {
    "google": 20,
    "yelp": 15
  },
  "referral_offers": {
    "sent": 30,
    "used": 12
  },
  "referral_conversion_rate": 0.4,
  "estimated_revenue": 2400
}
```

### Content Generation API

#### Generate Blog Post

```
POST /api/content-generation/blog-post
```

Generate a blog post.

Request body:
```json
{
  "topic": "custom software",
  "word_count": 800,
  "keywords": "software development, custom solutions, business growth",
  "call_to_action": "Contact us for a free consultation"
}
```

Response:
```json
{
  "message": "Generating blog post on topic 'custom software' in the background",
  "status": "pending"
}
```

#### Generate Social Media Post

```
POST /api/content-generation/social-media
```

Generate a social media post.

Request body:
```json
{
  "topic": "custom software",
  "platform": "linkedin",
  "hashtags": "#software #development #business",
  "call_to_action": "Visit our website"
}
```

Response:
```json
{
  "message": "Generating linkedin post on topic 'custom software' in the background",
  "status": "pending"
}
```

#### Generate Email Newsletter

```
POST /api/content-generation/email-newsletter
```

Generate an email newsletter.

Request body:
```json
{
  "topic": "monthly update",
  "newsletter_type": "monthly update",
  "content_sections": "company news, industry insights, tips",
  "primary_goal": "nurture relationships",
  "call_to_action": "Schedule a call",
  "word_count": 500
}
```

Response:
```json
{
  "message": "Generating email newsletter on topic 'monthly update' in the background",
  "status": "pending"
}
```

#### Generate Product Description

```
POST /api/content-generation/product-description
```

Generate a product description.

Request body:
```json
{
  "product_name": "Custom CRM Solution",
  "product_category": "CRM",
  "key_features": "Contact management, Sales pipeline, Reporting",
  "primary_benefits": "Increased productivity, Better customer insights",
  "technical_specifications": "Cloud-based, Mobile app, API integration",
  "price_point": "Starting at $99/month",
  "unique_selling_proposition": "Fully customizable to your business processes",
  "platform": "website",
  "keywords": "CRM, customer relationship management, sales"
}
```

Response:
```json
{
  "message": "Generating product description for 'Custom CRM Solution' in the background",
  "status": "pending"
}
```

#### Schedule Content Generation

```
POST /api/content-generation/schedule
```

Schedule content generation.

Request body:
```json
{
  "content_type": "blog_post",
  "frequency": "weekly",
  "day_of_week": "Monday",
  "time_of_day": "09:00",
  "topics": ["software development", "business growth", "technology trends"],
  "parameters": {
    "word_count": 800,
    "call_to_action": "Contact us for a free consultation"
  },
  "active": true
}
```

Response:
```json
{
  "success": true,
  "message": "Content generation schedule created/updated successfully",
  "schedule_id": "schedule-123"
}
```

#### Publish Content

```
POST /api/content-generation/publish/{content_id}
```

Publish content to a specified platform.

Request body:
```json
{
  "platform": "wordpress"
}
```

Response:
```json
{
  "message": "Publishing content content-123 to wordpress in the background",
  "status": "pending"
}
```

#### Get Content

```
GET /api/content-generation/content/{content_id}
```

Get content by ID.

Response:
```json
{
  "message": "Content content-123 retrieved successfully",
  "content": {
    "id": "content-123",
    "title": "How Custom Software Can Boost Your Business",
    "content": "This is a sample blog post content...",
    "status": "draft"
  }
}
```

#### Get Content Schedules

```
GET /api/content-generation/schedules
```

Get content generation schedules.

Response:
```json
{
  "message": "Content generation schedules retrieved successfully",
  "schedules": [
    {
      "id": "schedule-123",
      "content_type": "blog_post",
      "frequency": "weekly",
      "day_of_week": "Monday",
      "time_of_day": "09:00",
      "active": true
    }
  ]
}
```

#### Get Content Generation Analytics

```
GET /api/content-generation/analytics
```

Get analytics data for content generation.

Query parameters:
- `start_date` (optional): Start date for analytics (format: YYYY-MM-DD)
- `end_date` (optional): End date for analytics (format: YYYY-MM-DD)

Response:
```json
{
  "content_created": {
    "blog_post": 12,
    "social_media": 48,
    "email_newsletter": 4,
    "product_description": 8
  },
  "publishing_success_rate": 0.95,
  "engagement_metrics": {
    "views": 15000,
    "clicks": 750,
    "shares": 120
  },
  "conversion_metrics": {
    "leads": 45,
    "sales": 8
  },
  "top_performing_content": [
    {
      "id": "content-123",
      "title": "How Custom Software Can Boost Your Business",
      "type": "blog_post",
      "views": 2500,
      "clicks": 150
    },
    // More content...
  ]
}
```

### User Management API

#### Create User

```
POST /api/users
```

Create a new user.

Request body:
```json
{
  "username": "user@example.com",
  "email": "user@example.com",
  "password": "password",
  "full_name": "John Doe",
  "role": "user"
}
```

Response:
```json
{
  "id": "user-123",
  "username": "user@example.com",
  "email": "user@example.com",
  "full_name": "John Doe",
  "company_id": "company-123",
  "role": "user",
  "is_active": true,
  "created_at": "2025-06-01T12:00:00Z",
  "updated_at": "2025-06-01T12:00:00Z"
}
```

#### Get Users

```
GET /api/users
```

Get a list of users.

Query parameters:
- `role` (optional): Filter by role (admin, manager, user)
- `is_active` (optional): Filter by active status (true, false)
- `page` (optional): Page number for pagination (default: 1)
- `limit` (optional): Number of items per page (default: 20)

Response:
```json
{
  "items": [
    {
      "id": "user-123",
      "username": "user@example.com",
      "email": "user@example.com",
      "full_name": "John Doe",
      "company_id": "company-123",
      "role": "user",
      "is_active": true,
      "created_at": "2025-06-01T12:00:00Z",
      "updated_at": "2025-06-01T12:00:00Z"
    },
    // More users...
  ],
  "total": 5,
  "page": 1,
  "limit": 20
}
```

#### Get User by ID

```
GET /api/users/{user_id}
```

Get a specific user by ID.

Response:
```json
{
  "id": "user-123",
  "username": "user@example.com",
  "email": "user@example.com",
  "full_name": "John Doe",
  "company_id": "company-123",
  "role": "user",
  "is_active": true,
  "created_at": "2025-06-01T12:00:00Z",
  "updated_at": "2025-06-01T12:00:00Z"
}
```

#### Update User

```
PUT /api/users/{user_id}
```

Update a specific user.

Request body:
```json
{
  "full_name": "John Smith",
  "role": "manager",
  "is_active": true
}
```

Response:
```json
{
  "id": "user-123",
  "username": "user@example.com",
  "email": "user@example.com",
  "full_name": "John Smith",
  "company_id": "company-123",
  "role": "manager",
  "is_active": true,
  "created_at": "2025-06-01T12:00:00Z",
  "updated_at": "2025-06-01T12:30:00Z"
}
```

#### Delete User

```
DELETE /api/users/{user_id}
```

Delete a specific user.

Response:
```json
{
  "success": true,
  "message": "User deleted successfully"
}
```

#### Get Current User

```
GET /api/users/me
```

Get the current authenticated user.

Response:
```json
{
  "id": "user-123",
  "username": "user@example.com",
  "email": "user@example.com",
  "full_name": "John Doe",
  "company_id": "company-123",
  "role": "user",
  "is_active": true,
  "created_at": "2025-06-01T12:00:00Z",
  "updated_at": "2025-06-01T12:00:00Z"
}
```

### System API

#### Get System Health

```
GET /api/system/health
```

Get the health status of the system.

Response:
```json
{
  "status": "healthy",
  "version": "1.0.0",
  "database": "connected",
  "api": "operational",
  "services": {
    "openai": "operational",
    "email": "operational",
    "sms": "operational"
  }
}
```

#### Get System Stats

```
GET /api/system/stats
```

Get system statistics.

Response:
```json
{
  "users": 5,
  "companies": 1,
  "leads": 42,
  "reviews": 18,
  "referrals": 12,
  "content": 72,
  "api_calls": {
    "total": 15000,
    "last_24h": 500
  },
  "storage": {
    "used": "1.2 GB",
    "total": "10 GB"
  }
}
```

#### Backup System

```
POST /api/system/backup
```

Create a system backup.

Response:
```json
{
  "success": true,
  "message": "Backup created successfully",
  "backup_id": "backup-123",
  "created_at": "2025-06-01T12:00:00Z",
  "size": "1.2 GB"
}
```

#### Restore System

```
POST /api/system/restore
```

Restore the system from a backup.

Request body:
```json
{
  "backup_id": "backup-123"
}
```

Response:
```json
{
  "success": true,
  "message": "System restored successfully",
  "backup_id": "backup-123",
  "restored_at": "2025-06-01T12:30:00Z"
}
```

## Webhooks

The API supports webhooks for event notifications. To register a webhook:

```
POST /api/webhooks
```

Request body:
```json
{
  "url": "https://example.com/webhook",
  "events": ["lead.created", "review.submitted", "content.published"],
  "secret": "your_webhook_secret"
}
```

Response:
```json
{
  "id": "webhook-123",
  "url": "https://example.com/webhook",
  "events": ["lead.created", "review.submitted", "content.published"],
  "created_at": "2025-06-01T12:00:00Z",
  "updated_at": "2025-06-01T12:00:00Z"
}
```

Webhook payloads include:

```json
{
  "event": "lead.created",
  "timestamp": "2025-06-01T12:00:00Z",
  "data": {
    "id": "lead-123",
    "name": "John Doe",
    "email": "john.doe@example.com",
    "source": "website_form"
  }
}
```

## Pagination

List endpoints support pagination using the `page` and `limit` query parameters:

```
GET /api/lead-nurturing/leads?page=2&limit=10
```

Paginated responses include:

```json
{
  "items": [...],
  "total": 42,
  "page": 2,
  "limit": 10
}
```

## Filtering

Many endpoints support filtering using query parameters:

```
GET /api/lead-nurturing/leads?status=new&source=website_form
```

## Sorting

Some endpoints support sorting using the `sort` and `order` query parameters:

```
GET /api/lead-nurturing/leads?sort=created_at&order=desc
```

## Versioning

The API uses URL versioning. The current version is v1:

```
https://api.businessautomationsystem.com/v1/...
```

## CORS

The API supports Cross-Origin Resource Sharing (CORS) for all origins by default.

## Rate Limiting Headers

Rate limit information is included in the response headers:

```
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 99
X-RateLimit-Reset: 1622548800
```

## Changelog

### v1.0.0 (2025-06-01)

- Initial release with Lead Nurturing, Review & Referral, and Content Generation workflows
- User management and system administration
- Authentication and authorization
- Webhooks and event notifications


# Business Automation System - API Endpoints

## Overview

This document outlines the REST API endpoints for the Business Automation System. The API is organized around resources and follows RESTful principles. All requests and responses are in JSON format.

## Base URL

```
https://api.business-automation-system.com/v1
```

## Authentication

All API requests require authentication using JWT tokens. Include the token in the Authorization header:

```
Authorization: Bearer <token>
```

## Common Response Codes

- `200 OK`: Request succeeded
- `201 Created`: Resource created successfully
- `400 Bad Request`: Invalid request parameters
- `401 Unauthorized`: Authentication failed
- `403 Forbidden`: Permission denied
- `404 Not Found`: Resource not found
- `422 Unprocessable Entity`: Validation error
- `500 Internal Server Error`: Server error

## API Endpoints

### Authentication

#### Register User

```
POST /auth/register
```

Request body:
```json
{
  "email": "user@example.com",
  "password": "securepassword",
  "name": "John Doe",
  "company_name": "Acme Inc"
}
```

Response:
```json
{
  "user_id": "usr_123456",
  "company_id": "cmp_123456",
  "email": "user@example.com",
  "name": "John Doe",
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

#### Login

```
POST /auth/login
```

Request body:
```json
{
  "email": "user@example.com",
  "password": "securepassword"
}
```

Response:
```json
{
  "user_id": "usr_123456",
  "company_id": "cmp_123456",
  "email": "user@example.com",
  "name": "John Doe",
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

#### Refresh Token

```
POST /auth/refresh
```

Request body:
```json
{
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

Response:
```json
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

### Users

#### Get Current User

```
GET /users/me
```

Response:
```json
{
  "id": "usr_123456",
  "email": "user@example.com",
  "name": "John Doe",
  "company_id": "cmp_123456",
  "role": "admin",
  "created_at": "2023-01-01T00:00:00Z",
  "last_login": "2023-01-02T00:00:00Z",
  "settings": {
    "notifications": {
      "email": true,
      "push": false
    },
    "theme": "light"
  }
}
```

#### Update User

```
PATCH /users/me
```

Request body:
```json
{
  "name": "John Smith",
  "settings": {
    "notifications": {
      "email": false
    }
  }
}
```

Response:
```json
{
  "id": "usr_123456",
  "email": "user@example.com",
  "name": "John Smith",
  "company_id": "cmp_123456",
  "role": "admin",
  "created_at": "2023-01-01T00:00:00Z",
  "last_login": "2023-01-02T00:00:00Z",
  "settings": {
    "notifications": {
      "email": false,
      "push": false
    },
    "theme": "light"
  }
}
```

### Company

#### Get Company

```
GET /companies/current
```

Response:
```json
{
  "id": "cmp_123456",
  "name": "Acme Inc",
  "industry": "Technology",
  "website": "https://acme.example.com",
  "logo_url": "https://storage.example.com/logos/acme.png",
  "created_at": "2023-01-01T00:00:00Z",
  "subscription_tier": "professional",
  "subscription_status": "active",
  "settings": {
    "branding": {
      "primary_color": "#336699",
      "secondary_color": "#66AACC"
    }
  },
  "integrations": {
    "email": {
      "provider": "sendgrid",
      "configured": true
    },
    "sms": {
      "provider": "twilio",
      "configured": false
    }
  }
}
```

#### Update Company

```
PATCH /companies/current
```

Request body:
```json
{
  "name": "Acme Corporation",
  "website": "https://acmecorp.example.com",
  "settings": {
    "branding": {
      "primary_color": "#003366"
    }
  }
}
```

Response:
```json
{
  "id": "cmp_123456",
  "name": "Acme Corporation",
  "industry": "Technology",
  "website": "https://acmecorp.example.com",
  "logo_url": "https://storage.example.com/logos/acme.png",
  "created_at": "2023-01-01T00:00:00Z",
  "subscription_tier": "professional",
  "subscription_status": "active",
  "settings": {
    "branding": {
      "primary_color": "#003366",
      "secondary_color": "#66AACC"
    }
  },
  "integrations": {
    "email": {
      "provider": "sendgrid",
      "configured": true
    },
    "sms": {
      "provider": "twilio",
      "configured": false
    }
  }
}
```

### Leads

#### List Leads

```
GET /leads
```

Query parameters:
- `status`: Filter by status (optional)
- `source`: Filter by source (optional)
- `page`: Page number (default: 1)
- `per_page`: Items per page (default: 20)
- `sort_by`: Field to sort by (default: created_at)
- `sort_dir`: Sort direction (asc/desc, default: desc)

Response:
```json
{
  "data": [
    {
      "id": "lead_123456",
      "name": "Jane Smith",
      "email": "jane@example.com",
      "phone": "+1234567890",
      "source": "website_form",
      "status": "new",
      "created_at": "2023-01-15T00:00:00Z",
      "updated_at": "2023-01-15T00:00:00Z",
      "tags": ["interested", "high_value"],
      "assigned_to": "usr_123456"
    },
    {
      "id": "lead_123457",
      "name": "Bob Johnson",
      "email": "bob@example.com",
      "phone": "+1987654321",
      "source": "manual",
      "status": "contacted",
      "created_at": "2023-01-14T00:00:00Z",
      "updated_at": "2023-01-15T00:00:00Z",
      "tags": ["follow_up"],
      "assigned_to": null
    }
  ],
  "meta": {
    "current_page": 1,
    "per_page": 20,
    "total_items": 42,
    "total_pages": 3
  }
}
```

#### Create Lead

```
POST /leads
```

Request body:
```json
{
  "name": "Alice Brown",
  "email": "alice@example.com",
  "phone": "+1122334455",
  "source": "referral",
  "notes": "Referred by Bob Johnson",
  "tags": ["warm_lead"],
  "custom_fields": {
    "company": "XYZ Corp",
    "position": "Marketing Director"
  }
}
```

Response:
```json
{
  "id": "lead_123458",
  "name": "Alice Brown",
  "email": "alice@example.com",
  "phone": "+1122334455",
  "source": "referral",
  "status": "new",
  "created_at": "2023-01-16T00:00:00Z",
  "updated_at": "2023-01-16T00:00:00Z",
  "notes": "Referred by Bob Johnson",
  "tags": ["warm_lead"],
  "assigned_to": null,
  "custom_fields": {
    "company": "XYZ Corp",
    "position": "Marketing Director"
  }
}
```

#### Get Lead

```
GET /leads/{lead_id}
```

Response:
```json
{
  "id": "lead_123456",
  "name": "Jane Smith",
  "email": "jane@example.com",
  "phone": "+1234567890",
  "source": "website_form",
  "status": "new",
  "created_at": "2023-01-15T00:00:00Z",
  "updated_at": "2023-01-15T00:00:00Z",
  "notes": "Interested in premium package",
  "tags": ["interested", "high_value"],
  "assigned_to": "usr_123456",
  "custom_fields": {
    "budget": "$5000-$10000",
    "timeline": "3 months"
  },
  "interactions": [
    {
      "id": "int_123456",
      "type": "email",
      "direction": "outbound",
      "content": "Hello Jane, thank you for your interest...",
      "status": "delivered",
      "created_at": "2023-01-15T01:00:00Z"
    }
  ]
}
```

#### Update Lead

```
PATCH /leads/{lead_id}
```

Request body:
```json
{
  "status": "qualified",
  "notes": "Interested in premium package, follow up next week",
  "assigned_to": "usr_123456"
}
```

Response:
```json
{
  "id": "lead_123456",
  "name": "Jane Smith",
  "email": "jane@example.com",
  "phone": "+1234567890",
  "source": "website_form",
  "status": "qualified",
  "created_at": "2023-01-15T00:00:00Z",
  "updated_at": "2023-01-16T00:00:00Z",
  "notes": "Interested in premium package, follow up next week",
  "tags": ["interested", "high_value"],
  "assigned_to": "usr_123456",
  "custom_fields": {
    "budget": "$5000-$10000",
    "timeline": "3 months"
  }
}
```

#### Delete Lead

```
DELETE /leads/{lead_id}
```

Response:
```
204 No Content
```

### Interactions

#### List Lead Interactions

```
GET /leads/{lead_id}/interactions
```

Query parameters:
- `type`: Filter by type (optional)
- `page`: Page number (default: 1)
- `per_page`: Items per page (default: 20)

Response:
```json
{
  "data": [
    {
      "id": "int_123456",
      "lead_id": "lead_123456",
      "type": "email",
      "direction": "outbound",
      "content": "Hello Jane, thank you for your interest...",
      "channel": "automated_workflow",
      "status": "delivered",
      "created_at": "2023-01-15T01:00:00Z",
      "created_by": "system",
      "metadata": {
        "email_id": "email_123456",
        "template_id": "template_123"
      }
    },
    {
      "id": "int_123457",
      "lead_id": "lead_123456",
      "type": "email",
      "direction": "inbound",
      "content": "Thank you for reaching out. I'd like to schedule a call...",
      "channel": "reply",
      "status": "received",
      "created_at": "2023-01-15T02:00:00Z",
      "created_by": null,
      "metadata": {
        "email_id": "email_123457"
      }
    }
  ],
  "meta": {
    "current_page": 1,
    "per_page": 20,
    "total_items": 2,
    "total_pages": 1
  }
}
```

#### Create Interaction

```
POST /leads/{lead_id}/interactions
```

Request body:
```json
{
  "type": "email",
  "direction": "outbound",
  "content": "Hello Jane, following up on our previous conversation...",
  "channel": "manual",
  "status": "delivered"
}
```

Response:
```json
{
  "id": "int_123458",
  "lead_id": "lead_123456",
  "type": "email",
  "direction": "outbound",
  "content": "Hello Jane, following up on our previous conversation...",
  "channel": "manual",
  "status": "delivered",
  "created_at": "2023-01-16T00:00:00Z",
  "created_by": "usr_123456",
  "metadata": {}
}
```

### Customers

#### List Customers

```
GET /customers
```

Query parameters:
- `page`: Page number (default: 1)
- `per_page`: Items per page (default: 20)
- `sort_by`: Field to sort by (default: created_at)
- `sort_dir`: Sort direction (asc/desc, default: desc)

Response:
```json
{
  "data": [
    {
      "id": "cust_123456",
      "name": "Jane Smith",
      "email": "jane@example.com",
      "phone": "+1234567890",
      "created_at": "2023-01-10T00:00:00Z",
      "updated_at": "2023-01-15T00:00:00Z",
      "lifetime_value": 1500.00,
      "tags": ["vip", "repeat"]
    },
    {
      "id": "cust_123457",
      "name": "Bob Johnson",
      "email": "bob@example.com",
      "phone": "+1987654321",
      "created_at": "2023-01-05T00:00:00Z",
      "updated_at": "2023-01-14T00:00:00Z",
      "lifetime_value": 750.00,
      "tags": ["new"]
    }
  ],
  "meta": {
    "current_page": 1,
    "per_page": 20,
    "total_items": 35,
    "total_pages": 2
  }
}
```

#### Create Customer

```
POST /customers
```

Request body:
```json
{
  "name": "Alice Brown",
  "email": "alice@example.com",
  "phone": "+1122334455",
  "lead_id": "lead_123458",
  "tags": ["new"],
  "custom_fields": {
    "company": "XYZ Corp",
    "position": "Marketing Director"
  }
}
```

Response:
```json
{
  "id": "cust_123458",
  "name": "Alice Brown",
  "email": "alice@example.com",
  "phone": "+1122334455",
  "lead_id": "lead_123458",
  "created_at": "2023-01-16T00:00:00Z",
  "updated_at": "2023-01-16T00:00:00Z",
  "lifetime_value": 0.00,
  "tags": ["new"],
  "custom_fields": {
    "company": "XYZ Corp",
    "position": "Marketing Director"
  }
}
```

#### Get Customer

```
GET /customers/{customer_id}
```

Response:
```json
{
  "id": "cust_123456",
  "name": "Jane Smith",
  "email": "jane@example.com",
  "phone": "+1234567890",
  "lead_id": "lead_123456",
  "created_at": "2023-01-10T00:00:00Z",
  "updated_at": "2023-01-15T00:00:00Z",
  "lifetime_value": 1500.00,
  "tags": ["vip", "repeat"],
  "custom_fields": {
    "birthday": "1985-05-15",
    "preferences": "Prefers email communication"
  },
  "sales": [
    {
      "id": "sale_123456",
      "service_id": "serv_123456",
      "service_name": "Premium Package",
      "amount": 1000.00,
      "status": "completed",
      "created_at": "2023-01-10T00:00:00Z"
    },
    {
      "id": "sale_123457",
      "service_id": "serv_123457",
      "service_name": "Maintenance Service",
      "amount": 500.00,
      "status": "completed",
      "created_at": "2023-01-15T00:00:00Z"
    }
  ],
  "reviews": [
    {
      "id": "rev_123456",
      "platform": "Google",
      "rating": 5,
      "status": "completed",
      "completed_at": "2023-01-12T00:00:00Z"
    }
  ],
  "referrals": [
    {
      "id": "ref_123456",
      "code": "JANE10",
      "status": "active",
      "times_used": 2,
      "created_at": "2023-01-13T00:00:00Z"
    }
  ]
}
```

#### Update Customer

```
PATCH /customers/{customer_id}
```

Request body:
```json
{
  "phone": "+1234567891",
  "tags": ["vip", "repeat", "priority"],
  "custom_fields": {
    "preferences": "Prefers phone communication"
  }
}
```

Response:
```json
{
  "id": "cust_123456",
  "name": "Jane Smith",
  "email": "jane@example.com",
  "phone": "+1234567891",
  "lead_id": "lead_123456",
  "created_at": "2023-01-10T00:00:00Z",
  "updated_at": "2023-01-16T00:00:00Z",
  "lifetime_value": 1500.00,
  "tags": ["vip", "repeat", "priority"],
  "custom_fields": {
    "birthday": "1985-05-15",
    "preferences": "Prefers phone communication"
  }
}
```

### Sales

#### List Sales

```
GET /sales
```

Query parameters:
- `customer_id`: Filter by customer (optional)
- `status`: Filter by status (optional)
- `page`: Page number (default: 1)
- `per_page`: Items per page (default: 20)
- `sort_by`: Field to sort by (default: created_at)
- `sort_dir`: Sort direction (asc/desc, default: desc)

Response:
```json
{
  "data": [
    {
      "id": "sale_123456",
      "customer_id": "cust_123456",
      "customer_name": "Jane Smith",
      "service_id": "serv_123456",
      "service_name": "Premium Package",
      "amount": 1000.00,
      "status": "completed",
      "created_at": "2023-01-10T00:00:00Z",
      "payment_method": "credit_card"
    },
    {
      "id": "sale_123457",
      "customer_id": "cust_123456",
      "customer_name": "Jane Smith",
      "service_id": "serv_123457",
      "service_name": "Maintenance Service",
      "amount": 500.00,
      "status": "completed",
      "created_at": "2023-01-15T00:00:00Z",
      "payment_method": "credit_card"
    }
  ],
  "meta": {
    "current_page": 1,
    "per_page": 20,
    "total_items": 28,
    "total_pages": 2
  }
}
```

#### Create Sale

```
POST /sales
```

Request body:
```json
{
  "customer_id": "cust_123456",
  "service_id": "serv_123458",
  "amount": 750.00,
  "status": "completed",
  "payment_method": "bank_transfer",
  "notes": "Includes 10% discount"
}
```

Response:
```json
{
  "id": "sale_123458",
  "customer_id": "cust_123456",
  "customer_name": "Jane Smith",
  "service_id": "serv_123458",
  "service_name": "Consultation Service",
  "amount": 750.00,
  "status": "completed",
  "created_at": "2023-01-16T00:00:00Z",
  "payment_method": "bank_transfer",
  "notes": "Includes 10% discount",
  "referral_id": null
}
```

### Reviews

#### List Reviews

```
GET /reviews
```

Query parameters:
- `customer_id`: Filter by customer (optional)
- `status`: Filter by status (optional)
- `platform`: Filter by platform (optional)
- `page`: Page number (default: 1)
- `per_page`: Items per page (default: 20)

Response:
```json
{
  "data": [
    {
      "id": "rev_123456",
      "customer_id": "cust_123456",
      "customer_name": "Jane Smith",
      "sale_id": "sale_123456",
      "platform": "Google",
      "rating": 5,
      "content": "Excellent service! Highly recommended.",
      "status": "completed",
      "request_sent_at": "2023-01-11T00:00:00Z",
      "completed_at": "2023-01-12T00:00:00Z",
      "review_url": "https://g.co/review/abc123"
    },
    {
      "id": "rev_123457",
      "customer_id": "cust_123457",
      "customer_name": "Bob Johnson",
      "sale_id": "sale_123459",
      "platform": "Yelp",
      "rating": 4,
      "content": "Great service, would use again.",
      "status": "completed",
      "request_sent_at": "2023-01-06T00:00:00Z",
      "completed_at": "2023-01-07T00:00:00Z",
      "review_url": "https://yelp.com/review/def456"
    }
  ],
  "meta": {
    "current_page": 1,
    "per_page": 20,
    "total_items": 15,
    "total_pages": 1
  }
}
```

#### Create Review Request

```
POST /reviews/request
```

Request body:
```json
{
  "customer_id": "cust_123456",
  "sale_id": "sale_123457",
  "platform": "Google",
  "message_template": "thank_you_review_request"
}
```

Response:
```json
{
  "id": "rev_123458",
  "customer_id": "cust_123456",
  "customer_name": "Jane Smith",
  "sale_id": "sale_123457",
  "platform": "Google",
  "rating": null,
  "content": null,
  "status": "requested",
  "request_sent_at": "2023-01-16T00:00:00Z",
  "completed_at": null,
  "review_url": null
}
```

#### Update Review

```
PATCH /reviews/{review_id}
```

Request body:
```json
{
  "status": "completed",
  "rating": 5,
  "content": "Amazing service! Will definitely recommend to friends.",
  "review_url": "https://g.co/review/ghi789"
}
```

Response:
```json
{
  "id": "rev_123458",
  "customer_id": "cust_123456",
  "customer_name": "Jane Smith",
  "sale_id": "sale_123457",
  "platform": "Google",
  "rating": 5,
  "content": "Amazing service! Will definitely recommend to friends.",
  "status": "completed",
  "request_sent_at": "2023-01-16T00:00:00Z",
  "completed_at": "2023-01-16T01:00:00Z",
  "review_url": "https://g.co/review/ghi789"
}
```

### Referrals

#### List Referrals

```
GET /referrals
```

Query parameters:
- `customer_id`: Filter by customer (optional)
- `status`: Filter by status (optional)
- `page`: Page number (default: 1)
- `per_page`: Items per page (default: 20)

Response:
```json
{
  "data": [
    {
      "id": "ref_123456",
      "customer_id": "cust_123456",
      "customer_name": "Jane Smith",
      "code": "JANE10",
      "offer": "10% off your first purchase",
      "status": "active",
      "created_at": "2023-01-13T00:00:00Z",
      "expires_at": "2023-07-13T00:00:00Z",
      "times_used": 2,
      "max_uses": 10
    },
    {
      "id": "ref_123457",
      "customer_id": "cust_123457",
      "customer_name": "Bob Johnson",
      "code": "BOB15",
      "offer": "15% off your first purchase",
      "status": "active",
      "created_at": "2023-01-08T00:00:00Z",
      "expires_at": "2023-07-08T00:00:00Z",
      "times_used": 1,
      "max_uses": 10
    }
  ],
  "meta": {
    "current_page": 1,
    "per_page": 20,
    "total_items": 12,
    "total_pages": 1
  }
}
```

#### Create Referral

```
POST /referrals
```

Request body:
```json
{
  "customer_id": "cust_123458",
  "offer": "20% off your first purchase",
  "max_uses": 5,
  "expires_in_days": 180
}
```

Response:
```json
{
  "id": "ref_123458",
  "customer_id": "cust_123458",
  "customer_name": "Alice Brown",
  "code": "ALICE20",
  "offer": "20% off your first purchase",
  "status": "active",
  "created_at": "2023-01-16T00:00:00Z",
  "expires_at": "2023-07-15T00:00:00Z",
  "times_used": 0,
  "max_uses": 5
}
```

#### Track Referral Use

```
POST /referrals/{referral_id}/track
```

Request body:
```json
{
  "lead_id": "lead_123460"
}
```

Response:
```json
{
  "id": "ref_123456",
  "customer_id": "cust_123456",
  "customer_name": "Jane Smith",
  "code": "JANE10",
  "offer": "10% off your first purchase",
  "status": "active",
  "created_at": "2023-01-13T00:00:00Z",
  "expires_at": "2023-07-13T00:00:00Z",
  "times_used": 3,
  "max_uses": 10,
  "uses": [
    {
      "lead_id": "lead_123459",
      "used_at": "2023-01-14T00:00:00Z",
      "converted": true
    },
    {
      "lead_id": "lead_123460",
      "used_at": "2023-01-16T00:00:00Z",
      "converted": false
    }
  ]
}
```

### Content

#### List Content

```
GET /content
```

Query parameters:
- `type`: Filter by type (optional)
- `status`: Filter by status (optional)
- `page`: Page number (default: 1)
- `per_page`: Items per page (default: 20)
- `sort_by`: Field to sort by (default: created_at)
- `sort_dir`: Sort direction (asc/desc, default: desc)

Response:
```json
{
  "data": [
    {
      "id": "cont_123456",
      "title": "10 Ways to Improve Your Business",
      "type": "blog",
      "status": "published",
      "created_at": "2023-01-10T00:00:00Z",
      "published_at": "2023-01-11T00:00:00Z",
      "platform": "WordPress",
      "url": "https://example.com/blog/10-ways-to-improve"
    },
    {
      "id": "cont_123457",
      "title": "New Service Announcement",
      "type": "email",
      "status": "published",
      "created_at": "2023-01-14T00:00:00Z",
      "published_at": "2023-01-15T00:00:00Z",
      "platform": "Mailchimp",
      "url": null
    }
  ],
  "meta": {
    "current_page": 1,
    "per_page": 20,
    "total_items": 18,
    "total_pages": 1
  }
}
```

#### Generate Content

```
POST /content/generate
```

Request body:
```json
{
  "type": "blog",
  "title": "5 Benefits of Business Automation",
  "keywords": ["automation", "efficiency", "business"],
  "tone": "professional",
  "length": "medium"
}
```

Response:
```json
{
  "id": "cont_123458",
  "title": "5 Benefits of Business Automation",
  "type": "blog",
  "body": "In today's fast-paced business environment, automation has become...",
  "status": "draft",
  "created_at": "2023-01-16T00:00:00Z",
  "published_at": null,
  "created_by": "system",
  "platform": null,
  "url": null,
  "tags": ["automation", "efficiency", "business"],
  "metadata": {
    "word_count": 750,
    "reading_time": 4
  }
}
```

#### Get Content

```
GET /content/{content_id}
```

Response:
```json
{
  "id": "cont_123456",
  "title": "10 Ways to Improve Your Business",
  "type": "blog",
  "body": "In the competitive landscape of modern business...",
  "status": "published",
  "created_at": "2023-01-10T00:00:00Z",
  "published_at": "2023-01-11T00:00:00Z",
  "created_by": "system",
  "platform": "WordPress",
  "url": "https://example.com/blog/10-ways-to-improve",
  "tags": ["business", "improvement", "tips"],
  "metadata": {
    "word_count": 1200,
    "reading_time": 6
  },
  "metrics": {
    "views": 342,
    "clicks": 28,
    "shares": 15,
    "comments": 7,
    "conversions": 3
  }
}
```

#### Update Content

```
PATCH /content/{content_id}
```

Request body:
```json
{
  "title": "10 Proven Ways to Improve Your Business",
  "body": "In the competitive landscape of modern business...",
  "status": "scheduled",
  "published_at": "2023-01-17T09:00:00Z"
}
```

Response:
```json
{
  "id": "cont_123456",
  "title": "10 Proven Ways to Improve Your Business",
  "type": "blog",
  "body": "In the competitive landscape of modern business...",
  "status": "scheduled",
  "created_at": "2023-01-10T00:00:00Z",
  "published_at": "2023-01-17T09:00:00Z",
  "created_by": "system",
  "platform": "WordPress",
  "url": null,
  "tags": ["business", "improvement", "tips"],
  "metadata": {
    "word_count": 1200,
    "reading_time": 6
  }
}
```

#### Publish Content

```
POST /content/{content_id}/publish
```

Request body:
```json
{
  "platform": "WordPress",
  "schedule": false
}
```

Response:
```json
{
  "id": "cont_123456",
  "title": "10 Proven Ways to Improve Your Business",
  "type": "blog",
  "status": "published",
  "created_at": "2023-01-10T00:00:00Z",
  "published_at": "2023-01-16T00:00:00Z",
  "platform": "WordPress",
  "url": "https://example.com/blog/10-proven-ways-to-improve"
}
```

### Workflow Configurations

#### List Workflow Configs

```
GET /workflow-configs
```

Query parameters:
- `workflow_type`: Filter by workflow type (optional)
- `active`: Filter by active status (optional)
- `page`: Page number (default: 1)
- `per_page`: Items per page (default: 20)

Response:
```json
{
  "data": [
    {
      "id": "wf_123456",
      "name": "New Lead Follow-up",
      "workflow_type": "lead_nurturing",
      "active": true,
      "created_at": "2023-01-05T00:00:00Z",
      "updated_at": "2023-01-10T00:00:00Z"
    },
    {
      "id": "wf_123457",
      "name": "Post-Sale Review Request",
      "workflow_type": "review_referral",
      "active": true,
      "created_at": "2023-01-06T00:00:00Z",
      "updated_at": "2023-01-12T00:00:00Z"
    },
    {
      "id": "wf_123458",
      "name": "Weekly Blog Post",
      "workflow_type": "content_generation",
      "active": true,
      "created_at": "2023-01-07T00:00:00Z",
      "updated_at": "2023-01-14T00:00:00Z"
    }
  ],
  "meta": {
    "current_page": 1,
    "per_page": 20,
    "total_items": 5,
    "total_pages": 1
  }
}
```

#### Create Workflow Config

```
POST /workflow-configs
```

Request body:
```json
{
  "name": "VIP Lead Follow-up",
  "workflow_type": "lead_nurturing",
  "active": true,
  "triggers": {
    "lead_source": ["referral", "direct"],
    "tags": ["vip"]
  },
  "actions": {
    "initial_delay_minutes": 15,
    "message_template": "vip_lead_template",
    "channel": "email",
    "follow_up": [
      {
        "delay_hours": 24,
        "message_template": "vip_follow_up_1"
      },
      {
        "delay_hours": 72,
        "message_template": "vip_follow_up_2"
      }
    ]
  },
  "templates": {
    "vip_lead_template": "Hello {{name}}, thank you for your interest in our premium services...",
    "vip_follow_up_1": "Hello {{name}}, I wanted to follow up on our previous message...",
    "vip_follow_up_2": "Hello {{name}}, I noticed you haven't had a chance to respond..."
  }
}
```

Response:
```json
{
  "id": "wf_123459",
  "name": "VIP Lead Follow-up",
  "workflow_type": "lead_nurturing",
  "active": true,
  "created_at": "2023-01-16T00:00:00Z",
  "updated_at": "2023-01-16T00:00:00Z",
  "created_by": "usr_123456",
  "triggers": {
    "lead_source": ["referral", "direct"],
    "tags": ["vip"]
  },
  "actions": {
    "initial_delay_minutes": 15,
    "message_template": "vip_lead_template",
    "channel": "email",
    "follow_up": [
      {
        "delay_hours": 24,
        "message_template": "vip_follow_up_1"
      },
      {
        "delay_hours": 72,
        "message_template": "vip_follow_up_2"
      }
    ]
  },
  "templates": {
    "vip_lead_template": "Hello {{name}}, thank you for your interest in our premium services...",
    "vip_follow_up_1": "Hello {{name}}, I wanted to follow up on our previous message...",
    "vip_follow_up_2": "Hello {{name}}, I noticed you haven't had a chance to respond..."
  }
}
```

#### Get Workflow Config

```
GET /workflow-configs/{workflow_id}
```

Response:
```json
{
  "id": "wf_123456",
  "name": "New Lead Follow-up",
  "workflow_type": "lead_nurturing",
  "active": true,
  "created_at": "2023-01-05T00:00:00Z",
  "updated_at": "2023-01-10T00:00:00Z",
  "created_by": "usr_123456",
  "triggers": {
    "lead_source": ["website_form", "landing_page"],
    "tags": []
  },
  "actions": {
    "initial_delay_minutes": 30,
    "message_template": "new_lead_template",
    "channel": "email",
    "follow_up": [
      {
        "delay_hours": 24,
        "message_template": "follow_up_1"
      },
      {
        "delay_hours": 72,
        "message_template": "follow_up_2"
      }
    ]
  },
  "templates": {
    "new_lead_template": "Hello {{name}}, thank you for your interest in our services...",
    "follow_up_1": "Hello {{name}}, I wanted to follow up on our previous message...",
    "follow_up_2": "Hello {{name}}, I noticed you haven't had a chance to respond..."
  },
  "stats": {
    "runs_total": 156,
    "runs_successful": 142,
    "runs_failed": 14,
    "conversion_rate": 0.32
  }
}
```

#### Update Workflow Config

```
PATCH /workflow-configs/{workflow_id}
```

Request body:
```json
{
  "name": "New Lead Follow-up (Updated)",
  "active": true,
  "actions": {
    "initial_delay_minutes": 15,
    "follow_up": [
      {
        "delay_hours": 24,
        "message_template": "follow_up_1"
      },
      {
        "delay_hours": 48,
        "message_template": "follow_up_2"
      },
      {
        "delay_hours": 96,
        "message_template": "follow_up_3"
      }
    ]
  },
  "templates": {
    "follow_up_3": "Hello {{name}}, this is our final follow-up regarding your interest..."
  }
}
```

Response:
```json
{
  "id": "wf_123456",
  "name": "New Lead Follow-up (Updated)",
  "workflow_type": "lead_nurturing",
  "active": true,
  "created_at": "2023-01-05T00:00:00Z",
  "updated_at": "2023-01-16T00:00:00Z",
  "created_by": "usr_123456",
  "triggers": {
    "lead_source": ["website_form", "landing_page"],
    "tags": []
  },
  "actions": {
    "initial_delay_minutes": 15,
    "message_template": "new_lead_template",
    "channel": "email",
    "follow_up": [
      {
        "delay_hours": 24,
        "message_template": "follow_up_1"
      },
      {
        "delay_hours": 48,
        "message_template": "follow_up_2"
      },
      {
        "delay_hours": 96,
        "message_template": "follow_up_3"
      }
    ]
  },
  "templates": {
    "new_lead_template": "Hello {{name}}, thank you for your interest in our services...",
    "follow_up_1": "Hello {{name}}, I wanted to follow up on our previous message...",
    "follow_up_2": "Hello {{name}}, I noticed you haven't had a chance to respond...",
    "follow_up_3": "Hello {{name}}, this is our final follow-up regarding your interest..."
  }
}
```

### Workflow Runs

#### List Workflow Runs

```
GET /workflow-runs
```

Query parameters:
- `workflow_config_id`: Filter by workflow config (optional)
- `status`: Filter by status (optional)
- `page`: Page number (default: 1)
- `per_page`: Items per page (default: 20)
- `sort_by`: Field to sort by (default: started_at)
- `sort_dir`: Sort direction (asc/desc, default: desc)

Response:
```json
{
  "data": [
    {
      "id": "run_123456",
      "workflow_config_id": "wf_123456",
      "workflow_name": "New Lead Follow-up",
      "status": "completed",
      "started_at": "2023-01-15T01:00:00Z",
      "completed_at": "2023-01-15T01:01:00Z",
      "trigger_type": "new_lead",
      "trigger_id": "lead_123456"
    },
    {
      "id": "run_123457",
      "workflow_config_id": "wf_123457",
      "workflow_name": "Post-Sale Review Request",
      "status": "completed",
      "started_at": "2023-01-15T02:00:00Z",
      "completed_at": "2023-01-15T02:01:00Z",
      "trigger_type": "new_sale",
      "trigger_id": "sale_123456"
    }
  ],
  "meta": {
    "current_page": 1,
    "per_page": 20,
    "total_items": 45,
    "total_pages": 3
  }
}
```

#### Get Workflow Run

```
GET /workflow-runs/{run_id}
```

Response:
```json
{
  "id": "run_123456",
  "workflow_config_id": "wf_123456",
  "workflow_name": "New Lead Follow-up",
  "status": "completed",
  "started_at": "2023-01-15T01:00:00Z",
  "completed_at": "2023-01-15T01:01:00Z",
  "trigger_type": "new_lead",
  "trigger_id": "lead_123456",
  "actions_performed": [
    {
      "type": "generate_message",
      "timestamp": "2023-01-15T01:00:10Z",
      "details": {
        "template": "new_lead_template",
        "generated_content": "Hello Jane, thank you for your interest in our services..."
      }
    },
    {
      "type": "send_email",
      "timestamp": "2023-01-15T01:00:30Z",
      "details": {
        "recipient": "jane@example.com",
        "subject": "Thank you for your interest",
        "status": "delivered"
      }
    },
    {
      "type": "schedule_follow_up",
      "timestamp": "2023-01-15T01:00:45Z",
      "details": {
        "scheduled_for": "2023-01-16T01:00:00Z",
        "template": "follow_up_1"
      }
    }
  ],
  "results": {
    "message_delivered": true,
    "follow_up_scheduled": true
  }
}
```

#### Trigger Workflow Run

```
POST /workflow-runs/trigger
```

Request body:
```json
{
  "workflow_config_id": "wf_123456",
  "trigger_type": "manual",
  "entity_id": "lead_123460"
}
```

Response:
```json
{
  "id": "run_123458",
  "workflow_config_id": "wf_123456",
  "workflow_name": "New Lead Follow-up",
  "status": "pending",
  "started_at": "2023-01-16T00:00:00Z",
  "completed_at": null,
  "trigger_type": "manual",
  "trigger_id": "lead_123460"
}
```

### Analytics

#### Get Dashboard Analytics

```
GET /analytics/dashboard
```

Query parameters:
- `start_date`: Start date for analytics (format: YYYY-MM-DD)
- `end_date`: End date for analytics (format: YYYY-MM-DD)
- `compare_to_previous`: Whether to include comparison to previous period (default: true)

Response:
```json
{
  "period": {
    "start_date": "2023-01-01",
    "end_date": "2023-01-15"
  },
  "summary": {
    "new_leads": 42,
    "lead_conversion_rate": 0.28,
    "new_customers": 12,
    "total_sales": 15000.00,
    "average_sale": 1250.00,
    "reviews_requested": 15,
    "reviews_completed": 10,
    "average_rating": 4.7,
    "referrals_created": 8,
    "referrals_used": 5,
    "content_created": 6,
    "content_engagement_rate": 0.15
  },
  "comparison": {
    "new_leads": {
      "value": 42,
      "previous": 35,
      "change": 0.2,
      "change_type": "positive"
    },
    "lead_conversion_rate": {
      "value": 0.28,
      "previous": 0.25,
      "change": 0.12,
      "change_type": "positive"
    },
    "new_customers": {
      "value": 12,
      "previous": 10,
      "change": 0.2,
      "change_type": "positive"
    },
    "total_sales": {
      "value": 15000.00,
      "previous": 12500.00,
      "change": 0.2,
      "change_type": "positive"
    }
  },
  "charts": {
    "leads_over_time": {
      "labels": ["2023-01-01", "2023-01-02", "...", "2023-01-15"],
      "datasets": [
        {
          "label": "New Leads",
          "data": [3, 5, "...", 4]
        },
        {
          "label": "Converted Leads",
          "data": [1, 2, "...", 1]
        }
      ]
    },
    "sales_over_time": {
      "labels": ["2023-01-01", "2023-01-02", "...", "2023-01-15"],
      "datasets": [
        {
          "label": "Sales Amount",
          "data": [1000, 1500, "...", 1200]
        }
      ]
    },
    "workflow_performance": {
      "labels": ["Lead Nurturing", "Review & Referral", "Content Generation"],
      "datasets": [
        {
          "label": "Success Rate",
          "data": [0.92, 0.88, 0.95]
        },
        {
          "label": "Conversion Rate",
          "data": [0.28, 0.67, 0.15]
        }
      ]
    }
  },
  "roi": {
    "estimated_revenue_impact": 18500.00,
    "estimated_time_saved_hours": 42,
    "estimated_time_value": 2100.00,
    "total_value": 20600.00
  }
}
```

#### Get Workflow Analytics

```
GET /analytics/workflows
```

Query parameters:
- `workflow_type`: Filter by workflow type (optional)
- `start_date`: Start date for analytics (format: YYYY-MM-DD)
- `end_date`: End date for analytics (format: YYYY-MM-DD)

Response:
```json
{
  "period": {
    "start_date": "2023-01-01",
    "end_date": "2023-01-15"
  },
  "workflows": [
    {
      "id": "wf_123456",
      "name": "New Lead Follow-up",
      "type": "lead_nurturing",
      "runs_total": 42,
      "runs_successful": 39,
      "runs_failed": 3,
      "success_rate": 0.93,
      "conversion_rate": 0.28,
      "average_response_time_hours": 4.2,
      "estimated_revenue_impact": 8500.00
    },
    {
      "id": "wf_123457",
      "name": "Post-Sale Review Request",
      "type": "review_referral",
      "runs_total": 15,
      "runs_successful": 14,
      "runs_failed": 1,
      "success_rate": 0.93,
      "review_completion_rate": 0.67,
      "average_rating": 4.7,
      "referral_usage_rate": 0.4,
      "estimated_revenue_impact": 6000.00
    },
    {
      "id": "wf_123458",
      "name": "Weekly Blog Post",
      "type": "content_generation",
      "runs_total": 6,
      "runs_successful": 6,
      "runs_failed": 0,
      "success_rate": 1.0,
      "average_engagement_rate": 0.15,
      "average_conversion_rate": 0.03,
      "estimated_revenue_impact": 4000.00
    }
  ],
  "totals": {
    "runs_total": 63,
    "runs_successful": 59,
    "runs_failed": 4,
    "success_rate": 0.94,
    "estimated_revenue_impact": 18500.00,
    "estimated_time_saved_hours": 42
  }
}
```

#### Get Lead Analytics

```
GET /analytics/leads
```

Query parameters:
- `source`: Filter by source (optional)
- `start_date`: Start date for analytics (format: YYYY-MM-DD)
- `end_date`: End date for analytics (format: YYYY-MM-DD)

Response:
```json
{
  "period": {
    "start_date": "2023-01-01",
    "end_date": "2023-01-15"
  },
  "summary": {
    "total_leads": 42,
    "converted_leads": 12,
    "conversion_rate": 0.28,
    "average_response_time_hours": 4.2,
    "average_time_to_conversion_days": 3.5
  },
  "by_source": [
    {
      "source": "website_form",
      "count": 20,
      "conversion_rate": 0.3,
      "average_time_to_conversion_days": 3.2
    },
    {
      "source": "manual",
      "count": 10,
      "conversion_rate": 0.2,
      "average_time_to_conversion_days": 4.1
    },
    {
      "source": "referral",
      "count": 8,
      "conversion_rate": 0.38,
      "average_time_to_conversion_days": 2.8
    },
    {
      "source": "ad",
      "count": 4,
      "conversion_rate": 0.25,
      "average_time_to_conversion_days": 3.9
    }
  ],
  "by_status": [
    {
      "status": "new",
      "count": 15
    },
    {
      "status": "contacted",
      "count": 10
    },
    {
      "status": "qualified",
      "count": 5
    },
    {
      "status": "converted",
      "count": 12
    }
  ],
  "conversion_funnel": {
    "stages": ["new", "contacted", "qualified", "converted"],
    "counts": [42, 27, 15, 12],
    "conversion_rates": [1.0, 0.64, 0.36, 0.28]
  }
}
```

#### Get Content Analytics

```
GET /analytics/content
```

Query parameters:
- `type`: Filter by content type (optional)
- `start_date`: Start date for analytics (format: YYYY-MM-DD)
- `end_date`: End date for analytics (format: YYYY-MM-DD)

Response:
```json
{
  "period": {
    "start_date": "2023-01-01",
    "end_date": "2023-01-15"
  },
  "summary": {
    "total_content": 6,
    "total_views": 1250,
    "total_clicks": 180,
    "total_shares": 45,
    "total_conversions": 15,
    "average_engagement_rate": 0.15,
    "average_conversion_rate": 0.03
  },
  "by_type": [
    {
      "type": "blog",
      "count": 2,
      "views": 800,
      "clicks": 120,
      "shares": 30,
      "conversions": 8,
      "engagement_rate": 0.19,
      "conversion_rate": 0.01
    },
    {
      "type": "social",
      "count": 3,
      "views": 350,
      "clicks": 40,
      "shares": 15,
      "conversions": 4,
      "engagement_rate": 0.16,
      "conversion_rate": 0.01
    },
    {
      "type": "email",
      "count": 1,
      "views": 100,
      "clicks": 20,
      "shares": 0,
      "conversions": 3,
      "engagement_rate": 0.2,
      "conversion_rate": 0.03
    }
  ],
  "top_performing": [
    {
      "id": "cont_123456",
      "title": "10 Ways to Improve Your Business",
      "type": "blog",
      "views": 500,
      "clicks": 75,
      "shares": 20,
      "conversions": 5,
      "engagement_rate": 0.19,
      "conversion_rate": 0.01
    },
    {
      "id": "cont_123457",
      "title": "New Service Announcement",
      "type": "email",
      "views": 100,
      "clicks": 20,
      "shares": 0,
      "conversions": 3,
      "engagement_rate": 0.2,
      "conversion_rate": 0.03
    }
  ]
}
```

## Error Responses

### Validation Error

```
422 Unprocessable Entity
```

```json
{
  "error": "validation_error",
  "message": "Validation failed",
  "details": {
    "email": ["Invalid email format"],
    "name": ["Name is required"]
  }
}
```

### Authentication Error

```
401 Unauthorized
```

```json
{
  "error": "authentication_error",
  "message": "Invalid or expired token"
}
```

### Permission Error

```
403 Forbidden
```

```json
{
  "error": "permission_error",
  "message": "You do not have permission to access this resource"
}
```

### Resource Not Found

```
404 Not Found
```

```json
{
  "error": "not_found",
  "message": "Resource not found",
  "resource_type": "lead",
  "resource_id": "lead_123456"
}
```

### Server Error

```
500 Internal Server Error
```

```json
{
  "error": "server_error",
  "message": "An unexpected error occurred",
  "request_id": "req_123456"
}
```


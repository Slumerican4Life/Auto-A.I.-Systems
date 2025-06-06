# Business Automation System - Database Schema

## Overview

This document outlines the database schema for the Business Automation System. The system is designed to work with either Firebase Firestore (NoSQL) or PostgreSQL (SQL), with appropriate adaptations for each database type.

## Data Models

### Users

**Collection/Table**: `users`

| Field | Type | Description |
|-------|------|-------------|
| id | String | Unique identifier (UUID) |
| email | String | User email address |
| name | String | User's full name |
| company_id | String | Reference to company |
| role | String | User role (admin, manager, user) |
| created_at | Timestamp | Account creation timestamp |
| last_login | Timestamp | Last login timestamp |
| settings | JSON/Object | User preferences and settings |
| avatar_url | String | URL to user avatar image |

### Companies

**Collection/Table**: `companies`

| Field | Type | Description |
|-------|------|-------------|
| id | String | Unique identifier (UUID) |
| name | String | Company name |
| industry | String | Company industry |
| website | String | Company website URL |
| logo_url | String | URL to company logo |
| created_at | Timestamp | Account creation timestamp |
| subscription_tier | String | Subscription level |
| subscription_status | String | Active, trial, expired |
| settings | JSON/Object | Company-wide settings |
| integrations | JSON/Object | External service integration details |

### Leads

**Collection/Table**: `leads`

| Field | Type | Description |
|-------|------|-------------|
| id | String | Unique identifier (UUID) |
| company_id | String | Reference to company |
| name | String | Lead's full name |
| email | String | Lead's email address |
| phone | String | Lead's phone number |
| source | String | Lead source (form, ad, manual, etc.) |
| status | String | Lead status (new, contacted, qualified, converted, lost) |
| created_at | Timestamp | Lead creation timestamp |
| updated_at | Timestamp | Last update timestamp |
| notes | Text | Additional notes about the lead |
| tags | Array | Tags/categories for the lead |
| assigned_to | String | User ID of assigned team member |
| custom_fields | JSON/Object | Custom fields defined by company |

### Interactions

**Collection/Table**: `interactions`

| Field | Type | Description |
|-------|------|-------------|
| id | String | Unique identifier (UUID) |
| company_id | String | Reference to company |
| lead_id | String | Reference to lead |
| type | String | Interaction type (email, sms, call, meeting) |
| direction | String | Outbound or inbound |
| content | Text | Content of the interaction |
| channel | String | Communication channel |
| status | String | Delivered, opened, clicked, replied |
| created_at | Timestamp | Interaction timestamp |
| created_by | String | User ID or system |
| metadata | JSON/Object | Additional metadata about interaction |

### Reviews

**Collection/Table**: `reviews`

| Field | Type | Description |
|-------|------|-------------|
| id | String | Unique identifier (UUID) |
| company_id | String | Reference to company |
| customer_id | String | Reference to customer |
| platform | String | Review platform (Google, Yelp, etc.) |
| rating | Number | Review rating (1-5) |
| content | Text | Review content if available |
| status | String | Requested, completed, verified |
| request_sent_at | Timestamp | When review request was sent |
| completed_at | Timestamp | When review was completed |
| review_url | String | URL to the review if available |
| request_message | Text | Message sent to request review |

### Referrals

**Collection/Table**: `referrals`

| Field | Type | Description |
|-------|------|-------------|
| id | String | Unique identifier (UUID) |
| company_id | String | Reference to company |
| customer_id | String | Reference to referring customer |
| code | String | Unique referral code |
| status | String | Active, used, expired |
| created_at | Timestamp | Creation timestamp |
| expires_at | Timestamp | Expiration timestamp |
| offer_details | Text | Description of referral offer |
| times_used | Number | Number of times referral was used |
| max_uses | Number | Maximum allowed uses |
| referred_leads | Array | Array of lead IDs from this referral |

### Content

**Collection/Table**: `content`

| Field | Type | Description |
|-------|------|-------------|
| id | String | Unique identifier (UUID) |
| company_id | String | Reference to company |
| title | String | Content title |
| type | String | Content type (blog, social, email) |
| body | Text | Content body |
| status | String | Draft, scheduled, published |
| created_at | Timestamp | Creation timestamp |
| published_at | Timestamp | Publication timestamp |
| created_by | String | User ID or "system" |
| platform | String | Publishing platform |
| url | String | URL where content is published |
| tags | Array | Content tags/categories |
| metadata | JSON/Object | Additional metadata |

### Analytics

**Collection/Table**: `analytics`

| Field | Type | Description |
|-------|------|-------------|
| id | String | Unique identifier (UUID) |
| company_id | String | Reference to company |
| date | Date | Date of analytics record |
| metric_type | String | Type of metric |
| metric_name | String | Name of specific metric |
| value | Number | Metric value |
| source | String | Data source |
| metadata | JSON/Object | Additional context |

### Campaigns

**Collection/Table**: `campaigns`

| Field | Type | Description |
|-------|------|-------------|
| id | String | Unique identifier (UUID) |
| company_id | String | Reference to company |
| name | String | Campaign name |
| type | String | Campaign type |
| status | String | Active, paused, completed |
| start_date | Timestamp | Campaign start date |
| end_date | Timestamp | Campaign end date |
| budget | Number | Campaign budget if applicable |
| target_audience | JSON/Object | Target audience details |
| metrics | JSON/Object | Campaign performance metrics |
| content_ids | Array | Associated content IDs |

### Workflows

**Collection/Table**: `workflows`

| Field | Type | Description |
|-------|------|-------------|
| id | String | Unique identifier (UUID) |
| company_id | String | Reference to company |
| name | String | Workflow name |
| type | String | Workflow type (lead_nurturing, review_referral, content) |
| status | String | Active, paused, draft |
| trigger | JSON/Object | Trigger configuration |
| steps | Array | Array of workflow steps |
| created_at | Timestamp | Creation timestamp |
| updated_at | Timestamp | Last update timestamp |
| created_by | String | User ID |
| settings | JSON/Object | Workflow-specific settings |

### Scheduled Tasks

**Collection/Table**: `scheduled_tasks`

| Field | Type | Description |
|-------|------|-------------|
| id | String | Unique identifier (UUID) |
| company_id | String | Reference to company |
| workflow_id | String | Reference to workflow |
| type | String | Task type |
| status | String | Pending, processing, completed, failed |
| scheduled_for | Timestamp | Scheduled execution time |
| executed_at | Timestamp | Actual execution time |
| data | JSON/Object | Task data payload |
| result | JSON/Object | Task execution result |
| error | Text | Error message if failed |
| retry_count | Number | Number of retry attempts |

## Relationships

### SQL Database Relationships

For PostgreSQL implementation, the following relationships would be established:

1. **Users to Companies**: Many-to-One
   - Foreign key: `users.company_id` references `companies.id`

2. **Leads to Companies**: Many-to-One
   - Foreign key: `leads.company_id` references `companies.id`

3. **Interactions to Leads**: Many-to-One
   - Foreign key: `interactions.lead_id` references `leads.id`

4. **Reviews to Companies**: Many-to-One
   - Foreign key: `reviews.company_id` references `companies.id`

5. **Referrals to Customers**: Many-to-One
   - Foreign key: `referrals.customer_id` references `leads.id`

6. **Content to Companies**: Many-to-One
   - Foreign key: `content.company_id` references `companies.id`

7. **Analytics to Companies**: Many-to-One
   - Foreign key: `analytics.company_id` references `companies.id`

8. **Campaigns to Companies**: Many-to-One
   - Foreign key: `campaigns.company_id` references `companies.id`

9. **Workflows to Companies**: Many-to-One
   - Foreign key: `workflows.company_id` references `companies.id`

10. **Scheduled Tasks to Workflows**: Many-to-One
    - Foreign key: `scheduled_tasks.workflow_id` references `workflows.id`

### NoSQL Database Relationships

For Firebase Firestore implementation, relationships would be handled through:

1. **Document References**: Store IDs of related documents
2. **Subcollections**: For one-to-many relationships (e.g., company's leads)
3. **Denormalization**: Duplicate relevant data for performance optimization

## Indexes

### Primary Indexes

All collections/tables will have primary indexes on their `id` fields.

### Secondary Indexes

For optimal query performance, the following secondary indexes are recommended:

#### Firebase Firestore

1. `users`: `company_id`, `email`
2. `leads`: `company_id`, `status`, `created_at`
3. `interactions`: `lead_id`, `created_at`
4. `reviews`: `company_id`, `status`
5. `referrals`: `company_id`, `code`
6. `content`: `company_id`, `status`, `type`
7. `analytics`: `company_id`, `date`, `metric_type`
8. `campaigns`: `company_id`, `status`
9. `workflows`: `company_id`, `type`, `status`
10. `scheduled_tasks`: `scheduled_for`, `status`

#### PostgreSQL

1. `users`: (`company_id`), (`email`)
2. `leads`: (`company_id`, `status`), (`company_id`, `created_at`)
3. `interactions`: (`lead_id`, `created_at`)
4. `reviews`: (`company_id`, `status`)
5. `referrals`: (`company_id`), (`code`)
6. `content`: (`company_id`, `status`), (`company_id`, `type`)
7. `analytics`: (`company_id`, `date`), (`company_id`, `metric_type`)
8. `campaigns`: (`company_id`, `status`)
9. `workflows`: (`company_id`, `type`), (`company_id`, `status`)
10. `scheduled_tasks`: (`scheduled_for`, `status`)

## Data Migration Strategy

For system flexibility, we'll implement a data migration strategy that allows:

1. **Initial Setup**: Schema creation scripts for both PostgreSQL and Firebase
2. **Schema Versioning**: Track database schema versions for controlled updates
3. **Migration Scripts**: Up/down migration scripts for schema changes
4. **Data Import/Export**: Tools for moving data between database systems

## Backup Strategy

1. **PostgreSQL**:
   - Daily full backups
   - Point-in-time recovery with WAL archiving
   - Automated backup testing

2. **Firebase**:
   - Daily exports to cloud storage
   - Firestore backup and restore procedures
   - Retention policy management


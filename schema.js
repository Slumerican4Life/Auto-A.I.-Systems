/**
 * Firebase Database Schema
 * 
 * This file defines the schema for the Firebase Firestore database.
 * It includes collection structures, field types, and validation rules.
 */

/**
 * Users Collection
 * Stores user account information
 * 
 * Fields:
 * - id: string (auto-generated)
 * - email: string
 * - name: string
 * - role: string (admin, user)
 * - company_id: string (reference to companies collection)
 * - created_at: timestamp
 * - updated_at: timestamp
 * - last_login_at: timestamp
 * - settings: map
 *   - notifications: boolean
 *   - theme: string
 */

/**
 * Companies Collection
 * Stores company information
 * 
 * Fields:
 * - id: string (auto-generated)
 * - name: string
 * - industry: string
 * - website: string
 * - created_at: timestamp
 * - updated_at: timestamp
 * - settings: map
 *   - timezone: string
 *   - business_hours: map
 *     - start: string
 *     - end: string
 *   - branding: map
 *     - logo_url: string
 *     - primary_color: string
 *     - secondary_color: string
 */

/**
 * Leads Collection
 * Stores lead information
 * 
 * Fields:
 * - id: string (auto-generated)
 * - company_id: string (reference to companies collection)
 * - name: string
 * - email: string
 * - phone: string
 * - source: string
 * - status: string (new, contacted, qualified, converted, lost)
 * - notes: string
 * - tags: array of strings
 * - assigned_to: string (reference to users collection)
 * - created_at: timestamp
 * - updated_at: timestamp
 * - custom_fields: map
 */

/**
 * Interactions Collection
 * Stores interactions with leads
 * 
 * Fields:
 * - id: string (auto-generated)
 * - company_id: string (reference to companies collection)
 * - lead_id: string (reference to leads collection)
 * - type: string (email, sms, call, meeting)
 * - direction: string (outbound, inbound)
 * - content: string
 * - channel: string (automated_workflow, manual, reply)
 * - status: string (delivered, opened, clicked, replied)
 * - created_at: timestamp
 * - created_by: string (reference to users collection)
 * - metadata: map
 */

/**
 * Customers Collection
 * Stores customer information
 * 
 * Fields:
 * - id: string (auto-generated)
 * - company_id: string (reference to companies collection)
 * - lead_id: string (reference to leads collection)
 * - name: string
 * - email: string
 * - phone: string
 * - status: string (active, inactive)
 * - created_at: timestamp
 * - updated_at: timestamp
 * - custom_fields: map
 */

/**
 * Sales Collection
 * Stores sales information
 * 
 * Fields:
 * - id: string (auto-generated)
 * - company_id: string (reference to companies collection)
 * - customer_id: string (reference to customers collection)
 * - amount: number
 * - status: string (pending, completed, refunded)
 * - date: timestamp
 * - products: array of maps
 *   - name: string
 *   - quantity: number
 *   - price: number
 * - notes: string
 * - created_at: timestamp
 * - updated_at: timestamp
 */

/**
 * Reviews Collection
 * Stores customer reviews
 * 
 * Fields:
 * - id: string (auto-generated)
 * - company_id: string (reference to companies collection)
 * - customer_id: string (reference to customers collection)
 * - sale_id: string (reference to sales collection)
 * - rating: number
 * - content: string
 * - platform: string (google, yelp, facebook, etc.)
 * - status: string (requested, submitted, verified)
 * - request_sent_at: timestamp
 * - submitted_at: timestamp
 * - verified_at: timestamp
 * - created_at: timestamp
 * - updated_at: timestamp
 */

/**
 * Referrals Collection
 * Stores customer referrals
 * 
 * Fields:
 * - id: string (auto-generated)
 * - company_id: string (reference to companies collection)
 * - customer_id: string (reference to customers collection)
 * - review_id: string (reference to reviews collection)
 * - code: string
 * - status: string (created, sent, used)
 * - referred_leads: array of strings (references to leads collection)
 * - referred_customers: array of strings (references to customers collection)
 * - offer: map
 *   - type: string (discount, credit, gift)
 *   - value: number
 *   - description: string
 * - created_at: timestamp
 * - updated_at: timestamp
 * - expires_at: timestamp
 */

/**
 * Content Collection
 * Stores generated content
 * 
 * Fields:
 * - id: string (auto-generated)
 * - company_id: string (reference to companies collection)
 * - type: string (blog, social, email)
 * - title: string
 * - content: string
 * - status: string (draft, published)
 * - platform: string (wordpress, buffer, mailchimp, etc.)
 * - scheduled_for: timestamp
 * - published_at: timestamp
 * - created_at: timestamp
 * - updated_at: timestamp
 * - metadata: map
 *   - tags: array of strings
 *   - images: array of strings
 *   - links: array of strings
 */

/**
 * Workflow Configs Collection
 * Stores workflow configurations
 * 
 * Fields:
 * - id: string (auto-generated)
 * - company_id: string (reference to companies collection)
 * - workflow_type: string (lead_nurturing, review_referral, content_generation)
 * - name: string
 * - active: boolean
 * - triggers: map
 * - actions: map
 * - templates: map
 * - created_at: timestamp
 * - updated_at: timestamp
 * - created_by: string (reference to users collection)
 */

/**
 * Workflow Runs Collection
 * Stores workflow execution records
 * 
 * Fields:
 * - id: string (auto-generated)
 * - company_id: string (reference to companies collection)
 * - workflow_config_id: string (reference to workflow_configs collection)
 * - status: string (pending, running, completed, failed)
 * - started_at: timestamp
 * - completed_at: timestamp
 * - trigger_type: string
 * - trigger_id: string
 * - actions_performed: array of maps
 * - results: map
 * - error: string
 */

/**
 * Analytics Collection
 * Stores analytics data
 * 
 * Fields:
 * - id: string (auto-generated)
 * - company_id: string (reference to companies collection)
 * - type: string (lead, interaction, review, referral, content)
 * - date: timestamp
 * - metrics: map
 * - dimensions: map
 * - created_at: timestamp
 */

/**
 * Firestore Security Rules
 * 
 * These rules control access to the Firestore database.
 * 
 * Rules:
 * - Users can only read/write data for their own company
 * - Admin users can read/write all data for their company
 * - Super admins can read/write all data
 */

const firestoreRules = `
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    // Helper functions
    function isAuthenticated() {
      return request.auth != null;
    }
    
    function isUserInCompany(companyId) {
      return isAuthenticated() && 
        get(/databases/$(database)/documents/users/$(request.auth.uid)).data.company_id == companyId;
    }
    
    function isAdmin() {
      return isAuthenticated() && 
        get(/databases/$(database)/documents/users/$(request.auth.uid)).data.role == 'admin';
    }
    
    function isSuperAdmin() {
      return isAuthenticated() && 
        get(/databases/$(database)/documents/users/$(request.auth.uid)).data.role == 'super_admin';
    }
    
    // Users collection
    match /users/{userId} {
      allow read: if isAuthenticated() && (request.auth.uid == userId || isSuperAdmin());
      allow write: if isAuthenticated() && (request.auth.uid == userId || isSuperAdmin());
    }
    
    // Companies collection
    match /companies/{companyId} {
      allow read: if isUserInCompany(companyId);
      allow write: if isAdmin() && isUserInCompany(companyId) || isSuperAdmin();
    }
    
    // All other collections
    match /{collection}/{docId} {
      allow read: if isUserInCompany(resource.data.company_id);
      allow write: if isUserInCompany(resource.data.company_id);
    }
  }
}
`;

// Export the security rules
module.exports = {
  firestoreRules
};


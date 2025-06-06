-- Seed Data Migration for Business Automation System
-- This migration populates the database with initial test data.

-- Insert demo company
INSERT INTO companies (id, name, industry, website, settings)
VALUES (
    '11111111-1111-1111-1111-111111111111',
    'Demo Company',
    'Technology',
    'https://demo-company.example.com',
    '{
        "timezone": "America/New_York",
        "business_hours": {
            "start": "09:00",
            "end": "17:00"
        },
        "branding": {
            "primary_color": "#4f46e5",
            "secondary_color": "#10b981"
        }
    }'::JSONB
);

-- Insert admin user
INSERT INTO users (id, email, password_hash, name, role, company_id)
VALUES (
    '22222222-2222-2222-2222-222222222222',
    'admin@demo-company.example.com',
    '$2b$10$demohashdemohashdemohashtTLnD6OLMxH.I9TY5VNc1VV0Ciu', -- This is a fake hash, replace with real bcrypt hash
    'Admin User',
    'admin',
    '11111111-1111-1111-1111-111111111111'
);

-- Insert regular user
INSERT INTO users (id, email, password_hash, name, role, company_id)
VALUES (
    '33333333-3333-3333-3333-333333333333',
    'user@demo-company.example.com',
    '$2b$10$demohashdemohashdemohashtTLnD6OLMxH.I9TY5VNc1VV0Ciu', -- This is a fake hash, replace with real bcrypt hash
    'Regular User',
    'user',
    '11111111-1111-1111-1111-111111111111'
);

-- Insert leads
INSERT INTO leads (id, company_id, name, email, phone, source, status, notes, tags, assigned_to)
VALUES
    (
        '44444444-4444-4444-4444-444444444444',
        '11111111-1111-1111-1111-111111111111',
        'John Doe',
        'john.doe@example.com',
        '+1-555-123-4567',
        'website_form',
        'new',
        'Interested in our services',
        ARRAY['website', 'new_lead'],
        '22222222-2222-2222-2222-222222222222'
    ),
    (
        '55555555-5555-5555-5555-555555555555',
        '11111111-1111-1111-1111-111111111111',
        'Jane Smith',
        'jane.smith@example.com',
        '+1-555-987-6543',
        'referral',
        'contacted',
        'Referred by existing customer',
        ARRAY['referral', 'high_priority'],
        '33333333-3333-3333-3333-333333333333'
    ),
    (
        '66666666-6666-6666-6666-666666666666',
        '11111111-1111-1111-1111-111111111111',
        'Bob Johnson',
        'bob.johnson@example.com',
        '+1-555-456-7890',
        'google_ads',
        'qualified',
        'Looking for enterprise solution',
        ARRAY['google_ads', 'enterprise'],
        '22222222-2222-2222-2222-222222222222'
    );

-- Insert interactions
INSERT INTO interactions (company_id, lead_id, type, direction, content, channel, status, created_by)
VALUES
    (
        '11111111-1111-1111-1111-111111111111',
        '44444444-4444-4444-4444-444444444444',
        'email',
        'outbound',
        'Thank you for your interest in our services. How can we help you today?',
        'automated_workflow',
        'delivered',
        '22222222-2222-2222-2222-222222222222'
    ),
    (
        '11111111-1111-1111-1111-111111111111',
        '44444444-4444-4444-4444-444444444444',
        'email',
        'inbound',
        'I would like to learn more about your pricing plans.',
        'reply',
        'delivered',
        NULL
    ),
    (
        '11111111-1111-1111-1111-111111111111',
        '55555555-5555-5555-5555-555555555555',
        'sms',
        'outbound',
        'Hi Jane, thanks for your interest! Would you like to schedule a demo?',
        'automated_workflow',
        'delivered',
        '33333333-3333-3333-3333-333333333333'
    );

-- Insert customers
INSERT INTO customers (id, company_id, lead_id, name, email, phone, status)
VALUES
    (
        '77777777-7777-7777-7777-777777777777',
        '11111111-1111-1111-1111-111111111111',
        '66666666-6666-6666-6666-666666666666',
        'Bob Johnson',
        'bob.johnson@example.com',
        '+1-555-456-7890',
        'active'
    ),
    (
        '88888888-8888-8888-8888-888888888888',
        '11111111-1111-1111-1111-111111111111',
        NULL,
        'Alice Williams',
        'alice.williams@example.com',
        '+1-555-789-0123',
        'active'
    );

-- Insert sales
INSERT INTO sales (company_id, customer_id, amount, status, products)
VALUES
    (
        '11111111-1111-1111-1111-111111111111',
        '77777777-7777-7777-7777-777777777777',
        1999.99,
        'completed',
        '[
            {"name": "Enterprise Plan", "quantity": 1, "price": 1999.99}
        ]'::JSONB
    ),
    (
        '11111111-1111-1111-1111-111111111111',
        '88888888-8888-8888-8888-888888888888',
        499.99,
        'completed',
        '[
            {"name": "Professional Plan", "quantity": 1, "price": 499.99}
        ]'::JSONB
    );

-- Insert reviews
INSERT INTO reviews (company_id, customer_id, sale_id, rating, content, platform, status, request_sent_at, submitted_at)
VALUES
    (
        '11111111-1111-1111-1111-111111111111',
        '88888888-8888-8888-8888-888888888888',
        (SELECT id FROM sales WHERE customer_id = '88888888-8888-8888-8888-888888888888' LIMIT 1),
        5,
        'Great service! Highly recommended.',
        'google',
        'submitted',
        NOW() - INTERVAL '7 days',
        NOW() - INTERVAL '3 days'
    );

-- Insert referrals
INSERT INTO referrals (company_id, customer_id, review_id, code, status, offer)
VALUES
    (
        '11111111-1111-1111-1111-111111111111',
        '88888888-8888-8888-8888-888888888888',
        (SELECT id FROM reviews WHERE customer_id = '88888888-8888-8888-8888-888888888888' LIMIT 1),
        'REF123456',
        'created',
        '{
            "type": "discount",
            "value": 50,
            "description": "50% off first month"
        }'::JSONB
    );

-- Insert content
INSERT INTO content (company_id, type, title, content, status, platform)
VALUES
    (
        '11111111-1111-1111-1111-111111111111',
        'blog',
        '10 Tips for Small Businesses',
        'This is a sample blog post content. In a real application, this would be much longer and formatted with HTML.',
        'published',
        'wordpress'
    ),
    (
        '11111111-1111-1111-1111-111111111111',
        'social',
        'Check out our latest features!',
        'We just launched some amazing new features! Check out our website to learn more.',
        'published',
        'buffer'
    ),
    (
        '11111111-1111-1111-1111-111111111111',
        'email',
        'Monthly Newsletter - June 2025',
        'This is a sample email newsletter content. In a real application, this would be formatted with HTML.',
        'draft',
        'mailchimp'
    );

-- Insert workflow configs
INSERT INTO workflow_configs (company_id, workflow_type, name, active, triggers, actions, templates, created_by)
VALUES
    (
        '11111111-1111-1111-1111-111111111111',
        'lead_nurturing',
        'Website Lead Follow-up',
        TRUE,
        '{
            "lead_source": ["website_form", "landing_page"]
        }'::JSONB,
        '{
            "initial_delay_minutes": 5,
            "channel": "email",
            "message_template": "welcome_template",
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
        }'::JSONB,
        '{
            "welcome_template": "Hi {{name}},\n\nThank you for your interest in our services. How can we help you today?\n\nBest regards,\nDemo Company",
            "follow_up_1": "Hi {{name}},\n\nJust following up on your recent inquiry. Do you have any questions I can answer?\n\nBest regards,\nDemo Company",
            "follow_up_2": "Hi {{name}},\n\nI wanted to check in one more time to see if you have any questions about our services.\n\nBest regards,\nDemo Company"
        }'::JSONB,
        '22222222-2222-2222-2222-222222222222'
    ),
    (
        '11111111-1111-1111-1111-111111111111',
        'review_referral',
        'Post-Sale Review Request',
        TRUE,
        '{
            "sale_status": ["completed"]
        }'::JSONB,
        '{
            "initial_delay_hours": 48,
            "review_platforms": ["google", "yelp"],
            "referral_offer": {
                "type": "discount",
                "value": 50,
                "description": "50% off first month"
            }
        }'::JSONB,
        '{
            "review_request": "Hi {{name}},\n\nThank you for your recent purchase! We hope you're enjoying our product/service. Would you mind taking a moment to leave us a review?\n\nBest regards,\nDemo Company",
            "referral_offer": "Hi {{name}},\n\nThank you for your review! As a token of our appreciation, we'd like to offer you a referral code to share with friends and family. They'll get 50% off their first month, and you'll receive a $25 credit when they sign up.\n\nYour referral code: {{code}}\n\nBest regards,\nDemo Company"
        }'::JSONB,
        '22222222-2222-2222-2222-222222222222'
    ),
    (
        '11111111-1111-1111-1111-111111111111',
        'content_generation',
        'Weekly Blog Post',
        TRUE,
        '{
            "schedule": "0 9 * * 1"
        }'::JSONB,
        '{
            "content_type": "blog",
            "topics": ["industry_news", "tips_and_tricks", "case_studies"],
            "word_count": 1000,
            "publish": true,
            "platforms": ["wordpress"]
        }'::JSONB,
        '{
            "blog_template": "# {{title}}\n\n{{content}}\n\n## Conclusion\n\nThank you for reading our blog post. If you have any questions, please contact us."
        }'::JSONB,
        '22222222-2222-2222-2222-222222222222'
    );

-- Insert workflow runs
INSERT INTO workflow_runs (company_id, workflow_config_id, status, started_at, completed_at, trigger_type, trigger_id, actions_performed, results)
VALUES
    (
        '11111111-1111-1111-1111-111111111111',
        (SELECT id FROM workflow_configs WHERE name = 'Website Lead Follow-up' LIMIT 1),
        'completed',
        NOW() - INTERVAL '2 days',
        NOW() - INTERVAL '2 days' + INTERVAL '5 minutes',
        'new_lead',
        '44444444-4444-4444-4444-444444444444',
        '[
            {
                "type": "generate_message",
                "timestamp": "' || (NOW() - INTERVAL '2 days' + INTERVAL '1 minute')::TEXT || '",
                "details": {
                    "template": "welcome_template",
                    "generated_content": "Hi John,\n\nThank you for your interest in our services. How can we help you today?\n\nBest regards,\nDemo Company"
                }
            },
            {
                "type": "send_email",
                "timestamp": "' || (NOW() - INTERVAL '2 days' + INTERVAL '2 minutes')::TEXT || '",
                "details": {
                    "to": "john.doe@example.com",
                    "subject": "Thank you for your interest",
                    "status": "delivered"
                }
            },
            {
                "type": "schedule_follow_up",
                "timestamp": "' || (NOW() - INTERVAL '2 days' + INTERVAL '3 minutes')::TEXT || '",
                "details": {
                    "scheduled_for": "' || (NOW() - INTERVAL '1 day')::TEXT || '",
                    "template": "follow_up_1"
                }
            }
        ]'::JSONB,
        '{
            "message_sent": true,
            "follow_ups_scheduled": 2
        }'::JSONB
    ),
    (
        '11111111-1111-1111-1111-111111111111',
        (SELECT id FROM workflow_configs WHERE name = 'Post-Sale Review Request' LIMIT 1),
        'completed',
        NOW() - INTERVAL '10 days',
        NOW() - INTERVAL '10 days' + INTERVAL '3 minutes',
        'sale_completed',
        (SELECT id FROM sales WHERE customer_id = '88888888-8888-8888-8888-888888888888' LIMIT 1)::TEXT,
        '[
            {
                "type": "send_review_request",
                "timestamp": "' || (NOW() - INTERVAL '10 days' + INTERVAL '1 minute')::TEXT || '",
                "details": {
                    "to": "alice.williams@example.com",
                    "subject": "We value your feedback",
                    "status": "delivered"
                }
            }
        ]'::JSONB,
        '{
            "review_request_sent": true
        }'::JSONB
    );

-- Insert analytics data
INSERT INTO analytics (company_id, type, date, metrics, dimensions)
VALUES
    (
        '11111111-1111-1111-1111-111111111111',
        'lead',
        CURRENT_DATE - INTERVAL '7 days',
        '{
            "count": 5,
            "conversion_rate": 0.2,
            "response_rate": 0.6
        }'::JSONB,
        '{
            "source": "website_form"
        }'::JSONB
    ),
    (
        '11111111-1111-1111-1111-111111111111',
        'lead',
        CURRENT_DATE - INTERVAL '6 days',
        '{
            "count": 7,
            "conversion_rate": 0.28,
            "response_rate": 0.57
        }'::JSONB,
        '{
            "source": "website_form"
        }'::JSONB
    ),
    (
        '11111111-1111-1111-1111-111111111111',
        'lead',
        CURRENT_DATE - INTERVAL '5 days',
        '{
            "count": 4,
            "conversion_rate": 0.25,
            "response_rate": 0.5
        }'::JSONB,
        '{
            "source": "website_form"
        }'::JSONB
    ),
    (
        '11111111-1111-1111-1111-111111111111',
        'lead',
        CURRENT_DATE - INTERVAL '4 days',
        '{
            "count": 6,
            "conversion_rate": 0.33,
            "response_rate": 0.67
        }'::JSONB,
        '{
            "source": "website_form"
        }'::JSONB
    ),
    (
        '11111111-1111-1111-1111-111111111111',
        'lead',
        CURRENT_DATE - INTERVAL '3 days',
        '{
            "count": 8,
            "conversion_rate": 0.25,
            "response_rate": 0.625
        }'::JSONB,
        '{
            "source": "website_form"
        }'::JSONB
    ),
    (
        '11111111-1111-1111-1111-111111111111',
        'lead',
        CURRENT_DATE - INTERVAL '2 days',
        '{
            "count": 10,
            "conversion_rate": 0.3,
            "response_rate": 0.7
        }'::JSONB,
        '{
            "source": "website_form"
        }'::JSONB
    ),
    (
        '11111111-1111-1111-1111-111111111111',
        'lead',
        CURRENT_DATE - INTERVAL '1 day',
        '{
            "count": 12,
            "conversion_rate": 0.33,
            "response_rate": 0.75
        }'::JSONB,
        '{
            "source": "website_form"
        }'::JSONB
    );


"""
AI Prompt Templates for Business Automation System.

This module provides templates for AI-powered content generation.
"""

# Lead message templates
LEAD_MESSAGE_TEMPLATES = {
    "initial_contact": """
You are a professional sales representative for a company. 
Write a personalized initial outreach message to a lead named {lead_name} who came through {lead_source}.
The message should be friendly, professional, and aim to start a conversation about their needs.
Keep it concise (2-3 sentences) and include a question to encourage a response.
Do not use emojis or exclamation marks excessively.
""",
    
    "first_followup": """
You are a professional sales representative for a company.
Write a follow-up message to {lead_name} who hasn't responded to your initial outreach.
They originally came through {lead_source}.
The message should be friendly, professional, and provide a bit more value or information.
Keep it concise (2-3 sentences) and include a different call to action.
Do not be pushy or desperate.
""",
    
    "final_followup": """
You are a professional sales representative for a company.
Write a final follow-up message to {lead_name} who hasn't responded to your previous messages.
They originally came through {lead_source}.
The message should be friendly, professional, and make it easy for them to respond.
Keep it concise (2-3 sentences) and let them know this is your final follow-up.
Provide a clear, low-pressure call to action.
""",
    
    "response_to_inquiry": """
You are a professional sales representative for a company.
Write a response to {lead_name} who has asked for more information about your products/services.
They originally came through {lead_source}.
The message should be helpful, informative, and move the conversation forward.
Address their interest, provide some valuable information, and suggest next steps.
Keep it professional but conversational.
"""
}

# Review request templates
REVIEW_REQUEST_TEMPLATES = {
    "default": """
You are a customer service representative for a company.
Write a message to {customer_name} requesting they leave a review on {platform}.
The message should be friendly, appreciative, and explain why reviews are valuable.
Keep it concise (3-4 sentences) and make it easy for them to take action.
Include a thank you for their business.
""",
    
    "post_service": """
You are a customer service representative for a company.
Write a message to {customer_name} who just received your service, requesting they leave a review on {platform}.
The message should reference their recent experience, be friendly, and explain why reviews are valuable.
Keep it concise (3-4 sentences) and make it easy for them to take action.
Include a thank you for their business.
""",
    
    "post_purchase": """
You are a customer service representative for a company.
Write a message to {customer_name} who just purchased your product, requesting they leave a review on {platform}.
The message should reference their recent purchase, be friendly, and explain why reviews are valuable.
Keep it concise (3-4 sentences) and make it easy for them to take action.
Include a thank you for their business.
"""
}

# Referral offer templates
REFERRAL_OFFER_TEMPLATES = {
    "default": """
You are a customer service representative for a company.
Write a message to {customer_name} offering a referral program after they left a positive review.
The message should be appreciative of their review, explain the referral program clearly, and provide their unique referral code: {referral_code}.
Explain the benefits for both them and their friends when the code is used.
Keep it friendly and concise (4-5 sentences).
""",
    
    "post_review": """
You are a customer service representative for a company.
Write a message to {customer_name} thanking them for their positive review and offering a referral program.
The message should be genuinely appreciative, explain the referral program clearly, and provide their unique referral code: {referral_code}.
Explain the benefits for both them and their friends when the code is used.
Keep it friendly and concise (4-5 sentences).
""",
    
    "loyalty_program": """
You are a customer service representative for a company.
Write a message to {customer_name} who is a loyal customer, offering a referral program as part of your loyalty benefits.
The message should acknowledge their loyalty, explain the referral program clearly, and provide their unique referral code: {referral_code}.
Explain the benefits for both them and their friends when the code is used.
Keep it friendly and concise (4-5 sentences).
"""
}

# Content generation templates
CONTENT_GENERATION_TEMPLATES = {
    "blog": """
You are a professional content writer for a company.
Write a blog post about {topic}.
Keywords to include: {keywords}
Tone: {tone}
Length: {length} (short: 300-500 words, medium: 600-800 words, long: 1000+ words)
Target audience: {target_audience}
Additional instructions: {additional_instructions}

The blog post should be well-structured with headings, subheadings, and paragraphs.
Include an introduction, main points with supporting details, and a conclusion.
Write in a {tone} tone that resonates with the {target_audience}.
Format the content using Markdown.
""",
    
    "social": """
You are a social media manager for a company.
Write a social media post about {topic}.
Keywords to include: {keywords}
Tone: {tone}
Length: {length} (short: 1-2 sentences, medium: 3-4 sentences, long: 5-6 sentences)
Target audience: {target_audience}
Additional instructions: {additional_instructions}

The post should be engaging, concise, and designed to generate engagement.
Include relevant hashtags where appropriate.
Write in a {tone} tone that resonates with the {target_audience}.
Consider the character limits of social platforms.
""",
    
    "email": """
You are an email marketing specialist for a company.
Write an email newsletter about {topic}.
Keywords to include: {keywords}
Tone: {tone}
Length: {length} (short: 150-200 words, medium: 300-400 words, long: 500+ words)
Target audience: {target_audience}
Additional instructions: {additional_instructions}

The email should have a compelling subject line, engaging opening, valuable content, and clear call to action.
Structure it with short paragraphs and use formatting to highlight key points.
Write in a {tone} tone that resonates with the {target_audience}.
Make it personal and conversational while maintaining professionalism.
"""
}


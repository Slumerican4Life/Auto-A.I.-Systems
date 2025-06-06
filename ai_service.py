"""
AI Service for Business Automation System.

This module provides the service layer for AI-powered content generation.
"""

import os
import json
from typing import Dict, Any, List, Optional

from .prompt_templates import (
    LEAD_MESSAGE_TEMPLATES,
    REVIEW_REQUEST_TEMPLATES,
    REFERRAL_OFFER_TEMPLATES,
    CONTENT_GENERATION_TEMPLATES
)


class AIService:
    """Service for AI-powered content generation."""

    def __init__(self):
        """Initialize the AI service."""
        self.api_key = os.environ.get("OPENAI_API_KEY", "mock_api_key")
        self.model = os.environ.get("OPENAI_MODEL", "gpt-4")

    def _call_openai_api(self, prompt: str, max_tokens: int = 500, temperature: float = 0.7) -> str:
        """
        Call the OpenAI API to generate content.
        
        Args:
            prompt: Prompt to send to the API
            max_tokens: Maximum number of tokens to generate
            temperature: Temperature for generation
            
        Returns:
            Generated content
        """
        # In a real implementation, this would call the OpenAI API
        # For now, we'll just return a mock response based on the prompt
        
        # Mock implementation for development
        if "lead" in prompt.lower():
            return "Hello {lead_name}, thank you for your interest in our services. I noticed you came to us through {source}. I'd love to learn more about your needs and how we can help. Would you be available for a quick call this week?"
        
        elif "review" in prompt.lower():
            return "Hi {customer_name}, thank you for choosing our services! We hope you had a great experience. If you have a moment, we'd really appreciate it if you could leave us a review on {platform}. Your feedback helps us improve and helps others find us. Here's a link: {review_url}"
        
        elif "referral" in prompt.lower():
            return "Hi {customer_name}, thank you for your positive review! We'd love to show our appreciation by offering you and your friends a special discount. Share this code with friends or family: {referral_code}. They'll get 10% off their first purchase, and you'll get 10% off your next one when they use it!"
        
        elif "blog" in prompt.lower():
            return """# 10 Tips for Small Business Success

Running a small business can be challenging, but with the right strategies, you can set yourself up for success. Here are ten proven tips to help your small business thrive:

## 1. Define Your Unique Value Proposition

Understand what makes your business special and communicate it clearly. Your unique value proposition should explain why customers should choose you over competitors.

## 2. Know Your Target Audience

Identify your ideal customers and focus your marketing efforts on reaching them. Understanding their needs, preferences, and pain points will help you tailor your products and services effectively.

## 3. Build a Strong Online Presence

In today's digital world, having a professional website and active social media accounts is essential. Make sure your online presence accurately represents your brand and makes it easy for customers to find you.

## 4. Focus on Customer Service

Exceptional customer service can set your business apart. Train your team to prioritize customer satisfaction and create systems for addressing customer feedback.

## 5. Manage Your Finances Carefully

Keep track of your income and expenses, create a budget, and plan for taxes. Consider working with an accountant to ensure your financial management is sound.

## 6. Invest in Marketing

Allocate resources to marketing your business. This could include content marketing, social media advertising, email campaigns, or traditional advertising methods.

## 7. Build a Strong Team

Hire employees who share your vision and values. Invest in their development and create a positive work environment to reduce turnover.

## 8. Embrace Technology

Use technology to streamline operations, improve efficiency, and enhance the customer experience. This could include customer relationship management (CRM) software, accounting tools, or project management systems.

## 9. Network and Build Relationships

Connect with other business owners, join industry associations, and attend networking events. Building relationships can lead to partnerships, referrals, and valuable advice.

## 10. Adapt and Evolve

Stay flexible and be willing to adapt your business model as needed. Keep an eye on industry trends and be prepared to evolve your products or services to meet changing customer needs.

By implementing these strategies, you can position your small business for long-term success. Remember, building a successful business takes time, so be patient and persistent in your efforts."""
        
        elif "social" in prompt.lower():
            return "🚀 Excited to share our latest tips for small business success! Check out our new blog post where we cover everything from defining your unique value proposition to embracing technology. Link in bio! #SmallBusinessTips #Entrepreneurship #BusinessGrowth"
        
        elif "email" in prompt.lower():
            return """Subject: 10 Essential Tips to Grow Your Small Business

Dear Valued Customer,

We hope this email finds you well. At [Company Name], we're committed to helping small businesses like yours succeed.

Today, we're sharing our latest blog post: "10 Tips for Small Business Success." In this comprehensive guide, we cover essential strategies that can help take your business to the next level, including:

- Defining your unique value proposition
- Understanding your target audience
- Building a strong online presence
- Providing exceptional customer service
- Managing your finances effectively

We've seen these strategies work for countless businesses, and we believe they can work for you too.

[Read the Full Article]

We'd love to hear which tips resonate most with you. Simply reply to this email to share your thoughts or experiences.

Wishing you continued success,

[Your Name]
[Company Name]
"""
        
        else:
            return "Generated content based on your request."

    def generate_lead_message(self, params: Dict[str, Any]) -> str:
        """
        Generate a personalized message for a lead.
        
        Args:
            params: Parameters for message generation
            
        Returns:
            Generated message
        """
        # Get the appropriate template
        message_type = params.get("message_type", "initial_contact")
        template = LEAD_MESSAGE_TEMPLATES.get(message_type, LEAD_MESSAGE_TEMPLATES["initial_contact"])
        
        # Fill in template placeholders
        prompt = template.format(
            lead_name=params.get("lead_name", "there"),
            company_id=params.get("company_id", ""),
            lead_source=params.get("lead_source", "our website")
        )
        
        # Generate content
        return self._call_openai_api(prompt)

    def generate_review_request(self, params: Dict[str, Any]) -> str:
        """
        Generate a review request message.
        
        Args:
            params: Parameters for message generation
            
        Returns:
            Generated message
        """
        # Get the template
        template = REVIEW_REQUEST_TEMPLATES["default"]
        
        # Fill in template placeholders
        prompt = template.format(
            customer_name=params.get("customer_name", "there"),
            company_id=params.get("company_id", ""),
            platform=params.get("platform", "Google")
        )
        
        # Generate content
        return self._call_openai_api(prompt)

    def generate_referral_offer(self, params: Dict[str, Any]) -> str:
        """
        Generate a referral offer message.
        
        Args:
            params: Parameters for message generation
            
        Returns:
            Generated message
        """
        # Get the template
        template = REFERRAL_OFFER_TEMPLATES["default"]
        
        # Fill in template placeholders
        prompt = template.format(
            customer_name=params.get("customer_name", "there"),
            company_id=params.get("company_id", ""),
            referral_code=params.get("referral_code", "CODE123")
        )
        
        # Generate content
        return self._call_openai_api(prompt)

    def generate_content(self, content_type: str, topic: str, keywords: List[str] = None, tone: str = "professional", length: str = "medium", target_audience: str = None, additional_instructions: str = None, company_id: str = None) -> Dict[str, str]:
        """
        Generate content for marketing or communication.
        
        Args:
            content_type: Type of content to generate (blog, social, email)
            topic: Topic for the content
            keywords: Keywords to include
            tone: Tone of the content
            length: Length of the content
            target_audience: Target audience for the content
            additional_instructions: Additional instructions for generation
            company_id: ID of the company
            
        Returns:
            Dictionary with generated content
        """
        # Get the appropriate template
        template = CONTENT_GENERATION_TEMPLATES.get(content_type, CONTENT_GENERATION_TEMPLATES["blog"])
        
        # Fill in template placeholders
        prompt = template.format(
            topic=topic,
            keywords=", ".join(keywords) if keywords else "",
            tone=tone,
            length=length,
            target_audience=target_audience or "general audience",
            additional_instructions=additional_instructions or ""
        )
        
        # Generate content
        generated_content = self._call_openai_api(prompt, max_tokens=1000 if length == "long" else 500)
        
        # For blog posts, generate a title separately
        title = topic
        if content_type == "blog":
            title_prompt = f"Generate a catchy title for a blog post about {topic}. Make it SEO-friendly and include key terms if possible."
            title = self._call_openai_api(title_prompt, max_tokens=50, temperature=0.8)
        
        return {
            "title": title,
            "body": generated_content
        }


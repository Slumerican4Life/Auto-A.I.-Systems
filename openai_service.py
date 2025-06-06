import os
import logging
from typing import Dict, List, Any, Optional, Union

from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain.memory import ConversationBufferMemory

from core.config import settings

logger = logging.getLogger(__name__)

class OpenAIService:
    def __init__(self):
        self.api_key = settings.OPENAI_API_KEY
        self.initialize()
    
    def initialize(self):
        try:
            # Initialize OpenAI client
            if not self.api_key:
                raise ValueError("OpenAI API key is not set")
            
            # Initialize LangChain components
            self.llm = OpenAI(temperature=0.7, openai_api_key=self.api_key)
            self.chat_model = ChatOpenAI(temperature=0.7, openai_api_key=self.api_key)
            
            logger.info("OpenAI service initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize OpenAI service: {e}")
            raise
    
    async def generate_text(self, prompt: str, max_tokens: int = 500, temperature: float = 0.7) -> str:
        """
        Generate text using OpenAI's completion API
        """
        try:
            response = self.llm(prompt=prompt, max_tokens=max_tokens, temperature=temperature)
            return response
        except Exception as e:
            logger.error(f"Error generating text: {e}")
            raise
    
    async def generate_lead_response(self, lead_info: Dict[str, Any], tone: str = "professional") -> str:
        """
        Generate a personalized response for a lead
        """
        try:
            # Create prompt template
            template = """
            You are an AI assistant for a business. You need to generate a personalized response to a potential lead.
            
            Lead Information:
            - Name: {name}
            - Email: {email}
            - Source: {source}
            - Interest: {interest}
            
            Tone: {tone}
            
            Write a personalized response to this lead that acknowledges their interest and encourages them to take the next step.
            The response should be friendly, professional, and not too long (150-200 words).
            
            Response:
            """
            
            prompt = PromptTemplate(
                input_variables=["name", "email", "source", "interest", "tone"],
                template=template
            )
            
            # Create chain
            chain = LLMChain(llm=self.llm, prompt=prompt)
            
            # Run chain
            response = chain.run(
                name=lead_info.get("name", ""),
                email=lead_info.get("email", ""),
                source=lead_info.get("source", "website"),
                interest=lead_info.get("interest", "your services"),
                tone=tone
            )
            
            return response.strip()
        except Exception as e:
            logger.error(f"Error generating lead response: {e}")
            raise
    
    async def generate_review_request(self, customer_info: Dict[str, Any], service_info: Dict[str, Any]) -> str:
        """
        Generate a review request message for a customer
        """
        try:
            # Create prompt template
            template = """
            You are an AI assistant for a business. You need to generate a message requesting a review from a customer who recently purchased a service.
            
            Customer Information:
            - Name: {customer_name}
            - Email: {customer_email}
            
            Service Information:
            - Service Name: {service_name}
            - Purchase Date: {purchase_date}
            
            Write a friendly message thanking the customer for their purchase and requesting a review on Google or Yelp.
            The message should be concise, friendly, and include a clear call-to-action.
            
            Message:
            """
            
            prompt = PromptTemplate(
                input_variables=["customer_name", "customer_email", "service_name", "purchase_date"],
                template=template
            )
            
            # Create chain
            chain = LLMChain(llm=self.llm, prompt=prompt)
            
            # Run chain
            response = chain.run(
                customer_name=customer_info.get("name", ""),
                customer_email=customer_info.get("email", ""),
                service_name=service_info.get("name", "our service"),
                purchase_date=service_info.get("purchase_date", "recently")
            )
            
            return response.strip()
        except Exception as e:
            logger.error(f"Error generating review request: {e}")
            raise
    
    async def generate_referral_offer(self, customer_info: Dict[str, Any], offer_details: Dict[str, Any]) -> str:
        """
        Generate a referral offer message for a customer
        """
        try:
            # Create prompt template
            template = """
            You are an AI assistant for a business. You need to generate a message with a referral offer for a customer who recently left a review.
            
            Customer Information:
            - Name: {customer_name}
            - Email: {customer_email}
            
            Offer Details:
            - Discount: {discount}
            - Referral Code: {referral_code}
            - Expiration: {expiration}
            
            Write a friendly message thanking the customer for their review and offering them a referral discount for friends and family.
            The message should be concise, friendly, and include clear instructions on how to use the referral code.
            
            Message:
            """
            
            prompt = PromptTemplate(
                input_variables=["customer_name", "customer_email", "discount", "referral_code", "expiration"],
                template=template
            )
            
            # Create chain
            chain = LLMChain(llm=self.llm, prompt=prompt)
            
            # Run chain
            response = chain.run(
                customer_name=customer_info.get("name", ""),
                customer_email=customer_info.get("email", ""),
                discount=offer_details.get("discount", "10%"),
                referral_code=offer_details.get("referral_code", ""),
                expiration=offer_details.get("expiration", "30 days")
            )
            
            return response.strip()
        except Exception as e:
            logger.error(f"Error generating referral offer: {e}")
            raise
    
    async def generate_blog_post(self, topic: str, keywords: List[str], tone: str = "professional", length: str = "medium") -> Dict[str, Any]:
        """
        Generate a blog post on a given topic
        """
        try:
            # Determine word count based on length
            word_counts = {
                "short": 500,
                "medium": 1000,
                "long": 1500
            }
            target_word_count = word_counts.get(length, 1000)
            
            # Create prompt template
            template = """
            You are an AI content creator for a business. You need to write a blog post on the following topic:
            
            Topic: {topic}
            
            Keywords to include: {keywords}
            
            Tone: {tone}
            
            Target Word Count: {word_count} words
            
            Write a well-structured blog post that includes:
            1. An engaging title
            2. An introduction that hooks the reader
            3. 3-5 main sections with subheadings
            4. A conclusion with a call-to-action
            
            The blog post should be informative, engaging, and optimized for SEO using the provided keywords.
            
            Blog Post:
            """
            
            prompt = PromptTemplate(
                input_variables=["topic", "keywords", "tone", "word_count"],
                template=template
            )
            
            # Create chain
            chain = LLMChain(llm=self.llm, prompt=prompt)
            
            # Run chain
            response = chain.run(
                topic=topic,
                keywords=", ".join(keywords),
                tone=tone,
                word_count=target_word_count
            )
            
            # Extract title and content
            lines = response.strip().split("\n")
            title = lines[0].replace("# ", "").replace("#", "").strip()
            content = "\n".join(lines[1:]).strip()
            
            return {
                "title": title,
                "content": content,
                "word_count": len(content.split()),
                "keywords": keywords
            }
        except Exception as e:
            logger.error(f"Error generating blog post: {e}")
            raise
    
    async def generate_social_post(self, topic: str, platform: str, tone: str = "conversational") -> Dict[str, Any]:
        """
        Generate a social media post for a specific platform
        """
        try:
            # Create prompt template
            template = """
            You are an AI social media manager for a business. You need to write a social media post on the following topic:
            
            Topic: {topic}
            Platform: {platform}
            Tone: {tone}
            
            Write an engaging social media post that is optimized for the specified platform.
            The post should be attention-grabbing, concise, and include relevant hashtags.
            
            For Instagram/Facebook, include emojis and 3-5 hashtags.
            For Twitter, keep it under 280 characters and include 1-2 hashtags.
            For LinkedIn, maintain a more professional tone and include 1-3 hashtags.
            
            Social Media Post:
            """
            
            prompt = PromptTemplate(
                input_variables=["topic", "platform", "tone"],
                template=template
            )
            
            # Create chain
            chain = LLMChain(llm=self.llm, prompt=prompt)
            
            # Run chain
            response = chain.run(
                topic=topic,
                platform=platform,
                tone=tone
            )
            
            # Extract content and hashtags
            content = response.strip()
            hashtags = [word for word in content.split() if word.startswith("#")]
            
            return {
                "content": content,
                "hashtags": hashtags,
                "platform": platform,
                "character_count": len(content)
            }
        except Exception as e:
            logger.error(f"Error generating social post: {e}")
            raise
    
    async def generate_email_newsletter(self, topic: str, company_info: Dict[str, Any], news_items: List[str]) -> Dict[str, Any]:
        """
        Generate an email newsletter
        """
        try:
            # Create prompt template
            template = """
            You are an AI email marketer for a business. You need to write an email newsletter on the following topic:
            
            Topic: {topic}
            
            Company Information:
            - Name: {company_name}
            - Industry: {company_industry}
            
            News Items to Include:
            {news_items}
            
            Write an engaging email newsletter that includes:
            1. An attention-grabbing subject line
            2. A personalized greeting
            3. An introduction paragraph
            4. Sections for each news item
            5. A call-to-action
            6. A professional sign-off
            
            The newsletter should be professional, engaging, and not too long (300-400 words).
            
            Email Newsletter:
            """
            
            prompt = PromptTemplate(
                input_variables=["topic", "company_name", "company_industry", "news_items"],
                template=template
            )
            
            # Create chain
            chain = LLMChain(llm=self.llm, prompt=prompt)
            
            # Format news items
            formatted_news = "\n".join([f"- {item}" for item in news_items])
            
            # Run chain
            response = chain.run(
                topic=topic,
                company_name=company_info.get("name", "Our Company"),
                company_industry=company_info.get("industry", "Business"),
                news_items=formatted_news
            )
            
            # Extract subject line and content
            lines = response.strip().split("\n")
            subject_line = lines[0].replace("Subject:", "").replace("Subject Line:", "").strip()
            content = "\n".join(lines[1:]).strip()
            
            return {
                "subject": subject_line,
                "content": content,
                "word_count": len(content.split())
            }
        except Exception as e:
            logger.error(f"Error generating email newsletter: {e}")
            raise

# Create OpenAI service instance
openai_service = OpenAIService()


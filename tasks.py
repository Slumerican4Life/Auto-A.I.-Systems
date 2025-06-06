import logging
from typing import Dict, Any, Optional

from services.scheduler.scheduler_service import scheduler_service
from workflows.lead_nurturing.repository import LeadRepository
from workflows.lead_nurturing.service import LeadNurturingService

logger = logging.getLogger(__name__)

# Create Celery app
from celery import Celery
from core.config import settings

celery_app = Celery(
    "business_automation",
    broker=settings.REDIS_URL,
    backend=settings.REDIS_URL
)

@celery_app.task(name="workflows.lead_nurturing.tasks.send_initial_message")
def send_initial_message(lead_id: str, message: str, channel: str = "email") -> Dict[str, Any]:
    """
    Send initial message to a lead
    """
    try:
        import asyncio
        
        # Get lead
        lead = asyncio.run(LeadRepository.get_lead(lead_id))
        if not lead:
            raise ValueError(f"Lead {lead_id} not found")
        
        # Send message
        result = asyncio.run(LeadNurturingService.send_message(lead, message, channel))
        
        logger.info(f"Sent initial message to lead {lead_id} via {channel}")
        
        return {
            "lead_id": lead_id,
            "channel": channel,
            "result": result
        }
    except Exception as e:
        logger.error(f"Error sending initial message to lead {lead_id}: {e}")
        raise

@celery_app.task(name="workflows.lead_nurturing.tasks.send_follow_up")
def send_follow_up(lead_id: str, template_id: str) -> Dict[str, Any]:
    """
    Send follow-up message to a lead
    """
    try:
        import asyncio
        
        # Process follow-up
        result = asyncio.run(LeadNurturingService.process_follow_up(lead_id, template_id))
        
        logger.info(f"Sent follow-up to lead {lead_id} using template {template_id}")
        
        return result
    except Exception as e:
        logger.error(f"Error sending follow-up to lead {lead_id}: {e}")
        raise

@celery_app.task(name="workflows.lead_nurturing.tasks.check_lead_responses")
def check_lead_responses() -> Dict[str, Any]:
    """
    Check for responses from leads and update their status
    """
    try:
        import asyncio
        from datetime import datetime, timedelta
        from core.database import db
        
        # Get leads that were contacted in the last 7 days
        now = datetime.utcnow()
        seven_days_ago = now - timedelta(days=7)
        
        # This would typically involve checking an email inbox or SMS replies
        # For now, we'll just log that the check was performed
        logger.info("Checked for lead responses")
        
        return {
            "checked_at": now.isoformat(),
            "result": "success"
        }
    except Exception as e:
        logger.error(f"Error checking lead responses: {e}")
        raise


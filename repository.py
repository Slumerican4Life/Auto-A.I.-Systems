import logging
from datetime import datetime
from typing import Dict, List, Any, Optional, Union
from uuid import uuid4

from core.database import db
from workflows.lead_nurturing.models import Lead, LeadCreate, LeadUpdate, Interaction, InteractionCreate

logger = logging.getLogger(__name__)

class LeadRepository:
    """Repository for lead-related database operations"""
    
    @staticmethod
    async def create_lead(lead_data: LeadCreate) -> Lead:
        """Create a new lead"""
        try:
            # Generate ID and timestamps
            lead_id = f"lead_{uuid4().hex}"
            now = datetime.utcnow()
            
            # Prepare lead data
            lead_dict = lead_data.dict()
            lead_dict.update({
                "id": lead_id,
                "status": "new",
                "created_at": now,
                "updated_at": now
            })
            
            # Create lead in database
            result = await db.create_document("leads", lead_dict, lead_id)
            
            # Log lead creation
            logger.info(f"Created lead: {lead_id}")
            
            return Lead(**result)
        except Exception as e:
            logger.error(f"Error creating lead: {e}")
            raise
    
    @staticmethod
    async def get_lead(lead_id: str) -> Optional[Lead]:
        """Get a lead by ID"""
        try:
            # Get lead from database
            lead_data = await db.get_document("leads", lead_id)
            
            if not lead_data:
                return None
            
            # Get interactions for this lead
            interactions = await db.query_collection(
                "interactions",
                filters=[{"field": "lead_id", "op": "==", "value": lead_id}],
                order_by="created_at",
                order_direction="desc"
            )
            
            # Create lead object with interactions
            lead = Lead(**lead_data)
            lead.interactions = interactions
            
            return lead
        except Exception as e:
            logger.error(f"Error getting lead {lead_id}: {e}")
            raise
    
    @staticmethod
    async def update_lead(lead_id: str, lead_data: LeadUpdate) -> Optional[Lead]:
        """Update a lead"""
        try:
            # Get existing lead
            existing_lead = await db.get_document("leads", lead_id)
            
            if not existing_lead:
                return None
            
            # Prepare update data
            update_dict = {k: v for k, v in lead_data.dict().items() if v is not None}
            update_dict["updated_at"] = datetime.utcnow()
            
            # Update lead in database
            result = await db.update_document("leads", lead_id, update_dict)
            
            # Log lead update
            logger.info(f"Updated lead: {lead_id}")
            
            # Get updated lead with interactions
            return await LeadRepository.get_lead(lead_id)
        except Exception as e:
            logger.error(f"Error updating lead {lead_id}: {e}")
            raise
    
    @staticmethod
    async def delete_lead(lead_id: str) -> bool:
        """Delete a lead"""
        try:
            # Delete lead from database
            result = await db.delete_document("leads", lead_id)
            
            # Log lead deletion
            logger.info(f"Deleted lead: {lead_id}")
            
            return result.get("deleted", False)
        except Exception as e:
            logger.error(f"Error deleting lead {lead_id}: {e}")
            raise
    
    @staticmethod
    async def list_leads(company_id: str, filters: Dict[str, Any] = None, 
                        page: int = 1, per_page: int = 20,
                        sort_by: str = "created_at", sort_dir: str = "desc") -> Dict[str, Any]:
        """List leads with pagination"""
        try:
            # Prepare filters
            query_filters = [{"field": "company_id", "op": "==", "value": company_id}]
            
            if filters:
                for key, value in filters.items():
                    if value is not None:
                        query_filters.append({"field": key, "op": "==", "value": value})
            
            # Calculate pagination
            offset = (page - 1) * per_page
            
            # Query leads
            leads = await db.query_collection(
                "leads",
                filters=query_filters,
                order_by=sort_by,
                order_direction=sort_dir,
                limit=per_page,
                offset=offset
            )
            
            # Get total count for pagination
            # Note: This is a simplified approach. In a real application, you might want to use a more efficient method.
            all_leads = await db.query_collection(
                "leads",
                filters=query_filters
            )
            total_items = len(all_leads)
            total_pages = (total_items + per_page - 1) // per_page  # Ceiling division
            
            return {
                "data": leads,
                "meta": {
                    "current_page": page,
                    "per_page": per_page,
                    "total_items": total_items,
                    "total_pages": total_pages
                }
            }
        except Exception as e:
            logger.error(f"Error listing leads: {e}")
            raise

class InteractionRepository:
    """Repository for interaction-related database operations"""
    
    @staticmethod
    async def create_interaction(interaction_data: InteractionCreate) -> Interaction:
        """Create a new interaction"""
        try:
            # Generate ID and timestamp
            interaction_id = f"int_{uuid4().hex}"
            now = datetime.utcnow()
            
            # Prepare interaction data
            interaction_dict = interaction_data.dict()
            interaction_dict.update({
                "id": interaction_id,
                "created_at": now
            })
            
            # Create interaction in database
            result = await db.create_document("interactions", interaction_dict, interaction_id)
            
            # Log interaction creation
            logger.info(f"Created interaction: {interaction_id}")
            
            # Update lead's updated_at timestamp
            await db.update_document("leads", interaction_data.lead_id, {"updated_at": now})
            
            return Interaction(**result)
        except Exception as e:
            logger.error(f"Error creating interaction: {e}")
            raise
    
    @staticmethod
    async def get_interaction(interaction_id: str) -> Optional[Interaction]:
        """Get an interaction by ID"""
        try:
            # Get interaction from database
            interaction_data = await db.get_document("interactions", interaction_id)
            
            if not interaction_data:
                return None
            
            return Interaction(**interaction_data)
        except Exception as e:
            logger.error(f"Error getting interaction {interaction_id}: {e}")
            raise
    
    @staticmethod
    async def list_interactions(lead_id: str, page: int = 1, per_page: int = 20) -> Dict[str, Any]:
        """List interactions for a lead with pagination"""
        try:
            # Prepare filters
            query_filters = [{"field": "lead_id", "op": "==", "value": lead_id}]
            
            # Calculate pagination
            offset = (page - 1) * per_page
            
            # Query interactions
            interactions = await db.query_collection(
                "interactions",
                filters=query_filters,
                order_by="created_at",
                order_direction="desc",
                limit=per_page,
                offset=offset
            )
            
            # Get total count for pagination
            all_interactions = await db.query_collection(
                "interactions",
                filters=query_filters
            )
            total_items = len(all_interactions)
            total_pages = (total_items + per_page - 1) // per_page  # Ceiling division
            
            return {
                "data": interactions,
                "meta": {
                    "current_page": page,
                    "per_page": per_page,
                    "total_items": total_items,
                    "total_pages": total_pages
                }
            }
        except Exception as e:
            logger.error(f"Error listing interactions: {e}")
            raise


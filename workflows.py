from fastapi import APIRouter, Depends, HTTPException, Query, Path, status
from typing import Dict, List, Any, Optional
from datetime import datetime
from uuid import uuid4

from core.security import get_current_user, UserAuth
from core.database import db
from workflows.lead_nurturing.models import LeadNurturingConfig, LeadNurturingRun

router = APIRouter()

@router.get("/configs", response_model=Dict[str, Any])
async def list_workflow_configs(
    workflow_type: Optional[str] = Query(None, description="Filter by workflow type"),
    active: Optional[bool] = Query(None, description="Filter by active status"),
    page: int = Query(1, ge=1, description="Page number"),
    per_page: int = Query(20, ge=1, le=100, description="Items per page"),
    current_user: UserAuth = Depends(get_current_user)
):
    """
    List workflow configurations
    """
    # Prepare filters
    filters = [{"field": "company_id", "op": "==", "value": current_user.company_id}]
    
    if workflow_type:
        filters.append({"field": "workflow_type", "op": "==", "value": workflow_type})
    
    if active is not None:
        filters.append({"field": "active", "op": "==", "value": active})
    
    # Calculate pagination
    offset = (page - 1) * per_page
    
    # Query workflow configs
    configs = await db.query_collection(
        "workflow_configs",
        filters=filters,
        order_by="created_at",
        order_direction="desc",
        limit=per_page,
        offset=offset
    )
    
    # Get total count for pagination
    all_configs = await db.query_collection(
        "workflow_configs",
        filters=filters
    )
    total_items = len(all_configs)
    total_pages = (total_items + per_page - 1) // per_page  # Ceiling division
    
    return {
        "data": configs,
        "meta": {
            "current_page": page,
            "per_page": per_page,
            "total_items": total_items,
            "total_pages": total_pages
        }
    }

@router.post("/configs", response_model=LeadNurturingConfig)
async def create_workflow_config(
    config_data: LeadNurturingConfig,
    current_user: UserAuth = Depends(get_current_user)
):
    """
    Create a new workflow configuration
    """
    # Set company ID and created_by
    config_data.company_id = current_user.company_id
    config_data.created_by = current_user.id
    
    # Generate ID and timestamps
    config_id = f"wf_{uuid4().hex}"
    now = datetime.utcnow()
    
    config_data.id = config_id
    config_data.created_at = now
    config_data.updated_at = now
    
    # Create config in database
    result = await db.create_document("workflow_configs", config_data.dict(), config_id)
    
    return LeadNurturingConfig(**result)

@router.get("/configs/{config_id}", response_model=LeadNurturingConfig)
async def get_workflow_config(
    config_id: str = Path(..., description="Workflow config ID"),
    current_user: UserAuth = Depends(get_current_user)
):
    """
    Get a workflow configuration by ID
    """
    # Get config from database
    config_data = await db.get_document("workflow_configs", config_id)
    
    if not config_data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Workflow config {config_id} not found"
        )
    
    # Check if config belongs to user's company
    if config_data["company_id"] != current_user.company_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this workflow config"
        )
    
    # Get workflow runs stats
    runs = await db.query_collection(
        "workflow_runs",
        filters=[{"field": "workflow_config_id", "op": "==", "value": config_id}]
    )
    
    # Calculate stats
    runs_total = len(runs)
    runs_successful = sum(1 for run in runs if run["status"] == "completed")
    runs_failed = sum(1 for run in runs if run["status"] == "failed")
    
    # Add stats to config
    config_data["stats"] = {
        "runs_total": runs_total,
        "runs_successful": runs_successful,
        "runs_failed": runs_failed,
        "conversion_rate": 0.0  # This would be calculated from actual data
    }
    
    return LeadNurturingConfig(**config_data)

@router.patch("/configs/{config_id}", response_model=LeadNurturingConfig)
async def update_workflow_config(
    config_data: LeadNurturingConfig,
    config_id: str = Path(..., description="Workflow config ID"),
    current_user: UserAuth = Depends(get_current_user)
):
    """
    Update a workflow configuration
    """
    # Check if config exists and belongs to user's company
    existing_config = await db.get_document("workflow_configs", config_id)
    
    if not existing_config:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Workflow config {config_id} not found"
        )
    
    if existing_config["company_id"] != current_user.company_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this workflow config"
        )
    
    # Prepare update data
    update_dict = config_data.dict(exclude_unset=True)
    update_dict["updated_at"] = datetime.utcnow()
    
    # Don't allow changing company_id or created_by
    if "company_id" in update_dict:
        del update_dict["company_id"]
    
    if "created_by" in update_dict:
        del update_dict["created_by"]
    
    if "created_at" in update_dict:
        del update_dict["created_at"]
    
    # Update config in database
    result = await db.update_document("workflow_configs", config_id, update_dict)
    
    # Get updated config
    updated_config = await db.get_document("workflow_configs", config_id)
    
    return LeadNurturingConfig(**updated_config)

@router.delete("/configs/{config_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_workflow_config(
    config_id: str = Path(..., description="Workflow config ID"),
    current_user: UserAuth = Depends(get_current_user)
):
    """
    Delete a workflow configuration
    """
    # Check if config exists and belongs to user's company
    existing_config = await db.get_document("workflow_configs", config_id)
    
    if not existing_config:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Workflow config {config_id} not found"
        )
    
    if existing_config["company_id"] != current_user.company_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this workflow config"
        )
    
    # Delete config from database
    await db.delete_document("workflow_configs", config_id)
    
    return None

@router.get("/runs", response_model=Dict[str, Any])
async def list_workflow_runs(
    workflow_config_id: Optional[str] = Query(None, description="Filter by workflow config ID"),
    status: Optional[str] = Query(None, description="Filter by status"),
    page: int = Query(1, ge=1, description="Page number"),
    per_page: int = Query(20, ge=1, le=100, description="Items per page"),
    sort_by: str = Query("started_at", description="Field to sort by"),
    sort_dir: str = Query("desc", description="Sort direction (asc/desc)"),
    current_user: UserAuth = Depends(get_current_user)
):
    """
    List workflow runs
    """
    # Prepare filters
    filters = [{"field": "company_id", "op": "==", "value": current_user.company_id}]
    
    if workflow_config_id:
        filters.append({"field": "workflow_config_id", "op": "==", "value": workflow_config_id})
    
    if status:
        filters.append({"field": "status", "op": "==", "value": status})
    
    # Calculate pagination
    offset = (page - 1) * per_page
    
    # Query workflow runs
    runs = await db.query_collection(
        "workflow_runs",
        filters=filters,
        order_by=sort_by,
        order_direction=sort_dir,
        limit=per_page,
        offset=offset
    )
    
    # Get total count for pagination
    all_runs = await db.query_collection(
        "workflow_runs",
        filters=filters
    )
    total_items = len(all_runs)
    total_pages = (total_items + per_page - 1) // per_page  # Ceiling division
    
    # Enrich runs with workflow names
    config_ids = set(run["workflow_config_id"] for run in runs)
    configs = {}
    
    for config_id in config_ids:
        config_data = await db.get_document("workflow_configs", config_id)
        if config_data:
            configs[config_id] = config_data["name"]
    
    for run in runs:
        run["workflow_name"] = configs.get(run["workflow_config_id"], "Unknown")
    
    return {
        "data": runs,
        "meta": {
            "current_page": page,
            "per_page": per_page,
            "total_items": total_items,
            "total_pages": total_pages
        }
    }

@router.get("/runs/{run_id}", response_model=LeadNurturingRun)
async def get_workflow_run(
    run_id: str = Path(..., description="Workflow run ID"),
    current_user: UserAuth = Depends(get_current_user)
):
    """
    Get a workflow run by ID
    """
    # Get run from database
    run_data = await db.get_document("workflow_runs", run_id)
    
    if not run_data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Workflow run {run_id} not found"
        )
    
    # Check if run belongs to user's company
    if run_data["company_id"] != current_user.company_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this workflow run"
        )
    
    # Get workflow config name
    config_data = await db.get_document("workflow_configs", run_data["workflow_config_id"])
    if config_data:
        run_data["workflow_name"] = config_data["name"]
    else:
        run_data["workflow_name"] = "Unknown"
    
    return LeadNurturingRun(**run_data)

@router.post("/runs/trigger", response_model=LeadNurturingRun)
async def trigger_workflow_run(
    workflow_config_id: str = Query(..., description="Workflow config ID"),
    entity_id: str = Query(..., description="Entity ID (e.g., lead_id)"),
    current_user: UserAuth = Depends(get_current_user)
):
    """
    Manually trigger a workflow run
    """
    # Check if workflow config exists and belongs to user's company
    config_data = await db.get_document("workflow_configs", workflow_config_id)
    
    if not config_data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Workflow config {workflow_config_id} not found"
        )
    
    if config_data["company_id"] != current_user.company_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to trigger this workflow"
        )
    
    # Check if entity exists
    if entity_id.startswith("lead_"):
        from workflows.lead_nurturing.repository import LeadRepository
        entity = await LeadRepository.get_lead(entity_id)
        
        if not entity:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Lead {entity_id} not found"
            )
        
        if entity.company_id != current_user.company_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to access this lead"
            )
        
        # Create workflow run
        config = LeadNurturingConfig(**config_data)
        
        from workflows.lead_nurturing.service import LeadNurturingService
        run = await LeadNurturingService.execute_workflow(config, entity)
        
        return run
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Unsupported entity type: {entity_id}"
        )


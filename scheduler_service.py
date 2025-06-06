"""
Scheduler Service for Business Automation System.

This module provides the service layer for scheduling tasks.
"""

import uuid
import logging
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional, Callable

logger = logging.getLogger(__name__)


class SchedulerService:
    """Service for scheduling tasks."""

    def __init__(self):
        """Initialize the scheduler service."""
        # In a real implementation, this would connect to Celery or another task queue
        # For now, we'll just store scheduled tasks in memory
        self.scheduled_tasks = {}
        self.recurring_tasks = {}

    def schedule_task(self, task_type: str, params: Dict[str, Any], execute_at: datetime, company_id: str = None) -> Dict[str, Any]:
        """
        Schedule a task to be executed at a specific time.
        
        Args:
            task_type: Type of task to schedule
            params: Parameters for the task
            execute_at: Time to execute the task
            company_id: ID of the company
            
        Returns:
            Dictionary with schedule result
        """
        # Generate a task ID
        task_id = str(uuid.uuid4())
        
        # Store the task
        self.scheduled_tasks[task_id] = {
            "id": task_id,
            "type": task_type,
            "params": params,
            "execute_at": execute_at,
            "company_id": company_id,
            "status": "scheduled",
            "created_at": datetime.utcnow()
        }
        
        logger.info(f"Scheduled task {task_id} of type {task_type} to execute at {execute_at}")
        
        # In a real implementation, this would schedule the task with Celery
        # For now, we'll just return the task details
        return {
            "task_id": task_id,
            "type": task_type,
            "execute_at": execute_at,
            "status": "scheduled"
        }

    def schedule_recurring_task(self, task_type: str, params: Dict[str, Any], schedule: Dict[str, Any], company_id: str = None) -> Dict[str, Any]:
        """
        Schedule a recurring task.
        
        Args:
            task_type: Type of task to schedule
            params: Parameters for the task
            schedule: Schedule details (frequency, start_at, end_at, etc.)
            company_id: ID of the company
            
        Returns:
            Dictionary with schedule result
        """
        # Generate a task ID
        task_id = str(uuid.uuid4())
        
        # Store the task
        self.recurring_tasks[task_id] = {
            "id": task_id,
            "type": task_type,
            "params": params,
            "schedule": schedule,
            "company_id": company_id,
            "status": "active",
            "created_at": datetime.utcnow(),
            "last_executed_at": None,
            "next_execution_at": self._calculate_next_execution(schedule)
        }
        
        logger.info(f"Scheduled recurring task {task_id} of type {task_type} with frequency {schedule.get('frequency')}")
        
        # In a real implementation, this would schedule the task with Celery Beat
        # For now, we'll just return the task details
        return {
            "task_id": task_id,
            "type": task_type,
            "schedule": schedule,
            "next_execution_at": self.recurring_tasks[task_id]["next_execution_at"],
            "status": "active"
        }

    def _calculate_next_execution(self, schedule: Dict[str, Any]) -> datetime:
        """
        Calculate the next execution time based on a schedule.
        
        Args:
            schedule: Schedule details
            
        Returns:
            Next execution time
        """
        now = datetime.utcnow()
        frequency = schedule.get("frequency", "daily")
        start_at = schedule.get("start_at", now)
        
        if start_at < now:
            # If start time is in the past, calculate next occurrence
            if frequency == "hourly":
                # Next hour
                next_hour = now.replace(minute=0, second=0, microsecond=0) + timedelta(hours=1)
                return next_hour
            elif frequency == "daily":
                # Tomorrow at the same time
                tomorrow = now + timedelta(days=1)
                return tomorrow.replace(hour=start_at.hour, minute=start_at.minute, second=0, microsecond=0)
            elif frequency == "weekly":
                # Next week on the same day
                days_ahead = schedule.get("day_of_week", start_at.weekday())
                days_ahead -= now.weekday()
                if days_ahead <= 0:
                    days_ahead += 7
                next_week = now + timedelta(days=days_ahead)
                return next_week.replace(hour=start_at.hour, minute=start_at.minute, second=0, microsecond=0)
            elif frequency == "monthly":
                # Next month on the same day
                day_of_month = schedule.get("day_of_month", start_at.day)
                if now.day < day_of_month:
                    # Later this month
                    next_month = now.replace(day=day_of_month)
                else:
                    # Next month
                    if now.month == 12:
                        next_month = now.replace(year=now.year + 1, month=1, day=day_of_month)
                    else:
                        next_month = now.replace(month=now.month + 1, day=day_of_month)
                return next_month.replace(hour=start_at.hour, minute=start_at.minute, second=0, microsecond=0)
            else:
                # Default to tomorrow
                tomorrow = now + timedelta(days=1)
                return tomorrow.replace(hour=start_at.hour, minute=start_at.minute, second=0, microsecond=0)
        else:
            # If start time is in the future, use it
            return start_at

    def cancel_task(self, task_id: str) -> Dict[str, Any]:
        """
        Cancel a scheduled task.
        
        Args:
            task_id: ID of the task to cancel
            
        Returns:
            Dictionary with cancel result
        """
        # Check if task exists
        if task_id in self.scheduled_tasks:
            self.scheduled_tasks[task_id]["status"] = "cancelled"
            logger.info(f"Cancelled scheduled task {task_id}")
            return {
                "task_id": task_id,
                "status": "cancelled"
            }
        elif task_id in self.recurring_tasks:
            self.recurring_tasks[task_id]["status"] = "cancelled"
            logger.info(f"Cancelled recurring task {task_id}")
            return {
                "task_id": task_id,
                "status": "cancelled"
            }
        else:
            logger.warning(f"Task {task_id} not found")
            return {
                "task_id": task_id,
                "status": "not_found"
            }

    def get_task(self, task_id: str) -> Optional[Dict[str, Any]]:
        """
        Get a task by ID.
        
        Args:
            task_id: ID of the task
            
        Returns:
            Task details or None if not found
        """
        if task_id in self.scheduled_tasks:
            return self.scheduled_tasks[task_id]
        elif task_id in self.recurring_tasks:
            return self.recurring_tasks[task_id]
        else:
            return None

    def get_tasks(self, company_id: str = None, task_type: str = None, status: str = None) -> List[Dict[str, Any]]:
        """
        Get tasks with optional filtering.
        
        Args:
            company_id: Filter by company ID
            task_type: Filter by task type
            status: Filter by status
            
        Returns:
            List of tasks
        """
        # Combine scheduled and recurring tasks
        all_tasks = list(self.scheduled_tasks.values()) + list(self.recurring_tasks.values())
        
        # Apply filters
        filtered_tasks = all_tasks
        if company_id:
            filtered_tasks = [task for task in filtered_tasks if task.get("company_id") == company_id]
        if task_type:
            filtered_tasks = [task for task in filtered_tasks if task.get("type") == task_type]
        if status:
            filtered_tasks = [task for task in filtered_tasks if task.get("status") == status]
        
        return filtered_tasks

    def update_task(self, task_id: str, params: Dict[str, Any] = None, execute_at: datetime = None, status: str = None) -> Optional[Dict[str, Any]]:
        """
        Update a scheduled task.
        
        Args:
            task_id: ID of the task
            params: New parameters for the task
            execute_at: New execution time
            status: New status
            
        Returns:
            Updated task or None if not found
        """
        if task_id in self.scheduled_tasks:
            task = self.scheduled_tasks[task_id]
            
            if params:
                task["params"] = params
            if execute_at:
                task["execute_at"] = execute_at
            if status:
                task["status"] = status
            
            logger.info(f"Updated scheduled task {task_id}")
            return task
        else:
            logger.warning(f"Task {task_id} not found")
            return None

    def update_recurring_task(self, task_id: str, params: Dict[str, Any] = None, schedule: Dict[str, Any] = None, status: str = None) -> Optional[Dict[str, Any]]:
        """
        Update a recurring task.
        
        Args:
            task_id: ID of the task
            params: New parameters for the task
            schedule: New schedule details
            status: New status
            
        Returns:
            Updated task or None if not found
        """
        if task_id in self.recurring_tasks:
            task = self.recurring_tasks[task_id]
            
            if params:
                task["params"] = params
            if schedule:
                task["schedule"] = schedule
                task["next_execution_at"] = self._calculate_next_execution(schedule)
            if status:
                task["status"] = status
            
            logger.info(f"Updated recurring task {task_id}")
            return task
        else:
            logger.warning(f"Task {task_id} not found")
            return None

    def execute_task(self, task_id: str) -> Dict[str, Any]:
        """
        Execute a task immediately.
        
        Args:
            task_id: ID of the task
            
        Returns:
            Dictionary with execution result
        """
        # In a real implementation, this would trigger the task execution
        # For now, we'll just update the task status
        
        if task_id in self.scheduled_tasks:
            task = self.scheduled_tasks[task_id]
            task["status"] = "executed"
            task["executed_at"] = datetime.utcnow()
            
            logger.info(f"Executed scheduled task {task_id}")
            return {
                "task_id": task_id,
                "status": "executed",
                "executed_at": task["executed_at"]
            }
        elif task_id in self.recurring_tasks:
            task = self.recurring_tasks[task_id]
            task["last_executed_at"] = datetime.utcnow()
            task["next_execution_at"] = self._calculate_next_execution(task["schedule"])
            
            logger.info(f"Executed recurring task {task_id}")
            return {
                "task_id": task_id,
                "status": "executed",
                "executed_at": task["last_executed_at"],
                "next_execution_at": task["next_execution_at"]
            }
        else:
            logger.warning(f"Task {task_id} not found")
            return {
                "task_id": task_id,
                "status": "not_found"
            }

    def schedule_lead_followup(self, lead_id: str, company_id: str, delay_hours: int = 24) -> Dict[str, Any]:
        """
        Schedule a lead follow-up task.
        
        Args:
            lead_id: ID of the lead
            company_id: ID of the company
            delay_hours: Hours to delay before follow-up
            
        Returns:
            Dictionary with schedule result
        """
        execute_at = datetime.utcnow() + timedelta(hours=delay_hours)
        
        params = {
            "lead_id": lead_id,
            "company_id": company_id,
            "followup_type": "first" if delay_hours == 24 else "final"
        }
        
        return self.schedule_task("lead_followup", params, execute_at, company_id)

    def schedule_review_request(self, customer_id: str, company_id: str, delay_days: int = 3) -> Dict[str, Any]:
        """
        Schedule a review request task.
        
        Args:
            customer_id: ID of the customer
            company_id: ID of the company
            delay_days: Days to delay before sending request
            
        Returns:
            Dictionary with schedule result
        """
        execute_at = datetime.utcnow() + timedelta(days=delay_days)
        
        params = {
            "customer_id": customer_id,
            "company_id": company_id
        }
        
        return self.schedule_task("review_request", params, execute_at, company_id)

    def schedule_content_generation(self, company_id: str, content_type: str, topic: str, schedule: Dict[str, Any]) -> Dict[str, Any]:
        """
        Schedule content generation.
        
        Args:
            company_id: ID of the company
            content_type: Type of content to generate
            topic: Topic for the content
            schedule: Schedule details
            
        Returns:
            Dictionary with schedule result
        """
        params = {
            "company_id": company_id,
            "content_type": content_type,
            "topic": topic
        }
        
        return self.schedule_recurring_task("content_generation", params, schedule, company_id)


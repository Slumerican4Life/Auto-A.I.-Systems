import os
import logging
from typing import Dict, List, Any, Optional, Union
import json
from datetime import datetime

from core.config import settings

logger = logging.getLogger(__name__)

class DatabaseClient:
    """
    Abstract database client that provides a unified interface for different database backends.
    """
    
    def __init__(self):
        self.db_type = settings.DB_TYPE
        self.client = None
        self.initialize()
    
    def initialize(self):
        """Initialize the database client based on the configured type."""
        try:
            if self.db_type == "firebase":
                self._initialize_firebase()
            elif self.db_type == "postgresql":
                self._initialize_postgresql()
            else:
                raise ValueError(f"Unsupported database type: {self.db_type}")
            
            logger.info(f"Database client initialized with type: {self.db_type}")
        except Exception as e:
            logger.error(f"Failed to initialize database client: {e}")
            raise
    
    def _initialize_firebase(self):
        """Initialize Firebase client."""
        try:
            import firebase_admin
            from firebase_admin import credentials, firestore
            
            # Check if already initialized
            if not firebase_admin._apps:
                # Initialize with service account
                if settings.FIREBASE_SERVICE_ACCOUNT_PATH:
                    cred = credentials.Certificate(settings.FIREBASE_SERVICE_ACCOUNT_PATH)
                else:
                    # Use environment variables
                    service_account_info = {
                        "type": "service_account",
                        "project_id": settings.FIREBASE_PROJECT_ID,
                        "private_key": settings.FIREBASE_PRIVATE_KEY.replace("\\n", "\n"),
                        "client_email": settings.FIREBASE_CLIENT_EMAIL,
                        "token_uri": "https://oauth2.googleapis.com/token"
                    }
                    cred = credentials.Certificate(service_account_info)
                
                firebase_admin.initialize_app(cred)
            
            self.client = firestore.client()
            logger.info("Firebase client initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize Firebase client: {e}")
            raise
    
    def _initialize_postgresql(self):
        """Initialize PostgreSQL client."""
        try:
            import asyncpg
            
            self.pool = None
            self.dsn = f"postgresql://{settings.POSTGRES_USER}:{settings.POSTGRES_PASSWORD}@{settings.POSTGRES_HOST}:{settings.POSTGRES_PORT}/{settings.POSTGRES_DB}"
            
            logger.info("PostgreSQL client configuration set successfully")
        except Exception as e:
            logger.error(f"Failed to initialize PostgreSQL client: {e}")
            raise
    
    async def _get_pg_pool(self):
        """Get or create PostgreSQL connection pool."""
        if self.pool is None:
            import asyncpg
            self.pool = await asyncpg.create_pool(dsn=self.dsn)
        return self.pool
    
    async def create_document(self, collection: str, data: Dict[str, Any], doc_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Create a new document in the specified collection.
        
        Args:
            collection: Collection name
            data: Document data
            doc_id: Optional document ID
            
        Returns:
            Created document data
        """
        try:
            if self.db_type == "firebase":
                # Convert datetime objects to Firestore timestamps
                data = self._convert_datetimes_for_firebase(data)
                
                # Create document
                if doc_id:
                    doc_ref = self.client.collection(collection).document(doc_id)
                    doc_ref.set(data)
                else:
                    doc_ref = self.client.collection(collection).add(data)[1]
                
                # Get created document
                doc = doc_ref.get()
                result = doc.to_dict()
                result["id"] = doc.id
                
                return result
            elif self.db_type == "postgresql":
                pool = await self._get_pg_pool()
                
                # Convert data to JSON-compatible format
                data_json = self._convert_for_postgresql(data)
                
                # Create document
                async with pool.acquire() as conn:
                    if doc_id:
                        # Check if ID column exists
                        id_exists = await conn.fetchval(
                            f"SELECT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name = '{collection}' AND column_name = 'id')"
                        )
                        
                        if id_exists:
                            # Insert with specified ID
                            columns = list(data_json.keys())
                            values = list(data_json.values())
                            
                            # Add ID to columns and values
                            if "id" not in columns:
                                columns.append("id")
                                values.append(doc_id)
                            
                            placeholders = [f"${i+1}" for i in range(len(values))]
                            
                            query = f"""
                                INSERT INTO {collection} ({', '.join(columns)})
                                VALUES ({', '.join(placeholders)})
                                RETURNING *
                            """
                            
                            result = await conn.fetchrow(query, *values)
                            return dict(result)
                        else:
                            # Table doesn't have ID column, use regular insert
                            columns = list(data_json.keys())
                            values = list(data_json.values())
                            placeholders = [f"${i+1}" for i in range(len(values))]
                            
                            query = f"""
                                INSERT INTO {collection} ({', '.join(columns)})
                                VALUES ({', '.join(placeholders)})
                                RETURNING *
                            """
                            
                            result = await conn.fetchrow(query, *values)
                            return dict(result)
                    else:
                        # Insert without specified ID
                        columns = list(data_json.keys())
                        values = list(data_json.values())
                        placeholders = [f"${i+1}" for i in range(len(values))]
                        
                        query = f"""
                            INSERT INTO {collection} ({', '.join(columns)})
                            VALUES ({', '.join(placeholders)})
                            RETURNING *
                        """
                        
                        result = await conn.fetchrow(query, *values)
                        return dict(result)
            else:
                raise ValueError(f"Unsupported database type: {self.db_type}")
        except Exception as e:
            logger.error(f"Error creating document in {collection}: {e}")
            raise
    
    async def get_document(self, collection: str, doc_id: str) -> Optional[Dict[str, Any]]:
        """
        Get a document by ID.
        
        Args:
            collection: Collection name
            doc_id: Document ID
            
        Returns:
            Document data or None if not found
        """
        try:
            if self.db_type == "firebase":
                doc = self.client.collection(collection).document(doc_id).get()
                
                if not doc.exists:
                    return None
                
                result = doc.to_dict()
                result["id"] = doc.id
                
                return result
            elif self.db_type == "postgresql":
                pool = await self._get_pg_pool()
                
                async with pool.acquire() as conn:
                    # Check if ID column exists
                    id_exists = await conn.fetchval(
                        f"SELECT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name = '{collection}' AND column_name = 'id')"
                    )
                    
                    if id_exists:
                        query = f"SELECT * FROM {collection} WHERE id = $1"
                        result = await conn.fetchrow(query, doc_id)
                        
                        if result:
                            return dict(result)
                        else:
                            return None
                    else:
                        # If no ID column, return None
                        return None
            else:
                raise ValueError(f"Unsupported database type: {self.db_type}")
        except Exception as e:
            logger.error(f"Error getting document {doc_id} from {collection}: {e}")
            raise
    
    async def update_document(self, collection: str, doc_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Update a document by ID.
        
        Args:
            collection: Collection name
            doc_id: Document ID
            data: Document data to update
            
        Returns:
            Updated document data
        """
        try:
            if self.db_type == "firebase":
                # Convert datetime objects to Firestore timestamps
                data = self._convert_datetimes_for_firebase(data)
                
                # Update document
                doc_ref = self.client.collection(collection).document(doc_id)
                doc_ref.update(data)
                
                # Get updated document
                doc = doc_ref.get()
                result = doc.to_dict()
                result["id"] = doc.id
                
                return result
            elif self.db_type == "postgresql":
                pool = await self._get_pg_pool()
                
                # Convert data to JSON-compatible format
                data_json = self._convert_for_postgresql(data)
                
                async with pool.acquire() as conn:
                    # Check if ID column exists
                    id_exists = await conn.fetchval(
                        f"SELECT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name = '{collection}' AND column_name = 'id')"
                    )
                    
                    if id_exists:
                        # Build SET clause
                        set_clause = ", ".join([f"{key} = ${i+2}" for i, key in enumerate(data_json.keys())])
                        
                        query = f"""
                            UPDATE {collection}
                            SET {set_clause}
                            WHERE id = $1
                            RETURNING *
                        """
                        
                        result = await conn.fetchrow(query, doc_id, *data_json.values())
                        
                        if result:
                            return dict(result)
                        else:
                            raise ValueError(f"Document {doc_id} not found in {collection}")
                    else:
                        raise ValueError(f"Table {collection} does not have an ID column")
            else:
                raise ValueError(f"Unsupported database type: {self.db_type}")
        except Exception as e:
            logger.error(f"Error updating document {doc_id} in {collection}: {e}")
            raise
    
    async def delete_document(self, collection: str, doc_id: str) -> Dict[str, Any]:
        """
        Delete a document by ID.
        
        Args:
            collection: Collection name
            doc_id: Document ID
            
        Returns:
            Result of the operation
        """
        try:
            if self.db_type == "firebase":
                # Delete document
                self.client.collection(collection).document(doc_id).delete()
                
                return {"deleted": True, "id": doc_id}
            elif self.db_type == "postgresql":
                pool = await self._get_pg_pool()
                
                async with pool.acquire() as conn:
                    # Check if ID column exists
                    id_exists = await conn.fetchval(
                        f"SELECT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name = '{collection}' AND column_name = 'id')"
                    )
                    
                    if id_exists:
                        query = f"DELETE FROM {collection} WHERE id = $1 RETURNING id"
                        result = await conn.fetchval(query, doc_id)
                        
                        if result:
                            return {"deleted": True, "id": doc_id}
                        else:
                            return {"deleted": False, "id": doc_id}
                    else:
                        raise ValueError(f"Table {collection} does not have an ID column")
            else:
                raise ValueError(f"Unsupported database type: {self.db_type}")
        except Exception as e:
            logger.error(f"Error deleting document {doc_id} from {collection}: {e}")
            raise
    
    async def query_collection(
        self, 
        collection: str, 
        filters: Optional[List[Dict[str, Any]]] = None,
        order_by: Optional[str] = None,
        order_direction: Optional[str] = "asc",
        limit: Optional[int] = None,
        offset: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """
        Query a collection with filters and ordering.
        
        Args:
            collection: Collection name
            filters: List of filter conditions
            order_by: Field to order by
            order_direction: Order direction (asc or desc)
            limit: Maximum number of documents to return
            offset: Number of documents to skip
            
        Returns:
            List of documents matching the query
        """
        try:
            if self.db_type == "firebase":
                # Start query
                query = self.client.collection(collection)
                
                # Apply filters
                if filters:
                    for filter_condition in filters:
                        field = filter_condition.get("field")
                        op = filter_condition.get("op")
                        value = filter_condition.get("value")
                        
                        if field and op and value is not None:
                            query = query.where(field, op, value)
                
                # Apply ordering
                if order_by:
                    query = query.order_by(order_by, direction=order_direction)
                
                # Apply limit
                if limit:
                    query = query.limit(limit)
                
                # Execute query
                docs = query.stream()
                
                # Apply offset manually (Firestore doesn't support offset directly)
                results = []
                for i, doc in enumerate(docs):
                    if offset and i < offset:
                        continue
                    
                    data = doc.to_dict()
                    data["id"] = doc.id
                    results.append(data)
                
                return results
            elif self.db_type == "postgresql":
                pool = await self._get_pg_pool()
                
                async with pool.acquire() as conn:
                    # Build query
                    query = f"SELECT * FROM {collection}"
                    
                    # Apply filters
                    params = []
                    if filters:
                        where_clauses = []
                        for i, filter_condition in enumerate(filters):
                            field = filter_condition.get("field")
                            op = filter_condition.get("op")
                            value = filter_condition.get("value")
                            
                            if field and op and value is not None:
                                # Convert operator
                                pg_op = self._convert_operator_for_postgresql(op)
                                where_clauses.append(f"{field} {pg_op} ${len(params) + 1}")
                                params.append(value)
                        
                        if where_clauses:
                            query += f" WHERE {' AND '.join(where_clauses)}"
                    
                    # Apply ordering
                    if order_by:
                        query += f" ORDER BY {order_by} {order_direction.upper()}"
                    
                    # Apply limit
                    if limit:
                        query += f" LIMIT {limit}"
                    
                    # Apply offset
                    if offset:
                        query += f" OFFSET {offset}"
                    
                    # Execute query
                    rows = await conn.fetch(query, *params)
                    
                    # Convert to list of dicts
                    results = [dict(row) for row in rows]
                    
                    return results
            else:
                raise ValueError(f"Unsupported database type: {self.db_type}")
        except Exception as e:
            logger.error(f"Error querying collection {collection}: {e}")
            raise
    
    def _convert_datetimes_for_firebase(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Convert datetime objects to Firestore timestamps."""
        from firebase_admin import firestore
        
        result = {}
        for key, value in data.items():
            if isinstance(value, datetime):
                result[key] = firestore.SERVER_TIMESTAMP if value is None else firestore.Timestamp.from_datetime(value)
            elif isinstance(value, dict):
                result[key] = self._convert_datetimes_for_firebase(value)
            elif isinstance(value, list):
                result[key] = [
                    self._convert_datetimes_for_firebase(item) if isinstance(item, dict) else item
                    for item in value
                ]
            else:
                result[key] = value
        
        return result
    
    def _convert_for_postgresql(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Convert data to PostgreSQL-compatible format."""
        result = {}
        for key, value in data.items():
            if isinstance(value, dict) or isinstance(value, list):
                result[key] = json.dumps(value)
            else:
                result[key] = value
        
        return result
    
    def _convert_operator_for_postgresql(self, op: str) -> str:
        """Convert Firestore operator to PostgreSQL operator."""
        op_map = {
            "==": "=",
            "!=": "!=",
            "<": "<",
            "<=": "<=",
            ">": ">",
            ">=": ">=",
            "array-contains": "@>",
            "in": "IN",
            "not-in": "NOT IN"
        }
        
        return op_map.get(op, "=")

# Create database client instance
db = DatabaseClient()


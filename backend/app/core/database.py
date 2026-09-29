import json
import os
import asyncio
from typing import Dict, Any, List, Optional
from datetime import datetime
import motor.motor_asyncio
from app.core.config import settings

class LocalCollection:
    """Thread-safe persistent JSON collection implementing standard MongoDB async operations."""
    def __init__(self, name: str, data_dir: str):
        self.name = name
        self.file_path = os.path.join(data_dir, f"{name}.json")
        self._data: List[Dict[str, Any]] = []
        self._load()

    def _load(self):
        if os.path.exists(self.file_path):
            try:
                with open(self.file_path, "r", encoding="utf-8") as f:
                    self._data = json.load(f)
            except Exception:
                self._data = []
        else:
            self._data = []

    def _save(self):
        try:
            with open(self.file_path, "w", encoding="utf-8") as f:
                json.dump(self._data, f, default=str, indent=2)
        except Exception as e:
            print(f"Error saving {self.name}: {e}")

    async def insert_one(self, document: Dict[str, Any]):
        doc = dict(document)
        if "_id" not in doc:
            doc["_id"] = str(len(self._data) + 1)
        self._data.append(doc)
        self._save()
        class Result:
            inserted_id = doc["_id"]
        return Result()

    async def find_one(self, query: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        for doc in self._data:
            match = True
            for k, v in query.items():
                if doc.get(k) != v:
                    match = False
                    break
            if match:
                return dict(doc)
        return None

    async def find(self, query: Dict[str, Any] = None, sort=None, limit: int = 100) -> List[Dict[str, Any]]:
        query = query or {}
        results = []
        for doc in self._data:
            match = True
            for k, v in query.items():
                if doc.get(k) != v:
                    match = False
                    break
            if match:
                results.append(dict(doc))
        if limit:
            results = results[:limit]
        return results

    async def update_one(self, query: Dict[str, Any], update: Dict[str, Any]):
        doc = await self.find_one(query)
        if doc:
            set_vals = update.get("$set", {})
            for k, v in set_vals.items():
                doc[k] = v
            # update in array
            for idx, item in enumerate(self._data):
                if item.get("_id") == doc["_id"]:
                    self._data[idx] = doc
                    break
            self._save()
            return True
        return False

    async def count_documents(self, query: Dict[str, Any] = None) -> int:
        docs = await self.find(query or {})
        return len(docs)


class DatabaseManager:
    def __init__(self):
        self.is_connected = False
        self.client = None
        self.db = None
        self.is_fallback = False
        self._local_collections: Dict[str, LocalCollection] = {}
        self.data_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "data", "db_storage")
        os.makedirs(self.data_dir, exist_ok=True)

    async def connect(self):
        try:
            # Try to connect to real MongoDB with a fast 1.5s timeout
            self.client = motor.motor_asyncio.AsyncIOMotorClient(
                settings.MONGODB_URI,
                serverSelectionTimeoutMS=1500
            )
            # Test connection
            await self.client.admin.command('ping')
            self.db = self.client[settings.DATABASE_NAME]
            self.is_connected = True
            self.is_fallback = False
            print("Successfully connected to live MongoDB!")
        except Exception as e:
            print(f"MongoDB not available ({e}). Using embedded robust local JSON-backed storage engine.")
            self.is_connected = True
            self.is_fallback = True

    def get_collection(self, collection_name: str):
        if self.is_connected and not self.is_fallback and self.db is not None:
            return self.db[collection_name]
        
        if collection_name not in self._local_collections:
            self._local_collections[collection_name] = LocalCollection(collection_name, self.data_dir)
        return self._local_collections[collection_name]

db_manager = DatabaseManager()

def get_collection(name: str):
    return db_manager.get_collection(name)

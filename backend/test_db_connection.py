#!/usr/bin/env python3
"""
Simple test to verify MongoDB connection
"""

import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from app.core.config import settings

async def test_mongodb_connection():
    """Test MongoDB connection"""
    try:
        # Create MongoDB client
        client = AsyncIOMotorClient(settings.MONGODB_URL)
        
        # Test connection
        await client.admin.command('ping')
        print("✅ MongoDB connection successful!")
        
        # List databases
        databases = await client.list_database_names()
        print(f"📊 Available databases: {databases}")
        
        # Test database operations
        db = client[settings.DATABASE_NAME]
        
        # Test collection operations
        collection = db.test_collection
        
        # Insert a test document
        test_doc = {"test": "hello", "message": "MongoDB connection works!"}
        result = await collection.insert_one(test_doc)
        print(f"✅ Test document inserted with ID: {result.inserted_id}")
        
        # Read the document back
        doc = await collection.find_one({"_id": result.inserted_id})
        print(f"📄 Retrieved document: {doc}")
        
        # Clean up - delete the test document
        await collection.delete_one({"_id": result.inserted_id})
        print("🧹 Test document cleaned up")
        
        # Close connection
        client.close()
        print("✅ MongoDB connection test completed successfully!")
        
    except Exception as e:
        print(f"❌ MongoDB connection failed: {e}")
        return False
    
    return True

if __name__ == "__main__":
    asyncio.run(test_mongodb_connection())

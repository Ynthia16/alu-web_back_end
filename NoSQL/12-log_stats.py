#!/usr/bin/env python3
"""log stats from collection
"""
from pymongo import MongoClient

METHODS = ["GET", "POST", "PUT", "PATCH", "DELETE"]

def log_stats(mongo_collection):
    """Script that provides some stats about Nginx logs stored in MongoDB"""
    # Count all documents
    total_logs = mongo_collection.count_documents({})
    
    print(f"Total logs: {total_logs}")
    
    # Print methods
    print("\nMethods:")
    for method in METHODS:
        method_count = mongo_collection.count_documents({"method": method})
        print(f"\t{method}: {method_count}")

    # Check for status
    status_check = mongo_collection.count_documents({"path": "/status"})
    print(f"\nStatus check: {status_check}")

if __name__ == "__main__":
    client = MongoClient('mongodb://127.0.0.1:27017')
    db = client['your_database_name']
    nginx_collection = db['nginx']
    log_stats(nginx_collection)

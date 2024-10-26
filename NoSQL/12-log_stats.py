#!/usr/bin/env python3
"""Log stats from collection
"""
from pymongo import MongoClient

def log_stats():
    """Script that provides some stats about Nginx logs stored in MongoDB"""
    client = MongoClient('mongodb://localhost:27017')  # Adjust connection string if needed
    db = client['logs']  # Ensure we're using the correct database
    collection = db['nginx']

    # Count all documents
    total_logs = collection.count_documents({})

    print(f"{total_logs} logs")

    # Print methods
    print("\nMethods:")
    for method in ["GET", "POST", "PUT", "PATCH", "DELETE"]:
        method_count = collection.count_documents({"method": method})
        print(f"\t{method}: {method_count}")

    # Check for status
    status_check = collection.count_documents({"path": "/status"})
    print(f"\nStatus check: {status_check}")

if __name__ == "__main__":
    log_stats()

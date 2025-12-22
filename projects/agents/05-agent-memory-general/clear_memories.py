"""Quick script to clear Mem0 memories for demo reset."""
import os
from dotenv import load_dotenv
from mem0 import Memory

load_dotenv()


def build_memory_config():
    service_name = os.getenv("AZURE_SEARCH_SERVICE_NAME")
    if not service_name:
        endpoint = os.getenv("AZURE_SEARCH_ENDPOINT", "")
        if endpoint.startswith("https://"):
            endpoint = endpoint[len("https://"):]
        if endpoint:
            service_name = endpoint.split(".search.windows.net")[0].split(".")[0]

    embedding_deployment = os.getenv("AZURE_TEXT_EMBEDDING_DEPLOYMENT_NAME") or os.getenv(
        "AZURE_OPENAI_EMBEDDING_DEPLOYMENT_NAME"
    )
    collection_name = os.getenv("AZURE_SEARCH_COLLECTION_NAME") or os.getenv("AZURE_SEARCH_INDEX_NAME")

    # Same config as file 22 (no LLM - we use Responses API for fact extraction)
    return {
        "vector_store": {
            "provider": "azure_ai_search",
            "config": {
                "service_name": service_name,
                "api_key": os.getenv("AZURE_SEARCH_ADMIN_KEY"),
                "collection_name": collection_name,
            },
        },
        "embeddings": {
            "provider": "azure_openai",
            "config": {
                "api_key": os.getenv("AZURE_OPENAI_API_KEY"),
                "api_version": os.getenv("AZURE_OPENAI_API_VERSION"),
                "azure_endpoint": os.getenv("AZURE_OPENAI_ENDPOINT"),
                "deployment_name": embedding_deployment,
            },
        },
    }


def main():
    print("Initializing Mem0...")
    memory = Memory.from_config(build_memory_config())

    user_ids = [
        "user-ozgur",
        "user-ozgur-optimization",
        "user-ozgur-forecasting",
    ]

    total_deleted = 0
    for user_id in user_ids:
        print(f"\n[{user_id}]")
        try:
            # First, get all memories for this user
            all_memories = memory.get_all(user_id=user_id)
            memories_list = all_memories.get("results", []) if isinstance(all_memories, dict) else all_memories
            
            if not memories_list:
                print(f"  No memories found.")
                continue
                
            print(f"  Found {len(memories_list)} memories. Deleting...")
            
            # Delete each memory individually
            for mem in memories_list:
                mem_id = mem.get("id")
                if mem_id:
                    try:
                        memory.delete(memory_id=mem_id)
                        print(f"    ✓ Deleted: {mem_id[:20]}... ({mem.get('memory', '')[:40]}...)")
                        total_deleted += 1
                    except Exception as del_err:
                        print(f"    ✗ Failed to delete {mem_id}: {del_err}")
                        
        except Exception as e:
            print(f"  Error: {e}")

    print(f"\n✓ Done! Deleted {total_deleted} memories total.")


if __name__ == "__main__":
    main()

 #!/usr/bin/env python3
"""
Database Query Tool

Standalone script to query the object detection database using natural language.

Usage:
    python query_db.py "photos of burnt vegetation"
    python query_db.py "people walking" --count 10
    python query_db.py "cars in street" --open
"""

import os
import sys
import argparse
from colorama import Fore, Style
from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma

# Configuration (should match your main script)
db_name = 'db_photos'
db_collection_name = "photo_collection"
embedding_model = "nomic-embed-text:v1.5"

def query_database(query_text, k=5, open_files=False):
    """Query the vector database for similar content"""
    
    print(f"{Fore.CYAN}Querying database for: '{query_text}'{Style.RESET_ALL}")
    print(f"Returning top {k} results...")
    print("-" * 60)
    
    try:
        # Initialize database connection
        embedding_function = OllamaEmbeddings(model=embedding_model)
        db = Chroma(
            collection_name=db_collection_name,
            embedding_function=embedding_function,
            persist_directory=f"./{db_name}")
        
        # Perform similarity search
        results = db.similarity_search(query_text, k=k)
        
        if not results:
            print(f"{Fore.YELLOW}No results found for query: '{query_text}'{Style.RESET_ALL}")
            print("\nPossible reasons:")
            print("- Database is empty (no images/videos processed yet)")
            print("- Query terms don't match processed content")
            print("- Try broader search terms")
            return
        
        print(f"{Fore.GREEN}Found {len(results)} results:{Style.RESET_ALL}\n")
        
        opened_files = 0
        for i, doc in enumerate(results, 1):
            metadata = doc.metadata
            content_type = metadata.get('content_type', 'image')
            file_path = metadata.get('file_name', 'Unknown')
            
            print(f"{Fore.CYAN}Result {i}:{Style.RESET_ALL}")
            print(f"  📁 File: {file_path}")
            print(f"  📋 Type: {content_type}")
            
            if content_type == 'video_frame':
                timestamp = metadata.get('timestamp', 'Unknown')
                frame_num = metadata.get('frame_number', 'Unknown')
                print(f"  ⏱️  Time: {timestamp}s (Frame {frame_num})")
            
            # Show detected objects
            detected_objects = metadata.get('detected_objects', '')
            if detected_objects and detected_objects != 'NO_OBJECTS_DETECTED':
                print(f"  🔍 Objects: {detected_objects}")
            
            # Show camera info for images
            if content_type == 'image':
                make = metadata.get('make', '')
                model = metadata.get('model', '')
                if make or model:
                    print(f"  📷 Camera: {make} {model}".strip())
            
            # Show partial content
            content_preview = doc.page_content[:200] + "..." if len(doc.page_content) > 200 else doc.page_content
            print(f"  📝 Description: {content_preview}")
            
            # Try to open file if requested and it exists
            if open_files:
                try:
                    if os.path.exists(file_path):
                        print(f"  🚀 Opening: {file_path}")
                        os.startfile(file_path)
                        opened_files += 1
                    else:
                        print(f"  ❌ File not found: {file_path}")
                except Exception as e:
                    print(f"  ⚠️  Could not open file: {str(e)}")
            
            print()
        
        if open_files:
            print(f"{Fore.GREEN}Successfully opened {opened_files} of {len(results)} files{Style.RESET_ALL}")
        
        # Show additional tips
        print(f"{Fore.YELLOW}💡 Tips:{Style.RESET_ALL}")
        print("  • Use --open to automatically open found files")
        print("  • Use --count N to get more/fewer results")
        print("  • Try broader terms if no results found")
        
    except Exception as e:
        print(f"{Fore.RED}Error querying database: {str(e)}{Style.RESET_ALL}")
        print("\nPossible solutions:")
        print("- Make sure you've processed some images/videos first")
        print("- Check that Ollama is running")
        print("- Verify the database directory exists")

def print_examples():
    """Print example queries"""
    print(f"{Fore.CYAN}DATABASE QUERY EXAMPLES{Style.RESET_ALL}")
    print("=" * 50)
    print("Here are some example queries you can try:")
    print()
    
    examples = [
        ("General Objects", [
            "people in photos",
            "cars and vehicles", 
            "animals or pets",
            "buildings and architecture"
        ]),
        ("Activities", [
            "people walking",
            "sports activities",
            "cooking or food",
            "outdoor activities"
        ]),
        ("Scenes", [
            "outdoor scenes",
            "nature and landscapes", 
            "urban environments",
            "indoor spaces"
        ]),
        ("Specific", [
            "photos of burnt vegetation",
            "sunset or sunrise",
            "rainy weather",
            "crowded places"
        ])
    ]
    
    for category, queries in examples:
        print(f"{Fore.YELLOW}{category}:{Style.RESET_ALL}")
        for query in queries:
            print(f"  python query_db.py \"{query}\"")
        print()
    
    print(f"{Fore.GREEN}Usage patterns:{Style.RESET_ALL}")
    print("  python query_db.py \"search terms\" --count 10")
    print("  python query_db.py \"search terms\" --open")
    print("  python query_db.py \"search terms\" --count 3 --open")

def main():
    parser = argparse.ArgumentParser(description='Query the object detection database')
    parser.add_argument('query', help='Search query (natural language)')
    parser.add_argument('--count', '-c', type=int, default=5, 
                       help='Number of results to return (default: 5)')
    parser.add_argument('--open', '-o', action='store_true',
                       help='Automatically open found files')
    parser.add_argument('--examples', '-e', action='store_true',
                       help='Show example queries')
    
    args = parser.parse_args()
    
    if args.examples:
        print_examples()
        return
    
    if not args.query.strip():
        print(f"{Fore.RED}Error: Query cannot be empty{Style.RESET_ALL}")
        print("Usage: python query_db.py \"your search terms\"")
        print("For examples: python query_db.py --examples")
        return
    
    # Perform the query
    query_database(args.query, k=args.count, open_files=args.open)

if __name__ == "__main__":
    main()
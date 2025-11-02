#!/usr/bin/env python3
"""
Test script for URL-based video processing.

This script demonstrates how to process videos from URLs including:
1. Direct video URLs
2. Google Drive links
3. Frame extraction at custom intervals

Usage:
    python test_url_video.py
"""

from codev1_1 import (
    analyze_video_from_url,
    download_video_from_url,
    is_url,
    is_google_drive_url,
    extract_google_drive_file_id,
    ChatOllama,
    OllamaEmbeddings,
    Chroma,
    prompt_func,
    StrOutputParser,
    JsonOutputParser
)
from colorama import Fore, Style

# Configuration
vision_model = 'llava:13b'
embedding_model = "nomic-embed-text:v1.5"
db_name = 'db_photos'
db_collection_name = "photo_collection"

def test_url_processing():
    """Test URL validation and processing"""
    
    # Test URLs
    test_urls = [
        "https://example.com/sample_video.mp4",
        "https://drive.google.com/file/d/1234567890abcdef/view",
        "https://docs.google.com/file/d/1234567890abcdef/edit",
        "not_a_url.mp4",
        ""
    ]
    
    print(f"{Fore.CYAN}Testing URL validation:{Style.RESET_ALL}")
    for url in test_urls:
        is_valid_url = is_url(url)
        is_gdrive = is_google_drive_url(url) if is_valid_url else False
        
        print(f"URL: {url}")
        print(f"  Valid URL: {is_valid_url}")
        print(f"  Google Drive: {is_gdrive}")
        
        if is_gdrive:
            try:
                file_id = extract_google_drive_file_id(url)
                print(f"  File ID: {file_id}")
            except Exception as e:
                print(f"  Error extracting file ID: {e}")
        print()

def process_video_from_url(url, interval_seconds=10):
    """Process a video from URL"""
    
    print(f"{Fore.GREEN}Processing video from URL:{Style.RESET_ALL}")
    print(f"URL: {url}")
    print(f"Interval: {interval_seconds} seconds")
    
    if not is_url(url):
        print(f"{Fore.RED}Invalid URL provided{Style.RESET_ALL}")
        return
    
    # Initialize AI models
    embedding_function = OllamaEmbeddings(model=embedding_model)
    llm = ChatOllama(model=vision_model, temperature=0.2, num_gpu=-1)
    vision_chain = prompt_func | llm | StrOutputParser()
    object_chain = prompt_func | llm | JsonOutputParser()

    global db
    db = Chroma(
        collection_name=db_collection_name,
        embedding_function=embedding_function,
        persist_directory=f"./{db_name}")

    try:
        # Process the video
        frame_details_list = analyze_video_from_url(url, vision_chain, object_chain, interval_seconds)
        
        if frame_details_list:
            print(f"\n{Fore.GREEN}Successfully processed {len(frame_details_list)} frames!{Style.RESET_ALL}")
            
            # Print summary
            for i, frame_details in enumerate(frame_details_list):
                print(f"\n--- Frame {i+1} Summary ---")
                print(f"Timestamp: {frame_details.timestamp:.2f}s")
                print(f"Objects detected: {len(frame_details.detected_objects)}")
                if frame_details.detected_objects:
                    objects = [obj['name'] for obj in frame_details.detected_objects]
                    print(f"Objects: {', '.join(objects)}")
                
                # Print first few words of description
                description_preview = ' '.join(frame_details.description.split()[:15])
                if len(frame_details.description.split()) > 15:
                    description_preview += "..."
                print(f"Description: {description_preview}")
        else:
            print(f"{Fore.RED}Failed to process video from URL{Style.RESET_ALL}")
            
    except Exception as e:
        print(f"{Fore.RED}Error processing video: {str(e)}{Style.RESET_ALL}")

def main():
    print(f"{Fore.MAGENTA}=== URL Video Processing Test ==={Style.RESET_ALL}")
    print()
    
    # Test URL validation
    test_url_processing()
    
    # Example usage (you would replace with actual URLs)
    print(f"{Fore.YELLOW}To test with an actual video URL, modify this script or use:{Style.RESET_ALL}")
    print("python codev1.1.py <video_url> [interval_seconds]")
    print()
    print("Examples:")
    print("python codev1.1.py https://drive.google.com/file/d/YOUR_FILE_ID/view 10")
    print("python codev1.1.py https://example.com/video.mp4 5")
    print()
    
    # Uncomment and modify the line below to test with a real URL
    # process_video_from_url("YOUR_VIDEO_URL_HERE", 10)

if __name__ == "__main__":
    main()
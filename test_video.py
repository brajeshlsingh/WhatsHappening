#!/usr/bin/env python3
"""
Test script to demonstrate video processing capabilities.

This script shows how to:
1. Extract frames from an MP4 video every 10 seconds
2. Analyze each frame for objects and generate descriptions
3. Store the results in the vector database

Usage:
    python test_video.py path/to/your/video.mp4

If no video path is provided, it will process all videos in the ./images directory.
"""

import sys
import os
from code import (
    extract_frames_from_video, 
    analyze_video, 
    get_video_files,
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

def test_single_video(video_path, interval_seconds=10):
    """Test video processing on a single video file"""
    
    if not os.path.exists(video_path):
        print(f"{Fore.RED}Error: Video file not found: {video_path}{Style.RESET_ALL}")
        return
    
    print(f"{Fore.GREEN}Testing video processing on: {video_path}{Style.RESET_ALL}")
    print(f"Frame extraction interval: {interval_seconds} seconds")
    
    # Initialize the AI models
    embedding_function = OllamaEmbeddings(model=embedding_model)
    llm = ChatOllama(model=vision_model, temperature=0.2, num_gpu=-1)
    vision_chain = prompt_func | llm | StrOutputParser()
    object_chain = prompt_func | llm | JsonOutputParser()

    # Initialize the database
    global db
    db = Chroma(
        collection_name=db_collection_name,
        embedding_function=embedding_function,
        persist_directory=f"./{db_name}")

    # Process the video
    try:
        frame_details_list = analyze_video(video_path, vision_chain, object_chain, interval_seconds)
        
        print(f"\n{Fore.GREEN}Successfully processed {len(frame_details_list)} frames from the video!{Style.RESET_ALL}")
        
        # Print summary
        for i, frame_details in enumerate(frame_details_list):
            print(f"\n--- Frame {i+1} Summary ---")
            print(f"Timestamp: {frame_details.timestamp:.2f}s")
            print(f"Objects detected: {len(frame_details.detected_objects)}")
            if frame_details.detected_objects:
                print("Objects:", ", ".join([obj['name'] for obj in frame_details.detected_objects]))
            
    except Exception as e:
        print(f"{Fore.RED}Error processing video: {str(e)}{Style.RESET_ALL}")

def main():
    if len(sys.argv) > 1:
        # Process specific video file
        video_path = sys.argv[1]
        interval = int(sys.argv[2]) if len(sys.argv) > 2 else 10
        test_single_video(video_path, interval)
    else:
        # Look for videos in the images directory
        video_files = get_video_files("./images")
        
        if not video_files:
            print(f"{Fore.YELLOW}No video files found in ./images directory{Style.RESET_ALL}")
            print("To test with a specific video file, run:")
            print("    python test_video.py path/to/your/video.mp4 [interval_seconds]")
            print("\nSupported video formats: .mp4, .avi, .mov, .mkv")
            return
        
        print(f"{Fore.CYAN}Found {len(video_files)} video file(s):{Style.RESET_ALL}")
        for video in video_files:
            print(f"  - {video}")
        
        # Process the first video as a test
        test_single_video(video_files[0])

if __name__ == "__main__":
    main()
from typing import Optional

class ImageDetails():
    file_name:str=''
    make:str=''
    model:str=''
    dt:str=''
    aperture_value:str=''
    focal_length:str=''
    exposure_time:str=''
    f_stops:str=''
    iso:str=''
    gps:Optional[str]
    detected_objects:list[dict]
    description:str=''
    generated_with:str=''

    def __init__(self, file_name, make, model, dt, aperture_value, focal_length, exposure_time, f_stops, iso, gps, detected_objects, description, generated_with):
        self.file_name = file_name
        self.make = make
        self.model = model
        self.dt = dt
        self.aperture_value = aperture_value
        self.focal_length = focal_length
        self.exposure_time = exposure_time
        self.f_stops = f_stops
        self.iso = iso
        self.gps = gps
        self.detected_objects = detected_objects
        self.description = description
        self.generated_with = generated_with

    def to_dict(self):
        return {
            'file_name': self.file_name,
            'make': self.make,
            'model': self.model,
            'dt': self.dt,
            'aperture_value': self.aperture_value,
            'focal_length': self.focal_length,
            'exposure_time': self.exposure_time,
            'f_stops': self.f_stops,
            'iso': self.iso,
            'gps': self.gps,
            'detected_objects': self.get_detected_objects_text(),
            'description': self.description,
            'generated_with': self.generated_with
        }

    def get_page_content(self):
        retval = f"{self.get_detected_objects_text()}\n\n{self.description}"
        return retval

    def get_detected_objects_text(self) -> str:
         retval = '\n'.join([f"{item['name']} - {item['description']}" for item in self.detected_objects])
         return retval

    def __str__(self):
        retval = ''
        retval += f'EXIF DATA:\n'
        retval += f"MAKE    : {self.make}\n"
        retval += f"MODEL   : {self.model}\n"
        retval += f"DATE    : {self.dt}\n"
        retval += f"AV      : {self.aperture_value}\n"
        retval += f"TV      : {self.exposure_time}\n"
        retval += f"F/STOPs : {self.f_stops}\n"
        retval += f"ISO     : {self.iso}\n"
        retval += f"GPS     : {self.gps}\n"
        retval += '\n'
        retval += f'DETECTED OBJECTS:\n'
        retval += self.get_detected_objects_text()
        retval += '\n\n'
        retval += f'IMAGE DESCRIPTION:\n'
        retval += self.description
        return retval

class VideoFrameDetails():
    """Class to store details for video frames"""
    file_name: str = ''
    timestamp: float = 0.0
    frame_number: int = 0
    detected_objects: list[dict]
    description: str = ''
    generated_with: str = ''

    def __init__(self, file_name, timestamp, frame_number, detected_objects, description, generated_with):
        self.file_name = file_name
        self.timestamp = timestamp
        self.frame_number = frame_number
        self.detected_objects = detected_objects
        self.description = description
        self.generated_with = generated_with

    def to_dict(self):
        return {
            'file_name': self.file_name,
            'timestamp': self.timestamp,
            'frame_number': self.frame_number,
            'detected_objects': self.get_detected_objects_text(),
            'description': self.description,
            'generated_with': self.generated_with,
            'content_type': 'video_frame'
        }

    def get_page_content(self):
        retval = f"Video: {self.file_name}\n"
        retval += f"Timestamp: {self.timestamp:.2f}s\n"
        retval += f"Frame: {self.frame_number}\n\n"
        retval += f"{self.get_detected_objects_text()}\n\n{self.description}"
        return retval

    def get_detected_objects_text(self) -> str:
        retval = '\n'.join([f"{item['name']} - {item['description']}" for item in self.detected_objects])
        return retval

    def __str__(self):
        retval = ''
        retval += f'VIDEO FRAME DATA:\n'
        retval += f"FILE    : {self.file_name}\n"
        retval += f"TIME    : {self.timestamp:.2f} seconds\n"
        retval += f"FRAME   : {self.frame_number}\n"
        retval += '\n'
        retval += f'DETECTED OBJECTS:\n'
        retval += self.get_detected_objects_text()
        retval += '\n\n'
        retval += f'FRAME DESCRIPTION:\n'
        retval += self.description
        return retval
    
from PIL import ImageFile
#from ImageDetails import ImageDetails
from PIL.ExifTags import TAGS, GPSTAGS
from functools import partial



def _get_exif_data(img:ImageFile)->dict:
    exif_data = img._getexif()
    
    if exif_data:
        exif_dict = {}
        for tag, value in exif_data.items():
            tag_name = TAGS.get(tag, tag)
            exif_dict[tag_name] = value
        return exif_dict
    else:
        return {}
def __get_gps_info(exif_dict):
    gps_info = exif_dict.get('GPSInfo', {})
    
    if gps_info:
        gps_data = {}
        for key, value in gps_info.items():
            key_name = GPSTAGS.get(key, key)
            gps_data[key_name] = value
        return gps_data
    else:
        return None
    
def __convert_to_decimal(degrees, minutes, seconds, direction):
    decimal = degrees + (minutes / 60.0) + (seconds / 3600.0)
    if direction in ['S', 'W']:
        decimal = -decimal
    return decimal

def _get_coordinates(exif_dict):
    gps_info = __get_gps_info(exif_dict)
    if gps_info is not None and 'GPSLatitude' in gps_info and 'GPSLongitude' in gps_info and 'GPSLatitudeRef' in gps_info and 'GPSLongitudeRef' in gps_info:
        degrees_lat, minutes_lat, seconds_lat = gps_info['GPSLatitude']
        lat = __convert_to_decimal(degrees_lat, minutes_lat, seconds_lat, gps_info['GPSLatitudeRef'])
        degrees_lon, minutes_lon, seconds_lon = gps_info['GPSLongitude']
        lon = __convert_to_decimal(degrees_lon, minutes_lon, seconds_lon, gps_info['GPSLongitudeRef'])
        gps = f"{lat}, {lon}"
        return gps
    else:
        return ''
    
def _get_from_dict(property_name, dict):
    return str(dict[property_name]) if property_name in dict.keys() else ''

def _get_exposure_time(exif_dict)->str:
    if 'ExposureTime' in exif_dict.keys():
        exposure_time = str(exif_dict['ExposureTime'].numerator) + '/' + str(exif_dict['ExposureTime'].denominator)
    else:
        exposure_time=''
    return exposure_time

def _get_datetime(exif_dict)->str:
    if 'DateTime' in exif_dict.keys():
        dt = exif_dict['DateTime']
    elif 'DateTimeOriginal' in exif_dict.keys():
        dt = exif_dict['DateTimeOriginal']
    else:
        dt = ''
    return dt

# ImageDetailsFactory Module

class ImageDetailsFactory:
    @staticmethod
    def create(file_name, img, detected_objects, description, generated_with) -> ImageDetails:
        exif_dict = _get_exif_data(img)

        _get_prop = partial(_get_from_dict, dict=exif_dict)

        make = _get_prop('Make')
        model = _get_prop('Model')
        aperture_value = _get_prop('ApertureValue')
        focal_length = _get_prop('FocalLength')
        f_stops = _get_prop('FNumber')
        iso = _get_prop('ISOSpeedRatings')
        exposure_time = _get_exposure_time(exif_dict)
        dt = _get_datetime(exif_dict)
        gps = _get_coordinates(exif_dict)

        image_details = ImageDetails(
            file_name, make, model, dt, aperture_value, focal_length,
            exposure_time, f_stops, iso, gps, detected_objects, description, generated_with
        )

        return image_details
# def create(file_name, img, detected_objects, description, generated_with)->ImageDetails:
    
#     exif_dict = _get_exif_data(img)

#     _get_prop = partial(_get_from_dict, dict=exif_dict)

#     make = _get_prop('Make')
#     model = _get_prop('Model')
#     aperture_value = _get_prop('ApertureValue')
#     focal_length = _get_prop('FocalLength')
#     f_stops = _get_prop('FNumber')
#     iso = _get_prop('ISOSpeedRatings')
#     exposure_time = _get_exposure_time(exif_dict)
#     dt = _get_datetime(exif_dict)
#     gps = _get_coordinates(exif_dict)
        
#     image_details = ImageDetails(file_name, make, model, dt, aperture_value, focal_length, exposure_time, f_stops, iso, gps, detected_objects, description, generated_with)

#     return image_details

import os
import time
from contextlib import closing
import sqlite3
import base64
from io import BytesIO
from PIL import Image
import glob
import uuid
import cv2
import numpy as np
import requests
import tempfile
import urllib.parse
from pathlib import Path
import csv
import argparse
from datetime import datetime
from colorama import Fore, Style
from langchain_core.documents import Document
from langchain_ollama import ChatOllama, OllamaEmbeddings
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_core.output_parsers import JsonOutputParser, StrOutputParser
from langchain_chroma import Chroma


#from ImageDetails import ImageDetails
#import ImageDetailsFactory
# Configuration for CCTV Analysis System
# Directory structure example for 3 CCTV cameras:
# ./images_clips/
#   ├── camera_1/
#   │   ├── video1.mp4
#   │   └── video2.mp4
#   ├── camera_2/
#   │   ├── video3.mp4
#   │   └── video4.mp4
#   └── camera_3/
#       ├── video5.mp4
#       └── video6.mp4

root_image_dir = "./images_clips"  # Main directory containing camera folders
db_name = 'db_photos'             # Database for storing analysis results
db_collection_name="photo_collection"
vision_model = 'llava:13b'        # AI model for image/video analysis
#embedding_model="mxbai-embed-large"
embedding_model="nomic-embed-text:v1.5"

# CSV logging configuration
csv_output_dir = "./csv_logs"
enable_csv_logging = True

# Google Drive API configuration (optional)
# To enable Google Drive API integration:
# 1. pip install google-api-python-client google-auth-httplib2 google-auth-oauthlib
# 2. Set up Google Drive API credentials
# 3. Set enable_gdrive_api = True
enable_gdrive_api = False
gdrive_credentials_file = "credentials.json"  # Path to your Google Drive API credentials

def analyze_cctv_directory_structure(directory):
    """Analyze and display CCTV camera directory structure"""
    print(f"{Fore.CYAN}🔍 Analyzing CCTV directory structure in: {directory}{Style.RESET_ALL}")
    print("=" * 60)
    
    if not os.path.exists(directory):
        print(f"{Fore.RED}❌ Directory does not exist: {directory}{Style.RESET_ALL}")
        return
    
    # Get all subdirectories
    subdirs = []
    for root, dirs, files in os.walk(directory):
        for dir_name in dirs:
            subdir_path = os.path.join(root, dir_name)
            rel_path = os.path.relpath(subdir_path, directory)
            subdirs.append(rel_path)
    
    if subdirs:
        print(f"{Fore.GREEN}📁 Found {len(subdirs)} subdirectory(ies) - Perfect for CCTV camera organization!{Style.RESET_ALL}")
        for i, subdir in enumerate(subdirs[:10], 1):  # Show first 10
            print(f"  {i}. 📹 {subdir}/")
        if len(subdirs) > 10:
            print(f"  ... and {len(subdirs) - 10} more directories")
    else:
        print(f"{Fore.YELLOW}📁 No subdirectories found - all files will be processed from root directory{Style.RESET_ALL}")
    
    print("=" * 60)
    print()


def get_jpeg_files(directory):
    """Get all JPEG image files from directory and subdirectories recursively"""
    file_extensions = ['jpg', 'jpeg', 'JPG', 'JPEG']
    all_files = []
    
    print(f"{Fore.CYAN}Scanning for image files in: {directory}{Style.RESET_ALL}")
    
    for ext in file_extensions:
        pattern = os.path.join(directory, '**', f'*.{ext}')
        files_for_ext = glob.glob(pattern, recursive=True)
        all_files.extend(files_for_ext)
        if files_for_ext:
            print(f"  Found {len(files_for_ext)} .{ext} files")
    
    if all_files:
        print(f"{Fore.GREEN}Total image files found: {len(all_files)}{Style.RESET_ALL}")
        
        # Show directory structure
        dirs_with_images = {}
        for image_file in all_files:
            image_dir = os.path.dirname(image_file)
            rel_dir = os.path.relpath(image_dir, directory)
            if rel_dir not in dirs_with_images:
                dirs_with_images[rel_dir] = 0
            dirs_with_images[rel_dir] += 1
        
        print(f"{Fore.CYAN}Image files organized by directory:{Style.RESET_ALL}")
        for dir_name, count in dirs_with_images.items():
            if dir_name == '.':
                print(f"  📁 Root directory: {count} files")
            else:
                print(f"  📁 {dir_name}: {count} files")
    
    return all_files

def get_video_files(directory):
    """Get all video files from directory and subdirectories recursively
    Perfect for CCTV setups with multiple camera folders"""
    file_extensions = ['mp4', 'avi', 'mov', 'mkv', 'wmv', 'flv', 'webm']
    all_files = []
    
    print(f"{Fore.CYAN}Scanning for video files in: {directory}{Style.RESET_ALL}")
    
    for ext in file_extensions:
        pattern = os.path.join(directory, '**', f'*.{ext}')
        files_for_ext = glob.glob(pattern, recursive=True)
        all_files.extend(files_for_ext)
        if files_for_ext:
            print(f"  Found {len(files_for_ext)} .{ext} files")
    
    # Group files by subdirectory for CCTV camera organization
    if all_files:
        print(f"{Fore.GREEN}Total video files found: {len(all_files)}{Style.RESET_ALL}")
        
        # Show directory structure for CCTV cameras
        dirs_with_videos = {}
        for video_file in all_files:
            video_dir = os.path.dirname(video_file)
            rel_dir = os.path.relpath(video_dir, directory)
            if rel_dir not in dirs_with_videos:
                dirs_with_videos[rel_dir] = []
            dirs_with_videos[rel_dir].append(os.path.basename(video_file))
        
        print(f"{Fore.CYAN}Video files organized by directory:{Style.RESET_ALL}")
        for dir_name, files in dirs_with_videos.items():
            if dir_name == '.':
                print(f"  📁 Root directory: {len(files)} files")
            else:
                print(f"  📁 {dir_name}: {len(files)} files")
                # Show first few files as examples
                for i, filename in enumerate(files[:3]):
                    print(f"    📹 {filename}")
                if len(files) > 3:
                    print(f"    ... and {len(files) - 3} more files")
    
    return all_files

def extract_frames_from_video(video_path, interval_seconds=2):
    """Extract frames from video at specified interval (default 10 seconds)"""
    cap = cv2.VideoCapture(video_path)
    
    if not cap.isOpened():
        print(f"Error: Could not open video file {video_path}")
        return []
    
    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_interval = int(fps * interval_seconds)
    
    frames = []
    frame_count = 0
    
    print(f"Video FPS: {fps}, extracting every {frame_interval} frames ({interval_seconds} seconds)")
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
            
        if frame_count % frame_interval == 0:
            # Convert BGR to RGB (OpenCV uses BGR, PIL uses RGB)
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            pil_image = Image.fromarray(frame_rgb)
            
            timestamp = frame_count / fps
            frames.append({
                'image': pil_image,
                'timestamp': timestamp,
                'frame_number': frame_count
            })
            print(f"Extracted frame at {timestamp:.2f} seconds")
        
        frame_count += 1
    
    cap.release()
    return frames

def convert_frame_to_base64(pil_image)->str:
    """Convert PIL image to base64 string for video frames"""
    buffered = BytesIO()
    pil_image.save(buffered, format="JPEG")
    img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")
    return img_str

def is_url(string):
    """Check if a string is a valid URL"""
    try:
        result = urllib.parse.urlparse(string)
        return all([result.scheme, result.netloc])
    except:
        return False

def is_google_drive_url(url):
    """Check if URL is a Google Drive link"""
    return 'drive.google.com' in url or 'docs.google.com' in url

def is_google_drive_folder_url(url):
    """Check if URL is a Google Drive folder link"""
    return ('drive.google.com' in url and 
            ('/folders/' in url or '/drive/folders/' in url))

def is_google_drive_file_url(url):
    """Check if URL is a Google Drive file link"""
    return ('drive.google.com' in url and 
            ('/file/d/' in url or 'id=' in url) and
            '/folders/' not in url)

def extract_google_drive_folder_id(url):
    """Extract folder ID from Google Drive folder URL"""
    if '/folders/' in url:
        # Format: https://drive.google.com/drive/folders/FOLDER_ID
        folder_id = url.split('/folders/')[1].split('?')[0].split('/')[0]
    elif '/drive/folders/' in url:
        # Alternative format
        folder_id = url.split('/drive/folders/')[1].split('?')[0].split('/')[0]
    else:
        raise ValueError("Could not extract folder ID from Google Drive folder URL")
    
    return folder_id

def get_google_drive_folder_files(folder_url):
    """
    Extract individual file URLs from a Google Drive folder URL
    
    Args:
        folder_url: Google Drive folder URL
        
    Returns:
        list: List of individual video file URLs
    """
    try:
        folder_id = extract_google_drive_folder_id(folder_url)
        
        print(f"{Fore.CYAN}📁 Google Drive Folder Analysis{Style.RESET_ALL}")
        print(f"Folder ID: {folder_id}")
        print(f"Folder URL: {folder_url}")
        print()
        
        # Check if Google Drive API is enabled and available
        if enable_gdrive_api:
            try:
                # Try to import Google Drive API
                from googleapiclient.discovery import build
                from google.auth.transport.requests import Request
                from google.oauth2.credentials import Credentials
                from google_auth_oauthlib.flow import InstalledAppFlow
                import os
                
                print(f"{Fore.GREEN}🔧 Google Drive API integration enabled{Style.RESET_ALL}")
                return _get_folder_files_via_api(folder_id)
                
            except ImportError:
                print(f"{Fore.YELLOW}⚠️  Google Drive API libraries not installed{Style.RESET_ALL}")
                print("To enable API integration, install:")
                print("pip install google-api-python-client google-auth-httplib2 google-auth-oauthlib")
                print()
            except Exception as e:
                print(f"{Fore.YELLOW}⚠️  Google Drive API error: {str(e)}{Style.RESET_ALL}")
                print()
        
        # Manual approach (current default)
        print(f"{Fore.YELLOW}📋 Manual Extraction Required{Style.RESET_ALL}")
        print("Google Drive API integration is not configured.")
        print()
        print(f"{Fore.CYAN}🔧 To enable automatic folder processing:{Style.RESET_ALL}")
        print("1. Install Google Drive API libraries:")
        print("   pip install google-api-python-client google-auth-httplib2 google-auth-oauthlib")
        print("2. Set up Google Drive API credentials")
        print("3. Set enable_gdrive_api = True in the configuration")
        print()
        print(f"{Fore.CYAN}📋 Manual Alternative (Current Approach):{Style.RESET_ALL}")
        print("1. 📂 Open the Google Drive folder:")
        print(f"   {folder_url}")
        print("2. 📹 For each video file:")
        print("   - Right-click on the video")
        print("   - Select 'Get link' → 'Copy link'")
        print("   - Save the individual file URL")
        print("3. 🚀 Process each video individually:")
        print("   python codev1.2.py <individual_file_url> <interval>")
        print()
        
        # For demonstration, show how URLs would be structured
        print(f"{Fore.CYAN}📝 Example of individual file URLs you'll get:{Style.RESET_ALL}")
        print("   https://drive.google.com/file/d/1ABC123_VIDEO1/view")
        print("   https://drive.google.com/file/d/1DEF456_VIDEO2/view")
        print("   https://drive.google.com/file/d/1GHI789_VIDEO3/view")
        print()
        
        return []
        
    except Exception as e:
        print(f"{Fore.RED}❌ Error analyzing folder URL: {str(e)}{Style.RESET_ALL}")
        return []

def _get_folder_files_via_api(folder_id):
    """
    Get video files from Google Drive folder using API
    (Implementation for when API is enabled)
    """
    try:
        # This would contain the actual Google Drive API implementation
        # For now, return empty list with informational message
        print(f"{Fore.CYAN}🚀 Scanning folder via Google Drive API...{Style.RESET_ALL}")
        print(f"Folder ID: {folder_id}")
        
        # TODO: Implement actual API calls here
        # Example structure:
        # service = build('drive', 'v3', credentials=creds)
        # results = service.files().list(q=f"'{folder_id}' in parents", fields="files(id, name, mimeType)").execute()
        # video_files = [file for file in results.get('files', []) if 'video' in file.get('mimeType', '')]
        # return [f"https://drive.google.com/file/d/{file['id']}/view" for file in video_files]
        
        print(f"{Fore.YELLOW}API implementation pending - using manual approach{Style.RESET_ALL}")
        return []
        
    except Exception as e:
        print(f"{Fore.RED}❌ API error: {str(e)}{Style.RESET_ALL}")
        return []

def process_google_drive_folder(folder_url, vision_chain, object_chain, interval_seconds=2, csv_filepath=None):
    """
    Process all videos from a Google Drive folder
    
    Args:
        folder_url: Google Drive folder URL containing videos
        vision_chain: Vision processing chain
        object_chain: Object detection processing chain
        interval_seconds: Frame extraction interval
        csv_filepath: CSV logging file path
        
    Returns:
        list: List of all processed frame details from all videos
    """
    print(f"{Fore.CYAN}🚀 Processing Google Drive Folder{Style.RESET_ALL}")
    print(f"Folder: {folder_url}")
    print(f"Frame interval: {interval_seconds} seconds")
    print("=" * 80)
    
    # Get individual file URLs from folder
    file_urls = get_google_drive_folder_files(folder_url)
    
    if not file_urls:
        print(f"{Fore.YELLOW}📋 Manual Processing Required{Style.RESET_ALL}")
        print("Since Google Drive API is not configured, please:")
        print("1. Get individual video file URLs manually")
        print("2. Process each video separately:")
        print("   python codev1.2.py <file_url_1> <interval>")
        print("   python codev1.2.py <file_url_2> <interval>")
        print("   ...")
        print()
        print(f"{Fore.CYAN}💡 Alternative - Local Processing:{Style.RESET_ALL}")
        print("1. Download all videos from the folder")
        print("2. Organize in CCTV structure:")
        print("   ./images_clips/camera_1/video1.mp4")
        print("   ./images_clips/camera_2/video2.mp4")
        print("   ./images_clips/camera_3/video3.mp4")
        print("3. Run: python codev1.2.py")
        return []
    
    # Process each video file (when API is implemented)
    all_frame_details = []
    for i, file_url in enumerate(file_urls, 1):
        print(f"\n{Fore.MAGENTA}📹 Processing video {i}/{len(file_urls)}{Style.RESET_ALL}")
        print(f"URL: {file_url}")
        
        try:
            frame_details_list = analyze_video(file_url, vision_chain, object_chain, interval_seconds, csv_filepath)
            all_frame_details.extend(frame_details_list)
            
            if frame_details_list:
                total_objects = sum(len(frame.detected_objects) for frame in frame_details_list)
                print(f"{Fore.GREEN}✅ Video {i}: {len(frame_details_list)} frames, {total_objects} objects{Style.RESET_ALL}")
            else:
                print(f"{Fore.YELLOW}⚠️  Video {i}: No frames extracted{Style.RESET_ALL}")
                
        except Exception as e:
            print(f"{Fore.RED}❌ Video {i} failed: {str(e)}{Style.RESET_ALL}")
    
    return all_frame_details

def extract_google_drive_file_id(url):
    """Extract file ID from Google Drive URL"""
    
    # Check if it's a folder URL first
    if is_google_drive_folder_url(url):
        raise ValueError(
            "Google Drive folder URLs are not supported for direct video processing.\n"
            f"URL provided: {url}\n"
            "This appears to be a folder containing multiple files.\n\n"
            "To process videos from Google Drive:\n"
            "1. Open the folder and get individual video file URLs\n"
            "2. Right-click on each video → 'Get link' → 'Copy link'\n"
            "3. Use individual file URLs like: https://drive.google.com/file/d/FILE_ID/view\n\n"
            "Alternative: Download the videos locally and place them in your ./images_clips/ folder structure."
        )
    
    # Handle different Google Drive file URL formats
    if '/file/d/' in url:
        # Format: https://drive.google.com/file/d/FILE_ID/view
        file_id = url.split('/file/d/')[1].split('/')[0]
    elif 'id=' in url:
        # Format: https://drive.google.com/open?id=FILE_ID
        file_id = url.split('id=')[1].split('&')[0]
    else:
        # Try to extract from other formats
        parts = url.split('/')
        for i, part in enumerate(parts):
            if part == 'd' and i + 1 < len(parts):
                file_id = parts[i + 1]
                break
        else:
            raise ValueError(
                "Could not extract file ID from Google Drive URL.\n"
                f"URL provided: {url}\n\n"
                "Supported Google Drive URL formats:\n"
                "- https://drive.google.com/file/d/FILE_ID/view\n"
                "- https://drive.google.com/open?id=FILE_ID\n\n"
                "Please ensure you're using a direct file link, not a folder link."
            )
    
    return file_id

def download_from_google_drive(url, destination):
    """Download file from Google Drive using direct download link"""
    try:
        file_id = extract_google_drive_file_id(url)
        download_url = f"https://drive.google.com/uc?export=download&id={file_id}"
        
        print(f"Downloading from Google Drive (ID: {file_id})...")
        
        # First request to get the download confirmation page
        session = requests.Session()
        response = session.get(download_url)
        
        # Check if we need to confirm download (for large files)
        if 'confirm=' in response.text:
            # Extract confirmation token
            import re
            token_match = re.search(r'confirm=([^&]+)', response.text)
            if token_match:
                token = token_match.group(1)
                download_url = f"https://drive.google.com/uc?export=download&confirm={token}&id={file_id}"
                response = session.get(download_url)
        
        # Download the file
        with open(destination, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
        
        print(f"Downloaded successfully to: {destination}")
        return True
        
    except Exception as e:
        print(f"Error downloading from Google Drive: {str(e)}")
        return False

def download_from_url(url, destination):
    """Download file from any URL"""
    try:
        print(f"Downloading from URL: {url}")
        
        response = requests.get(url, stream=True)
        response.raise_for_status()
        
        with open(destination, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
        
        print(f"Downloaded successfully to: {destination}")
        return True
        
    except Exception as e:
        print(f"Error downloading from URL: {str(e)}")
        return False

def download_video_from_url(url, temp_dir=None):
    """Download video from URL and return local path"""
    if temp_dir is None:
        temp_dir = tempfile.mkdtemp()
    
    # Enhanced validation for Google Drive URLs
    if is_google_drive_url(url):
        if is_google_drive_folder_url(url):
            print(f"{Fore.RED}❌ Google Drive Folder URL Detected{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}The URL you provided is a folder, not a single video file:{Style.RESET_ALL}")
            print(f"   {url}")
            print()
            print(f"{Fore.CYAN}📁 To process videos from Google Drive folders:{Style.RESET_ALL}")
            print("1. 📂 Open the Google Drive folder")
            print("2. 📹 Right-click on each video file")
            print("3. 🔗 Select 'Get link' → 'Copy link'")
            print("4. 🎯 Use individual file URLs like:")
            print("   https://drive.google.com/file/d/YOUR_FILE_ID/view")
            print()
            print(f"{Fore.CYAN}💡 Alternative - Download and organize locally:{Style.RESET_ALL}")
            print("1. 📥 Download videos from the Google Drive folder")
            print("2. 📁 Place them in your CCTV folder structure:")
            print("   ./images_clips/camera_1/video1.mp4")
            print("   ./images_clips/camera_2/video2.mp4")
            print("   ./images_clips/camera_3/video3.mp4")
            print("3. 🚀 Run: python codev1.2.py")
            print()
            return None
        
        try:
            filename = f"gdrive_video_{extract_google_drive_file_id(url)}.mp4"
        except ValueError as e:
            print(f"{Fore.RED}❌ Google Drive URL Error:{Style.RESET_ALL}")
            print(str(e))
            return None
    else:
        # Extract filename from URL or use generic name
        parsed_url = urllib.parse.urlparse(url)
        filename = os.path.basename(parsed_url.path) or "downloaded_video.mp4"
        
        # Ensure it has a video extension
        if not any(filename.lower().endswith(ext) for ext in ['.mp4', '.avi', '.mov', '.mkv']):
            filename += '.mp4'
    
    destination = os.path.join(temp_dir, filename)
    
    print(f"{Fore.CYAN}📥 Attempting to download video...{Style.RESET_ALL}")
    print(f"   Source: {url}")
    print(f"   Destination: {destination}")
    
    # Download based on URL type
    try:
        if is_google_drive_url(url):
            success = download_from_google_drive(url, destination)
        else:
            success = download_from_url(url, destination)
        
        if success and os.path.exists(destination):
            file_size = os.path.getsize(destination) / (1024 * 1024)  # Size in MB
            print(f"{Fore.GREEN}✅ Download successful! File size: {file_size:.2f} MB{Style.RESET_ALL}")
            return destination
        else:
            print(f"{Fore.RED}❌ Download failed or file not found{Style.RESET_ALL}")
            return None
            
    except Exception as e:
        print(f"{Fore.RED}❌ Download error: {str(e)}{Style.RESET_ALL}")
        return None

def convert_to_base64(pil_image)->str:
    buffered = BytesIO()
    pil_image.save(buffered, format="JPEG")
    img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")
    return img_str

def get_processed_files():
    with closing(sqlite3.connect(f"./{db_name}/chroma.sqlite3")) as connection:
        sql = "select string_value from embedding_metadata where key='file_name'"
        rows = connection.execute(sql).fetchall()
        processed_files = [file_name for file_name, in rows]
    return processed_files

def get_processed_video_frames():
    """Get list of processed video frames to avoid reprocessing"""
    with closing(sqlite3.connect(f"./{db_name}/chroma.sqlite3")) as connection:
        sql = "select string_value from embedding_metadata where key='content_type' and string_value='video_frame'"
        rows = connection.execute(sql).fetchall()
        # Also get the file names for these video frames
        sql2 = "select string_value from embedding_metadata where key='file_name'"
        file_rows = connection.execute(sql2).fetchall()
        processed_files = [file_name for file_name, in file_rows]
    return processed_files

def setup_csv_logging():
    """Create CSV output directory and return session-specific filename"""
    if not enable_csv_logging:
        return None
    
    # Create CSV output directory if it doesn't exist
    os.makedirs(csv_output_dir, exist_ok=True)
    
    # Create session-specific CSV filename with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    csv_filename = f"object_detection_log_{timestamp}.csv"
    csv_filepath = os.path.join(csv_output_dir, csv_filename)
    
    # Create CSV file with headers
    with open(csv_filepath, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = [
            'session_timestamp', 'file_path', 'content_type', 'timestamp_seconds', 
            'frame_number', 'object_name', 'object_description', 'scene_description',
            'make', 'model', 'camera_date', 'aperture_value', 'focal_length', 
            'exposure_time', 'f_stops', 'iso', 'gps_coordinates', 'generated_with',
            'processing_time_seconds'
        ]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
    
    print(f"{Fore.GREEN}CSV logging enabled: {csv_filepath}{Style.RESET_ALL}")
    return csv_filepath

def log_to_csv(csv_filepath, data):
    """Log detection data to CSV file"""
    if not csv_filepath or not enable_csv_logging:
        return
    
    try:
        with open(csv_filepath, 'a', newline='', encoding='utf-8') as csvfile:
            fieldnames = [
                'session_timestamp', 'file_path', 'content_type', 'timestamp_seconds', 
                'frame_number', 'object_name', 'object_description', 'scene_description',
                'make', 'model', 'camera_date', 'aperture_value', 'focal_length', 
                'exposure_time', 'f_stops', 'iso', 'gps_coordinates', 'generated_with',
                'processing_time_seconds'
            ]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writerow(data)
    except Exception as e:
        print(f"{Fore.YELLOW}Warning: Could not write to CSV: {str(e)}{Style.RESET_ALL}")

def log_image_to_csv(csv_filepath, image_details, processing_time):
    """Log image analysis results to CSV"""
    if not csv_filepath:
        return
    
    session_timestamp = datetime.now().isoformat()
    
    # Log each detected object as a separate row
    if image_details.detected_objects:
        for obj in image_details.detected_objects:
            log_data = {
                'session_timestamp': session_timestamp,
                'file_path': image_details.file_name,
                'content_type': 'image',
                'timestamp_seconds': '',
                'frame_number': '',
                'object_name': obj.get('name', ''),
                'object_description': obj.get('description', ''),
                'scene_description': image_details.description,
                'make': image_details.make,
                'model': image_details.model,
                'camera_date': image_details.dt,
                'aperture_value': image_details.aperture_value,
                'focal_length': image_details.focal_length,
                'exposure_time': image_details.exposure_time,
                'f_stops': image_details.f_stops,
                'iso': image_details.iso,
                'gps_coordinates': image_details.gps,
                'generated_with': image_details.generated_with,
                'processing_time_seconds': f"{processing_time:.4f}"
            }
            log_to_csv(csv_filepath, log_data)
    else:
        # Log even if no objects detected
        log_data = {
            'session_timestamp': session_timestamp,
            'file_path': image_details.file_name,
            'content_type': 'image',
            'timestamp_seconds': '',
            'frame_number': '',
            'object_name': 'NO_OBJECTS_DETECTED',
            'object_description': '',
            'scene_description': image_details.description,
            'make': image_details.make,
            'model': image_details.model,
            'camera_date': image_details.dt,
            'aperture_value': image_details.aperture_value,
            'focal_length': image_details.focal_length,
            'exposure_time': image_details.exposure_time,
            'f_stops': image_details.f_stops,
            'iso': image_details.iso,
            'gps_coordinates': image_details.gps,
            'generated_with': image_details.generated_with,
            'processing_time_seconds': f"{processing_time:.4f}"
        }
        log_to_csv(csv_filepath, log_data)

def log_video_frame_to_csv(csv_filepath, frame_details, processing_time):
    """Log video frame analysis results to CSV"""
    if not csv_filepath:
        return
    
    session_timestamp = datetime.now().isoformat()
    
    # Log each detected object as a separate row
    if frame_details.detected_objects:
        for obj in frame_details.detected_objects:
            log_data = {
                'session_timestamp': session_timestamp,
                'file_path': frame_details.file_name,
                'content_type': 'video_frame',
                'timestamp_seconds': f"{frame_details.timestamp:.2f}",
                'frame_number': str(frame_details.frame_number),
                'object_name': obj.get('name', ''),
                'object_description': obj.get('description', ''),
                'scene_description': frame_details.description,
                'make': '',
                'model': '',
                'camera_date': '',
                'aperture_value': '',
                'focal_length': '',
                'exposure_time': '',
                'f_stops': '',
                'iso': '',
                'gps_coordinates': '',
                'generated_with': frame_details.generated_with,
                'processing_time_seconds': f"{processing_time:.4f}"
            }
            log_to_csv(csv_filepath, log_data)
    else:
        # Log even if no objects detected
        log_data = {
            'session_timestamp': session_timestamp,
            'file_path': frame_details.file_name,
            'content_type': 'video_frame',
            'timestamp_seconds': f"{frame_details.timestamp:.2f}",
            'frame_number': str(frame_details.frame_number),
            'object_name': 'NO_OBJECTS_DETECTED',
            'object_description': '',
            'scene_description': frame_details.description,
            'make': '',
            'model': '',
            'camera_date': '',
            'aperture_value': '',
            'focal_length': '',
            'exposure_time': '',
            'f_stops': '',
            'iso': '',
            'gps_coordinates': '',
            'generated_with': frame_details.generated_with,
            'processing_time_seconds': f"{processing_time:.4f}"
        }
        log_to_csv(csv_filepath, log_data)

def get_vision_system_message()->str:
    system_message_text = '''
You're an expert image and photo analyzer.
You are very perceptive in analyzing images and photos. 
You possess excelent vision. 
Do not read any text unless it is the most prominent in the image. 
Your description should be neutral in tone.
'''
    return system_message_text

def get_object_system_message()->str:
    system_message_text = '''
You're an expert image and photo analyzer.
You are very perceptive in analyzing images and photos. 
You possess excelent vision. 
Do not read any text unless it is the most prominent in the image. 
You should always output your results in json format, for example:

[
 {'name': 'a detected object', 'description': 'the detected object's description'},
 {'name': 'another detected object', 'description': 'the other detected object's description'}
]
'''
    return system_message_text

def prompt_func(data):
    text = data["text"]
    image = data["image"]
    system_message = SystemMessage(content=data["system_message_text"])
    image_part = {
        "type": "image_url",
        "image_url": f"data:image/jpeg;base64,{image}",
    }
    content_parts = []
    text_part = {"type": "text", "text": text}
    content_parts.append(image_part)
    content_parts.append(text_part)
    human_message = HumanMessage(content=content_parts)
    return [system_message, human_message]


def analyze_image(image_file, vision_chain, object_chain, csv_filepath=None)->ImageDetails:
    start_time = time.time()
    model = vision_chain.steps[1].model
    with Image.open(image_file) as img: 

        print(f'PROCESSING FILE: {image_file}')
        print('CONVERTING TO B64...')
        image_b64 = convert_to_base64(img)
        print('OK')
        
        print('DETECTING OBJECTS...')
        detected_objects = object_chain.invoke({"text":"Identify objects in the image. Return a json list of json items of the detected objects. Include only the names of each object and a short description of the object. The field names should be 'name' and 'description' respectively.", "image": image_b64, "system_message_text":get_object_system_message()})
        print('OK')
        
        print('GENERATING DESCRIPTION...')
        image_description = vision_chain.invoke({"text": "Describe the image in as much detail as possible. Do not try to read any text.", "image": image_b64, "system_message_text":get_vision_system_message()})
        print('OK')

        print('CREATING OBJECT...')
        image_details = ImageDetailsFactory.create(image_file, img, detected_objects, image_description, model)
        print('OK')

        print('ADDING TO VECTOR STORE...')
        doc = Document(id=str(uuid.uuid4()), page_content=image_details.get_page_content(), metadata=image_details.to_dict())
        db.add_documents([doc])
        print('OK')

        end_time = time.time()
        execution_time = end_time - start_time

        # Log to CSV
        if csv_filepath:
            print('LOGGING TO CSV...')
            log_image_to_csv(csv_filepath, image_details, execution_time)
            print('OK')

        print(f"{Fore.CYAN}Description:\n{Style.RESET_ALL}{image_details.description}")
        print(f"{Fore.CYAN}Detected Objects:\n{Style.RESET_ALL}{image_details.get_detected_objects_text()}")
        print('<=----------------------------------------------=>')

    print('\n')
    print(f"{Fore.YELLOW}Execution time: {execution_time:.4f} seconds{Style.RESET_ALL}")

    print(str(image_details))

    return image_details

def analyze_video_frame(video_file, frame_data, vision_chain, object_chain, csv_filepath=None)->VideoFrameDetails:
    """Analyze a single frame from a video"""
    start_time = time.time()
    model = vision_chain.steps[1].model
    
    frame_id = f"{video_file}_frame_{frame_data['frame_number']}"
    print(f'PROCESSING VIDEO FRAME: {frame_id}')
    print(f'TIMESTAMP: {frame_data["timestamp"]:.2f}s')
    
    print('CONVERTING FRAME TO B64...')
    image_b64 = convert_frame_to_base64(frame_data['image'])
    print('OK')
    
    print('DETECTING OBJECTS IN FRAME...')
    detected_objects = object_chain.invoke({
        "text": "Identify objects in the video frame. Return a json list of json items of the detected objects. Include only the names of each object and a short description of the object. The field names should be 'name' and 'description' respectively.", 
        "image": image_b64, 
        "system_message_text": get_object_system_message()
    })
    print('OK')
    
    print('GENERATING FRAME DESCRIPTION...')
    frame_description = vision_chain.invoke({
        "text": "Describe this video frame in as much detail as possible. Focus on the main subjects, actions, and scene composition. Do not try to read any text.", 
        "image": image_b64, 
        "system_message_text": get_vision_system_message()
    })
    print('OK')

    print('CREATING VIDEO FRAME OBJECT...')
    frame_details = VideoFrameDetails(
        video_file, 
        frame_data['timestamp'], 
        frame_data['frame_number'], 
        detected_objects, 
        frame_description, 
        model
    )
    print('OK')

    print('ADDING TO VECTOR STORE...')
    doc = Document(
        id=str(uuid.uuid4()), 
        page_content=frame_details.get_page_content(), 
        metadata=frame_details.to_dict()
    )
    db.add_documents([doc])
    print('OK')

    end_time = time.time()
    execution_time = end_time - start_time

    # Log to CSV
    if csv_filepath:
        print('LOGGING FRAME TO CSV...')
        log_video_frame_to_csv(csv_filepath, frame_details, execution_time)
        print('OK')

    print(f"{Fore.CYAN}Frame Description:\n{Style.RESET_ALL}{frame_details.description}")
    print(f"{Fore.CYAN}Detected Objects:\n{Style.RESET_ALL}{frame_details.get_detected_objects_text()}")
    print('<=----------------------------------------------=>')

    print(f"{Fore.YELLOW}Frame processing time: {execution_time:.4f} seconds{Style.RESET_ALL}")
    print('\n')

    return frame_details

def analyze_video(video_file_or_url, vision_chain, object_chain, interval_seconds=2, csv_filepath=None):
    """Analyze an entire video by extracting frames at specified intervals
    
    Args:
        video_file_or_url: Local file path or URL (including Google Drive links)
        vision_chain: Vision processing chain
        object_chain: Object detection processing chain
        interval_seconds: Interval between frame extractions
        csv_filepath: Path to CSV file for logging
    """
    temp_file = None
    local_video_path = video_file_or_url
    
    # Check if input is a URL
    if is_url(video_file_or_url):
        print(f"{Fore.CYAN}Detected URL input: {video_file_or_url}{Style.RESET_ALL}")
        
        # Download the video
        temp_file = download_video_from_url(video_file_or_url)
        if temp_file is None:
            print(f"{Fore.RED}Failed to download video from URL{Style.RESET_ALL}")
            return []
        
        local_video_path = temp_file
        print(f"{Fore.GREEN}Using downloaded video: {local_video_path}{Style.RESET_ALL}")
    
    try:
        print(f"{Fore.GREEN}PROCESSING VIDEO: {video_file_or_url}{Style.RESET_ALL}")
        print(f"Extracting frames every {interval_seconds} seconds...")
        
        frames = extract_frames_from_video(local_video_path, interval_seconds)
        
        if not frames:
            print(f"{Fore.RED}No frames extracted from video{Style.RESET_ALL}")
            return []
        
        print(f"Extracted {len(frames)} frames from video")
        
        frame_details_list = []
        for i, frame_data in enumerate(frames):
            print(f"\n--- Processing frame {i+1}/{len(frames)} ---")
            # Use original URL/filename for metadata, not temp file path
            frame_details = analyze_video_frame(video_file_or_url, frame_data, vision_chain, object_chain, csv_filepath)
            frame_details_list.append(frame_details)
        
        return frame_details_list
        
    finally:
        # Clean up temporary file if it was downloaded
        if temp_file and os.path.exists(temp_file):
            try:
                os.remove(temp_file)
                print(f"Cleaned up temporary file: {temp_file}")
            except:
                print(f"Warning: Could not remove temporary file: {temp_file}")

def analyze_video_from_url(url, vision_chain, object_chain, interval_seconds=2):
    """Convenience function specifically for URL inputs"""
    return analyze_video(url, vision_chain, object_chain, interval_seconds)

def query_database(query_text, k=5, open_files=False):
    """Query the vector database for similar content"""
    
    # Initialize database connection
    embedding_function = OllamaEmbeddings(model=embedding_model)
    db = Chroma(
        collection_name=db_collection_name,
        embedding_function=embedding_function,
        persist_directory=f"./{db_name}")
    
    print(f"{Fore.CYAN}Querying database for: '{query_text}'{Style.RESET_ALL}")
    print(f"Returning top {k} results...")
    print("-" * 60)
    
    try:
        # Perform similarity search
        results = db.similarity_search(query_text, k=k)
        
        if not results:
            print(f"{Fore.YELLOW}No results found for query: '{query_text}'{Style.RESET_ALL}")
            return
        
        print(f"{Fore.GREEN}Found {len(results)} results:{Style.RESET_ALL}\n")
        
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
            
            # Show partial content
            content_preview = doc.page_content[:200] + "..." if len(doc.page_content) > 200 else doc.page_content
            print(f"  📝 Description: {content_preview}")
            
            # Try to open file if requested and it exists
            if open_files:
                try:
                    if os.path.exists(file_path):
                        print(f"  🚀 Opening: {file_path}")
                        os.startfile(file_path)
                    else:
                        print(f"  ❌ File not found: {file_path}")
                except Exception as e:
                    print(f"  ⚠️  Could not open file: {str(e)}")
            
            print()
        
        if open_files:
            print(f"{Fore.GREEN}Attempted to open {len(results)} files{Style.RESET_ALL}")
        
    except Exception as e:
        print(f"{Fore.RED}Error querying database: {str(e)}{Style.RESET_ALL}")
        print("Make sure the database exists and contains data.")

def print_query_help():
    """Print help information for query mode"""
    print(f"{Fore.CYAN}DATABASE QUERY MODE{Style.RESET_ALL}")
    print("=" * 50)
    print("Query your processed images and videos using natural language.")
    print()
    print("Usage examples:")
    print("  python codev1.1.py --query 'photos of burnt vegetation'")
    print("  python codev1.1.py --query 'people walking' --count 10")
    print("  python codev1.1.py --query 'cars in street' --open")
    print("  python codev1.1.py --query 'sunset scenes' --count 3 --open")
    print()
    print("Options:")
    print("  --query TEXT    Search query (natural language)")
    print("  --count N       Number of results to return (default: 5)")
    print("  --open          Automatically open found files")
    print("  --help-query    Show this help message")
    print()
    print("Query examples:")
    print("  • 'people in photos'")
    print("  • 'cars and vehicles'") 
    print("  • 'outdoor scenes'")
    print("  • 'animals or pets'")
    print("  • 'buildings and architecture'")
    print("  • 'food and cooking'")
    print("  • 'sports activities'")
    print("  • 'nature and landscapes'")
    print()
    print(f"{Fore.YELLOW}Note: Database must exist and contain processed data.{Style.RESET_ALL}")

if __name__ == '__main__':
    import sys
    import argparse
    
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Object Detection and Database Query System')
    parser.add_argument('url_or_query', nargs='?', help='Video URL, Google Drive folder URL, or query text')
    parser.add_argument('interval', nargs='?', type=int, default=10, help='Frame interval for video processing')
    
    # Query mode arguments
    parser.add_argument('--query', '-q', type=str, help='Query the database with natural language')
    parser.add_argument('--count', '-c', type=int, default=5, help='Number of query results to return')
    parser.add_argument('--open', '-o', action='store_true', help='Automatically open found files')
    parser.add_argument('--help-query', action='store_true', help='Show query help and examples')
    
    # Google Drive specific arguments
    parser.add_argument('--gdrive-folder', action='store_true', help='Force treat URL as Google Drive folder')
    parser.add_argument('--setup-gdrive', action='store_true', help='Show Google Drive API setup instructions')
    
    args = parser.parse_args()
    
    # Handle Google Drive setup help
    if args.setup_gdrive:
        print(f"{Fore.CYAN}🔧 Google Drive API Setup Instructions{Style.RESET_ALL}")
        print("=" * 60)
        print("To enable automatic Google Drive folder processing:")
        print()
        print("1. Install required libraries:")
        print("   pip install google-api-python-client google-auth-httplib2 google-auth-oauthlib")
        print()
        print("2. Set up Google Drive API credentials:")
        print("   - Go to https://console.cloud.google.com/")
        print("   - Create/select a project")
        print("   - Enable Google Drive API")
        print("   - Create OAuth 2.0 credentials")
        print("   - Download as 'credentials.json'")
        print()
        print("3. Configure the system:")
        print("   - Set enable_gdrive_api = True in codev1.2.py")
        print()
        print("4. Usage:")
        print("   python codev1.2.py <google_drive_folder_url> <interval>")
        print()
        print(f"📚 See GOOGLE_DRIVE_API_SETUP.md for detailed instructions")
        sys.exit(0)
    
    # Handle query help
    if args.help_query:
        print_query_help()
        sys.exit(0)
    
    # Handle database query mode
    if args.query:
        query_database(args.query, k=args.count, open_files=args.open)
        sys.exit(0)
    
    # Setup CSV logging for processing mode
    csv_filepath = setup_csv_logging()
    
    # Check if URL is provided as legacy positional argument
    if args.url_or_query:
        input_arg = args.url_or_query
        interval = args.interval
        
        if is_url(input_arg):
            print(f"{Fore.CYAN}🔗 Processing video from URL...{Style.RESET_ALL}")
            print(f"URL: {input_arg}")
            print(f"Frame interval: {interval} seconds")
            print()
            
            # Validate Google Drive URLs
            if is_google_drive_url(input_arg):
                if is_google_drive_folder_url(input_arg):
                    print(f"{Fore.CYAN}📁 Google Drive folder URL detected{Style.RESET_ALL}")
                    print(f"{Fore.YELLOW}Attempting to process folder contents...{Style.RESET_ALL}")
                    print()
                    
                    # Initialize AI models for folder processing
                    embedding_function = OllamaEmbeddings(model=embedding_model)
                    llm = ChatOllama(model=vision_model, temperature=0.2, num_gpu=-1)
                    vision_chain = prompt_func | llm | StrOutputParser()
                    object_chain = prompt_func | llm | JsonOutputParser()

                    db = Chroma(
                        collection_name=db_collection_name,
                        embedding_function=embedding_function,
                        persist_directory=f"./{db_name}")

                    # Process the entire folder
                    all_frame_details = process_google_drive_folder(
                        input_arg, vision_chain, object_chain, interval, csv_filepath
                    )
                    
                    if all_frame_details:
                        total_videos = len(set(frame.file_name for frame in all_frame_details))
                        total_objects = sum(len(frame.detected_objects) for frame in all_frame_details)
                        print(f"\n{Fore.GREEN}🎉 Folder processing summary:{Style.RESET_ALL}")
                        print(f"   📹 Videos processed: {total_videos}")
                        print(f"   🎬 Total frames: {len(all_frame_details)}")
                        print(f"   🔍 Total objects detected: {total_objects}")
                        if csv_filepath:
                            print(f"   📋 Results logged to: {csv_filepath}")
                    else:
                        print(f"\n{Fore.YELLOW}Manual processing required - see instructions above{Style.RESET_ALL}")
                    
                    sys.exit(0)
                else:
                    print(f"{Fore.GREEN}✅ Valid Google Drive file URL detected{Style.RESET_ALL}")
            
            # Initialize AI models
            embedding_function = OllamaEmbeddings(model=embedding_model)
            llm = ChatOllama(model=vision_model, temperature=0.2, num_gpu=-1)
            vision_chain = prompt_func | llm | StrOutputParser()
            object_chain = prompt_func | llm | JsonOutputParser()

            db = Chroma(
                collection_name=db_collection_name,
                embedding_function=embedding_function,
                persist_directory=f"./{db_name}")

            # Process the video from URL
            frame_details_list = analyze_video(input_arg, vision_chain, object_chain, interval, csv_filepath)
            
            if frame_details_list:
                print(f"\n{Fore.GREEN}Successfully processed {len(frame_details_list)} frames from URL!{Style.RESET_ALL}")
                if csv_filepath:
                    print(f"{Fore.GREEN}Results logged to: {csv_filepath}{Style.RESET_ALL}")
                for i, frame_details in enumerate(frame_details_list):
                    print(f"Frame {i+1}: {frame_details.timestamp:.2f}s - {len(frame_details.detected_objects)} objects detected")
            else:
                print(f"{Fore.RED}Failed to process video from URL{Style.RESET_ALL}")
            
            sys.exit(0)
        else:
            print(f"{Fore.RED}Invalid URL provided: {input_arg}{Style.RESET_ALL}")
            print("For database queries, use: python codev1.1.py --query 'your search text'")
            print("For video URLs, use: python codev1.1.py <video_url> [interval_seconds]")
            print("For help with queries, use: python codev1.1.py --help-query")
            sys.exit(1)
    
    # Regular processing of local files
    print(f"{Fore.CYAN}🚀 Starting Object Detection & Analysis System{Style.RESET_ALL}")
    print(f"{Fore.CYAN}Processing local files in {root_image_dir}...{Style.RESET_ALL}")
    print("💡 TIP: To query the database, use: python codev1.1.py --query 'your search text'")
    print("💡 TIP: To process a video from URL, use: python codev1.1.py <video_url> [interval_seconds]")
    print()
    
    # Analyze directory structure for CCTV setup
    analyze_cctv_directory_structure(root_image_dir)
    
    # Get both image and video files
    image_files = get_jpeg_files(root_image_dir)
    video_files = get_video_files(root_image_dir)
    
    embedding_function = OllamaEmbeddings(model=embedding_model)

    llm = ChatOllama(model=vision_model, temperature=0.2, num_gpu=-1)
    vision_chain = prompt_func | llm | StrOutputParser()
    object_chain = prompt_func | llm | JsonOutputParser()

    db = Chroma(
        collection_name=db_collection_name,
        embedding_function=embedding_function,
        persist_directory=f"./{db_name}")

    processed_files = get_processed_files()

    # Process images
    if image_files:
        print(f"{Fore.MAGENTA}Processing {len(image_files)} image files...{Style.RESET_ALL}")
        counter = 1
        for file in image_files:
            print('---------------------------------------------------------------')
            print(f'{counter} / {len(image_files)} (Images)')
            print(file)
            print('\n\n')
            if file in processed_files:
                print(f'{Fore.LIGHTYELLOW_EX}FILE ALREADY PROCESSED, SKIPPED{Style.RESET_ALL}')
            else:
                analyze_image(file, vision_chain, object_chain, csv_filepath)
            counter += 1

    # Process videos
    if video_files:
        print(f"\n{Fore.MAGENTA}Processing {len(video_files)} video files...{Style.RESET_ALL}")
        print(f"{Fore.CYAN}Perfect for CCTV camera setups with multiple folders!{Style.RESET_ALL}")
        
        # Group videos by camera folder for better organization
        videos_by_folder = {}
        for video_file in video_files:
            folder_path = os.path.dirname(video_file)
            folder_name = os.path.basename(folder_path) if folder_path != root_image_dir else "Root"
            if folder_name not in videos_by_folder:
                videos_by_folder[folder_name] = []
            videos_by_folder[folder_name].append(video_file)
        
        print(f"{Fore.CYAN}Videos organized by camera/folder:{Style.RESET_ALL}")
        for folder, videos in videos_by_folder.items():
            print(f"  📹 {folder}: {len(videos)} video(s)")
        print()
        
        counter = 1
        for video_file in video_files:
            # Determine camera/folder context
            folder_path = os.path.dirname(video_file)
            folder_name = os.path.basename(folder_path) if folder_path != root_image_dir else "Root"
            video_filename = os.path.basename(video_file)
            
            print('=' * 80)
            print(f'{Fore.CYAN}📹 VIDEO {counter} / {len(video_files)}{Style.RESET_ALL}')
            print(f'{Fore.CYAN}📁 Camera/Folder: {folder_name}{Style.RESET_ALL}')
            print(f'{Fore.CYAN}🎬 File: {video_filename}{Style.RESET_ALL}')
            print(f'{Fore.CYAN}📍 Full Path: {video_file}{Style.RESET_ALL}')
            print('=' * 80)
            print('\n')
            
            # Check if video has already been processed by looking for any frames from this video
            video_already_processed = any(
                pf.startswith(video_file) and 'frame_' in pf 
                for pf in processed_files
            )
            
            if video_already_processed:
                print(f'{Fore.LIGHTYELLOW_EX}VIDEO ALREADY PROCESSED, SKIPPED{Style.RESET_ALL}')
                print(f'{Fore.LIGHTYELLOW_EX}(Found existing frame data in database){Style.RESET_ALL}')
            else:
                print(f'{Fore.GREEN}🚀 Starting analysis...{Style.RESET_ALL}')
                # Process video with 2-second intervals (you can change this)
                try:
                    frame_details_list = analyze_video(video_file, vision_chain, object_chain, interval_seconds=2, csv_filepath=csv_filepath)
                    if frame_details_list:
                        total_objects = sum(len(frame.detected_objects) for frame in frame_details_list)
                        print(f'{Fore.GREEN}✅ Successfully processed {len(frame_details_list)} frames from {folder_name}/{video_filename}{Style.RESET_ALL}')
                        print(f'{Fore.GREEN}🔍 Total objects detected: {total_objects}{Style.RESET_ALL}')
                    else:
                        print(f'{Fore.YELLOW}⚠️  No frames extracted from {folder_name}/{video_filename}{Style.RESET_ALL}')
                except Exception as e:
                    print(f'{Fore.RED}❌ Error processing {folder_name}/{video_filename}: {str(e)}{Style.RESET_ALL}')
            
            counter += 1
            print('\n')
    
    # Final CCTV processing summary
    total_files = len(image_files) + len(video_files)
    if total_files > 0:
        print("\n" + "=" * 80)
        print(f"{Fore.GREEN}🎉 CCTV PROCESSING COMPLETE! 🎉{Style.RESET_ALL}")
        print("=" * 80)
        
        if image_files:
            print(f"📷 Images processed: {len(image_files)}")
        if video_files:
            print(f"📹 Videos processed: {len(video_files)}")
            
            # Show videos by camera folder
            videos_by_folder = {}
            for video_file in video_files:
                folder_path = os.path.dirname(video_file)
                folder_name = os.path.basename(folder_path) if folder_path != root_image_dir else "Root"
                if folder_name not in videos_by_folder:
                    videos_by_folder[folder_name] = 0
                videos_by_folder[folder_name] += 1
            
            print(f"{Fore.CYAN}📁 Videos by camera/folder:{Style.RESET_ALL}")
            for folder, count in videos_by_folder.items():
                print(f"  📹 {folder}: {count} video(s)")
        
        print(f"📊 Total files: {total_files}")
        
        if csv_filepath:
            print(f"📋 Results logged to: {csv_filepath}")
        
        print(f"\n{Fore.CYAN}🔍 To search your processed CCTV footage:{Style.RESET_ALL}")
        print(f"   python codev1.2.py --query 'people walking'")
        print(f"   python codev1.2.py --query 'vehicles' --count 10")
        print(f"   python codev1.2.py --query 'suspicious activity' --open")
        
        print("=" * 80)
    else:
        print(f"{Fore.RED}No image or video files found in {root_image_dir}{Style.RESET_ALL}")
        print("Supported formats:")
        print("- Images: .jpg, .jpeg")
        print("- Videos: .mp4, .avi, .mov, .mkv")
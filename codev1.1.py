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

root_image_dir = "./images_clips"
db_name = 'db_photos'
db_collection_name="photo_collection"
vision_model = 'llava:13b'
#embedding_model="mxbai-embed-large"
embedding_model="nomic-embed-text:v1.5"

# CSV logging configuration
csv_output_dir = "./csv_logs"
enable_csv_logging = True


def get_jpeg_files(directory):
    file_extensions = ['jpg', 'jpeg']
    all_files = []
    for ext in file_extensions:
        pattern = os.path.join(directory, '**', f'*.{ext}')
        all_files.extend(glob.glob(pattern, recursive=True))
    return all_files

def get_video_files(directory):
    """Get all MP4 video files from directory and subdirectories"""
    file_extensions = ['mp3', 'mp4', 'avi', 'mov', 'mkv']
    all_files = []
    for ext in file_extensions:
        pattern = os.path.join(directory, '**', f'*.{ext}')
        all_files.extend(glob.glob(pattern, recursive=True))
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

def extract_google_drive_file_id(url):
    """Extract file ID from Google Drive URL"""
    # Handle different Google Drive URL formats
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
            raise ValueError("Could not extract file ID from Google Drive URL")
    
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
    
    # Create filename from URL or use generic name
    if is_google_drive_url(url):
        filename = f"gdrive_video_{extract_google_drive_file_id(url)}.mp4"
    else:
        # Extract filename from URL or use generic name
        parsed_url = urllib.parse.urlparse(url)
        filename = os.path.basename(parsed_url.path) or "downloaded_video.mp4"
        
        # Ensure it has a video extension
        if not any(filename.lower().endswith(ext) for ext in ['.mp4', '.avi', '.mov', '.mkv']):
            filename += '.mp4'
    
    destination = os.path.join(temp_dir, filename)
    
    # Download based on URL type
    if is_google_drive_url(url):
        success = download_from_google_drive(url, destination)
    else:
        success = download_from_url(url, destination)
    
    if success and os.path.exists(destination):
        return destination
    else:
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
    parser.add_argument('url_or_query', nargs='?', help='Video URL or query text (legacy positional argument)')
    parser.add_argument('interval', nargs='?', type=int, default=10, help='Frame interval for video processing')
    
    # Query mode arguments
    parser.add_argument('--query', '-q', type=str, help='Query the database with natural language')
    parser.add_argument('--count', '-c', type=int, default=5, help='Number of query results to return')
    parser.add_argument('--open', '-o', action='store_true', help='Automatically open found files')
    parser.add_argument('--help-query', action='store_true', help='Show query help and examples')
    
    args = parser.parse_args()
    
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
            print(f"{Fore.CYAN}Processing video from URL...{Style.RESET_ALL}")
            print(f"URL: {input_arg}")
            print(f"Frame interval: {interval} seconds")
            
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
    print(f"{Fore.CYAN}Processing local files in {root_image_dir}...{Style.RESET_ALL}")
    print("💡 TIP: To query the database, use: python codev1.1.py --query 'your search text'")
    print("💡 TIP: To process a video from URL, use: python codev1.1.py <video_url> [interval_seconds]")
    print()
    
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
        counter = 1
        for video_file in video_files:
            print('---------------------------------------------------------------')
            print(f'{counter} / {len(video_files)} (Videos)')
            print(video_file)
            print('\n\n')
            
            # Check if video has already been processed by looking for any frames from this video
            video_already_processed = any(
                pf.startswith(video_file) and 'frame_' in pf 
                for pf in processed_files
            )
            
            if video_already_processed:
                print(f'{Fore.LIGHTYELLOW_EX}VIDEO ALREADY PROCESSED, SKIPPED{Style.RESET_ALL}')
            else:
                # Process video with 2-second intervals (you can change this)
                analyze_video(video_file, vision_chain, object_chain, interval_seconds=2, csv_filepath=csv_filepath)
            counter += 1
    
    # Final summary
    total_files = len(image_files) + len(video_files)
    if total_files > 0:
        if csv_filepath:
            print(f"\n{Fore.GREEN}Processing complete! Results logged to: {csv_filepath}{Style.RESET_ALL}")
        else:
            print(f"\n{Fore.GREEN}Processing complete!{Style.RESET_ALL}")
    else:
        print(f"{Fore.RED}No image or video files found in {root_image_dir}{Style.RESET_ALL}")
        print("Supported formats:")
        print("- Images: .jpg, .jpeg")
        print("- Videos: .mp4, .avi, .mov, .mkv")
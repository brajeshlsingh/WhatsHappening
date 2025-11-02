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
from colorama import Fore, Style
from langchain_core.documents import Document
from langchain_ollama import ChatOllama, OllamaEmbeddings
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_core.output_parsers import JsonOutputParser, StrOutputParser
from langchain_chroma import Chroma


#from ImageDetails import ImageDetails
#import ImageDetailsFactory

root_image_dir = "./images"
db_name = 'db_photos'
db_collection_name="photo_collection"
vision_model = 'llava:13b'
#embedding_model="mxbai-embed-large"
embedding_model="nomic-embed-text:v1.5"


def get_jpeg_files(directory):
    file_extensions = ['jpg', 'jpeg']
    all_files = []
    for ext in file_extensions:
        pattern = os.path.join(directory, '**', f'*.{ext}')
        all_files.extend(glob.glob(pattern, recursive=True))
    return all_files

def get_video_files(directory):
    """Get all MP4 video files from directory and subdirectories"""
    file_extensions = ['mp4', 'avi', 'mov', 'mkv']
    all_files = []
    for ext in file_extensions:
        pattern = os.path.join(directory, '**', f'*.{ext}')
        all_files.extend(glob.glob(pattern, recursive=True))
    return all_files

def extract_frames_from_video(video_path, interval_seconds=10):
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


def analyze_image(image_file, vision_chain, object_chain)->ImageDetails:
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

        print(f"{Fore.CYAN}Description:\n{Style.RESET_ALL}{image_details.description}")
        print(f"{Fore.CYAN}Detected Objects:\n{Style.RESET_ALL}{image_details.get_detected_objects_text()}")
        print('<=----------------------------------------------=>')

    end_time = time.time()
    execution_time = end_time - start_time
    print('\n')
    print(f"{Fore.YELLOW}Execution time: {execution_time:.4f} seconds{Style.RESET_ALL}")

    print(str(image_details))

    return image_details

def analyze_video_frame(video_file, frame_data, vision_chain, object_chain)->VideoFrameDetails:
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

    print(f"{Fore.CYAN}Frame Description:\n{Style.RESET_ALL}{frame_details.description}")
    print(f"{Fore.CYAN}Detected Objects:\n{Style.RESET_ALL}{frame_details.get_detected_objects_text()}")
    print('<=----------------------------------------------=>')

    end_time = time.time()
    execution_time = end_time - start_time
    print(f"{Fore.YELLOW}Frame processing time: {execution_time:.4f} seconds{Style.RESET_ALL}")
    print('\n')

    return frame_details

def analyze_video(video_file, vision_chain, object_chain, interval_seconds=10):
    """Analyze an entire video by extracting frames at specified intervals"""
    print(f"{Fore.GREEN}PROCESSING VIDEO: {video_file}{Style.RESET_ALL}")
    print(f"Extracting frames every {interval_seconds} seconds...")
    
    frames = extract_frames_from_video(video_file, interval_seconds)
    
    if not frames:
        print(f"{Fore.RED}No frames extracted from video{Style.RESET_ALL}")
        return []
    
    print(f"Extracted {len(frames)} frames from video")
    
    frame_details_list = []
    for i, frame_data in enumerate(frames):
        print(f"\n--- Processing frame {i+1}/{len(frames)} ---")
        frame_details = analyze_video_frame(video_file, frame_data, vision_chain, object_chain)
        frame_details_list.append(frame_details)
    
    return frame_details_list

if __name__ == '__main__':
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
                analyze_image(file, vision_chain, object_chain)
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
                # Process video with 10-second intervals (you can change this)
                analyze_video(video_file, vision_chain, object_chain, interval_seconds=10)
            counter += 1
    
    if not image_files and not video_files:
        print(f"{Fore.RED}No image or video files found in {root_image_dir}{Style.RESET_ALL}")
        print("Supported formats:")
        print("- Images: .jpg, .jpeg")
        print("- Videos: .mp4, .avi, .mov, .mkv")
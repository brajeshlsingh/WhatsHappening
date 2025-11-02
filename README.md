# Object Detection with Video Support

This project now supports object detection and analysis for both images and MP4 video files.

## New Features

### Video Processing
- **Frame Extraction**: Extracts frames from MP4 videos at configurable intervals (default: every 10 seconds)
- **Object Detection**: Analyzes each extracted frame for objects using vision AI
- **Description Generation**: Creates detailed descriptions of each video frame
- **Vector Storage**: Stores frame analysis results in the same ChromaDB database as images

### Supported Formats
- **Images**: `.jpg`, `.jpeg`
- **Videos**: `.mp4`, `.avi`, `.mov`, `.mkv`

## Usage

### 1. Process All Files (Images + Videos)
```bash
python code.py
```
This will process all images and videos in the `./images` directory.

### 2. Test Video Processing
```bash
# Test with a specific video file
python test_video.py path/to/your/video.mp4

# Test with custom interval (e.g., every 5 seconds)
python test_video.py path/to/your/video.mp4 5

# Test with videos in ./images directory
python test_video.py
```

### 3. Customize Frame Extraction Interval
You can modify the frame extraction interval by changing the `interval_seconds` parameter:

```python
# Extract frames every 5 seconds instead of 10
analyze_video(video_file, vision_chain, object_chain, interval_seconds=5)
```

## How Video Processing Works

1. **Frame Extraction**: The system uses OpenCV to extract frames from the video at specified intervals
2. **Timestamp Tracking**: Each frame is tagged with its timestamp and frame number
3. **AI Analysis**: Each frame is analyzed using the same vision model as images:
   - Object detection using JSON output parser
   - Scene description using string output parser
4. **Database Storage**: Results are stored with metadata including:
   - Original video filename
   - Frame timestamp
   - Frame number
   - Detected objects
   - Frame description

## Database Schema

### Video Frame Metadata
```python
{
    'file_name': 'path/to/video.mp4',
    'timestamp': 10.5,  # seconds
    'frame_number': 315,
    'detected_objects': 'person - walking, car - parked',
    'description': 'A person walking past a parked car...',
    'generated_with': 'llava:13b',
    'content_type': 'video_frame'
}
```

## Requirements

### New Dependencies
```bash
pip install opencv-python
```

### Existing Dependencies
- langchain-ollama
- langchain-chroma
- PIL (Pillow)
- colorama
- sqlite3

## Configuration

### Video Processing Settings
```python
# In code.py, you can modify these settings:
root_image_dir = "./images"        # Directory to scan for videos
vision_model = 'llava:13b'         # Vision AI model
embedding_model = "nomic-embed-text:v1.5"  # Embedding model

# Frame extraction interval (seconds)
interval_seconds = 10  # Extract frame every 10 seconds
```

## Performance Considerations

- **Processing Time**: Video processing takes longer than images due to frame extraction and multiple AI calls
- **Storage**: Each frame creates a separate database entry
- **Memory**: Large videos may require significant memory for frame processing

### Example Processing Times
- **10-second video** (1 frame): ~30-60 seconds
- **60-second video** (6 frames): ~3-6 minutes
- **300-second video** (30 frames): ~15-30 minutes

## Examples

### Extract and Analyze Frames
```python
# Extract frames every 15 seconds
frames = extract_frames_from_video("video.mp4", interval_seconds=15)

# Analyze each frame
for frame_data in frames:
    frame_details = analyze_video_frame(
        "video.mp4", 
        frame_data, 
        vision_chain, 
        object_chain
    )
```

### Query Video Content
After processing, you can query the vector database to find specific content across both images and video frames:

```python
# Find frames with specific objects
results = db.similarity_search("person walking dog", k=5)

# Results may include both image and video frame matches
for result in results:
    if result.metadata.get('content_type') == 'video_frame':
        print(f"Found in video: {result.metadata['file_name']}")
        print(f"At timestamp: {result.metadata['timestamp']}s")
    else:
        print(f"Found in image: {result.metadata['file_name']}")
```

## Troubleshooting

### Common Issues

1. **OpenCV Import Error**
   ```bash
   pip install opencv-python
   ```

2. **Video File Not Opening**
   - Ensure the video file exists and is not corrupted
   - Check that the video format is supported
   - Try converting to MP4 if using other formats

3. **Memory Issues with Large Videos**
   - Increase the frame extraction interval
   - Process shorter video segments
   - Ensure sufficient system memory

4. **Slow Processing**
   - Reduce frame extraction frequency
   - Use a faster vision model if available
   - Process videos in smaller batches

## Future Enhancements

- Audio analysis integration
- Motion detection for dynamic frame extraction
- Video summarization across multiple frames
- Real-time video stream processing

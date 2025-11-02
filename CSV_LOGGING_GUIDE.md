# CSV Logging Documentation

## Overview

The object detection system now automatically logs all processing results to CSV files for comprehensive analysis and record-keeping. Each run creates a timestamped CSV file containing detailed information about every processed image and video frame.

## CSV File Structure

### Location
- **Directory**: `./csv_logs/`
- **Filename Format**: `object_detection_log_YYYYMMDD_HHMMSS.csv`
- **Example**: `object_detection_log_20251101_143022.csv`

### CSV Columns

| Column | Description | Example |
|--------|-------------|---------|
| `session_timestamp` | When the item was processed | `2025-11-01T14:30:22.123456` |
| `file_path` | Path to the source file/URL | `./images_clips/video.mp4` |
| `content_type` | Type of content | `image` or `video_frame` |
| `timestamp_seconds` | Video timestamp (empty for images) | `10.50` |
| `frame_number` | Video frame number (empty for images) | `315` |
| `object_name` | Name of detected object | `person` |
| `object_description` | Description of the object | `person walking` |
| `scene_description` | Overall scene description | `A busy street scene...` |
| `make` | Camera make (images only) | `Canon` |
| `model` | Camera model (images only) | `EOS R5` |
| `camera_date` | Date photo was taken | `2025:10:30 14:25:33` |
| `aperture_value` | Camera aperture | `2.8` |
| `focal_length` | Lens focal length | `85mm` |
| `exposure_time` | Shutter speed | `1/250` |
| `f_stops` | F-stop value | `f/2.8` |
| `iso` | ISO sensitivity | `400` |
| `gps_coordinates` | GPS location | `40.7128, -74.0060` |
| `generated_with` | AI model used | `llava:13b` |
| `processing_time_seconds` | Time to process this item | `45.2341` |

## Key Features

### 📊 **Per-Object Logging**
- Each detected object gets its own CSV row
- Multiple objects in one image/frame = multiple rows
- Items with no objects get logged as `NO_OBJECTS_DETECTED`

### 🎯 **Session-Based Files**
- Each run creates a new CSV file
- No data overwriting between sessions
- Easy to track processing history

### 📸 **Complete EXIF Data**
- Full camera metadata for images
- GPS coordinates when available
- Technical photo details preserved

### 🎥 **Video Frame Details**
- Precise timestamp for each frame
- Frame number tracking
- Video source URL/path preserved

## Configuration

### Enable/Disable CSV Logging
```python
# In codev1.1.py
enable_csv_logging = True   # Enable logging
enable_csv_logging = False  # Disable logging
```

### Change Output Directory
```python
# In codev1.1.py
csv_output_dir = "./csv_logs"     # Default
csv_output_dir = "./my_logs"      # Custom directory
```

## Usage Examples

### 1. Basic Analysis
```bash
# Analyze the most recent CSV log
python analyze_csv_logs.py

# Analyze a specific CSV file
python analyze_csv_logs.py csv_logs/object_detection_log_20251101_143022.csv
```

### 2. Generate Summary Report
```bash
# Create a text summary report
python analyze_csv_logs.py --export-report
```

### 3. Working with CSV Data
```python
import pandas as pd

# Load CSV data
df = pd.read_csv('csv_logs/object_detection_log_20251101_143022.csv')

# Find all images with people
people_images = df[(df['object_name'] == 'person') & (df['content_type'] == 'image')]

# Get video frames at specific timestamps
frame_10s = df[(df['content_type'] == 'video_frame') & (df['timestamp_seconds'] == '10.00')]

# Count objects per file
objects_per_file = df.groupby('file_path')['object_name'].count()
```

## Analysis Features

The `analyze_csv_logs.py` script provides:

### 📈 **Statistical Overview**
- Total entries processed
- Unique files analyzed
- Content type breakdown
- Processing time statistics

### 🔍 **Object Detection Insights**
- Most frequently detected objects
- Objects per file statistics
- Files with most objects
- Detection success rate

### 🎥 **Video Analytics**
- Timeline coverage analysis
- Objects detected across video duration
- Frame-by-frame object tracking

### 📸 **Image Metadata Analysis**
- Camera equipment statistics
- EXIF data insights
- GPS-tagged image count

### ⏰ **Session Timeline**
- Processing duration
- Start/end timestamps
- Processing efficiency metrics

## File Examples

### Sample CSV Row (Image)
```csv
session_timestamp,file_path,content_type,timestamp_seconds,frame_number,object_name,object_description,scene_description,make,model,camera_date,aperture_value,focal_length,exposure_time,f_stops,iso,gps_coordinates,generated_with,processing_time_seconds
2025-11-01T14:30:22.123456,./images_clips/photo.jpg,image,,,person,person standing,A person standing in a park with trees in the background,Canon,EOS R5,2025:10:30 14:25:33,2.8,85mm,1/250,f/2.8,400,40.7128 -74.0060,llava:13b,45.2341
```

### Sample CSV Row (Video Frame)
```csv
session_timestamp,file_path,content_type,timestamp_seconds,frame_number,object_name,object_description,scene_description,make,model,camera_date,aperture_value,focal_length,exposure_time,f_stops,iso,gps_coordinates,generated_with,processing_time_seconds
2025-11-01T14:32:15.789012,./videos/clip.mp4,video_frame,10.50,315,car,red car driving,A red car driving down a city street,,,,,,,,,llava:13b,38.1547
```

## Benefits

### 🎯 **Data Analysis**
- Track object detection accuracy over time
- Identify most common objects in your dataset
- Analyze processing performance

### 📊 **Reporting**
- Generate automated reports
- Share processing results with stakeholders
- Create visualizations and charts

### 🔄 **Process Improvement**
- Monitor AI model performance
- Optimize processing parameters
- Track system efficiency

### 📝 **Record Keeping**
- Maintain audit trail of all processing
- Export data for external analysis
- Integrate with other data systems

## Integration

### With Excel/Google Sheets
```bash
# CSV files can be directly opened in:
# - Microsoft Excel
# - Google Sheets
# - LibreOffice Calc
# - Any spreadsheet application
```

### With Data Analysis Tools
```python
# Pandas for Python
import pandas as pd
df = pd.read_csv('csv_logs/log_file.csv')

# R for statistical analysis
df <- read.csv('csv_logs/log_file.csv')

# Power BI, Tableau, etc.
# Direct CSV import supported
```

### With Databases
```sql
-- Import into SQLite, PostgreSQL, MySQL, etc.
-- Most databases support CSV import functionality
```

## Troubleshooting

### Common Issues

1. **CSV File Not Created**
   - Check `enable_csv_logging = True`
   - Verify write permissions for `csv_output_dir`
   - Ensure directory exists (auto-created if possible)

2. **Missing Data in CSV**
   - Some EXIF fields may be empty for certain images
   - Video frames don't have camera metadata
   - GPS coordinates only available if embedded in image

3. **Large CSV Files**
   - Video processing creates many rows (one per object per frame)
   - Consider processing shorter video segments
   - Use the analysis script to generate summaries

4. **Encoding Issues**
   - CSV files use UTF-8 encoding
   - Some special characters in filenames may appear differently
   - Use proper encoding when opening in text editors

## Performance Impact

### Storage Requirements
- **Per Image**: ~1-10 rows (depending on objects detected)
- **Per Video Frame**: ~1-15 rows (depending on objects detected)
- **Average Row Size**: ~500-800 bytes
- **Example**: 100 images with 5 objects each = ~400KB CSV file

### Processing Overhead
- **CSV logging adds**: ~0.1-0.5 seconds per item
- **Minimal performance impact** compared to AI processing
- **Can be disabled** if not needed for maximum speed

## Tips and Best Practices

### 🎯 **Optimization**
- Regularly analyze logs to optimize frame extraction intervals
- Use summary reports for quick insights
- Archive old CSV files to maintain performance

### 📊 **Analysis**
- Combine multiple CSV files for comprehensive analysis
- Use filtering to focus on specific content types
- Track object detection trends over time

### 🔄 **Maintenance**
- Clean up old CSV files periodically
- Monitor disk space usage
- Backup important analysis results

---

*The CSV logging feature provides comprehensive tracking and analysis capabilities for your object detection workflows. Use it to gain insights, improve processes, and maintain detailed records of all processing activities.*
# 🔗 Google Drive Integration Guide

## 📋 Overview
This guide explains how to process videos from Google Drive with your CCTV Object Detection System.

## ⚠️ Important: Folder vs File URLs

### ❌ NOT Supported - Folder URLs
```
❌ https://drive.google.com/drive/folders/FOLDER_ID
❌ https://drive.google.com/folders/FOLDER_ID
```
**These contain multiple files and cannot be processed directly.**

### ✅ Supported - Individual File URLs
```
✅ https://drive.google.com/file/d/FILE_ID/view
✅ https://drive.google.com/open?id=FILE_ID
```

## 🎯 How to Get Individual Video File URLs

### Method 1: Right-Click Method
1. 📂 Open your Google Drive folder
2. 📹 **Right-click** on each video file
3. 🔗 Select **"Get link"** → **"Copy link"**
4. 🎯 This gives you the correct file URL format

### Method 2: Share Button Method
1. 📂 Open your Google Drive folder
2. 📹 Click on a video file to select it
3. 🔗 Click the **"Share"** button (person with +)
4. 🔗 Click **"Copy link"**

## 🚀 Usage Examples

### Process Single Video from Google Drive
```bash
python codev1.2.py "https://drive.google.com/file/d/1ABC123DEF456/view" 5
```

### Process Multiple Videos (One at a time)
```bash
# Camera 1 video
python codev1.2.py "https://drive.google.com/file/d/1CAM1VIDEO/view" 2

# Camera 2 video  
python codev1.2.py "https://drive.google.com/file/d/1CAM2VIDEO/view" 2

# Camera 3 video
python codev1.2.py "https://drive.google.com/file/d/1CAM3VIDEO/view" 2
```

## 💡 Alternative: Local CCTV Setup (Recommended)

### Step 1: Download Videos from Google Drive
1. 📂 Open your Google Drive folder
2. ✅ Select all videos (Ctrl+A or Cmd+A)
3. 📥 Right-click → **"Download"**
4. 📦 Extract the downloaded ZIP file

### Step 2: Organize in CCTV Structure
```
./images_clips/
├── camera_1/
│   ├── recording_001.mp4
│   ├── recording_002.mp4
│   └── ...
├── camera_2/
│   ├── recording_003.mp4
│   ├── recording_004.mp4
│   └── ...
└── camera_3/
    ├── recording_005.mp4
    ├── recording_006.mp4
    └── ...
```

### Step 3: Process All Videos
```bash
python codev1.2.py
```
**This will automatically process all videos recursively!**

## 🎥 Frame Extraction Settings

| Interval | Use Case | Frames per Minute |
|----------|----------|-------------------|
| 1 second | High detail analysis | 60 |
| 2 seconds | Balanced (default) | 30 |
| 5 seconds | Quick overview | 12 |
| 10 seconds | Fast processing | 6 |

## 📊 Performance Comparison

### Google Drive URL Processing
- ✅ **Pros:** Direct cloud processing
- ❌ **Cons:** Download time, single file only
- ⏱️ **Speed:** Slower (download + process)

### Local CCTV Processing  
- ✅ **Pros:** Batch processing, faster, better organization
- ✅ **Pros:** Recursive folder scanning
- ✅ **Pros:** Camera folder organization
- ⏱️ **Speed:** Faster (process only)

## 🔍 Search Examples After Processing

```bash
# Search for people across all cameras
python codev1.2.py --query "people walking" --count 10

# Search for vehicles
python codev1.2.py --query "cars and vehicles" --count 5

# Search for suspicious activity
python codev1.2.py --query "suspicious activity" --open

# Search for specific camera footage
python codev1.2.py --query "camera_1 recordings" --count 3
```

## 🛠️ Troubleshooting

### Error: "Could not extract file ID"
- ❌ **Problem:** Using folder URL instead of file URL
- ✅ **Solution:** Get individual file URLs using right-click method

### Error: "Download failed"
- ❌ **Problem:** File might be private or restricted
- ✅ **Solution:** Ensure file is shared publicly or with your account

### Error: "No frames extracted"
- ❌ **Problem:** Video file might be corrupted or unsupported format
- ✅ **Solution:** Try different video or check format (MP4 recommended)

## 🎯 Best Practices for CCTV

1. **📁 Use Local Processing:** Download and organize videos locally
2. **🏗️ Folder Structure:** Organize by camera (camera_1, camera_2, etc.)
3. **⏱️ Frame Intervals:** Use 2-5 seconds for CCTV footage
4. **🔍 Descriptive Search:** Use specific terms for better results
5. **📊 CSV Logs:** Enable logging for analysis and reporting

---

**Recommendation:** For CCTV analysis, download videos locally and use the recursive folder processing for best performance and organization! 🚀
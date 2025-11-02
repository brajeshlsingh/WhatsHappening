# 🔧 Google Drive API Integration Setup

## 📋 Overview
This guide explains how to enable automatic Google Drive folder processing for your CCTV Object Detection System.

## 🎯 What This Enables
- **Automatic folder scanning**: Extract all video URLs from a Google Drive folder automatically
- **Batch processing**: Process all videos in a folder with a single command
- **No manual URL extraction**: Skip the manual right-click → copy link process

## 📦 Installation Steps

### Step 1: Install Required Libraries
```bash
pip install google-api-python-client google-auth-httplib2 google-auth-oauthlib
```

### Step 2: Set Up Google Drive API Credentials

#### 2.1 Create a Google Cloud Project
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. Note your project ID

#### 2.2 Enable Google Drive API
1. In the Google Cloud Console, go to **APIs & Services** → **Library**
2. Search for "Google Drive API"
3. Click on it and press **"Enable"**

#### 2.3 Create Credentials
1. Go to **APIs & Services** → **Credentials**
2. Click **"Create Credentials"** → **"OAuth 2.0 Client IDs"**
3. If prompted, configure the OAuth consent screen:
   - Choose **"External"** user type
   - Fill in required fields (App name, User support email, Developer contact)
   - Add your email to test users
4. For Application type, choose **"Desktop application"**
5. Give it a name (e.g., "CCTV Video Processor")
6. Click **"Create"**

#### 2.4 Download Credentials
1. Click the download button (⬇️) next to your newly created OAuth 2.0 Client ID
2. Save the file as `credentials.json` in your project directory (`c:\MiniPrj\ObjDetPrompt\`)

### Step 3: Configure the System
Edit `codev1.2.py` and change:
```python
enable_gdrive_api = True  # Change from False to True
```

## 🚀 Usage After Setup

### Process Entire Google Drive Folder
```bash
# Process all videos in folder with 5-second intervals
python codev1.2.py "https://drive.google.com/drive/folders/YOUR_FOLDER_ID" 5

# Process all videos in folder with 2-second intervals (more detailed)
python codev1.2.py "https://drive.google.com/drive/folders/YOUR_FOLDER_ID" 2
```

### Example with Your Folder
```bash
python codev1.2.py "https://drive.google.com/drive/folders/1nVnJFcr_F7qcv8JoFhUYocgg3dIpU3Nu?usp=sharing" 5
```

## 🔐 First-Time Authentication
When you run the command for the first time:

1. **Browser will open automatically**
2. **Sign in** to your Google account
3. **Grant permissions** to access Google Drive
4. **Copy the authorization code** if prompted
5. **Paste it back** in the terminal

The system will save your authentication token for future use.

## 📁 What the API Does

### Automatic Processing Flow
1. **Extract folder ID** from the URL
2. **Scan folder** for video files via Google Drive API
3. **Get direct download URLs** for each video
4. **Process each video** automatically with AI analysis
5. **Store results** in vector database and CSV logs

### Supported Video Formats
- `.mp4`, `.avi`, `.mov`, `.mkv`, `.wmv`, `.flv`, `.webm`

## 📊 Expected Output

```
🚀 Processing Google Drive Folder
Folder: https://drive.google.com/drive/folders/YOUR_FOLDER_ID
Frame interval: 5 seconds
================================================================================

🔧 Google Drive API integration enabled
🚀 Scanning folder via Google Drive API...
Found 3 video files in folder

📹 Processing video 1/3
URL: https://drive.google.com/file/d/1ABC123_VIDEO1/view
✅ Video 1: 15 frames, 45 objects

📹 Processing video 2/3  
URL: https://drive.google.com/file/d/1DEF456_VIDEO2/view
✅ Video 2: 22 frames, 67 objects

📹 Processing video 3/3
URL: https://drive.google.com/file/d/1GHI789_VIDEO3/view
✅ Video 3: 18 frames, 33 objects

🎉 Folder processing summary:
   📹 Videos processed: 3
   🎬 Total frames: 55
   🔍 Total objects detected: 145
   📋 Results logged to: ./csv_logs/object_detection_log_20251101_135041.csv
```

## 🔒 Security & Privacy

### What Access is Granted
- **Read-only access** to your Google Drive files
- **File metadata** (names, types, folder structure)
- **Download permissions** for processing

### What is NOT Accessed
- ❌ No file modification or deletion
- ❌ No access to other Google services
- ❌ No sharing or uploading capabilities

### Data Handling
- **Videos are downloaded temporarily** for processing
- **Temporary files are deleted** after processing
- **Only analysis results** are stored locally
- **Original videos remain** in your Google Drive

## 🛠️ Troubleshooting

### Common Issues

#### "Import Error: No module named 'googleapiclient'"
```bash
pip install google-api-python-client google-auth-httplib2 google-auth-oauthlib
```

#### "Credentials not found"
- Ensure `credentials.json` is in the project directory
- Check that `enable_gdrive_api = True` in the configuration

#### "Access denied" or "Permission error"
- Check OAuth consent screen configuration
- Add your email to test users
- Re-run the authentication process

#### "Quota exceeded"
- Google Drive API has daily quotas
- For heavy usage, request quota increases in Google Cloud Console

### Alternative if API Setup Fails
If you can't set up the API, the system will fall back to manual processing:

1. **Open the Google Drive folder**
2. **Right-click each video** → "Get link" → "Copy link"
3. **Process individually:**
   ```bash
   python codev1.2.py <video_url_1> 5
   python codev1.2.py <video_url_2> 5
   python codev1.2.py <video_url_3> 5
   ```

## 🎯 Benefits of API Integration

| Method | Videos | Time | Effort |
|--------|--------|------|--------|
| **Manual** | 10 videos | 30+ minutes | High |
| **API** | 10 videos | 5 minutes | Low |
| **Local** | 10 videos | 2 minutes | Medium |

## 💡 Recommendations

### For Development/Testing
- ✅ **Use API integration** for convenience
- ✅ Small video folders (< 20 videos)

### For Production/Heavy Use
- ✅ **Download videos locally** and use CCTV folder structure
- ✅ Better performance and reliability
- ✅ No API quotas or internet dependency

### For CCTV Camera Integration
- ✅ **Set up local folder structure** with camera organization
- ✅ Use scheduled batch processing
- ✅ Combine with automated video downloads from cameras

---

**Ready to process your CCTV footage automatically!** 🎥🚀
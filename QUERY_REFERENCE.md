# Database Query Reference

## Overview
Your object detection system now includes powerful database querying capabilities. You can search through all processed images and video frames using natural language queries.

## Quick Start

### Method 1: Using the main script
```bash
# Basic query
python codev1.1.py --query "photos of burnt vegetation"

# Get more results
python codev1.1.py --query "people walking" --count 10

# Automatically open found files
python codev1.1.py --query "cars in street" --open

# Combined options
python codev1.1.py --query "sunset scenes" --count 3 --open
```

### Method 2: Using the standalone query tool
```bash
# Basic query
python query_db.py "photos of burnt vegetation"

# Get more results  
python query_db.py "people walking" --count 10

# Open files automatically
python query_db.py "cars in street" --open

# Show example queries
python query_db.py --examples
```

## Command Options

| Option | Short | Description | Example |
|--------|-------|-------------|---------|
| `--query` | `-q` | Search query text | `--query "burnt vegetation"` |
| `--count` | `-c` | Number of results | `--count 10` |
| `--open` | `-o` | Auto-open files | `--open` |
| `--help-query` | | Show query help | `--help-query` |

## Example Queries

### 🔍 **Object-Based Searches**
```bash
python query_db.py "people in photos"
python query_db.py "cars and vehicles"
python query_db.py "animals or pets"
python query_db.py "buildings and architecture"
python query_db.py "food and cooking"
```

### 🎬 **Activity-Based Searches**
```bash
python query_db.py "people walking"
python query_db.py "sports activities"
python query_db.py "outdoor activities"
python query_db.py "people sitting"
```

### 🌅 **Scene-Based Searches**
```bash
python query_db.py "outdoor scenes"
python query_db.py "nature and landscapes"
python query_db.py "urban environments"
python query_db.py "indoor spaces"
python query_db.py "sunset or sunrise"
```

### 🎯 **Specific Searches**
```bash
python query_db.py "photos of burnt vegetation"
python query_db.py "rainy weather"
python query_db.py "crowded places"
python query_db.py "empty rooms"
```

## Query Results

### Result Format
```
Result 1:
  📁 File: ./images_clips/photo.jpg
  📋 Type: image
  📷 Camera: Canon EOS R5
  🔍 Objects: person - walking, tree - large oak tree
  📝 Description: A person walking through a park with large trees...

Result 2:
  📁 File: ./videos/clip.mp4
  📋 Type: video_frame
  ⏱️  Time: 15.50s (Frame 465)
  🔍 Objects: car - red sedan, person - pedestrian
  📝 Description: A red car stopped at a traffic light while a person crosses...
```

### Information Shown
- **File path**: Location of the source file
- **Content type**: `image` or `video_frame`
- **Camera info**: For images with EXIF data
- **Timestamp**: For video frames
- **Detected objects**: Objects found in the content
- **Description**: AI-generated scene description

## Advanced Usage

### 1. **Workflow Integration**
```bash
# Find specific content and open it
python query_db.py "damaged buildings" --open

# Get comprehensive results
python query_db.py "vegetation analysis" --count 20

# Quick spot checks
python query_db.py "people" --count 3 --open
```

### 2. **Content Discovery**
```bash
# Explore your dataset
python query_db.py "outdoor"
python query_db.py "urban"
python query_db.py "nature"

# Find specific scenarios
python query_db.py "emergency situations"
python query_db.py "infrastructure damage"
```

### 3. **Quality Control**
```bash
# Check processing quality
python query_db.py "blurry images"
python query_db.py "poor lighting"
python query_db.py "clear photos"
```

## Tips and Best Practices

### 🎯 **Effective Querying**
- **Be descriptive**: "people walking in park" vs "people"
- **Use synonyms**: "cars, vehicles, automobiles" 
- **Try variations**: "burnt vegetation" vs "burned plants"
- **Combine concepts**: "outdoor activities with people"

### 📊 **Result Optimization**
- Start with `--count 5` then increase if needed
- Use `--open` carefully with many results
- Try broader terms if no results found
- Check database has processed content first

### 🔧 **Troubleshooting**

**No results found:**
```bash
# Check if database exists and has content
python query_db.py "anything" --count 1

# Try broader search terms
python query_db.py "photo" --count 10
```

**Files won't open:**
- Check file paths are still valid
- Ensure you have permissions to open files
- Some file types may need specific applications

**Query errors:**
- Make sure Ollama is running
- Verify database directory exists
- Check network connection for embeddings

## Integration Examples

### 1. **Research Workflow**
```bash
# Find relevant images
python query_db.py "research subject" --count 20

# Open promising results
python query_db.py "specific criteria" --count 5 --open

# Export findings using CSV logs
python analyze_csv_logs.py --export-report
```

### 2. **Content Management**
```bash
# Categorize content
python query_db.py "outdoor scenes"
python query_db.py "indoor spaces" 
python query_db.py "people activities"

# Quality assessment
python query_db.py "high quality photos"
python query_db.py "clear detailed images"
```

### 3. **Analysis Pipeline**
```bash
# Step 1: Process content
python codev1.1.py

# Step 2: Query specific content
python query_db.py "target objects" --open

# Step 3: Analyze results
python analyze_csv_logs.py
```

## Query Language Guide

### Natural Language Patterns
✅ **Good queries:**
- "people walking in urban areas"
- "damaged buildings after storm"
- "vehicles on highway"
- "outdoor recreational activities"

❌ **Less effective:**
- "stuff"
- "things"
- "image"
- Single words without context

### Combining Concepts
```bash
# Object + Location
"cars in parking lot"
"people in building"

# Object + Activity  
"people running"
"dogs playing"

# Scene + Condition
"outdoor sunny day"
"indoor dim lighting"

# Multiple Objects
"people and vehicles"
"buildings and infrastructure"
```

## Performance Notes

- **Database size**: Larger databases take longer to query
- **Query complexity**: Simple queries are faster
- **Result count**: Higher `--count` values take more time
- **File opening**: `--open` adds overhead for each file

---

*The database query feature lets you instantly find specific content from all your processed images and videos using natural language. Perfect for research, analysis, and content management workflows.*
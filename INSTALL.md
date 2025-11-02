# Installation Guide

## Quick Setup

1. **Create a virtual environment (recommended):**
   ```bash
   python -m venv .venv
   ```

2. **Activate the virtual environment:**
   ```bash
   # Windows
   .venv\Scripts\activate
   
   # Linux/Mac
   source .venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## Alternative Installation Methods

### Option 1: Install all at once
```bash
pip install Pillow opencv-python numpy requests langchain-core langchain-ollama langchain-chroma chromadb colorama gdown
```

### Option 2: Install core packages only
```bash
pip install Pillow opencv-python numpy requests langchain-core langchain-ollama langchain-chroma chromadb colorama
```

### Option 3: With specific versions
```bash
pip install Pillow==10.0.1 opencv-python==4.8.1.78 numpy==1.24.3 requests==2.31.0 langchain-core==0.1.52 langchain-ollama==0.1.0 langchain-chroma==0.1.0 chromadb==0.4.15 colorama==0.4.6
```

## System Requirements

- **Python**: 3.8 or higher
- **Operating System**: Windows, macOS, or Linux
- **Memory**: At least 4GB RAM (8GB+ recommended for video processing)
- **Storage**: At least 2GB free space for models and database

## Ollama Setup

This project requires Ollama to be installed and running with the vision model:

1. **Install Ollama**: Visit [https://ollama.ai](https://ollama.ai) and download for your OS

2. **Pull the vision model**:
   ```bash
   ollama pull llava:13b
   ```

3. **Pull the embedding model**:
   ```bash
   ollama pull nomic-embed-text:v1.5
   ```

4. **Verify installation**:
   ```bash
   ollama list
   ```

## Verification

Test your installation:
```bash
python -c "import cv2, PIL, requests, langchain_core, langchain_ollama, langchain_chroma, chromadb, colorama; print('All packages imported successfully!')"
```

## Troubleshooting

### Common Issues

1. **OpenCV issues on Windows**:
   ```bash
   pip install opencv-python-headless
   ```

2. **ChromaDB version conflicts**:
   ```bash
   pip install --upgrade chromadb
   ```

3. **LangChain compatibility**:
   ```bash
   pip install --upgrade langchain-core langchain-ollama langchain-chroma
   ```

4. **Permission errors**:
   ```bash
   pip install --user -r requirements.txt
   ```

### Platform-Specific Notes

**Windows:**
- May need Visual C++ Build Tools for some packages
- Use `py` instead of `python` if needed

**macOS:**
- May need Xcode command line tools: `xcode-select --install`
- For M1/M2 Macs, ensure you're using ARM64 compatible packages

**Linux:**
- May need additional system packages:
  ```bash
  sudo apt-get update
  sudo apt-get install python3-dev python3-pip ffmpeg libsm6 libxext6 libfontconfig1 libxrender1
  ```
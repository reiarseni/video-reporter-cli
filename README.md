
# 📌 About the Project  

This project is an advanced video analysis tool that extracts key information from multimedia files efficiently. Its modular and optimized design makes it ideal for processing large volumes of videos, leveraging parallelization techniques to improve performance. 

**It utilizes **FFmpeg** to accurately extract media durations and supports various formats such as MP4, MKV, AVI, MOV, MPG, MP3, and more.**  

## 🚀 **Features** 
✅ **Recursively scans directories** – Up to a configurable depth  
✅ **Video Duration Extraction** – Retrieves the exact duration of each analyzed video using FFmpeg.  
✅ **Parallel Processing with `multiprocessing`** – Speeds up the processing of multiple files in parallel, optimizing performance for large video batches.  
✅ **Support for Common Formats** – Compatible with MP4, AVI, MKV, and other widely used video formats.  
✅ **Efficiency & Scalability** – Optimized implementation to handle large amounts of videos without affecting system performance.  
✅ **Result Logging** – Exports analysis results in a readable format for further reporting or integration with other applications.  

This tool is ideal for content creators, video archivists, and developers who need a quick overview of media durations in large collections. 🚀

---

## 🛠 **Installation Instructions:**

To use **video-reporter-cli**, you need **FFmpeg** and **Python 3** installed on your system.

1. **Install FFmpeg:**

   - On **Linux (Ubuntu/Debian)**:  
     ```bash
     sudo apt update
     sudo apt install ffmpeg
     ```

   - On **MacOS** (using Homebrew):  
     ```bash
     brew install ffmpeg
     ```

   - On **Windows (using Chocolatey)**:  
     ```powershell
     choco install ffmpeg
     ```

   - On **Windows**:  
     1. Download FFmpeg from the [official website](https://ffmpeg.org/download.html).
     2. Extract the zip file and add the bin folder to your system's PATH variable.


2. **Install Python 3:**

   Ensure you have **Python 3** installed (version 3.6 or higher is required).

   - On **Linux (Ubuntu/Debian)**:  
     ```bash
     sudo apt update
     sudo apt install python3 python3-pip
     ```

   - On **MacOS** (using Homebrew):  
     ```bash
     brew install python3
     ```

   - On **Windows**:  
     Download Python 3 from the [official website](https://www.python.org/downloads/), and ensure you check "Add Python to PATH" during installation.

## 📦 Installation  

1. Clone this repository:  
   ```bash
   git clone https://github.com/reiarseni/video-reporter-cli.git
   cd video-reporter-cli
   ```  
2. Install dependencies:  
   ```bash
   pip install -r requirements.txt
   ```  
3. Run the analysis on a folder of videos:  
   ```bash
   python video_reporter.py /path/to/videos
   
   #or with full options
   python video_reporter.py /path/to/videos --output --depth 2
   ```  

## 👨‍💻 Contributing  

Contributions are welcome! If you find a bug or want to improve the code, feel free to open an **Issue** or submit a **Pull Request**.  

## ⚖️ License  

This project is licensed under the **MIT License**, meaning you can use, modify, and distribute it freely.  

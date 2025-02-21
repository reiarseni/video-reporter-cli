import os
from pathlib import Path
import ffmpeg
import argparse
import mimetypes

def get_video_duration(video_path):
    """Gets the duration of a video in minutes using ffmpeg."""
    try:
        probe = ffmpeg.probe(video_path)
        duration_seconds = float(probe['format']['duration'])
        duration_minutes = duration_seconds / 60
        return duration_minutes
    except Exception as e:
        print(f"Error processing {video_path}: {e}")
        return 0

def get_file_size(file_path):
    """Gets the file size in bytes."""
    try:
        return os.path.getsize(file_path)
    except Exception as e:
        print(f"Error getting size of {file_path}: {e}")
        return 0

def format_size(size_bytes):
    """Formats the file size in KB, MB, or GB."""
    if size_bytes < 1024:
        return f"{size_bytes} bytes"
    elif size_bytes < 1024 * 1024:
        return f"{size_bytes / 1024:.2f} KB"
    elif size_bytes < 1024 * 1024 * 1024:
        return f"{size_bytes / (1024 * 1024):.2f} MB"
    else:
        return f"{size_bytes / (1024 * 1024 * 1024):.2f} GB"

def is_video_file(file_path):
    """Checks if the file is a video by MIME type."""
    mime_type, _ = mimetypes.guess_type(file_path)
    return mime_type and mime_type.startswith('video')

def scan_folder(folder, depth=2):
    """Scans the folder up to a specific depth and calculates the duration and size of the videos."""
    folder = Path(folder)
    if not folder.is_dir():
        print(f"The path {folder} is not a valid directory.")
        return

    report = []
    total_duration = 0
    total_size = 0

    # Sort folders and files for ordered output
    for root, dirs, files in sorted(os.walk(folder)):
        relative_path = Path(root).relative_to(folder)
        current_depth = len(relative_path.parts)

        if current_depth > depth:
            continue

        folder_duration = 0
        folder_size = 0
        folder_report = []

        for file in sorted(files):
            file_path = Path(root) / file
            if is_video_file(file_path):  # Check if the file is a video
                duration = get_video_duration(str(file_path))
                size_bytes = get_file_size(file_path)
                folder_duration += duration
                folder_size += size_bytes
                folder_report.append(f"    {file} ({duration:.2f} minutes, {format_size(size_bytes)})")

        if folder_report:
            report.append(f"{relative_path}/")
            report.extend(folder_report)
            report.append(f"  Total duration in folder: {folder_duration:.2f} minutes, Total size: {format_size(folder_size)}\n")
        total_duration += folder_duration
        total_size += folder_size

    report.append(f"Total duration of all videos: {total_duration:.2f} minutes")
    report.append(f"Total size of all videos: {format_size(total_size)}\n")
    return "\n".join(report)

def main():
    parser = argparse.ArgumentParser(description="Scans a folder and calculates the duration and size of videos.")
    parser.add_argument("folder", type=str, help="Path to the folder to scan")
    parser.add_argument("--depth", type=int, default=2, help="Maximum depth to scan (default 2)")
    args = parser.parse_args()

    folder_to_scan = args.folder
    depth = args.depth

    report = scan_folder(folder_to_scan, depth)

    if report:
        print("\n=== Video Durations and Sizes Report ===\n")
        print(report)

if __name__ == "__main__":
    main()

# usage: python video_reporter.py "/path/to/videos_folder" --depth 2

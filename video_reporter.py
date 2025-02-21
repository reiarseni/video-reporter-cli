import os
from pathlib import Path
import ffmpeg
import argparse

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

def scan_folder(folder, depth=2):
    """Scans the folder up to a specific depth and calculates the duration of the videos."""
    folder = Path(folder)
    if not folder.is_dir():
        print(f"The path {folder} is not a valid folder.")
        return

    report = []
    total_duration = 0

    # Sort folders and files for ordered output
    for root, dirs, files in sorted(os.walk(folder)):
        relative_path = Path(root).relative_to(folder)
        current_depth = len(relative_path.parts)

        if current_depth > depth:
            continue

        folder_duration = 0
        folder_report = []

        for file in sorted(files):
            file_path = Path(root) / file
            if file_path.suffix.lower() in [".mp4", ".mkv", ".avi", ".mov", ".mpg", ".mp3"]:
                duration = get_video_duration(str(file_path))
                folder_duration += duration
                folder_report.append(f"    {file} ({duration:.2f} minutes)")

        if folder_report:
            report.append(f"{relative_path}/")
            report.extend(folder_report)
            report.append(f"  Total duration in folder: {folder_duration:.2f} minutes\n")
        total_duration += folder_duration

    report.append(f"Total duration of all videos: {total_duration:.2f} minutes\n")
    return "\n".join(report)

def main():
    parser = argparse.ArgumentParser(description="Scans a folder and calculates the duration of the videos.")
    parser.add_argument("folder", type=str, help="Path of the folder to scan")
    parser.add_argument("--depth", type=int, default=2, help="Maximum depth to scan (default is 2)")
    args = parser.parse_args()

    folder_to_scan = args.folder
    depth = args.depth

    report = scan_folder(folder_to_scan, depth)

    if report:
        print("\n=== Video Duration Report ===\n")
        print(report)

if __name__ == "__main__":
    main()

#usage: python video_reporter.py "/path/to/videos_folder" --depth 2

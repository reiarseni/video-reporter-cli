import os
from pathlib import Path
import ffmpeg
import argparse
import mimetypes
import multiprocessing  # For parallel processing

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
    """Formats the file size into KB, MB, or GB."""
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
    if mime_type:
        if mime_type.startswith('video') or mime_type.startswith('audio'):
            return True
    return False

def scan_folder(folder, depth=2):
    """
    Scans the folder up to a specified depth and calculates the duration and size of video files.
    Uses multiprocessing to parallelize the video duration extraction.
    """
    folder = Path(folder)
    if not folder.is_dir():
        print(f"The path {folder} is not a valid directory.")
        return

    report = []
    total_duration = 0
    total_size = 0

    # Create a pool for parallel video duration calculation
    with multiprocessing.Pool() as pool:
        # Sort folders and files for ordered output
        for root, dirs, files in sorted(os.walk(folder)):
            relative_path = Path(root).relative_to(folder)
            current_depth = len(relative_path.parts)

            if current_depth > depth:
                continue

            folder_duration = 0
            folder_size = 0
            folder_report = []

            video_file_paths = []
            video_file_names = []

            for file in sorted(files):
                file_path = Path(root) / file
                if is_video_file(file_path):  # Check if the file is a video
                    video_file_paths.append(str(file_path))
                    video_file_names.append(file)

            if video_file_paths:
                # Obtain video durations in parallel
                durations = pool.map(get_video_duration, video_file_paths)
                for file_name, duration in zip(video_file_names, durations):
                    size_bytes = get_file_size(Path(root) / file_name)
                    folder_duration += duration
                    folder_size += size_bytes
                    folder_report.append(f"    {file_name} ({duration:.2f} minutes, {format_size(size_bytes)})")

            if folder_report:
                report.append(f"{relative_path}/")
                report.extend(folder_report)
                report.append(f"  Total duration in folder: {folder_duration:.2f} minutes, Total size: {format_size(folder_size)}\n")
            total_duration += folder_duration
            total_size += folder_size

    report.append(f"Total duration of all videos: {total_duration:.2f} minutes")
    report.append(f"Total size of all videos: {format_size(total_size)}\n")
    return "\n".join(report)

def format_report_to_markdown(report_str):
    """
    Converts the plain text report into Markdown format.
    Adds headers and converts items into lists.
    """
    lines = report_str.splitlines()
    md_lines = ["# Video Durations and Sizes Report", ""]
    for line in lines:
        if line.endswith("/") and not line.startswith("    "):
            # Header for folder
            folder_name = line.rstrip("/")
            md_lines.append(f"## {folder_name}/")
        elif line.startswith("    "):
            # File: convert to list item
            md_lines.append(f"- {line.strip()}")
        elif line.startswith("  Total duration in folder:"):
            md_lines.append(f"**{line.strip()}**")
        elif line.startswith("Total duration of all videos:") or line.startswith("Total size of all videos:"):
            md_lines.append(f"**{line.strip()}**")
        else:
            md_lines.append(line)
    return "\n".join(md_lines)

def main():
    parser = argparse.ArgumentParser(description="Scans a folder and calculates the duration and size of videos.")
    parser.add_argument("folder", type=str, help="Path to the folder to scan")
    parser.add_argument("--depth", type=int, default=2, help="Maximum depth to scan (default is 2)")
    # Option to export the report in Markdown format
    parser.add_argument("--output", nargs="?", const="", default=None,
                        help="Optional output file path for Markdown report. If provided without a filename, 'resume.md' will be created in the scanned folder.")
    args = parser.parse_args()

    folder_to_scan = args.folder
    depth = args.depth

    report = scan_folder(folder_to_scan, depth)

    if report:
        print("\n=== Video Durations and Sizes Report ===\n")
        print(report)

        # Markdown report export
        if args.output is not None:
            md_report = format_report_to_markdown(report)
            if args.output == "":
                output_md_path = Path(folder_to_scan) / "resume.md"
            else:
                output_md_path = Path(args.output)
            try:
                with open(output_md_path, "w", encoding="utf-8") as f:
                    f.write(md_report)
                print(f"Markdown report saved to {output_md_path}")
            except Exception as e:
                print(f"Error writing Markdown report: {e}")

if __name__ == "__main__":
    main()

# usage: python video_reporter.py "/path/to/videos_folder" --output --depth 2

import cv2
import subprocess
import tempfile
from functools import partial
import math
import os

def run_pipeline(pipeline, input_path, output_path):
    """
    Executes a pipeline of video processing functions.

    Parameters:
    - pipeline: List of partially applied functions that accept 'video_path' and 'output_path'.
    - input_path: Path to the input video file.
    - output_path: Path to save the final output video.
    """
    temp_files = []
    current_input = input_path

    for i, func in enumerate(pipeline):
        # Determine the output path for the current function
        if i == len(pipeline) - 1:
            # Last function in the pipeline; use the final output path
            current_output = output_path
        else:
            # Create a temporary file for intermediate output
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.mp4')
            current_output = temp_file.name
            temp_files.append(current_output)
            temp_file.close()

        # Call the function with the current input and output paths
        func(video_path=current_input, output_path=current_output)

        # Update the input path for the next function in the pipeline
        current_input = current_output

    # Clean up temporary files
    for temp_file in temp_files:
        if os.path.exists(temp_file):
            os.remove(temp_file)

    return output_path


def reencode_video(video_path, output_path):
    """
    Re-encodes a video using ffmpeg with specific encoding parameters.

    Parameters:
    - video_path: Path to the input video file.
    - output_path: Path to save the re-encoded video file.
    """
    ffmpeg_cmd = [
        'ffmpeg',
        '-y',  # Overwrite output files without asking
        '-i', video_path,
        '-c:v', 'libx264',
        '-pix_fmt', 'yuv420p',
        '-profile:v', 'baseline',
        '-level', '3.0',
        '-c:a', 'aac',
        '-b:a', '128k',
        output_path
    ]
    try:
        subprocess.run(ffmpeg_cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print(f"Video re-encoded successfully. Saved to {output_path}")
    except subprocess.CalledProcessError as e:
        print(f"Error during re-encoding: {e.stderr.decode('utf-8')}")

def video_to_gif(input_video_path, output_gif_path, start_time=None, end_time=None, resize_ratio=1.0, fps=None):
    """
    Converts a video file to a GIF.

    Parameters:
    - input_video_path: Path to the input video file.
    - output_gif_path: Path to save the output GIF file.
    - start_time: (Optional) Start time in seconds to begin the GIF.
    - end_time: (Optional) End time in seconds to end the GIF.
    - resize_ratio: (Optional) Ratio to resize the GIF (e.g., 0.5 for half size).
    - fps: (Optional) Frames per second for the GIF. Defaults to video FPS.
    """
    clip = VideoFileClip(input_video_path)

    # Trim the video clip if start_time and end_time are provided
    if start_time is not None and end_time is not None:
        clip = clip.subclip(start_time, end_time)

    # Resize the clip if resize_ratio is provided
    if resize_ratio != 1.0:
        clip = clip.resize(resize_ratio)

    # Set the frames per second if fps is provided
    if fps is not None:
        clip = clip.set_fps(fps)

    # Write the GIF to the output path
    clip.write_gif(output_gif_path)

    print(f"GIF has been saved to {output_gif_path}")

def dramatize_video_effect(video_path, a_time, b_time, output_path, slow_motion_speed=0.5):
    """
    Applies a dramatized effect to highlight a particular portion of the video.

    Parameters:
    - video_path: Path to the input video file.
    - a_time: Start time in seconds (a < b).
    - b_time: End time in seconds.
    - output_path: Path to the output video file.
    - slow_motion_speed: Speed factor for slow motion (e.g., 0.5 for half speed).
    """

    # Open the video file
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print("Error opening video file")
        return

    # Get video properties
    fps = cap.get(cv2.CAP_PROP_FPS)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    # Calculate the frame numbers corresponding to times a and b
    frame_a = int(a_time * fps)
    frame_b = int(b_time * fps)

    if frame_a < 0 or frame_b >= total_frames or frame_a >= frame_b:
        print("Invalid times provided.")
        cap.release()
        return

    # Prepare to write the output video
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    # Define the codec and create VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # You can use 'XVID' or 'MJPG' as well
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

    # Step 1: Read and write frames from 0 to frame_b (normal speed)
    cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
    current_frame = 0
    while current_frame <= frame_b:
        ret, frame = cap.read()
        if not ret:
            break
        out.write(frame)
        current_frame += 1

    # Step 2: Read frames from frame_a to frame_b (forward order), store in list
    frames_to_reverse = []
    cap.set(cv2.CAP_PROP_POS_FRAMES, frame_a)
    current_frame = frame_a
    while current_frame <= frame_b:
        ret, frame = cap.read()
        if not ret:
            break
        frames_to_reverse.append(frame)
        current_frame += 1

    # Step 3: Reverse the list
    frames_to_reverse.reverse()

    # Step 4: Write frames in slow motion (backward from b to a)
    slow_motion_factor = int(1 / slow_motion_speed)
    if slow_motion_factor < 1:
        slow_motion_factor = 1  # Ensure at least 1

    for frame in frames_to_reverse:
        for _ in range(slow_motion_factor):
            out.write(frame)

    # Step 5: Read and write frames from frame_a to end (normal speed)
    cap.set(cv2.CAP_PROP_POS_FRAMES, frame_a)
    current_frame = frame_a
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        out.write(frame)
        current_frame += 1

    # Release everything if job is finished
    cap.release()
    out.release()
    print("Video effect applied successfully. Saved to", output_path)

def reorder_video(video_path, start_time, output_path):
    # Open the video file
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print("Error opening video file")
        return

    # Get video properties
    fps = cap.get(cv2.CAP_PROP_FPS)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    # Calculate the frame number corresponding to start_time
    start_frame = int(start_time * fps) % total_frames

    # Prepare to write the output video
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    # Define the codec and create VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # You can use 'XVID' or 'MJPG' as well
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

    # First pass: Read from start_frame to end
    cap.set(cv2.CAP_PROP_POS_FRAMES, start_frame)
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        out.write(frame)

    # Second pass: Read from frame 0 to start_frame
    cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
    current_frame = 0
    while current_frame < start_frame:
        ret, frame = cap.read()
        if not ret:
            break
        out.write(frame)
        current_frame += 1

    # Release everything if job is finished
    cap.release()
    out.release()
    print("Video reordering complete. Saved to", output_path)

if __name__ == "__main__":
    # video_path = "basic_videos_for_website/img_007_012.mp4"  # Your input video file path
    # output_path = "final_output.mp4"                         # Desired output video file path
    # start_time = 3.0                                         # Start time for reorder_video
    # a_time = 0.0                                             # Start time for dramatize effect
    # b_time = 0.6                                             # End time for dramatize effect

    # # Create partial functions with the required additional parameters
    # pipeline = [
    #     partial(reorder_video, start_time=start_time),
    #     partial(dramatize_video_effect, a_time=a_time, b_time=b_time),
    #     reencode_video,
    # ]

    # # Run the pipeline
    # run_pipeline(pipeline, video_path, output_path)

    # print("Processing complete. Final video saved to", output_path)

    # video_path = "miniature_videos_laid_out/img_003_017.mp4"  # Your input video file path
    # output_path = "img_003_017.mp4"                         # Desired output video file path
    # start_time = 2.0                                         # Start time for reorder_video
    # a_time = 0.0                                             # Start time for dramatize effect
    # b_time = 0.6                                             # End time for dramatize effect

    # # Create partial functions with the required additional parameters
    # pipeline = [
    #     partial(reorder_video, start_time=start_time),
    #     partial(dramatize_video_effect, a_time=a_time, b_time=b_time),
    #     reencode_video,
    # ]

    # # Run the pipeline
    # run_pipeline(pipeline, video_path, output_path)

    # print("Processing complete. Final video saved to", output_path)
    
    # video_path = "basic_videos_for_website/img_009_015.mp4"  # Your input video file path
    # output_path = os.path.split(video_path)[1]
    # start_time = 2.5                                         # Start time for reorder_video
    # a_time = 0.0                                             # Start time for dramatize effect
    # b_time = 0.8                                             # End time for dramatize effect

    # # Create partial functions with the required additional parameters
    # pipeline = [
    #     partial(reorder_video, start_time=start_time),
    #     partial(dramatize_video_effect, a_time=a_time, b_time=b_time),
    #     reencode_video,
    # ]

    # # Run the pipeline
    # run_pipeline(pipeline, video_path, output_path)

    # print("Processing complete. Final video saved to", output_path)

    # video_path = "basic_female_out/img_002_005.mp4"  # Your input video file path
    # output_path = os.path.split(video_path)[1]
    # start_time = 2.5                                         # Start time for reorder_video
    # a_time = 0.0                                             # Start time for dramatize effect
    # b_time = 0.8                                             # End time for dramatize effect

    # # Create partial functions with the required additional parameters
    # pipeline = [
    #     partial(reorder_video, start_time=start_time),
    #     partial(dramatize_video_effect, a_time=a_time, b_time=b_time),
    #     reencode_video,
    # ]

    # # Run the pipeline
    # run_pipeline(pipeline, video_path, output_path)

    # print("Processing complete. Final video saved to", output_path)

    # video_path = "miniature_videos_laid_out/img_000_003.mp4"  # Your input video file path
    # output_path = os.path.split(video_path)[1]
    # start_time = 2.2
    # a_time = 0.0                                             # Start time for dramatize effect
    # b_time = 0.8                                             # End time for dramatize effect

    # # Create partial functions with the required additional parameters
    # pipeline = [
    #     partial(reorder_video, start_time=start_time),
    #     partial(dramatize_video_effect, a_time=a_time, b_time=b_time),
    #     reencode_video,
    # ]

    # # Run the pipeline
    # run_pipeline(pipeline, video_path, output_path)

    # print("Processing complete. Final video saved to", output_path)

    video_path = "rim_effects_out/videos/img_001_001.mp4"  # Your input video file path
    output_path = os.path.split(video_path)[1]
    start_time = 3.0
    a_time = 0.0                                             # Start time for dramatize effect
    b_time = 0.8                                             # End time for dramatize effect

    # Create partial functions with the required additional parameters
    pipeline = [
        partial(reorder_video, start_time=start_time),
        partial(dramatize_video_effect, a_time=a_time, b_time=b_time),
        reencode_video,
    ]

    # Run the pipeline
    run_pipeline(pipeline, video_path, output_path)

    print("Processing complete. Final video saved to", output_path)

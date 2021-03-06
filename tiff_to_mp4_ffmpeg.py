from tiff_handler import load_series, get_frame_rate, plot_framedrops, plot_frame_hist
import numpy as np
from pyhelper.progress_bar import Bar
import os

def fill_dropped_frames(timestamps, frames):
    intervals = np.diff(timestamps)
    min_interval = intervals.min()
    filled_frames = []
    filled_timestamps = []
    for i in range(len(frames) - 1):
        interval = intervals[i]
        for j in range(int(interval / min_interval)):
            filled_frames.append(frames[i].copy())
            filled_timestamps.append(timestamps[i] + j * min_interval)
    filled_frames.append(frames[-1].copy())
    filled_timestamps.append(timestamps[-1])
    return filled_timestamps, filled_frames


if __name__ == "__main__":
    file_type = "tiff"
    path = "data/old/image_2022-02-15T15-36-26.04_0.tif"
    # path = "data/image_2022-02-15T15-37-09.663_0.tif"
    # path = "data/image_2022-02-15T15-37-36.853_0.tif"
    # path = "data/old/image_2022-02-17T12-13-05.09_0.tif"
    timestamps, frames, x, y, _ = load_series(path, ax=None, return_frames=True)
    frame_rate = get_frame_rate(timestamps)
    timestamps, frames = fill_dropped_frames(timestamps, frames)

    # setup Progress Bar
    progress_bar = Bar(len(timestamps))

    print(f"loaded files with size {x[0]}x{y[0]}")
    print(f"{frame_rate=:.4f} s, time: {(len(frames) - 1) / frame_rate:.2f} s")
    interval = 1 / frame_rate * 1000
    try:
        dir = path.replace("data", "output").replace("_0.tif", "").replace("old/", "")
        os.mkdir(dir)
    except FileExistsError:
        pass
    filenames = []
    for i, frame in enumerate(frames):
        progress_bar.update(i)
        frame.save(f"{dir}/frame{i:04d}.{file_type}")
        filenames.append(f"frame{i:04d}.{file_type}")
    print("done saving frames")
    cmd = f'ffmpeg -r {frame_rate:.4f} -i {dir}/frame%04d.{file_type} -threads 4 -c:v libx264 -vf fps={frame_rate:.4f} -pix_fmt yuv420p {dir}.mp4'
    print("running ffmpeg")
    print(cmd)
    os.system(cmd)

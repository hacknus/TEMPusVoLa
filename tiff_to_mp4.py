from tiff_handler import open_tiff, get_frame_rate, plot_framedrops, plot_frame_hist
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import os


def load_series(path, return_frames=False):
    i = 0
    timestamps = []
    frames = []
    path_core = path[:33]
    print(path_core)
    while True:
        path = f"{path_core}_{i}.tif"
        i += 1
        if os.path.exists(path):
            timestamps_i, frames_i = open_tiff(path, return_frames)
            timestamps += timestamps_i
            frames += frames_i
        else:
            break
    return timestamps, frames


def fill_dropped_frames(timestamps, frames):
    intervals = np.diff(timestamps)
    min_interval = intervals.min()
    filled_frames = []
    filled_timestamps = []
    for i in range(len(frames) - 1):
        interval = intervals[i]
        for j in range(int(interval / min_interval)):
            filled_frames.append(frames[i])
            filled_timestamps.append(timestamps[i] + j * min_interval)
    filled_frames.append(frames[-1])
    filled_timestamps.append(timestamps[-1])
    return filled_timestamps, filled_frames


if __name__ == "__main__":
    fig = plt.figure()

    path = "data/image_2022-02-15T15-36-26.04_0.tif"
    timestamps, frames = load_series(path, True)
    frame_rate = get_frame_rate(timestamps)
    # timestamps, frames = fill_dropped_frames(timestamps, frames)
    print(f"{frame_rate=:.2f} s, time: {(len(timestamps) - 1) / frame_rate:.2f} s")

    interval = 1 / frame_rate * 1000
    print(frames)
    ani = animation.ArtistAnimation(fig, frames, interval=interval, blit=True, repeat_delay=1000)
    # save animation

    # needs ffmpeg to be installed
    mywriter = animation.FFMpegWriter(fps=frame_rate)
    print("saving mp4...")
    ani.save(f'output/test_file.mp4', writer=mywriter)

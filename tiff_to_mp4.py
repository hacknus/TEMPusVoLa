from tiff_handler import load_series, get_frame_rate, plot_framedrops, plot_frame_hist
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import os


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

    path = "data/image_2022-02-15T15-37-36.853_0.tif"
    timestamps, frames, _ = load_series(path, True)
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
    out_path = path.replace("data", "output").replace("tif","mp4")
    ani.save(out_path, writer=mywriter)

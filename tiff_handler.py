from PIL import Image, ImageSequence
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import os


def load_series(path, ax=None, return_frames=False):
    i = 0
    timestamps = []
    frames = []
    x = []
    y = []
    size = 0
    path_core = path.split('_')[0] + "_" + path.split('_')[1]
    print(path_core)
    while True:
        path = f"{path_core}_{i}.tif"
        i += 1
        if os.path.exists(path):
            print(f"opening {path=}")
            timestamps_i, frames_i, x_i, y_i = open_tiff(path, ax, return_frames)
            timestamps += timestamps_i
            frames += frames_i
            x += x_i
            y += y_i
            size += os.path.getsize(path)
        else:
            break
    return timestamps, frames, x, y, size


def open_tiff(path, ax=None, return_frames=False):
    tiff_img = Image.open(path)
    frames = []
    timestamps = []
    x = []
    y = []
    for i, page in enumerate(ImageSequence.Iterator(tiff_img)):
        if return_frames:
            if ax:
                im = ax.imshow(page, cmap="gray")
                frames.append([im])
            else:
                frames.append(page.copy())
        else:
            frames.append(None)
        # the timestamp entries to get a 64bit value in nano seconds
        timestamp = np.int64((np.int64(page.tag_v2[32781]) << 32) | page.tag_v2[32782])
        timestamps.append(timestamp)
        x.append(page.tag_v2[256])
        y.append(page.tag_v2[257])

        # print(f"reading {i} with size {page.tag_v2[256]} x {page.tag_v2[257]}")

    return timestamps, frames, x, y


def get_frame_rate(timestamps):
    interval = np.diff(timestamps).min() / 1000 / 1000 / 1000
    return 1 / interval


def plot_framedrops(timestamps, ax, color="black"):
    intervals = np.diff(timestamps) / 1000 / 1000 / 1000
    intervals = np.round(intervals, 4)
    frames = range(len(intervals))
    ax.step(frames, intervals, color=color, where='pre')
    ax.set_xlabel("frame")
    ax.set_ylabel(r"interval $\Delta t$")


def plot_frame_hist(timestamps, ax):
    intervals = np.diff(timestamps) / 1000 / 1000 / 1000
    intervals = np.round(intervals, 4)
    n, bins, patches = ax.hist(intervals, color="black")
    total_frames = np.sum(n) + np.sum(n[1:])
    print(f"frame drop: {np.sum(n[1:]) / total_frames * 100:.1f}%")
    ax.set_title(f"total frames: {len(intervals)}, dropped {np.sum(n[1:]) / total_frames * 100:.1f}%")
    ax.set_ylabel("frame number")
    print(bins)
    # ax.set_xticks([min(bins), max(bins)], ["frame on time", "frame delayed"])


if __name__ == "__main__":
    dpi = 1
    fig, ax = plt.subplots()

    path = "/Volumes/NO NAME/image_2022-02-17T14-55-13.447_0.tif"
    timestamps, frames, _, _, _ = load_series(path, ax, False)

    interval = np.diff(timestamps).mean() / 1000 / 1000 / 1000
    intervals = np.diff(timestamps) / 1000 / 1000 / 1000
    frame_rate = get_frame_rate(timestamps)

    print(f"detected a framerate of {1 / interval:.2f} fps")
    print(f"detected an interval of {1000 * interval:.2f} ms")
    print(f"{frame_rate=:.2f} s, time: {(len(timestamps) - 1) / frame_rate:.2f} s")

    # plot_framedrops(timestamps, ax)
    plot_frame_hist(timestamps, ax)
    plt.show()

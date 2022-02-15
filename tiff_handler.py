from PIL import Image, ImageSequence
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import os


def load_series(path, return_frames=False):
    i = 0
    timestamps = []
    frames = []
    sizes = []
    path_core = path.split('_')[0] + "_" + path.split('_')[1]
    print(path_core)
    while True:
        path = f"{path_core}_{i}.tif"
        i += 1
        if os.path.exists(path):
            timestamps_i, frames_i, sizes_i = open_tiff(path, return_frames)
            timestamps += timestamps_i
            frames += frames_i
            sizes += sizes_i
        else:
            break
    return timestamps, frames, sizes


def open_tiff(path, return_frames=False):
    tiff_img = Image.open(path)
    frames = []
    timestamps = []
    sizes = []
    for i, page in enumerate(ImageSequence.Iterator(tiff_img)):
        if return_frames:
            im = plt.imshow(page, cmap="gray")
            frames.append([im])
        else:
            frames.append(None)
        # two's complement of the timestamp entries to get a 64bit value in nano seconds
        timestamp = np.int64((np.int64(page.tag_v2[32781]) << 32) | page.tag_v2[32782])
        timestamps.append(timestamp)
        sizes.append(page.tag_v2[256] * page.tag_v2[257])
        print(f"reading {i} with size {page.tag_v2[256]} x {page.tag_v2[257]}")

    return timestamps, frames, sizes


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
    # fig = plt.figure()

    timestamps, frames = open_tiff("data/image_2022-02-14T11-35-14.018_0.tif", True)

    interval = np.diff(timestamps).mean() / 1000 / 1000 / 1000
    intervals = np.diff(timestamps) / 1000 / 1000 / 1000
    print(f"detected a framerate of {1 / interval:.2f} fps")
    print(f"detected a inverval of {1000 * interval:.2f} ms")
    frames = range(len(intervals))
    plt.step(frames, intervals, color="black", where='pre')
    plt.xlabel("frame")
    plt.ylabel(r"interval $\Delta t$")
    plt.savefig("interval.pdf")
    plt.show()

    n, bins, patches = plt.hist(intervals, color="black")
    total_frames = np.sum(n) + n[-1]
    print(f"frame drop: {n[-1] / total_frames * 100:.1f}%")
    plt.title(f"total frames: {len(intervals)}, dropped {n[-1] / total_frames * 100:.1f}%")
    plt.ylabel("frame number")
    plt.xticks([min(bins), max(bins)], ["frame on time", "frame delayed"])
    plt.savefig("hist.pdf")
    plt.show()

    exit()

    interval = 50
    fig = plt.figure()

    ani = animation.ArtistAnimation(fig, frames, interval=interval, blit=True, repeat_delay=1000)
    # save animation

    # needs ffmpeg to be installed
    mywriter = animation.FFMpegWriter(fps=24)
    print("saving mp4...")
    ani.save(f'test.mp4', savefig_kwargs={'facecolor': 'black'}, writer=mywriter, dpi=600)

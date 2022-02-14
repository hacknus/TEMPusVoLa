from PIL import Image, ImageSequence
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation


def open_tiff(path, return_ims=False):
    tiff_img = Image.open(path)
    ims = []
    timestamps = []
    for i, page in enumerate(ImageSequence.Iterator(tiff_img)):
        if return_ims:
            im = plt.imshow(page, cmap="gray")
            ims.append([im])
        # two's complement of the timestamp entries to get a 64bit value in nano seconds
        timestamp = np.int64((np.int64(page.tag_v2[32781]) << 32) | page.tag_v2[32782])
        timestamps.append(timestamp)
        print(f"reading {i}")
    if return_ims:
        return timestamps, ims
    else:
        return timestamps


if __name__ == "__main__":
    # fig = plt.figure()

    timestamps, ims = open_tiff("data/image_2022-02-04T14-46-57.899_7.tif", True)

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

    ani = animation.ArtistAnimation(fig, ims, interval=interval, blit=True, repeat_delay=1000)
    # save animation

    # needs ffmpeg to be installed
    mywriter = animation.FFMpegWriter(fps=24)
    print("saving mp4...")
    ani.save(f'test.mp4', savefig_kwargs={'facecolor': 'black'}, writer=mywriter, dpi=600)

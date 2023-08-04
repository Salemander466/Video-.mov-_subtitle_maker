import sched, time, os
from threading import Thread
from typing import Type

from input_handler.buffer import Buffer
from input_handler.drive.drive_downloader import download_file_from_google_drive
from input_handler.drive.drive_scraper import find_clips
from input_handler.json_transfer import load_root


''''''
def single_iter(root, buffer):

    ep_names = root.get_children_names
    print(ep_names)
    for ep_name in ep_names:
        episode_dir = root.get_directory(ep_name)
        if episode_dir.is_uploaded():
            continue

    all_clips = find_clips(root, [])

    buffer.add_clips(all_clips)

    print(buffer.clips)



def main():
    scheduler = sched.scheduler(time.monotonic(), time.sleep)
    buffer = Buffer()
    root = load_root()

    single_iter(root, buffer)

    # while True:
    #     scheduler.enter(10000, 1, single_iter(root, buffer))




if __name__ == "__main__":
    main()
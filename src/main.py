import sched, time, os
from threading import Thread
from typing import Type

from input_handler.buffer import Buffer
from input_handler.json_transfer import load_root, save_root

import nltk
import ssl

# try:
#     _create_unverified_https_context = ssl._create_unverified_context
# except AttributeError:
#     pass
# else:
#     ssl._create_default_https_context = _create_unverified_https_context





# set to the amount of hours to wait before upload
SCHEDULE_UPLOAD_TIME_HOURS = 4

'''
Input: root Directory of raw_files, buffer class
'''
def single_iter(root, buffer):

    ep_names = root.get_children_names()

    for ep_name in ep_names:
        ep_dir = root.get_directory(ep_name)
        if ep_dir.is_uploaded():
            continue

        all_ep_clips = ep_dir.find_clips([])

        # early return if there are clips in buffer
        if len(buffer.clips) != 0:
            buffer.upload_clip_youtube()
            return

        buffer.add_clips(all_ep_clips)





def main():
    scheduler = sched.scheduler(time.monotonic(), time.sleep)
    buffer = Buffer()
    root = load_root()

    single_iter(root, buffer)

    save_root(root)

    # while True:
    #     scheduler.enter(10000, 1, single_iter(root, buffer))


if __name__ == "__main__":
    main()

import sched, time, os
import threading
from threading import Thread
from typing import Type

from input_handler.buffer import Buffer
from input_handler.json_transfer import load_root, save_root
from root_generator import root_gen_loop

# set to the amount of hours to wait before upload
SCHEDULE_UPLOAD_TIME_HOURS = 4

'''
Input: root Directory of raw_files, buffer class
'''
def single_iter(root_lock, buffer):
    root_lock.acquire()

    root = load_root()

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

        # only executed if len(buffer.clips) == 0
        buffer.add_clips(all_ep_clips)


def test_schedule():
    print("10 seconds have passed!")

def test_main():
    pass

def main():
    # operations on the root directories must aquire the root_lock first
    root_lock = threading.Lock()
    # runs in background to append to the root variable.
    # root variable is shared
    check_root = threading.Thread(target=root_gen_loop, args=(root_lock,))
    check_root.start()

    upload_scheduler = sched.scheduler(time.monotonic, time.sleep)
    buffer = Buffer()
    root = load_root()

    first = True

    # change this to run without first variable later
    while True:
        if first:
            print(F'scheduling for 10 seconds')
            upload_scheduler.enter(10, 1, single_iter, argument=(root_lock, buffer,))
            upload_scheduler.run()
            first = False
        else:
            upload_scheduler.enter(60*60*3, 1, single_iter, argument=(root_lock, buffer,))
            upload_scheduler.run()










    # single_iter(root, buffer)
    # save_root(root)





    # while True:
    #     scheduler.enter(10000, 1, single_iter(root, buffer))


if __name__ == "__main__":
    main()

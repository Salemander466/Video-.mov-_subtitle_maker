import sched
import time

from input_handler.drive.drive_scraper import scan_main_directory



def root_gen_exec(update=True):
    scan_main_directory(update)



'''
Single iteration of scheduling a refresh for the root contents
'''


def root_gen_single_iter(root_lock):
    root_refresh = sched.scheduler(time.monotonic, time.sleep)
    # set the scheduler to one day
    root_refresh.enter(60 * 60 * 24, 1, scan_main_directory, argument=(root_lock,))
    root_refresh.run()


'''
This code should only be called from a non-main thread.
It will update the root directory with new episodes, if new episodes come out.
'''


def root_gen_loop(root_lock):

    while True:
        root_gen_single_iter(root_lock)


def main():
    pass



if __name__ == "__main__":
    # only call with False param if you want to reset all 'updated' attributes on clips
    root_gen_exec()

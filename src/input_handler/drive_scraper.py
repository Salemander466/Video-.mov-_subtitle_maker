import drive_downloader
import json

import google.auth
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from json_transfer import Clip
from json_transfer import Directory

from quickstart import quickstart









'''
TODO
Input: realative path of clipname
Output: processed clip name
'''
def process_clips(clip_id):
    pass








def download_video(file_id):
    ptr = drive_downloader.download_file(file_id)



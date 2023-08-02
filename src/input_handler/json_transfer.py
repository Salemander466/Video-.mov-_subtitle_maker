import drive_downloader
import json

import google.auth
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from quickstart import quickstart

raw_shorts = "1rgRvJf2qwDypmFaMa67s2405qyMbUe__"

video_formats = [".mov", ".mp4"]

'''
:return True if file is in a video format
'''


def is_video(filename):
    for format in video_formats:
        if filename.find(format) != -1:
            return True
    return False


class Directory:
    uploaded = False

    def __init__(self, id, name, directories=[], clips=[]):
        self.directories = directories
        self.clips = clips
        self.id = id
        self.name = name

    def add_dir(self, dir):
        self.directories.append(dir)

    def add_clip(self, clip):
        self.clips.append(clip)

    def set_uploaded(self, uploaded):
        self.uploaded = uploaded


class Clip:
    def __init__(self, id, name, edited=False, uploaded=False):
        self.id = id
        self.name = name
        self.edited = edited
        self.uploaded = uploaded

    def __str__(self):
        return F'("id": {self.id}, "name": {self.name}, "edited": {self.edited}, "uploaded": {self.uploaded})'

    def set_edited(self, edited):
        self.edited = edited

    def set_uploaded(self, uploaded):
        self.uploaded = uploaded


class DirectoryEncoder(json.JSONEncoder):
    def default(self, obj):

        if isinstance(obj, Directory):
            directories = obj.directories
            clips = obj.clips
            json_clips = []

            for clip in clips:
                json_clips.append(self.default(clip))

            if len(directories) == 0:
                return {"id": obj.id, "name": obj.name, "directories": [], "clips": json_clips}

            for directory in directories:
                return {"id": obj.id, "name": obj.name, "directories": [self.default(directory)], "clips": json_clips}

        if isinstance(obj, Clip):
            return {"id": obj.id, "name": obj.name, "edited": obj.edited, "uploaded": obj.uploaded}

        return super().default

class DirectoryDecoder:
    def default(self):
        pass



# class DirectoryDecoder(json.JSONDecoder):
#     def default(self, obj):
#         if isinstance(obj, Directory):
#             return {"id": obj.id, "name": obj.name}
#         return super().default


'''
TODO
Input: id of the folder to look into
Output: a list of clip ids inside the folder
'''


def find_clips(service, dir_list, video_ids):
    if len(dir_list) == 0:
        print("all videos found!")
        return video_ids

    page_token = None
    # pop from the dir stack
    dir_id = dir_list.pop(0)
    response = service.files().list(q=f"'{dir_id}' in parents",
                                    spaces='drive',
                                    fields='nextPageToken, '
                                           'files(id, name)',
                                    pageToken=page_token).execute()

    for file in response.get('files', []):
        filename = file.get("name")
        id = file.get("id")
        if is_video(filename):
            print("appending video")
            video_ids.append(id)
        else:
            print("appending dir")
            dir_list.append(id)

    # recursively call find_clips until all directories have been checked.
    return find_clips(service, dir_list, video_ids)


'''
one iteration of checking for new clips

Search file in drive location

Load pre-authorized user credentials from the environment.
TODO(developer) - See https://developers.google.com/identity
for guides on implementing OAuth2 for the application.
 
'''


def scan_main_directory():
    creds = quickstart.get_creds()



    try:
        # create drive api client
        service = build('drive', 'v3', credentials=creds)
        files = []
        page_token = None
        while True:
            # pylint: disable=maybe-no-member
            response = service.files().list(q=f"'{raw_shorts}' in parents",
                                            spaces='drive',
                                            fields='nextPageToken, '
                                                   'files(id, name)',
                                            pageToken=page_token).execute()

            for file in response.get('files', []):
                (id, name) = parse_raw_folder(file)
                # if id not in uploaded_videos:
                #     print(F'Found new clips: {file.get("name")}')
                #     print(F'Processing and uploading new file')
                #     # get all raw clips within a directory
                #     clip_ids = find_clips(service, [id], [])
                #     print(clip_ids)
                #     # processed_clip_ids = process_clips(clips)

            files.extend(response.get('files', []))
            page_token = response.get('nextPageToken', None)
            if page_token is None:
                break

    except HttpError as error:
        print(F'An error occurred: {error}')
        files = None

    return files



'''
input: file
output: (id, name) touple
'''


def parse_raw_folder(folder):
    name = folder.get("name")
    id = folder.get("id")
    return (id, name)


def test_dir():
    dir = Directory("123", "nametop", [Directory("", "", [], []), Directory("", "", [], [])],
                    [Clip("", "", False, False)])

    fp = open("root.json", "w")
    json.dump(dir, fp, cls=DirectoryEncoder)
    fp.close()





def test_load():
    fp = open("root.json", "r")
    json.load(dir, fp, cls=DirectoryDecoder)
    fp.close()


if __name__ == "__main__":
    test_dir()
    test_load()


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



'''
TODO
Input: id of the folder to look into
Output: a list of clip ids inside the folder
'''
def find_clips(service, dir_list, video_ids):
    if len(dir_list) == 0:
        return video_ids

    page_token = None
    dir_id = dir_list.pop(0) # pop from the dir stack
    response = service.files().list(q=f"'{dir_id}' in parents",
                        spaces='drive',
                        fields='nextPageToken, '
                        'files(id, name)',
                        pageToken=page_token).execute()


    for file in response.get('files', []):
        filename = file.get("name")
        id = file.get("id")
        if is_video(filename):
            video_ids.append(id)
        else:
            dir_list.append(id)
    find_clips(service, dir_list, video_ids)






'''
TODO
Input: realative path of clipname
Output: processed clip name
'''
def process_clips(clip_id):
    pass

'''
one iteration of checking for new clips
'''
def search_file():
    """Search file in drive location

    Load pre-authorized user credentials from the environment.
    TODO(developer) - See https://developers.google.com/identity
    for guides on implementing OAuth2 for the application.
    """
    creds = quickstart.get_creds()

    uploaded_videos = get_uploaded_videos()

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
                if id not in uploaded_videos:
                    print(F'Found new clips: {file.get("name")}')
                    print(F'Processing and uploading new file')
                    clip_ids = find_clips(service, id)
                    # processed_clip_ids = process_clips(clips)


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

def get_uploaded_videos():
    f = open("uploaded_clips.txt", "r")
    ids = []
    has_content = True

    while has_content:
        line = f.readline()
        if line != "":
            ids.append(line)
        else:
            has_content = False


    f.close()
    return ids



def add_upload_id(id):
    f = open("uploaded_clips.txt", "a")
    f.write(id+"\n")
    f.close()



def download_video(file_id):
    ptr = drive_downloader.download_file(file_id)


if __name__ == '__main__':
    search_file()

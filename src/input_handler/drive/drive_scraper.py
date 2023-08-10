from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from input_handler.directory import Directory, Clip
from input_handler.json_transfer import save_root, load_root
from quickstart import quickstart

video_formats = [".mov", ".mp4"]
raw_shorts = "1rgRvJf2qwDypmFaMa67s2405qyMbUe__"

'''
:return True if file is in a video format
'''


def is_video(filename):
    for format in video_formats:
        if filename.find(format) != -1:
            return True
    return False







# '''
# Input: id of the folder to look into
# Output: a list of clip ids inside the folder
# '''
# def find_clips(service, dir_list, clips):
#     if len(dir_list) == 0:
#         print("all videos found!")
#         return clips
#
#     page_token = None
#     # pop from the dir stack
#     dir_id = dir_list.pop(0)
#     response = service.files().list(q=f"'{dir_id}' in parents",
#                                     spaces='drive',
#                                     fields='nextPageToken, '
#                                            'files(id, name)',
#                                     pageToken=page_token).execute()
#
#     for file in response.get('files', []):
#         filename = file.get("name")
#         id = file.get("id")
#         if is_video(filename):
#             print("appending video")
#             clips.append(Clip(id, filename))
#         else:
#             print("appending dir")
#             dir_list.append(id)
#
#     # recursively call find_clips until all directories have been checked.
#     return find_clips(service, dir_list, clips)


'''TODO'''
def is_new_episodes(files):
    names = []
    for file in files:
        name = file.get("name")
        names.append(name)


'''
one iteration of checking for new clips

Search file in drive location

Load pre-authorized user credentials from the environment.
TODO(developer) - See https://developers.google.com/identity
for guides on implementing OAuth2 for the application.

'''
def generate_tree(parent, files, service):
    page_token = None
    if len(files) == 0:
        return parent
    for file in files:
        (id, name) = parse_raw_folder(file)
        if is_video(name):
            clip = Clip(id, name, False, False)
            parent.add_clip(clip)
        else:
            dir = Directory(id, name, [], [])
            response = service.files().list(q=f"'{id}' in parents",
                                            spaces='drive',
                                            fields='nextPageToken, '
                                                   'files(id, name)',
                                            pageToken=page_token).execute()
            to_add = generate_tree(dir, response.get('files', []), service)

            parent.add_dir(to_add)
    return parent




def get_root():
    root = load_root()
    root.directories

def scan_main_directory():
    creds = quickstart.get_creds()

    try:
        root = Directory(raw_shorts, "root", [], [])
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

            # Check all the files within raw shorts
            is_new_episodes(response.get('files', []))
            tree = generate_tree(root, response.get('files', []), service)
            save_root(tree)

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

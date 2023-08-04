from input_handler.drive.drive_downloader import download_file_from_google_drive


import os

# from uploaders.youtube.youtube_uploader import start_upload


class Buffer:
    def __init__(self, clips=[]):
        self.clips = clips

    def add_clip(self, clip):
        self.clips.append(clip)

    def add_clips(self, clips):
        self.clips.extend(clips)

    def upload_clip_youtube(self):
        if len(self.clips) == 0:
            return

        clip = self.clips.pop(0)

        # if already uploaded, upload the next one in queue.
        if clip.youtube:
            self.upload_clip_youtube()

        download_file_from_google_drive(clip.id, "raw_clip.mov")
        clip_path = os.path + "raw_clip.mov"
        print("Editing & Uploading: " + clip_path)
        # start_upload(clip_path)
        # set uploaded status to true
        clip.youtube = True

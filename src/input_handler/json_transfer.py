import json

from input_handler.directory import Directory, Clip


class DirectoryEncoder(json.JSONEncoder):
    def default(self, obj):

        if isinstance(obj, Directory):
            directories = obj.directories
            clips = obj.clips
            json_clips = []
            json_dirs = []

            for clip in clips:
                json_clips.append(self.default(clip))

            if len(directories) == 0:
                return {"id": obj.id, "name": obj.name, "directories": [], "clips": json_clips}

            for directory in directories:
                json_dirs.append(self.default(directory))
            return {"id": obj.id, "name": obj.name, "directories": json_dirs, "clips": json_clips}

        if isinstance(obj, Clip):
            return {"id": obj.id, "name": obj.name, "edited": obj.edited, "uploaded": obj.uploaded}

        return super().default


class DirectoryDecoder(json.JSONDecoder):
    def __init__(self, *args, **kwargs):
        json.JSONDecoder.__init__(self, object_hook=self.object_hook, *args, **kwargs)

    def object_hook(self, obj):

        keys = list(obj.keys())
        # if it is a directory return a directory class
        if "directories" in keys:
            directories = obj.get("directories")
            clips = obj.get("clips")
            obj_clips = []

            for clip in clips:
                obj_clips.append(Clip(clip.get("id"), clip.get("name"), clip.get("edited"), clip.get("uploaded")))

            if len(directories) == 0:
                return Directory(obj.get("id"), obj.get("name"), [], obj_clips)

            return Directory(obj.get("id"), obj.get("name"), directories, obj_clips)
        return obj


def save_root(root):
    fp = open("root.json", "w")
    json.dump(root, fp, cls=DirectoryEncoder)
    fp.close()


def load_root():
    fp = open("root.json", "r")
    root = json.load(fp, cls=DirectoryDecoder)
    fp.close()
    return root

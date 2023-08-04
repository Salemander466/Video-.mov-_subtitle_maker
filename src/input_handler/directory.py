class Directory:
    uploaded = False

    def __init__(self, id, name, directories=[], clips=[]):
        self.id = id
        self.name = name
        self.directories = directories
        self.clips = clips

    def __repr__(self):
        return F'name: {self.name} \nclips: {self.clips} \nlist:{self.directories}\n'

    def get_children_names(self):
        names = []
        for directory in self.directories:
            names.append(directory.name)
        return names

    def add_dir(self, dir):
        self.directories.append(dir)

    def add_clip(self, clip):
        self.clips.append(clip)

    def get_directory(self, name):
        directories = self.directories
        if len(self.directories) == 0:
            return None
        for directory in directories:
            if directory.name == name:
                return directory
        return None

    def is_uploaded(self):
        for clip in self.clips:
            if clip is not clip.uploaded:
                return False

        if len(self.directories) == 0:
            return True

        for directory in self.directories:
            return directory.is_uploaded()


class Clip:

    def __init__(self, id, name, youtube=False, instagram=False):
        self.id = id
        self.name = name
        self.youtube = youtube
        self.instagram = instagram

    def __repr__(self):
        return F'name: {self.name} id:({self.id}) '

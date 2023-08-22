class Directory:
    uploaded = False

    def __init__(self, id, name, directories=[], clips=[]):
        self.id = id
        self.name = name
        self.directories = directories
        self.clips = clips


    def __repr__(self):
        return F'name: {self.name} \nclips: {self.clips} \nlist:{self.directories}\n'

    def find_clips(self, all_clips):
        clips = self.clips
        directories = self.directories

        if len(clips) != 0:
            all_clips.extend(clips)

        if len(directories) == 0:
            return all_clips

        for directory in directories:
            all_clips.extend(directory.find_clips(all_clips))
        return all_clips

    def get_children_names(self):
        names = []
        for directory in self.directories:
            name = directory.name
            names.append(name)
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
            if clip is not clip.youtube:
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

"""A video playlist class."""


class Playlist:
    """A class used to represent a Playlist."""

    def __init__(self):
        self._user_playlist = {}

    """Creates the key value pair in the dictionary """

    def create_internal_playlist(self, user_input):
        self._user_playlist[user_input] = []

    """Checks if the playlist exists"""

    def check_existing_playlist(self, user_input):
        does_playlist_exist = user_input.lower()
        if does_playlist_exist in self._user_playlist.keys():
            return True
        return False

    """Checks if the video inside a playlist exists"""

    def check_existing_video(self, playlist_name, user_input):
        video = user_input.lower()
        playlist = playlist_name.lower()
        if video in self._user_playlist.get(playlist):
            return True
        return False

    """Adds a video to the specified playlist"""

    def add_to_playlist(self, playlist_name, user_input):
        video = user_input.lower()
        playlist = playlist_name.lower()
        self._user_playlist.get(playlist).append(video)

    """Returns a specific playlist"""

    def get_playlist(self, user_input):
        playlist_name = user_input.lower()
        return self._user_playlist.get(playlist_name)

    """Removes a playlist"""

    def remove_video_from_playlist(self, playlist_name, video_id):
        playlist = playlist_name.lower()
        remove_from_playlist = self._user_playlist.get(playlist)
        remove_from_playlist.remove(video_id)

    """Checks if a playlist is empty, this is not covered in the test cases"""

    def empty_playlist(self, playlist_name):
        playlist = self._user_playlist.get(playlist_name.lower())
        if len(playlist) == 0:
            return True
        return False

    """Clears an existing playlist"""

    def clear_playlist(self, playlist_name):
        playlist = self._user_playlist.get(playlist_name.lower())
        playlist.clear()

    """Deletes an existing playlist"""

    def delete_playlist(self, playlist_name):
        self._user_playlist.pop(playlist_name.lower())

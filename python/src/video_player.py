"""A video player class."""

from .video_library import VideoLibrary
from .video_playlist import Playlist
import random


class VideoPlayer:
    """A class used to represent a Video Player."""

    def __init__(self):
        self._video_library = VideoLibrary()
        self._playing_currently = []
        self.paused = False
        self._playlist = Playlist()
        self._raw_playlist = []
        self._flagged = {}

    def number_of_videos(self):
        num_videos = len(self._video_library.get_all_videos())
        print(f"{num_videos} videos in the library")

    """Helper functions"""

    def format_tags(self, tags):
        tagstr = ""
        if not tags:
            return []
        for tag in tags:
            if tag != tags[-1]:
                tagstr += tag + " "
            else:
                tagstr += tag
        return "[" + tagstr + "]"

    def format_videos(self, video_id):
        video = self._video_library.get_video(video_id)
        tags = self.format_tags(video.tags)
        print(f"{video.title} ({video.video_id}) {tags}")

    def valid_video_id(self, video_id):
        all_video_ids = [
            video.video_id for video in self._video_library.get_all_videos()]
        if video_id in all_video_ids:
            return True
        return False

    def is_video_playing(self):
        if len(self._playing_currently) != 0:
            return True
        return False

    def get_all_video_titles(self):
        all_video_titles = [
            video.title for video in self._video_library.get_all_videos()]
        return all_video_titles

    def get_video_title_from_id(self, video_id):
        return self._video_library.get_video(video_id).title

    def does_word_exists(self, st, word):
        new_str = st.lower()
        new_word = word.lower()
        # return f' {new_word} ' in f' {new_str} '
        if new_word in new_str:
            return True
        return False

    def does_tag_exists(self, lst, tag):
        new_tag = tag.lower()
        # return f' {new_word} ' in f' {new_str} '
        new_str = ''.join(lst).lower()
        if new_tag in new_str:
            return True
        return False

    def is_flagged(self, video_id):
        if video_id in self._flagged.keys():
            return True
        return False

    def get_current_playing_video(self):
        return self._playing_currently[0]

    """End of helper functions"""

    """Part 1"""

    def show_all_videos(self):
        """Returns all videos."""
        all_videos = self._video_library.get_all_videos()
        all_videos = sorted(all_videos, key=lambda v: (v.title))
        print("Here's a list of all available videos:")
        for video in all_videos:
            if self.is_flagged(video.video_id):
                tags = self.format_tags(video.tags)
                reason = self._flagged.get(video.video_id)
                print(
                    f"{video.title} ({video.video_id}) {tags} - FLAGGED (reason: {reason})")
            else:
                self.format_videos(video.video_id)

    def play_video(self, video_id):
        """Plays the respective video.

        Args:
            video_id: The video_id to be played.
        """
        if self.is_flagged(video_id):
            reason = self._flagged.get(video_id)
            print(
                f"Cannot play video: Video is currently flagged (reason: {reason})")
            return

        if not self.valid_video_id(video_id):
            print("Cannot play video: Video does not exist")
            return

        current_video = self._video_library.get_video(video_id)
        self.paused = False

        if self.is_video_playing():
            self.stop_video()
            self._playing_currently.append(current_video)
            print(f"Playing video: {current_video.title}")
        else:
            self._playing_currently.append(current_video)
            print(f"Playing video: {current_video.title}")

    def stop_video(self):
        """Stops the current video."""
        if self.is_video_playing():
            current_video = self._playing_currently.pop()
            self.paused = False
            print(f"Stopping video: {current_video.title}")
        else:
            print("Cannot stop video: No video is currently playing")

    def play_random_video(self):
        """Plays a random video from the video library."""
        random_video = random.choice(self._video_library.get_all_videos())
        if len(self._video_library.get_all_videos()) == len(self._flagged.keys()):
            print("No videos available")
            return

        self.play_video(random_video.video_id)

    def pause_video(self):
        """Pauses the current video."""
        if not self.is_video_playing():
            print("Cannot pause video: No video is currently playing")
            return

        if not self.paused:
            print(f"Pausing video: {self._playing_currently[0].title}")
            self.paused = True
            return
        else:
            print(f"Video already paused: {self._playing_currently[0].title}")

    def continue_video(self):
        """Resumes playing the current video."""
        if not self.is_video_playing():
            print("Cannot continue video: No video is currently playing")
            return
        if self.paused:
            print(f"Continuing video: {self._playing_currently[0].title}")
        else:
            print("Cannot continue video: Video is not paused")

    def show_playing(self):
        """Displays video currently playing."""
        if not self.is_video_playing():
            print("No video is currently playing")
            return
        current_video = self._playing_currently[0]
        tags = self.format_tags(current_video.tags)
        if self.paused:
            print(
                f"Currently playing: {current_video.title} ({current_video.video_id}) {tags} - PAUSED")
        else:
            print(
                f"Currently playing: {current_video.title} ({current_video.video_id}) {tags}")

    """End of part 1"""

    """Part 2"""

    def create_playlist(self, playlist_name):
        """Creates a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """
        user_input = playlist_name
        stored_playlist = playlist_name.lower()
        if self._playlist.check_existing_playlist(stored_playlist):
            print("Cannot create playlist: A playlist with the same name already exists")
        else:
            self._raw_playlist.append(user_input)
            self._playlist.create_internal_playlist(stored_playlist)
            print(f"Successfully created new playlist: {user_input}")

    def add_to_playlist(self, playlist_name, video_id):
        """Adds a video to a playlist with a given name.

        Args:
            playlist_name: The playlist name.
            video_id: The video_id to be added.
        """
        if self.is_flagged(video_id):
            reason = self._flagged.get(video_id)
            print(
                f"Cannot add video to {playlist_name}: Video is currently flagged (reason: {reason})")
            return

        if not self._playlist.check_existing_playlist(playlist_name):
            print(
                f"Cannot add video to {playlist_name}: Playlist does not exist")
            return
        if not self.valid_video_id(video_id):
            print(f"Cannot add video to {playlist_name}: Video does not exist")
            return
        if self._playlist.check_existing_video(playlist_name, video_id):
            print(f"Cannot add video to {playlist_name}: Video already added")
            return

        self._playlist.add_to_playlist(playlist_name, video_id)
        title = self.get_video_title_from_id(video_id)

        print(f"Added video to {playlist_name}: {title}")
        return

    def show_all_playlists(self):
        """Display all playlists."""

        if len(self._raw_playlist) == 0:
            print("No playlists exist yet")
            return
        print("Showing all playlists:")
        sorted_playlist = sorted(self._raw_playlist, key=lambda x: x[0])
        for playlist in sorted_playlist:
            print(playlist)

    def show_playlist(self, playlist_name):
        """Display all videos in a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """
        if not self._playlist.check_existing_playlist(playlist_name):
            print(
                f"Cannot show playlist {playlist_name}: Playlist does not exist")
            return
        playlist = self._playlist.get_playlist(playlist_name)
        print(f"Showing playlist: {playlist_name}")
        if len(playlist) == 0:
            print("No videos here yet")
            return
        for pl in playlist:
            if self.is_flagged(pl):
                video = self._video_library.get_video(pl)
                tags = self.format_tags(video.tags)
                reason = self._flagged.get(pl)
                print(
                    f"{video.title} ({pl}) {tags} - FLAGGED (reason: {reason})")
            else:
                self.format_videos(pl)
        return

    def remove_from_playlist(self, playlist_name, video_id):
        """Removes a video to a playlist with a given name.

        Args:
            playlist_name: The playlist name.
            video_id: The video_id to be removed.
        """
        if not self._playlist.check_existing_playlist(playlist_name):
            print(
                f"Cannot remove video from {playlist_name}: Playlist does not exist")
            return
        if not self.valid_video_id(video_id):
            print(
                f"Cannot remove video from {playlist_name}: Video does not exist")
            return
        if not self._playlist.check_existing_video(playlist_name, video_id):
            print(
                f"Cannot remove video from {playlist_name}: Video is not in playlist")
            return
        video_title = self.get_video_title_from_id(video_id)
        self._playlist.remove_video_from_playlist(playlist_name, video_id)
        print(f"Removed video from {playlist_name}: {video_title}")
        return

    def clear_playlist(self, playlist_name):
        """Removes all videos from a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """
        if not self._playlist.check_existing_playlist(playlist_name):
            print(
                f"Cannot clear playlist {playlist_name}: Playlist does not exist")
            return
        # Checks if the playlist has already been cleared, this is not present in the test cases :)
        if self._playlist.empty_playlist(playlist_name):
            print(f"Cannot clear {playlist_name}: Playlist is empty")

        else:
            self._playlist.clear_playlist(playlist_name)
            print(f"Successfully removed all videos from {playlist_name}")

    def delete_playlist(self, playlist_name):
        """Deletes a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """
        if self._playlist.check_existing_playlist(playlist_name):
            self._playlist.delete_playlist(playlist_name)
            print(f"Deleted playlist: {playlist_name}")
        else:
            print(
                f"Cannot delete playlist {playlist_name}: Playlist does not exist")

    """End of part 2"""

    """Part 3"""

    def search_videos(self, search_term):
        """Display all the videos whose titles contain the search_term.

        Args:
            search_term: The query to be used in search.
        """
        all_videos = self._video_library.get_all_videos()
        all_videos = sorted(all_videos, key=lambda v: v.title)
        valid_results = []
        potential_output = []
        i = 1
        for video in all_videos:
            if self.does_word_exists(video.title, search_term):
                if not self.is_flagged(video.video_id):
                    valid_results.append(video)
                    potential_output.append((i, video.video_id))
                    i += 1

        if len(valid_results) == 0:
            print(f"No search results for {search_term}")
            return

        print(f"Here are the results for {search_term}:")
        for i, res in enumerate(valid_results, 1):
            tags = self.format_tags(res.tags)
            video_res = f"{res.title} ({res.video_id}) {tags}"
            print(str(i) + ") " + video_res)

        print("Would you like to play any of the above? If yes, specify the number of the video.")
        print("If your answer is not a valid number, we will assume it's a no.")
        command = input()

        try:
            cmd = int(command)
        except ValueError:
            return

        res_video = ""

        for video in potential_output:
            if video[0] == cmd:
                res_video = video[1]

        if len(res_video) != 0:
            self.play_video(res_video)
            return

    def search_videos_tag(self, video_tag):
        """Display all videos whose tags contains the provided tag.

        Args:
            video_tag: The video tag to be used in search.
        """
        all_videos = self._video_library.get_all_videos()
        all_videos = sorted(all_videos, key=lambda v: v.title)
        valid_results = []
        potential_output = []
        i = 1
        for video in all_videos:
            if self.does_tag_exists(video.tags, video_tag):
                if not self.is_flagged(video.video_id):
                    valid_results.append(video)
                    potential_output.append((i, video.video_id))
                    i += 1
        if len(valid_results) == 0:
            print(f"No search results for {video_tag}")
            return

        print(f"Here are the results for {video_tag}:")
        for i, res in enumerate(valid_results, 1):
            tags = self.format_tags(res.tags)
            video_res = f"{res.title} ({res.video_id}) {tags}"
            print(str(i) + ") " + video_res)

        print("Would you like to play any of the above? If yes, specify the number of the video.")
        print("If your answer is not a valid number, we will assume it's a no.")
        command = input()

        try:
            cmd = int(command)
        except ValueError:
            return

        res_video = ""

        for video in potential_output:
            if video[0] == cmd:
                res_video = video[1]

        if len(res_video) != 0:
            self.play_video(res_video)
            return

    """End of part 3"""

    """Part 4"""

    def flag_video(self, video_id, flag_reason=""):
        """Mark a video as flagged.

        Args:
            video_id: The video_id to be flagged.
            flag_reason: Reason for flagging the video.
        """
        if not self.valid_video_id(video_id):
            print("Cannot flag video: Video does not exist")
            return

        if self.is_flagged(video_id):
            print("Cannot flag video: Video is already flagged")
            return

        if self.is_video_playing() and self.get_current_playing_video().video_id == video_id:
            self.stop_video()

        title = self.get_video_title_from_id(video_id)
        if flag_reason != "":
            self._flagged[video_id] = flag_reason
            print(
                f"Successfully flagged video: {title} (reason: {flag_reason})")
        else:
            self._flagged[video_id] = "Not supplied"
            print(
                f"Successfully flagged video: {title} (reason: Not supplied)")

    def allow_video(self, video_id):
        """Removes a flag from a video.

        Args:
            video_id: The video_id to be allowed again.
        """
        if not self.valid_video_id(video_id):
            print("Cannot remove flag from video: Video does not exist")
            return

        if self.is_flagged(video_id):
            self._flagged.pop(video_id)
            video = self.get_video_title_from_id(video_id)
            print(f"Successfully removed flag from video: {video}")
        else:
            print("Cannot remove flag from video: Video is not flagged")

    """End of part 4"""

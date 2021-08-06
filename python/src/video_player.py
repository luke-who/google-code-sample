"""A video player class."""

from .video_library import VideoLibrary
from .video_playlist import Playlist
import ast
import random

class VideoPlayer:
    """A class used to represent a Video Player."""

    def __init__(self):
        self._video_library = VideoLibrary()
        self._num_videos = len(self._video_library.get_all_videos())
        self.video_ids = [video._video_id for video in self._video_library.get_all_videos()]
        self._currently_playing = None
        self._pause = False
        self._playlist = {}
    def number_of_videos(self):
        print(f"{self._num_videos} videos in the library")

    def videos(self):
        """Returns all videos in a list."""
        videos = []
        for video in self._video_library.get_all_videos():
            tags = list(video._tags)
            tags = str(tags).replace(',','').replace('\'','')
            if video._flagged == True:
                videos.append(f"{video._title} ({video._video_id}) {tags} - FLAGGED (reason: {video._flagged_reason})")
            else:
                videos.append(f"{video._title} ({video._video_id}) {tags}")
        return videos

    def show_all_videos(self):
        """Returns all videos."""
        videos = self.videos()
        videos.sort()
        print(f"Here's a list of all available videos: ")
        for video in videos:
            print("\t",video)
        

    def play_video(self, video_id):
        """Plays the respective video.

        Args:
            video_id: The video_id to be played.
        """ 
        video_id_exist = sum([video_id==id for id in self.video_ids])

        if video_id_exist != 1:
            print("Cannot play video: Video does not exist")
        else:
            if self._video_library.get_video(video_id)._flagged == True:
                print(f"Cannot play video: Video is currently flagged (reason: {self._video_library.get_video(video_id)._flagged_reason})")
            else:
                if self._currently_playing == None:     
                    self._currently_playing = video_id
                    print("Playing video:",self._video_library.get_video(self._currently_playing)._title)
                else:
                    self.stop_video()
                    self._currently_playing = video_id
                    print("Playing video:",self._video_library.get_video(self._currently_playing)._title)
                self._pause = False

    def stop_video(self):
        """Stops the current video."""
        if self._currently_playing == None:
            print("Cannot stop video: No video is currently playing")
        else:
            print("Stopping video:",self._video_library.get_video(self._currently_playing)._title)
            self._currently_playing = None
            self._pause = True

    def play_random_video(self):
        """Plays a random video from the video library."""
        if self._num_videos == 0:
            print("No videos available")
        else:
            unflagged_video_ids = []
            for video_id in self.video_ids:
                if self._video_library.get_video(video_id)._flagged == True:
                    pass
                else:
                    unflagged_video_ids.append(video_id)
            if len(unflagged_video_ids) != 0:
                random_video_id = random.choice(unflagged_video_ids)
                self.play_video(random_video_id)
            else:
                print("No videos available")

    def pause_video(self):
        """Pauses the current video."""
        if self._currently_playing == None:
            print("Cannot pause video: No video is currently playing")
        else:
            if self._pause == True:
                print("Video already paused:",self._video_library.get_video(self._currently_playing)._title)
            else:
                self._pause = True
                print("Pausing video:",self._video_library.get_video(self._currently_playing)._title)

    def continue_video(self):
        """Resumes playing the current video."""
        if self._currently_playing == None:
            print("Cannot continue video: No video is currently playing")
        else:
            if self._pause == True:
                self._pause = False
                print("Continuing video:",self._video_library.get_video(self._currently_playing)._title)
            else:
                print("Cannot continue video: Video is not paused")

    def show_playing(self):
        """Displays video currently playing."""
        if self._currently_playing == None:
            print("No video is currently playing")
        else:
            videos = self.videos()
            id_index = self.video_ids.index(self._currently_playing)
            video = videos[id_index]
            if self._pause == True:
                print("Currently playing:",video,"- PAUSED")
            else:
                print("Currently playing:",video)

    def create_playlist(self, playlist_name):
        """Creates a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """
        if len(self._playlist) == 0:
            playlist = Playlist()
            playlist.playlist_name = playlist_name
            self._playlist[playlist_name.lower()] = playlist
            print(f"Successfully created new playlist: {playlist_name}")
        else:
            playlist_exist = sum([playlist_name.lower() == playlist_n.lower() for playlist_n,Playlist in self._playlist.items()])
            if playlist_exist == 1:
                print("Cannot create playlist: A playlist with the same name already exists")
            else:
                playlist = Playlist()
                playlist.playlist_name = playlist_name
                self._playlist[playlist_name.lower()] = playlist
                print(f"Successfully created new playlist: {playlist_name}")

    def add_to_playlist(self, playlist_name, video_id):
        """Adds a video to a playlist with a given name.

        Args:
            playlist_name: The playlist name.
            video_id: The video_id to be added.
        """
        playlist_exist = sum([playlist_name.lower() == playlist_n.lower() for playlist_n,Playlist in self._playlist.items()])
        if playlist_exist == 0:
            print(f"Cannot add video to {playlist_name}: Playlist does not exist")
        else:
            video_id_exist = sum([video_id==id for id in self.video_ids])
            if video_id_exist == 0:
                print(f"Cannot add video to {playlist_name}: Video does not exist")
            else:
                if self._video_library.get_video(video_id)._flagged == True:
                    print(f"Cannot add video to {playlist_name}: Video is currently flagged (reason: {self._video_library.get_video(video_id)._flagged_reason})")
                else:
                    video_added = sum([video_id==id for id in self._playlist[playlist_name.lower()].playlist_video_ids])
                    if video_added == 1:
                        print(f"Cannot add video to {playlist_name}: Video already added")
                    else:
                        self._playlist[playlist_name.lower()].playlist_video_ids.append(video_id)
                        print(f"Added video to {playlist_name}: {self._video_library.get_video(video_id)._title}")

    def show_all_playlists(self):
        """Display all playlists."""
        if len(self._playlist) == 0:
            print("No playlists exist yet")
        else:
            playlist = [Playlist.playlist_name for Playlist in self._playlist.values()]
            playlist.sort()
            print("Showing all playlists:")
            for p in playlist:
                print("  {}".format(p))

    def show_playlist(self, playlist_name):
        """Display all videos in a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """
        playlist_exist = sum([playlist_name.lower() == playlist_n.lower() for playlist_n,Playlist in self._playlist.items()])
        if playlist_exist == 1:
            print("Showing playlist: {}".format(playlist_name))
            if len(self._playlist[playlist_name.lower()].playlist_video_ids) == 0:
                print("  No videos here yet")
            else:
                videos = self.videos()
                for video_id in self._playlist[playlist_name.lower()].playlist_video_ids:
                    id_index = self.video_ids.index(video_id)
                    video = videos[id_index]
                    print(f"  {video}")
        else:
            print(f"Cannot show playlist {playlist_name}: Playlist does not exist")

    def remove_from_playlist(self, playlist_name, video_id):
        """Removes a video to a playlist with a given name.

        Args:
            playlist_name: The playlist name.
            video_id: The video_id to be removed.
        """        
        playlist_exist = sum([playlist_name.lower() == playlist_n.lower() for playlist_n,Playlist in self._playlist.items()])
        if playlist_exist == 0:
            print(f"Cannot remove video from {playlist_name}: Playlist does not exist")
        else:
            video_id_exist = sum([video_id==id for id in self.video_ids])
            if video_id_exist == 0:
                print(f"Cannot remove video from {playlist_name}: Video does not exist")
            else:
                video_in_playlist = sum([video_id==video_ID for video_ID in self._playlist[playlist_name.lower()].playlist_video_ids])
                if video_in_playlist == 0:
                    print(f"Cannot remove video from {playlist_name}: Video is not in playlist")
                else:
                    self._playlist[playlist_name.lower()].playlist_video_ids.remove(video_id)
                    print(f"Removed video from {playlist_name}: {self._video_library.get_video(video_id)._title}")

    def clear_playlist(self, playlist_name):
        """Removes all videos from a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """
        playlist_exist = sum([playlist_name.lower() == playlist_n.lower() for playlist_n,Playlist in self._playlist.items()])
        if playlist_exist == 0:
            print(f"Cannot clear playlist {playlist_name}: Playlist does not exist")
        else:
            self._playlist[playlist_name.lower()].playlist_video_ids.clear()
            print(f"Successfully removed all videos from {playlist_name}")

    def delete_playlist(self, playlist_name):
        """Deletes a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """
        playlist_exist = sum([playlist_name.lower() == playlist_n.lower() for playlist_n,Playlist in self._playlist.items()])
        if playlist_exist == 0:
            print(f"Cannot delete playlist {playlist_name}: Playlist does not exist")
        else:
            del self._playlist[playlist_name.lower()]
            print(f"Deleted playlist: {playlist_name}")

    def search_videos(self, search_term):
        """Display all the videos whose titles contain the search_term.

        Args:
            search_term: The query to be used in search.
        """
        videos = self.videos()
        all_videos_titles = [video._title.lower() for video in self._video_library.get_all_videos()]
        search_results = []
        search_results_video_ids = []
        for video_title in all_videos_titles:
            if search_term.lower() in video_title:
                video_index = all_videos_titles.index(video_title)
                video = videos[video_index]
                video_id = self.video_ids[video_index]
                if self._video_library.get_video(video_id)._flagged == False:
                    search_results.append(video)
                    search_results_video_ids.append(video_id)
                else:
                    pass
        search_results.sort()
        if len(search_results) == 0:
            print(f"No search results for {search_term}")
        else:
            print(f"Here are the results for {search_term}:")
            for i,result in enumerate(search_results):
                print(f'  {i+1}) {result}')
            print("Would you like to play any of the above? If yes, specify the number of the video.")
            print("If your answer is not a valid number, we will assume it's a no.")
            inp = input()
            if inp.isalpha():
                pass
            elif inp.isnumeric():
                if 1 <= int(inp) and int(inp) <= len(search_results):
                    self.play_video(search_results_video_ids[int(inp)-1])
                else:
                    pass
            else:
                pass
    def search_videos_tag(self, video_tag):
        """Display all videos whose tags contains the provided tag.

        Args:
            video_tag: The video tag to be used in search.
        """
        videos = self.videos()
        #convert all tags into lower case
        all_videos_tags = []
        for video in self._video_library.get_all_videos():
            video_tags = []
            for tag in video._tags:
                video_tags.append(tag.lower())
            all_videos_tags.append(video_tags)

        #search result for video tag
        search_results = []
        search_results_video_ids = []
        for i,video_tags in enumerate(all_videos_tags):
            if video_tag.lower() in video_tags:
                video = videos[i]
                video_id = self.video_ids[i]
                if self._video_library.get_video(video_id)._flagged == False:
                    search_results.append(video)
                    search_results_video_ids.append(video_id)
                else:
                    pass
        search_results.sort()

        if len(search_results) == 0:
            print(f"No search results for {video_tag}")
        else:
            print(f"Here are the results for {video_tag}:")
            for i,result in enumerate(search_results):
                print(f'{  i+1}) {result}')
            print("Would you like to play any of the above? If yes, specify the number of the video.")
            print("If your answer is not a valid number, we will assume it's a no.")
            inp = input()
            if inp.isalpha():
                pass
            elif inp.isnumeric():
                if 1 <= int(inp) and int(inp) <= len(search_results):
                    self.play_video(search_results_video_ids[int(inp)-1])
                else:
                    pass
            else:
                pass

    def flag_video(self, video_id, flag_reason=""):
        """Mark a video as flagged.

        Args:
            video_id: The video_id to be flagged.
            flag_reason: Reason for flagging the video.
        """
        video_id_exist = sum([video_id==id for id in self.video_ids])

        if video_id_exist != 1:
            print("Cannot flag video: Video does not exist")
        else:
            if self._video_library.get_video(video_id)._flagged == True:
                print("Cannot flag video: Video is already flagged")
            else:
                if flag_reason == "":
                    pass
                else:
                    self._video_library.get_video(video_id)._flagged_reason = flag_reason
                self._video_library.get_video(video_id)._flagged = True
                if self._currently_playing == None:
                    pass
                else:
                    if self._video_library.get_video(self._currently_playing)._flagged == False:
                        pass
                    else:
                        self.stop_video()
                print(f"Successfully flagged video: {self._video_library.get_video(video_id)._title} (reason: {self._video_library.get_video(video_id)._flagged_reason})")


    def allow_video(self, video_id):
        """Removes a flag from a video.

        Args:
            video_id: The video_id to be allowed again.
        """
        video_id_exist = sum([video_id==id for id in self.video_ids])

        if video_id_exist != 1:
            print("Cannot remove flag from video: Video does not exist")
        else:
            if self._video_library.get_video(video_id)._flagged == False:
                print("Cannot remove flag from video: Video is not flagged")
            else:
                self._video_library.get_video(video_id)._flagged = False
                self._video_library.get_video(video_id)._flagged_reason = "Not supplied"
                print(f"Successfully removed flag from video: {self._video_library.get_video(video_id)._title}")
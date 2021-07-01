"""A video player class."""

from .video_library import VideoLibrary
import bisect
import random

""" 
    bisect.insort() is being used here to sort as it is being added to a list.
"""


class VideoPlayer:
    """A class used to represent a Video Player."""
    
    """ 
    self.stream -> currently playing
    self.pause -> is the current video paused or not
    self.playlists -> stores all playlists in a dictionary. It maps the playlist name to the list of videos in the playlist
    self.lower_keyset -> stores all the playllist names in lower case
    self.flagged -> dictionary which maps video_id to the reason why the video was flagged
    """
    def __init__(self):
        self._video_library = VideoLibrary()
        self.stream = ''
        self.pause = False
        self.playlists = {}
        self.lower_keyset=[]
        self.flagged={}

    def number_of_videos(self):
        num_videos = len(self._video_library.get_all_videos())
        print(f"{num_videos} videos in the library")


    
    def show_all_videos(self):
        """Returns all videos."""
        elements=[]
        print("Here's a list of all available videos:")
        for video in self._video_library.get_all_videos():
            if(video._video_id in self.flagged.keys()):
                bisect.insort(elements,("  " + video._title + " (" + video._video_id + ") " + "[" + " ".join(video._tags) + "]" + " - FLAGGED (reason: " + self.flagged[video._video_id] + ")"))
            else:
                bisect.insort(elements,("  " + video._title + " (" + video._video_id + ") " + "[" + " ".join(video._tags) + "]"))
        print("\n".join(elements))


 
    def play_video(self, video_id):
        """Plays the respective video.

        Args:
            video_id: The video_id to be played.
        """
        if(any(video._video_id == video_id for video in self._video_library.get_all_videos())):
            if(video_id in self.flagged.keys()):
                print("Cannot play video: Video is currently flagged (reason: " + self.flagged[video_id] + ")")
            else:
                if (self.stream != ""):
                    self.pause = False
                    print("Stopping video: " + self.stream)
                print("Playing video: " + self._video_library.get_video(video_id)._title)
                self.stream = self._video_library.get_video(video_id)._title
        else:
            print("Cannot play video: Video does not exist")


    def stop_video(self):
        """Stops the current video."""
        if (self.stream != ""):
            print("Stopping video: " + self.stream)
            self.stream=""
            self.pause=False
        else:
            print("Cannot stop video: No video is currently playing")

    def play_random_video(self):
        """Plays a random video from the video library."""
        if((len(self._video_library.get_all_videos()) == 0) or (len(self.flagged)==len(self._video_library.get_all_videos()))):
            print("No videos available")
        else:
            self.play_video(random.choice(self._video_library.get_all_videos())._video_id)
        

    def pause_video(self):
        """Pauses the current video."""

        if(self.stream!=""):
            if(self.pause==False):
                print("Pausing video: " + self.stream)
                self.pause = True 
            else:
                print("Video already paused: " + self.stream)
        else:
            print("Cannot pause video: No video is currently playing")

    def continue_video(self):
        if(self.stream!=""):
            if(self.pause == True):
                print("Continuing video: " + self.stream)
                self.pause = False
            else:
                print("Cannot continue video: Video is not paused")
        else:
            print("Cannot continue video: No video is currently playing")

    def show_playing(self):
        """Displays video currently playing."""
        not_paused = ""
        if(self.stream!=""):
            for video in self._video_library.get_all_videos():
                if (self.stream == video._title):
                    if(self.pause == True):
                        status = " - PAUSED"
                    else:
                        status = ""
                    print("Currently playing: " +  video._title + " (" + video._video_id + ") " + "[" + " ".join(video._tags) + "]" + status)
                    break
        else:
            print("No video is currently playing")

            

    def create_playlist(self, playlist_name):
        """Creates a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """
        flag=0
        for playlist in self.playlists.keys():
            if (playlist.lower() == playlist_name.lower()):
                print("Cannot create playlist: A playlist with the same name already exists")
                flag=1
                break
        if(flag==0):
            self.lower_keyset.append(playlist_name.lower())
            self.playlists[playlist_name]= []
            print("Successfully created new playlist: " + playlist_name)

    def add_to_playlist(self, playlist_name, video_id):
        """Adds a video to a playlist with a given name.

        Args:
            playlist_name: The playlist name.
            video_id: The video_id to be added.
        """
        if any(playlist_name.lower() == playlist for playlist in self.lower_keyset):
            for playlist in self.playlists.keys():
                if (playlist.lower() == playlist_name.lower()):
                    if(any(video._video_id == video_id for video in self._video_library.get_all_videos())):
                        if(video_id in self.flagged.keys()):
                            print("Cannot add video to " + playlist_name  +": Video is currently flagged (reason: " + self.flagged[video_id] + ")")
                        else:
                            if video_id in str(self.playlists[playlist]):
                                print("Cannot add video to " + playlist_name + ": Video already added")
                            else:
                                self.playlists[playlist].append(video_id)
                                print("Added video to " + playlist_name + ": " + self._video_library.get_video(video_id)._title)
                    else:
                        print("Cannot add video to " + playlist_name + ": Video does not exist")
        else:
            print("Cannot add video to " + playlist_name + ": Playlist does not exist")



    def show_all_playlists(self):
        """Display all playlists."""
        if(len(self.playlists) == 0):
            print("No playlists exist yet")
        else:
            list = []
            print("Showing all playlists:")
            for playlist in self.playlists.keys():
                bisect.insort(list, "  " + playlist)
            print("\n".join(list))



    def show_playlist(self, playlist_name):
        """Display all videos in a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """
        if any(playlist_name.lower() == playlist for playlist in self.lower_keyset):
            for playlist in self.playlists.keys():
                if (playlist.lower() == playlist_name.lower()):
                    print("Showing playlist: " + playlist_name)
                    if(len(self.playlists[playlist]) == 0):
                        print("  No videos here yet.")
                    else:
                        for ele in self.playlists[playlist]:
                            video = self._video_library.get_vid_from_title(ele)
                            if(video._video_id in self.flagged.keys()):
                                print("  " + video._title + " (" + video._video_id + ") " + "[" + " ".join(video._tags) + "]" + " - FLAGGED (reason: " + self.flagged[video._video_id] + ")")
                            else:
                                print("  " + video._title + " (" + video._video_id + ") " + "[" + " ".join(video._tags) + "]")
        else:
            print("Cannot show playlist " + playlist_name + ": Playlist does not exist")


    def remove_from_playlist(self, playlist_name, video_id):
        """Removes a video to a playlist with a given name.

        Args:
            playlist_name: The playlist name.
            video_id: The video_id to be removed.
        """
        if any(playlist_name.lower() == playlist for playlist in self.lower_keyset):
            if(any(video._video_id == video_id for video in self._video_library.get_all_videos())):
                for playlist in self.playlists.keys():
                    if (playlist.lower() == playlist_name.lower()):
                        # to_remove = self._video_library.get_video(video_id)._title
                        if video_id in self.playlists[playlist]:
                            self.playlists[playlist].remove(video_id)
                            print("Removed video from " + playlist_name + ": " + self._video_library.get_video(video_id)._title)
                        else:
                            print("Cannot remove video from " + playlist_name + ": Video is not in playlist")
            else:
                print("Cannot remove video from " + playlist_name + ": Video does not exist")
        else:
            print("Cannot remove video from " + playlist_name + ": Playlist does not exist")


        

    def clear_playlist(self, playlist_name):
        """Removes all videos from a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """
        if any(playlist_name.lower() == playlist for playlist in self.lower_keyset):
            for playlist in self.playlists.keys():
                if (playlist.lower() == playlist_name.lower()):
                    del self.playlists[playlist][0:]
                    print("Successfully removed all videos from " + playlist_name)
        else:
            print("Cannot clear playlist " + playlist_name + ": Playlist does not exist")
        

    def delete_playlist(self, playlist_name):
        """Deletes a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """
        if any(playlist_name.lower() == playlist for playlist in self.lower_keyset):
            for playlist in self.playlists.keys():
                if (playlist.lower() == playlist_name.lower()):
                    del self.playlists[playlist]
                    self.lower_keyset.remove(playlist.lower())
                    print("Deleted playlist: " + playlist_name)
                    break
        else:
            print("Cannot delete playlist " + playlist_name + ": Playlist does not exist")
        

    def search_videos(self, search_term):
        """Display all the videos whose titles contain the search_term.

        Args:
            search_term: The query to be used in search.
        """
        searches=[]
        count=0
        vid_ids =[]
        if(any((search_term.lower() in video._title.lower()) for video in self._video_library.get_all_videos())):
            for video in self._video_library.get_all_videos():
                if(search_term.lower() in video._title.lower()):
                    if(video._video_id not in self.flagged.keys()):
                        bisect.insort(searches,(video._title + " (" + video._video_id + ") " + "[" + " ".join(video._tags) + "]"))
                        bisect.insort(vid_ids, video._video_id)
            if(len(searches)!=0):
                print("Here are the results for " + search_term + ": ")
                for element in searches:
                    count+=1
                    print("  " + str(count) + ") " + element)
                print("Would you like to play any of the above? If yes, specify the number of the video. \nIf your answer is not a valid number, we will assume it's a no.")
                play = input()
                if(play.isnumeric()):
                    to_play=int(play)
                    if(int(to_play) <= len(searches)):
                        self.play_video(vid_ids[to_play-1])
            else: 
                print("No search results for " + search_term)
        else:
            print("No search results for " + search_term)
            
        

    def search_videos_tag(self, video_tag):
        """Display all videos whose tags contains the provided tag.

        Args:
            video_tag: The video tag to be used in search.
        """
        """ 
        To call on the play_video() function, video_id of each search result is stored in video_ids which is later used as a helper in calling the play_video() function
        """
        searches=[]
        count=0
        vid_ids =[]
        if(any(video_tag.lower() in video._tags for video in self._video_library.get_all_videos())):
            for video in self._video_library.get_all_videos():
                if(video_tag.lower() in video._tags):
                    if(video._video_id not in self.flagged.keys()):
                        bisect.insort(searches,(video._title + " (" + video._video_id + ") " + "[" + " ".join(video._tags) + "]"))
                        bisect.insort(vid_ids, video._video_id)
            if(len(searches)!=0):
                print("Here are the results for " + video_tag + ": ")
                for element in searches:
                    count+=1
                    print("  " + str(count) + ") " + element)
                print("Would you like to play any of the above? If yes, specify the number of the video. \nIf your answer is not a valid number, we will assume it's a no.")
                play = input()
                if(play.isnumeric()):
                    to_play=int(play)
                    if(to_play <= len(searches)):
                        self.play_video(vid_ids[to_play-1])
            else:
                print("No search results for " + video_tag)
        else:
            print("No search results for " + video_tag)


    def flag_video(self, video_id, flag_reason=""):
        """Mark a video as flagged.

        Args:
            video_id: The video_id to be flagged.
            flag_reason: Reason for flagging the video.
        """
        if(any(video._video_id == video_id for video in self._video_library.get_all_videos())):
            if(video_id in self.flagged.keys()):
                print("Cannot flag video: Video is already flagged")
            else:
                if(flag_reason==""):
                    flag_reason = "Not supplied"
                if(self._video_library.get_video(video_id)._title == self.stream):
                    self.stop_video()
                print("Successfully flagged video: " + self._video_library.get_video(video_id)._title + " (reason: " +  flag_reason +")")
                self.flagged[video_id] = flag_reason
        else:
            print("Cannot flag video: Video does not exist")
        

    def allow_video(self, video_id):
        """Removes a flag from a video.

        Args:
            video_id: The video_id to be allowed again.
        """
        if(any(video._video_id == video_id for video in self._video_library.get_all_videos())):
            if(video_id in self.flagged.keys()):
                del self.flagged[video_id]
                print("Successfully removed flag from video: " + self._video_library.get_video(video_id)._title)
            else:
                print("Cannot remove flag from video: Video is not flagged")
        else:
            print("Cannot remove flag from video: Video does not exist")

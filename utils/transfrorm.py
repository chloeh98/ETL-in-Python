import pandas as pd

class TransformTracksData:
    def __init__(self):
        self.tracks_dictionary = {}
        self.song_names = []
        self.artists = []
        self.track_played_at = []

    def tracks_from_json(self, json_data):
        tracks = json_data["items"]
        for track in tracks:
            self.song_names.append(track["track"]["name"])
            self.artists.append(track["track"]["album"]["artists"][0]["name"])
            self.track_played_at.append(track["played_at"])
            self.tracks_dictionary = {
                'track_name':  self.song_names,
                'artist_name': self.artists,
                'time_stamp': self.track_played_at
            }
        return self.tracks_dictionary

    def tracks_dict_to_df(self):
        tracks_df = pd.DataFrame.from_dict(self.tracks_dictionary)
        return tracks_df


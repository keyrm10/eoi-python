#!/usr/bin/env python3


class Song:
    def __init__(self, track, artist, genre, bpm, energy, danceability, length):
        self.track = track
        self.artist = artist
        self.genre = genre
        self.bpm = bpm
        self.energy = energy
        self.danceability = danceability
        self.length = length

    def __str__(self):
        return f"{self.track},{self.artist},{self.genre},{self.bpm},{self.energy},{self.danceability},{self.length}"

    def change_speed(self, relative_bpm):
        self.bpm += relative_bpm
        self.energy += 2 * relative_bpm
        self.danceability += 3 * relative_bpm
        self.length -= relative_bpm

    @staticmethod
    def load_songs(path):
        songs = []
        with open(path) as input_file:
            for line in input_file:
                args = []
                args = [f for f in line.split(",")[:3]]
                args += [int(f) for f in line.rstrip().split(",")[3:]]
                songs.append(Song(*(args)))
        return songs

    @staticmethod
    def save_songs(songs, path):
        with open(path, "w") as output_file:
            for song in songs:
                output_file.write(f"{song}\n")

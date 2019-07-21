import os
import math
import argparse
import wave
import contextlib

parser = argparse.ArgumentParser()
parser.add_argument("bpm", type=int, help="beats per minutes of the audio track")
parser.add_argument("beats_per_episode", type=int, help="number of beats in an episode")
parser.add_argument("file", type=str, help="the audio file name for which we create labels")
parser.add_argument("-s", "--start_offset", type=float, default=0.0, help="track start offset in seconds")
parser.add_argument("-o", "--out_dir", type=str, default=os.getcwd(), help="directory for output label files")
args = parser.parse_args()

file_name_with_extension = os.path.basename(args.file)
file_name = os.path.splitext(file_name_with_extension)[0]
print("file name: '{}'".format(file_name))

with contextlib.closing(wave.open(args.file, 'r')) as f:
    frames = f.getnframes()
    rate = f.getframerate()
    total_song_time_seconds = frames / float(rate)
print("total time in seconds: {}".format(total_song_time_seconds))

beat_length = 60.0 / args.bpm
episode_length = beat_length * args.beats_per_episode

num_of_episodes = math.ceil(total_song_time_seconds / episode_length)
num_of_beats = num_of_episodes * args.beats_per_episode


def create_labels_series(outfile, start, duration, repeats, label):
    print("writing lable file: '{}'".format(outfile))
    with open(outfile, "w+") as f:
        for i in range(0, repeats):
            start_time = start + i * duration
            f.write(str(start_time) + "\t" + str(start_time) + "\t" + label + str(i) + "\n")

outfile_episodes = os.path.join(args.out_dir, file_name + "_audacity_episodes.txt")
create_labels_series(outfile_episodes, args.start_offset, episode_length, num_of_episodes, "episode_")

outfile_beats = os.path.join(args.out_dir, file_name + "_audacity_beats.txt")
create_labels_series(outfile_beats, args.start_offset, beat_length, num_of_beats, "beat_")

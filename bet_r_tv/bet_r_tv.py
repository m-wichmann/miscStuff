#! /usr/bin/env python3
"""
This script chooses an episode of a list of shows randomly and starts vlc.
If another instance was already running, it is killed. It's the perfect alternative to TV ;)

The variables DIRS and SHOWS need to contain the dir names. Following file hierachy is expected:

BASE_DIR/SHOW_DIR/EPISODE.avi

"""


import os
import random

DIRS  = [
    """NOTE: Insert list of dirs to search for shows."""
]
SHOWS = [
    """NOTE: Insert list of shows."""
]

# kill possible instance of vlc started by bet_r_tv
# marker '--video-title BET_R_TV_MAGIC_STRING' is used to id process
cmd = 'pkill -f "^vlc.*--video-title BET_R_TV_MAGIC_STRING"'
os.system(cmd)

# create list of all episodes out of the dirs
episodes = []
for s in SHOWS:
    exists_once = False
    for d in DIRS:
        if not os.path.exists(d + s):
            continue
        exists_once = True
        for f in os.listdir(d + s):
            episodes.append(d + s + '/' + f)
    if not exists_once:
        print('Not found: ' + s)

# choose one episode randomly
chosen_episode = random.choice(episodes)

# start vlc
cmd = 'vlc '                                    \
    + '--quiet '                                \
    + '--play-and-exit '                        \   # exit after episode
    + '--fullscreen '                           \   # fullscreen...
    + '--qt-fullscreen-screennumber=1 '         \   # ...on second monitor
    + '--video-title BET_R_TV_MAGIC_STRING '    \   # marker to later id the process
    + '"' + chosen_episode + '" '               \
    + '&'
os.system(cmd)


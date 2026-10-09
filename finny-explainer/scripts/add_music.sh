#!/bin/bash
# usage: add_music.sh in.mp4 music.wav out.mp4   (video stream copied untouched)
ffmpeg -v error -y -i "$1" -i "$2" -filter_complex "\
[0:a]aresample=48000,pan=stereo|c0=c0|c1=c0,volume=6.6dB,asplit=2[vo][sc];\
[1:a]highpass=f=60,equalizer=f=2500:t=q:w=1.2:g=-4,volume=-6dB[mus];\
[mus][sc]sidechaincompress=threshold=0.04:ratio=3:attack=25:release=450:makeup=1,\
volume='if(lt(t,3.3),2,if(lt(t,3.9),2-(t-3.3)/0.6,if(gt(t,131.6),2,if(gt(t,131.0),1+(t-131.0)/0.6,1))))':eval=frame[duck];\
[vo][duck]amix=inputs=2:normalize=0:duration=first,alimiter=limit=0.87:level=false[out]" \
-map 0:v -map "[out]" -c:v copy -c:a aac -b:a 192k -movflags +faststart "$3"

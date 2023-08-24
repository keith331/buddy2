ssh device pkill arecord
ssh device rm -f /media/recs/dutmics.wav
ssh device arecord -f dat -Dplug:\'hw:0,3,0\' /media/recs/dutmics.wav
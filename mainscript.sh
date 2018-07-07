#!/bin/bash
TARGET=/home/linaro/pic

export APIKEY="1ed0e88c3e964912a1baa09fab757356"
export PUBLICKEY="AKIAJTJGMZQ26WIB65IQ"
export SECRETKEY="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"

# for i in {1..5}
#
FILENAME=$RANDOM.jpg
gst-launch-1.0 v4l2src num-buffers=1 ! jpegenc ! filesink location=$TARGET/$FILENAME
sleep 2s
python3 ~/qdroptables/analysis.py $TARGET/$FILENAME
#done
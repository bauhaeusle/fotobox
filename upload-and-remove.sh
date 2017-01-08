#!/bin/bash
# for use with webdav
#echo put $1 | cadaver [WEBDAV-URL]
#rm $1

# to use dropbox uploader
echo "upload image $1"
../Dropbox-Uploader/dropbox_uploader.sh $1 $1
echo "uploaded image $1"
rm $1
echo "removed image $1"

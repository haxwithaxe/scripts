#!/bin/bash
# copyright (c) 2014 haxwithaxe
# License: GPLv3
###############################
## Link the media folders in the downloads folder to a cleaner directory
# structure for sharing over the network

orig=/mnt/mega/downloads
dest=/mnt/mega/media

# video destination directories
dest_video=${dest}/video
dest_tv=${dest_video}/tv
tv_list=media_tv.lst
dest_movie=${dest_video}/movies
movie_list=media_movie.lst
dest_con=${dest_video}/cons
con_list=media_con.lst
dest_class=${dest_video}/classes
class_list=media_class.lst

# music destination directories
dest_music=${dest}/music
music_list=media_music.lst
dest_audiobook=${dest}/audiobooks
audiobook_list=media_audio.lst

link(){
	# requires
	# $src_dir
	# $dest_dir
	# $item_list
	for d in ${item_list[@]} ;do
		d=`awk '{gsub(";;;"," ");print $0}' <<< $d`
		echo $d
		ln -sf $orig_dir/$d $dest_dir/$d
	done
}

link_tv(){
	if [ -e $tv_list ] ;then
		item_list=`awk '{gsub(" ",";;;");print $0}' $tv_list`
		src_dir=$orig
		dest_dir=$dest_tv
		link
	fi
}

link_movie(){
	if [ -e $movie_list ] ;then
		item_list=`awk '{gsub(" ",";;;");print $0}' $movie_list`
		src_dir=$orig
		dest_dir=$dest_movie
		link
	fi
}

link_con(){
	if [ -e $con_list ] ;then
		item_list=`awk '{gsub(" ",";;;");print $0}' $con_list`
		src_dir=$orig
		dest_dir=$dest_con
		link
	fi
}

link_class(){
	if [ -e $class_list ] ;then
		item_list=`awk '{gsub(" ",";;;");print $0}' $class_list`
		src_dir=$orig
		dest_dir=$dest_class
		link
	fi
}

link_music(){
	if [ -e $music_list ] ;then
		item_list=`awk '{gsub(" ",";;;");print $0}' $music_list`
		src_dir=$orig
		dest_dir=$dest_music
		link
	fi
}

link_audiobook(){
	if [ -e $audiobook_list ] ;then
		item_list=`awk '{gsub(" ",";;;");print $0}' $audiobook_list`
		src_dir=$orig
		dest_dir=$dest_audiobook
		link
	fi
}


link_tv
link_movie
link_con
link_class
link_music
link_audiobook


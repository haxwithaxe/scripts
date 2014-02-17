#!/bin/bash
# copyright (c) 2014 haxwithaxe
# License: GPLv3

orig=/mnt/mega/downloads
dest=/mnt/mega/media/video/tv

directories=(bbc-random bizarre_foods bush_tucker_man derren_brown dirty_jobs
		discovery_channel downton_abbey dr_who futurama good_eats 
		great_migrations harvey_birdman history_channel
		inside_the_actors_studio james_may-man_lab james_may_toy_stories
		james_may_tyntk kill_it_cook_it_eat_it mad_scientists modern_marvels
		movies mythbusters nat_geo no_reservations parts_unknown pbs_docu
		penn_teller real_time-with_bill_maher red_dwarf river_monsters
		samurai_champloo star_wars_the_clone_wars the_new_yankee_workshop
		the_red_green_show top_gear venture_bros standup)

for d in ${directories[@]} ;do
	echo $d
	ln -sf $orig/$d $dest/$d
done

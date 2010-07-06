#!/bin/bash
intro="Today's Weather For Kensington, Maryland"
id="KAID"
city="washington_dulles_intl_airport"
saycity="Kensington"
state="va"
weather_func(){
echo $intro
weather -q -i $id | sed "s/ F / degrees ferenheit/" | sed "s/(.*)//" | sed "s/$/ .../" | sed "s/ W /west/" | sed "s/ E /east/" | sed "s/ S /south/" | sed "s/ N /north/" | sed "s/NNE/north north east/" | sed "s/NE/north east/" | sed "s/ENE/east north east/" | sed "s/ESE/east south east/" | sed "s/SE/south east/" | sed "s/SSE/south south east/" | sed "s/SSW/south south west/" | sed "s/SW/south west/" | sed "s/WSW/west south west/" | sed "s/WNW/west north west/" | sed "s/NW/north west/" | sed "s/NNW/north north west/"
if [[ `wget -q http://weather.noaa.gov/pub/data/watches_warnings/urgent_weather_message/md/mdz003.txt -O- | grep Expires | cut -d':' -f3- | sed 's/;.*$//'` > `date +%Y%m%d%H%M` ]]
	then
		echo Weather Advisiory ...
		wget -q http://weather.noaa.gov/pub/data/watches_warnings/urgent_weather_message/md/mdz003.txt -O- | sed "/^[0-9]*.*[0-9]$/d" | sed "/^\/.*\/$/d" | sed "/^MD.*$/d" | sed "/\-$/d" | sed "/^[a-z,A-Z].*\.\.\./d" | sed "/^[A-Z][A-Z][A-Z][A-Z][A-Z][A-Z]$/d" | sed "/^\$\$$/d"| sed "s/MD/maryland/"
		echo ...
fi
echo "Forcast for $saycity ..."
weather -n -q -c $city -s $state | sed "s/ F / degrees ferenheit/" | sed "s/(.*)//"
}
weather_func | festival --tts
exit 0

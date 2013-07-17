#!/bin/bash
get_version() {
	wget -q http://www.slimroms.net/index.php/downloads/all/viewcategory/399-grouper
	off_string=$(grep -Po -m 1 "Slim-grouper.*-OFFICIAL" 399-grouper | grep -Po '\d+(\.\d+)*-')
	echo "${off_string%?}" > version-bridge
	rm 399-grouper
	
	wget -q http://www.slimroms.net/index.php/downloads/all/viewcategory/624-grouper
	week_string=$(grep -Po -m 1 "Slim-grouper.*-WEEKLY" 624-grouper | grep -Po '\d+(\.\d+)*-')
	echo "${week_string%?}" >> version-bridge
	rm 624-grouper
}

if [[ ! -f version-bridge ]]; then
	get_version
elif [[ `find version-bridge -mmin +30` ]]; then
	get_version
fi

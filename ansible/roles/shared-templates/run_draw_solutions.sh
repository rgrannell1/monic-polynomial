#!/usr/bin/env sh

folder_name="/root/tasks/{{ start_time }}"
mkdir -p "$folder_name"

rm "/root/tasks/current"
ln -s "$(readlink -f $folder_name)" "/root/tasks/current"


mkdir -p "$folder_name/logs"
mkdir -p "$folder_name/output"
mkdir -p "$folder_name/output/json"
mkdir -p "$folder_name/output/images"

{% for argset in args['draw'] %}

{{ repo_path }}/src/python/draw-solutions.py        \
	--width={{ argset.width }}                      \
	--height={{ argset.height }}                    \
	--xrange={{ argset.xrange }}                    \
	--yrange={{ argset.yrange }}                    \
	--in-path=$folder_name/json/{{ start_time }} \
	--out-path=$folder_name/images/{{ start_time }} 2>&1 | tee "$folder_name/logs/draw-solutions.log"

{% endfor %}

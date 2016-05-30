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

{{ repo_path }}/src/python/render-pixels.py         \
	--width={{ argset.width }}                      \
	--height={{ argset.height }}                    \
	--xrange={{ argset.xrange }}                    \
	--yrange={{ argset.yrange }}                    \
	--input_path=$folder_name/json/{{ start_time }} \
	--output_path=$folder_name/images/{{ start_time }} 2>&1 | tee "$folder_name/logs/draw-solutions.log"

{% endfor %}

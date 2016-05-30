#!/usr/bin/env sh

folder_name="~/polynomial-builds/{{start_time}}/"
mkdir -p "$folder_name"

{% for argset in args['draw'] %}

{{ repo_path }}/src/python/draw-solutions.py \
	--width={{ argset.width }}            \
	--height={{ argset.height }}          \
	--xrange={{ argset.xrange }}          \
	--yrange={{ argset.yrange }}          \
	--input_path=$folder_name/json/{{ start_time }}
	--output_path=$folder_name/images/{{ start_time }}
	| tee "$folder_name/draw-solutions.log"

{% endfor %}

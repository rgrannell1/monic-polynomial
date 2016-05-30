#!/usr/bin/env sh

readable_date=$(date +"%H:%M_%m-%d-%Y")
folder_name="~/polynomial-builds/{{ start_time }}"

mkdir -p "$folder_name"
mkdir -p "$folder_name/logs"
mkdir -p "$folder_name/output"
mkdir -p "$folder_name/output/json"
mkdir -p "$folder_name/output/images"

rm "/root/tasks/current"
ln -s "$(readlink -f $folder_name)" "/root/tasks/current"

{% for argset in args['solve'] %}

echo "order: {{ argset['order'] }}" | tee "$folder_name/solve-polynomial.log"
echo "range: {{ argset['range'] }}" | tee "$folder_name/solve-polynomial.log"

{{ repo_path }}/src/python/solve-polynomials.py \
	--order={{ argset['order'] }}              \
	--range={{ argset['range'] }}
	--assume-yes 2>&1 | tee "$folder_name/logs/solve-polynomial.log"

{% endfor %}

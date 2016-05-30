#!/usr/bin/env sh

readable_date=$(date +"%H:%M_%m-%d-%Y")
folder_name="/root/tasks/{{ start_time }}"

mkdir -p "$folder_name"
mkdir -p "$folder_name/logs"
mkdir -p "$folder_name/output"
mkdir -p "$folder_name/output/json"
mkdir -p "$folder_name/output/images"

ln -s "$(readlink -f $folder_name)" "/root/tasks/current"

out_path="$folder_name/output/json/solutions.jsonl"

{% for argset in args['solve'] %}

echo "order:  {{ argset['order'] }}" | tee "$folder_name/solve-polynomial.log"
echo "range:  {{ argset['range'] }}" | tee "$folder_name/solve-polynomial.log"
echo "target: $out_path"             | tee "$folder_name/solve-polynomial.log"

{{ repo_path }}/src/python/solve-polynomials.py \
	--order={{ argset['order'] }}               \
	--range={{ argset['range'] }}               \
	--out-path="$out_path"                      \
	--assume-yes 2>&1 | tee "$folder_name/logs/solve-polynomial.log"

{% endfor %}

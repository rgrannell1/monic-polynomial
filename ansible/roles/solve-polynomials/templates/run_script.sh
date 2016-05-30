#!/usr/bin/env sh

readable_date=$(date +"%H:%M_%m-%d-%Y")
folder_name="~/polynomial-builds/$readable_date/"

mkdir -p "$folder_name"

{% for argset in args['solve'] %}

echo "order: {{ argset['order'] }}" | tee "$folder_name/solve-polynomial.log"
echo "range: {{ argset['range'] }}" | tee "$folder_name/solve-polynomial.log"

{{ repo_path }}/src/python/solve-polynomials.py \
	--order={{ argset['order'] }}              \
	--range={{ argset['range'] }}
	--assume-yes | tee "$folder_name/solve-polynomial.log"

{% endfor %}

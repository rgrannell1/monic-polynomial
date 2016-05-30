#!/usr/bin/env sh

mkdir ~/polynomial-builds/

#screen -dmS "run-everything-{{start_time}}" bash run_solve_polynomials.sh && bash run_draw_solutions.sh && bash run_render_pixels.sh

bash run_solve_polynomials.sh
bash run_draw_solutions.sh
bash run_render_pixels.sh

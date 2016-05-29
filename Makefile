
inventory_script_path = ansible/inventory-script.py

environment:
	ansible-playbook -i $(inventory_script_path) ansible/setup-environment.yaml

solve-polynomials:
	ansible-playbook -i $(inventory_script_path) ansible/solve-polynomials.yaml

draw-solutions:
	ansible-playbook -i $(inventory_script_path) ansible/draw-solutions.yaml

fetch:
	src="{{ repo_path }}/output"
	dest=
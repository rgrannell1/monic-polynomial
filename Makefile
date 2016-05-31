
ip_address=`cat ./security/ip_address`
inventory_script_path = ansible/inventory-script.py

create-vm:
	bash provision/new-vm.sh

environment:
	ansible-playbook -i $(inventory_script_path) ansible/setup-environment.yaml

solve-polynomials:
	ansible-playbook -i $(inventory_script_path) ansible/solve-polynomials.yaml

render-pixels:
	ansible-playbook -i $(inventory_script_path) ansible/render-pixels.yaml

draw-solutions:
	ansible-playbook -i $(inventory_script_path) ansible/draw-solutions.yaml

run:
	ansible-playbook -i $(inventory_script_path) ansible/create-image.yaml

fetch-images:

	mkdir -p ~/polynomial-output
	scp -r root@$(ip_address):tasks/current/output/images ~/polynomial-output

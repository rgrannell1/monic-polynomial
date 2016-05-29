
inventory_script_path = ansible/inventory-script.py

environment:
	ansible-playbook -i $(inventory_script_path) ansible/setup-environment.yaml

solve-polynomials:
	ansible-playbook -i $(inventory_script_path) ansible/solve-polynomials.yaml

draw-solutions:
	ansible-playbook -i $(inventory_script_path) ansible/draw-solutions.yaml

fetch-images:

	mkdir -p ~/monic-output/images
	scp -r root@$(MONIC_TARGET_VM_IP):monic-polynomial/output/images ~/monic-output/images

create-vm:
	bash provision/provision-vm.sh


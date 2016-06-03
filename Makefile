
ip_address=`cat ./security/ip_address`
inventory_script_path = ansible/play/inventory-script.py

new-vm:
	bash provision/new-vm.sh

remove-vm:
	bash provision/remove-vm.sh


environment:
	ansible-playbook -i $(inventory_script_path) ansible/setup-environment.yaml

run:
	ansible-playbook -i $(inventory_script_path) ansible/build-directory.yaml

fetch-images:

	mkdir -p ~/polynomial-output
	scp -r root@$(ip_address):tasks/current/output/images ~/polynomial-output

rerun:
	ansible-playbook -i $(inventory_script_path) ansible/create-image.yaml


ip_address=`cat ./security/ip_address`
inventory_script_path = ansible/inventory-script.py

new-vm:
	bash provision/new-vm.sh

remove-vm:
	bash provision/remove-vm.sh

build-directory:
	ansible-playbook -i $(inventory_script_path) ansible/build-directory.yaml

create-images:
	ansible-playbook -i $(inventory_script_path) ansible/create-images.yaml

fetch-images:

	mkdir -p ~/polynomial-output
	scp -r root@$(ip_address):tasks/current/output/images ~/polynomial-output

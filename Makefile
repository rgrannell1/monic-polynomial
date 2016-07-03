
ip_address=`cat ./security/ip_address`
inventory_script_path = ansible/inventory-script.py





# create a new VM on digital-ocean.

new-vm:

	bash provision/new-vm.sh

# remove the VM from digital-ocean.

remove-vm:

	bash provision/remove-vm.sh

# install system and package dependencies

setup-environment:

	ansible-playbook -i $(inventory_script_path) ansible/setup-environment.yaml

# download repo, copy templates, create build-directory.

build-directory:

	ansible-playbook -i $(inventory_script_path) ansible/build-directory.yaml

# run the image-creation script.

create-images:

	ansible-playbook -i $(inventory_script_path) ansible/create-images.yaml

# retrieve all images from the digital-ocean VM.

fetch-images:

	ansible-playbook -i $(inventory_script_path) ansible/fetch-images.yaml

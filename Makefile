HOST       = 127.0.0.1
TEST_PATH  = ./
CFG_PATH   = ./config

.PHONY: help

clean-pyc:
    find . -name '*.pyc' -exec rm --force {} +
    find . -name '*.pyo' -exec rm --force {} +
    find . -name '*~' -exec rm --force  {} +

clean-build:
    rm --force --recursive build/
    rm --force --recursive dist/
    rm --force --recursive *.egg-info

init:
    wget http://www.laurent-fournier.be/rpi/.bashrc && mv .bashrc ~/
    wget http://www.laurent-fournier.be/rpi/config.txt && sudo mv .bashrc /boot/
    wget http://www.laurent-fournier.be/rpi/wpa_supplicant.conf && sudo mv wpa_supplicant.conf /etc/wpa_supplicant/
    mkdir logs
    sudo apt-get autoremove -y rm_apt.txt
    sudo apt-get update
    sudo apt-get upgrade
	sudo apt-get install -y deps_apt.txt
	pip install -r deps_pip.txt
	garden install graph
	sudo reboot
	
test: 
    clean-pyc
    py.test --verbose --color=yes $(TEST_PATH)

run:
    python main.py runserver
    
help:
    @echo "    clean-pyc"
    @echo "        Remove python artifacts."
    @echo "    clean-build"
    @echo "        Remove build artifacts."
    @echo "    init"
    @echo "        Install dependencies and create required directories."
    @echo "    test"
    @echo "        Run py.test"
    @echo '    run'
    @echo '        Run the `my_project` service on your local machine.'

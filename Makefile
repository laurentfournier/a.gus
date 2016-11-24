HOST       = 127.0.0.1
TEST_PATH  = ./
CFG_PATH   = ./config

.PHONY: help

clean:
	find . -name '*.pyc' -exec rm --force {} +
	find . -name '*.pyo' -exec rm --force {} +
	find . -name '*~' -exec rm --force  {} +

init:
	wget http://www.laurent-fournier.be/rpi/.bashrc
	mv .bashrc ~/
	sudo su -
	wget http://www.laurent-fournier.be/rpi/config.txt
	mv .bashrc /boot/
	wget http://www.laurent-fournier.be/rpi/wpa_supplicant.conf
	mv wpa_supplicant.conf /etc/wpa_supplicant/
	apt-get update
	apt-get autoremove -y $(CFG_PATH)/rm_apt.txt
	apt-get install -y $(CFG_PATH)/deps_apt.txt
	apt-get upgrade
	pip install -r $(CFG_PATH)/deps_pip.txt
	garden install graph
	source ~/.bashrc
	mkdir logs
	reboot
	
run:
	python main.py runserver
    
help:
	@echo "    clean"
	@echo "        Remove python artifacts."
	@echo "    init"
	@echo "        Install dependencies and create required directories."
	@echo '    run'
	@echo '        Run the `my_project` service on your local machine.'

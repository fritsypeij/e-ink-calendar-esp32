#!/bin/bash -e

echo "This script will build the docker image and run the container."
echo "You may need to run this script with elevated permissions (sudo)."

while true; do
	read -p "Do you want to continue? (Y/n) " CONTINUE
	if [ "$CONTINUE" == "n" ]; then
		exit 0
	elif [ "$CONTINUE" == "y" ] || [ "$CONTINUE" == "Y" ] || [ -z "$INPUT" ]; then
		break
	else
		echo "Invalid input. Please enter y or n."
	fi
done

echo ""

skipcreateconfig=false
# check if the config file exists
if [ -f config.sh ]; then
	source config.sh

	echo "A config file already exists:"
	echo ""
	echo "--------------- config.sh ---------------"
	echo ""
	echo "ESP32 IP: $EID_IP"
	echo "ESP32 Port: $EID_PORT"
	echo "Calendar URLs:"
	for url in "${ICAL_SECRET_URLS[@]}"; do
		echo "  $url"
	done
	echo ""
	echo "-----------------------------------------"
	echo ""
	while true; do
		read -p "Do you want to continue with these settings? [Y/n]: " CONTINUE
		if [ "$CONTINUE" == "n" ]; then
			break
		elif [ "$CONTINUE" == "y" ] || [ "$CONTINUE" == "Y" ] || [ -z "$INPUT" ]; then
			echo "Using the existing config file."
			skipcreateconfig=true
			break
		else
			echo "Invalid input. Please enter y or n."
		fi
	done
fi
if [ "$skipcreateconfig" == false ]; then
	echo "You will need to provide the IP address and port of the ESP32."
	echo ""
	while true; do
		read -p "Enter the IP address: " EID_IP
		if [[ $EID_IP =~ ^[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}$ ]]; then
			IFS='.' read -ra IP <<< "$EID_IP"
			for i in "${IP[@]}"; do
				if [[ $i -lt 0 || $i -gt 255 ]]; then
					echo "Invalid IP address. Please try again."
					continue 2
				fi
			done
			break
		else
			echo "Invalid IP address. Please try again."
		fi
	done

	while true; do
		read -p "Enter the web port: " EID_PORT
		if [[ $EID_PORT =~ ^[0-9]+$ ]] && [ $EID_PORT -ge 1 ] && [ $EID_PORT -le 65535 ]; then
			break
		else
			echo "Invalid port number. Please enter a number between 1 and 65535."
		fi
	done
	echo ""
	echo "GREAT! Now let's add one or multiple calendar URLs."
	echo "Just press enter to add another. Keep empty to finish."
	echo ""

	while true; do
		ICAL_SECRET_URLS=()
		while true; do
			read -p "Enter a calendar URL: " URL
			if [ -z "$URL" ]; then
				break
			elif [[ "$URL" == https://* ]]; then
				ICAL_SECRET_URLS+=("$URL")
			elif [[ "$URL" == webcal://* ]]; then
				echo "Replacing webcal:// with https://"
				URL=${URL/webcal:\/\//https:\/\/}
				ICAL_SECRET_URLS+=("$URL")
			else
				echo "Invalid URL. The URL should start with https://"
				continue
			fi
		done
		if [ ${#ICAL_SECRET_URLS[@]} -eq 0 ]; then
			echo "No URLs provided. Please enter at least one URL."
		else
			break
		fi
	done

	# write the config file
	echo "ICAL_SECRET_URLS=(" > config.sh
	for url in "${ICAL_SECRET_URLS[@]}"; do
		echo "  \"$url\"" >> config.sh
	done
	echo ")" >> config.sh
	echo "EID_IP=\"$EID_IP\"" >> config.sh
	echo "EID_PORT=\"$EID_PORT\"" >> config.sh

	echo ""
	echo "Config file created with:"
	echo ""
	echo "--------------- config.sh ---------------"
	echo ""
	echo "ESP32 IP: $EID_IP"
	echo "ESP32 Port: $EID_PORT"
	echo "Calendar URLs:"
	for url in "${ICAL_SECRET_URLS[@]}"; do
		echo "  $url"
	done
	echo ""
	echo "-----------------------------------------"
	echo ""
fi

echo ""

if ! command -v docker &> /dev/null; then
	echo "From this point on you need to run this script with elevated permissions (sudo)."
	echo "Sudo is needed to install (apt-get) and run Docker."
	while true; do
		read -p "Do you want to install Docker? [Y/n]: " CONTINUE
		if [ "$CONTINUE" == "n" ]; then
			exit 0
		elif [ "$CONTINUE" == "y" ] || [ "$CONTINUE" == "Y" ] || [ -z "$INPUT" ]; then
			break
		else
			echo "Invalid input. Please enter y or n."
		fi
	done

	echo ""
	echo "Installing Docker..."
	echo ""

	sudo apt-get update
	sudo apt-get install -y docker.io

	echo ""
	echo "Docker installed."
	echo ""

	while true; do
		read -p "Do you want to enable and start the Docker service? [Y/n]: " CONTINUE
		if [ "$CONTINUE" == "n" ]; then
			break
		elif [ "$CONTINUE" == "y" ] || [ "$CONTINUE" == "Y" ] || [ -z "$INPUT" ]; then
			sudo systemctl enable docker
			sudo systemctl start docker
			break
		else
			echo "Invalid input. Please enter y or n."
		fi
	done
else
	echo "Docker is installed."
	echo ""
	echo "From this point on you need to run this script with elevated permissions (sudo)."
	echo "Sudo is needed to run Docker."
fi

echo ""
echo "Going to build the docker image..."
echo ""

sudo docker build -t calendar .

echo ""
echo "Building the calendar container done."
while true; do
	read -p "Do you want to start the calendar container? [Y/n]: " CONTINUE
	if [ "$CONTINUE" == "n" ]; then
		exit 0
	elif [ "$CONTINUE" == "y" ] || [ "$CONTINUE" == "Y" ] || [ -z "$INPUT" ]; then
		break
	else
		echo "Invalid input. Please enter y or n."
	fi
done
echo ""
echo "Running the calendar container..."
echo ""
sudo docker run -d --name calendar calendar
echo ""
echo "Calendar container running! You should see the display flicker soon(tm)."
while true; do
	read -p "Do you want to show the logs while starting the container for the first time? [Y/n]: " CONTINUE
	if [ "$CONTINUE" == "n" ]; then
		echo "You can see the logs at any time by running 'sudo docker logs -f calendar'"
		echo ""
		echo "goodbye!"
		exit 0
	elif [ "$CONTINUE" == "y" ] || [ "$CONTINUE" == "Y" ] || [ -z "$INPUT" ]; then
		echo "You can stop viewing the logs by pressing Ctrl+C"
		echo "Showing logs..."
		echo ""
		echo ""
		sudo docker logs -f calendar
		break
	else
		echo "Invalid input. Please enter y or n."
	fi
done

import subprocess
import os

if os.getuid() == 0:
	print("The script is running as root.")
else:
	print("The script is not running as root. Please Run it as root")
	exit()

while True:
	print("Would you like to update?")
	yes_or_no = input("Y/n: ")

	if yes_or_no.lower() == "y" or yes_or_no.lower() == "":
		print("this may take a while")
		command = "apt update -y && apt upgrade -y"
		result = subprocess.run(command, shell=True, capture_output=True, text=True)
		if result.returncode == 0:
			output = result.stdout
			print("Command executed successfully. Output:")
		else:
			error = result.stderr
			print("An error occurred while updating please try again")
		break

	elif yes_or_no.lower() == "n":
		print("Skipping update\n")
		break

	else:
		print("Please answer Y or N")

print("installing nginx")
command = "apt install nginx -y"
result = subprocess.run(command, shell=True, capture_output=True, text=True)
if result.returncode == 0:
	output = result.stdout
	print("Nginx installed successfully.")
else:
	error = result.stderr
	print("An error occurred while executing the command. Error message:")

FQDN = input("please enter your FQDN: ")

print("editing default config in /etc/nginx/sites-available/default")
command = """echo 'server {
	listen 80;
	listen [::]:80;
	server_name """ + FQDN + """;
	return 301 https://$host$request_uri;
}

server {
	listen 443 ssl;
	server_name """ + FQDN +""";

	ssl_certificate /root/cert.crt;
	ssl_certificate_key /root/key.key;

	root /var/www/html/;
	index index.html index.html index.nginx-debian.html;

	location / {
		index index.nginx-debian.html;
	}
}' | tee /etc/nginx/sites-available/default"""
print(command)
result = subprocess.run(command, shell=True, capture_output=True, text=True)
if result.returncode == 0:
	output = result.stdout
	print("Config written to default file in /etc/nginx/sites-available/default")
else:
	error = result.stderr
	print("An error occurred while changing the config please try again.")
	exit()

file_path1 = "/root/key.key"
file_path2 = "/root/cert.crt"

while True:
    if os.path.exists(file_path1) and os.path.exists(file_path2):
        print("Self-signed certificate already exists.")
        yes_or_no = input("Would you like to generate new self-signed certificates? (y/N): ")
        if yes_or_no.lower() == "n" or yes_or_no.lower() == "":
            break
        elif yes_or_no.lower() == "y":
            command = "openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout /root/key.key -out /root/cert.crt"
            result = subprocess.run(command, input='\n\n\n\n\n\n\n', shell=True, capture_output=True, text=True)
            break
        else:
            print("Please answer Y or N")
    else:
        print("Self-signed certificate is missing...\nGenerating now:")
        command = "openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout /root/key.key -out /root/cert.crt"
        result = subprocess.run(command, input='\n\n\n\n\n\n\n', shell=True, capture_output=True, text=True)


print("Done Nginx is configured restarting Nginx service now\nplease try to access your nginx server using the command \"curl -k https://127.0.0.1\"")
command = "systemctl start nginx" 
result = subprocess.run(command, shell=True, capture_output=True, text=True)
command = "systemctl restart nginx" 
result = subprocess.run(command, shell=True, capture_output=True, text=True)

# Nginx_Ubuntu_Deployment_tool
a script designed to deploy a fresh new nginx webserver on an ubuntu sever ISO. when the script is run It will configure the nginx install the sever config, the webroot and the self signed ssl cdrtificates for you.


steps to run below
Download the python file onto the Ubuntu server. I am running Ubuntu Server 22.04.2 LTS and then run it with python3. 
"sudo python3 nginxsetup.py" 
it will ask you a few questions and then setup your server for you.

once its done test it with 
"curl -k https://127.0.0.1/"
you should see the introduction file for nginx from there you can put whatever files you want in the webroot to serve

note make sure to change the location part of the 443 server to match whatever your index.html page is called 

        location / {
                index {index file name here};
        }

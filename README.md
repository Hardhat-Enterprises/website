# [Hardhat Enterprises](https://hardhat.pythonanywhere.com/)

Hardhat Enterprises is an organization that aims to create cyber weapons and tools that can be used to empower white-hat operations. All deliverables produced by the company will be open source so that anyone may use and benefit from them. These deliverables should either improve on existing tools or fill a market need that is not yet met. 

# [Hardhat Enterprises](hardhatwebdev2024.pythonanywhere.com/) T2 2024
[Note: The Hardhat website has been deployed already. Below is the rundown of how it can be deployed from PythonAnywhere. For T1 2024, it already has been deployed. It can be accessed through this domain: hardhatwebdev2024.pythonanywhere.com ]

Deploying HardHat Website from Python Anywhere Platform
For launching the Hardhat website, we have chosen the Python Anywhere platform since it offers free tiers and the website can be hosted for three months without any charge or cost. 
In this document, I will describe the process of deploying the website from the platform with the steps necessary.

Step 1: First, a user account needs to be opened using the free tier (Beginners). In this case, the login credentials are:
Username: hardhatwebdev2024;
Email: s222340498@deakin.edu.au;
Password: "consult lead";
Web app domain: hardhatwebdev2024.pythonanywhere.com

Step 2: Launch the bash console. Run the command ‘git clone https://github.com/Hardhat-Enterprises/website.git’

Step 3: Create a virtual environment using the command – ‘mkvirtualenv <virtual environment name>’. The name of the virtual environment can be anything. Keeping it simple and short is recommended. In this case, I have used ‘venv’ as the environment name.

Step 4: Once the virtual environment is created, the necessary tools and dependencies need to be installed in it using the command- ‘pip install -r requirements.txt’. This command will install all the necessary tools with the correct versions that are needed to launch the website. 

Step 5: After that, we have to open the ‘web’ configuration page by clicking the ‘Web’ button on the top right option panel. In the config page, we have to add the exact name of the virtual environment name in the virtual environment section. 

Step 6: From the web config page, under the ‘Code’ section, the WSGI Configuration File needs to be opened and in the ‘Django’ section, the code lines need to be uncommented as shown. The path needs to be changed to the git repository. The os.environ [‘DJANGO_SETTINGS_MODULE’] = ‘<folder_name>.settings’ should be set accordingly. The <folder_name> needs to be replaced by the name of the folder in which the settings.py file is located.

Step 7: We have to open the ‘settings.py’ config file from the ‘Files’ tab and add the Hardhat website URL as an allowed host in the ‘Allowed_Hosts’ option brackets. This will allow the website URL to launch the website whenever searched from any browser. 

Step 8: After reloading the website using the green reload button on the Web configuration page, the URL can be used to check the deployed website.

Step 9:





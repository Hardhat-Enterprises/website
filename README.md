# Hardhat Enterprises Deployment Process

1. **Create an Account on PythonAnywhere**
   - Go to [PythonAnywhere](https://www.pythonanywhere.com) and sign up for a free account (Beginner tier).
   - Use the following credentials to log in:
     - Username: `hardhatwebdev2024`
     - Email: `s222340498@deakin.edu.au`
     - Password: `consult lead`
     - Web app domain: `hardhatwebdev2024.pythonanywhere.com`

2. **Clone the GitHub Repository**
   - Open the **Bash console** in PythonAnywhere.
   - Run the following command to clone the GitHub repository:
     ```bash
     git clone https://github.com/Hardhat-Enterprises/website.git
     ```

3. **Create a Virtual Environment**
   - In the Bash console, create a virtual environment by running:
     ```bash
     mkvirtualenv venv
     ```
   - (You can replace `venv` with any other name for the environment.)

4. **Install Dependencies**
   - Install the necessary dependencies by running:
     ```bash
     pip install -r requirements.txt
     ```

5. **Configure the Web Application**
   - In the **Web** tab on the PythonAnywhere dashboard, click the **Web** button.
   - In the **Virtualenv** section, set the virtual environment to the one you created (`venv`).

6. **Configure the WSGI File**
   - In the **Web** configuration page, under the **Code** section, click on the **WSGI Configuration File**.
   - Uncomment the relevant code in the **Django** section and set the path to the cloned repository:
     ```python
     import os
     from django.core.wsgi import get_wsgi_application

     os.environ['DJANGO_SETTINGS_MODULE'] = 'website.settings'
     application = get_wsgi_application()
     ```

7. **Update `settings.py`**
   - Open the `settings.py` file from the **Files** tab.
   - Add the following URL to the `ALLOWED_HOSTS` section:
     ```python
     ALLOWED_HOSTS = ['hardhatwebdev2024.pythonanywhere.com']
     ```

8. **Reload the Website**
   - Once all configurations are set, go back to the **Web** tab and click the green **Reload** button.
   - The website will now be live at the following URL: `https://hardhatwebdev2024.pythonanywhere.com/`.






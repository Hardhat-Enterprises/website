# PostgreSQL Database Migration Documentation

## Overview
This document describes the changes made to upgrade the Django application from SQLite to PostgreSQL. The application can run both in Docker containers and locally using `python manage.py runserver`.

## Changes Made

### 1. Python Dependencies (requirements.txt)
Added PostgreSQL adapter for Python:
```
# Database
psycopg2-binary==2.9.9
```

### 2. Docker Configuration

#### docker-compose.yml
Added a new PostgreSQL service and updated the web service configuration:

**New PostgreSQL Service:**
```yaml
postgres:
  container_name: postgres_db
  image: postgres:15-alpine
  restart: always
  ports:
    - "5432:5432"
  volumes:
    - postgres_data:/var/lib/postgresql/data
  networks:
    - web_network
  environment:
    - POSTGRES_DB=hardhat_db
    - POSTGRES_USER=hardhat_user
    - POSTGRES_PASSWORD=hardhat_pass
  healthcheck:
    test: ["CMD-SHELL", "pg_isready -U hardhat_user"]
    interval: 5s
    timeout: 5s
    retries: 5
```

**Updated Web Service:**
- Added database environment variables:
  ```yaml
  environment:
    - DEBUG=0
    - DB_ENGINE=postgresql
    - DB_NAME=hardhat_db
    - DB_USERNAME=hardhat_user
    - DB_PASS=hardhat_pass
    - DB_HOST=postgres
    - DB_PORT=5432
  ```
- Added dependency on PostgreSQL with health check:
  ```yaml
  depends_on:
    postgres:
      condition: service_healthy
  ```
- Added new volume for PostgreSQL data:
  ```yaml
  volumes:
    postgres_data: {}
  ```

#### Dockerfile
Added PostgreSQL client libraries to system dependencies:
```dockerfile
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*
```

### 3. Django Configuration
The Django settings (`core/settings.py`) already supported multiple database backends through environment variables, so no changes were needed there. The configuration automatically detects the database settings from environment variables:

```python
if DB_ENGINE and DB_NAME and DB_USERNAME:
    DATABASES = { 
      'default': {
        'ENGINE'  : 'django.db.backends.' + DB_ENGINE, 
        'NAME'    : DB_NAME,
        'USER'    : DB_USERNAME,
        'PASSWORD': DB_PASS,
        'HOST'    : DB_HOST,
        'PORT'    : DB_PORT,
        }, 
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }
```

## Database Connection Details

- **Database Engine**: PostgreSQL 15 (Alpine Linux variant for smaller image size)
- **Database Name**: `hardhat_db`
- **Database User**: `hardhat_user`
- **Database Password**: `hardhat_pass`
- **Host**: `postgres` (Docker service name)
- **Port**: `5432` (default PostgreSQL port)

## How to Use

### Option 1: Docker Deployment (Recommended)

1. **Start the application**:
   ```bash
   docker compose up -d
   ```

2. **Check container status**:
   ```bash
   docker ps
   ```

3. **View Django logs**:
   ```bash
   docker logs django_app
   ```

4. **Run Django management commands**:
   ```bash
   docker exec django_app python manage.py <command>
   ```

5. **Connect to PostgreSQL directly**:
   ```bash
   docker exec -it postgres_db psql -U hardhat_user -d hardhat_db
   ```

### Option 2: Local Development (python manage.py runserver)

#### Prerequisites
1. **Install PostgreSQL locally**:
   - Windows: Download from https://www.postgresql.org/download/windows/
   - macOS: `brew install postgresql`
   - Linux: `sudo apt-get install postgresql postgresql-contrib`

2. **Create PostgreSQL database and user**:
   ```sql
   sudo -u postgres psql
   CREATE DATABASE hardhat_db;
   CREATE USER hardhat_user WITH PASSWORD 'hardhat_pass';
   GRANT ALL PRIVILEGES ON DATABASE hardhat_db TO hardhat_user;
   \q
   ```

3. **Install Python dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

#### Configuration

1. **Create a `.env` file** in the project root:
   ```env
   # For local development
   DEBUG=True
   SECRET_KEY=your-secret-key-here
   DB_ENGINE=postgresql
   DB_HOST=localhost
   DB_NAME=hardhat_db
   DB_USERNAME=hardhat_user
   DB_PASS=hardhat_pass
   DB_PORT=5432
   ```

2. **Run migrations**:
   ```bash
   python manage.py migrate
   ```

3. **Create superuser** (optional):
   ```bash
   python manage.py createsuperuser
   ```

4. **Collect static files**:
   ```bash
   python manage.py collectstatic
   ```

5. **Run the development server**:
   ```bash
   python manage.py runserver
   ```

The application will be available at http://localhost:8000/

#### Using Helper Scripts

For convenience, helper scripts are provided:

- **Linux/macOS**: `./run_local.sh`
- **Windows**: `run_local.bat`

These scripts will:
1. Check if `.env` file exists (create from `env.sample` if not)
2. Verify PostgreSQL is running (Linux/macOS only)
3. Install Python dependencies
4. Run database migrations
5. Collect static files
6. Start the development server

To use:
```bash
# Linux/macOS
chmod +x run_local.sh
./run_local.sh

# Windows
run_local.bat
```

#### Switching Between SQLite and PostgreSQL

The application automatically uses PostgreSQL when the database environment variables are set. To use SQLite (default), simply comment out or remove the database variables from your `.env` file:

```env
# Comment these out to use SQLite
# DB_ENGINE=postgresql
# DB_HOST=localhost
# DB_NAME=hardhat_db
# DB_USERNAME=hardhat_user
# DB_PASS=hardhat_pass
# DB_PORT=5432
```

## Data Migration

When switching from SQLite to PostgreSQL for an existing application with data:

1. **Backup SQLite data**:
   ```bash
   python manage.py dumpdata > backup.json
   ```

2. **Start with PostgreSQL**:
   ```bash
   docker compose up -d
   ```

3. **Load data into PostgreSQL**:
   ```bash
   docker exec django_app python manage.py loaddata backup.json
   ```

## Environment Variables

For production deployment, create a `.env` file with:
```env
DB_ENGINE=postgresql
DB_HOST=postgres
DB_NAME=hardhat_db
DB_USERNAME=hardhat_user
DB_PASS=hardhat_pass
DB_PORT=5432
```

## Benefits of PostgreSQL

1. **Better Performance**: PostgreSQL handles concurrent connections better than SQLite
2. **Scalability**: Can handle larger datasets and more complex queries
3. **Advanced Features**: Support for JSON fields, full-text search, and advanced indexing
4. **Production Ready**: Better suited for production environments
5. **Data Integrity**: ACID compliance with better transaction support

## Troubleshooting

### Local Development Issues

1. **PostgreSQL Connection Error**:
   - Ensure PostgreSQL service is running
   - Check credentials in `.env` file
   - Verify PostgreSQL is listening on localhost:5432

2. **Module Not Found Error**:
   - Run `pip install -r requirements.txt`
   - Consider using a virtual environment

3. **Migration Errors**:
   - Drop and recreate the database if switching from SQLite
   - Run `python manage.py migrate --run-syncdb`

4. **Static Files Not Loading**:
   - Run `python manage.py collectstatic`
   - Check `STATIC_ROOT` and `STATIC_URL` settings

### Docker Issues

1. **Connection Issues**: Ensure PostgreSQL is healthy before Django starts (handled by health check)
2. **Migration Issues**: Run `docker exec django_app python manage.py migrate` if needed
3. **Permission Issues**: Check PostgreSQL user permissions
4. **Port Conflicts**: Ensure port 5432 is not in use by another service

## Authentication Flow Improvements

During the PostgreSQL migration, several improvements were made to the user authentication system to enhance user experience and resolve blocking issues.

### Changes Made

#### 1. Sign-up Flow Redirect
**Issue**: After successful OTP verification during sign-up, users were redirected to the home page.
**Solution**: Modified the redirect to send users to the login page after account verification.

**Files Modified**:
- `home/views.py` - Line ~763:
```python
# Changed from: return redirect('/')
# To:
return redirect('login')

# Updated success message
messages.success(request, "Your account has been successfully verified! Your passkeys have been sent via email. Please sign in to continue.")
```

#### 2. reCAPTCHA Disabled for Login
**Issue**: reCAPTCHA v3 was preventing login form submissions, causing users to be unable to sign in.
**Solution**: Permanently disabled reCAPTCHA for login while keeping it available for other forms.

**Backend Changes** (`home/views.py`):
```python
def login_with_otp(request):
    """
    For Login
    """
    if request.method == 'POST':
        # Direct login logic without reCAPTCHA
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        print(f"DEBUG: Login attempt - Username: {username}, Password: HIDDEN")
        
        user = authenticate(request, username=username, password=password)
        # ... rest of login logic
```

**Frontend Changes** (`home/templates/accounts/sign-in.html`):
- Commented out reCAPTCHA script inclusion
- Commented out hidden reCAPTCHA response input
- Commented out reCAPTCHA JavaScript execution

```html
<!-- Hidden Recaptcha Input (Commented out for now) -->
<!-- <input type="hidden" name="g-recaptcha-response" id="g-recaptcha-response"> -->

<!-- reCAPTCHA Script (Commented out for now) -->
<!-- <script src="https://www.google.com/recaptcha/api.js?render={{ RECAPTCHA_SITE_KEY }}"></script> -->

// reCAPTCHA JavaScript (Commented out for now)
/*
grecaptcha.ready(function () {
    grecaptcha.execute('{{ RECAPTCHA_SITE_KEY }}', {action: 'submit'})
    .then(function (token) {
        console.log("reCAPTCHA token generated onload:", token);
        document.getElementById('g-recaptcha-response').value = token;
    });
});
*/
```

#### 3. Improved Password Validation Display
**Issue**: Password validation errors were not clearly displayed to users during sign-up.
**Solution**: Enhanced error message display and added password requirements info box.

**Files Modified**:
- `home/templates/accounts/sign-up.html`:
  - Improved error message display for each field
  - Added password requirements information box
  - Better visual feedback for validation errors

```html
<!-- Password Requirements Info Box -->
<div class="alert alert-info mb-4">
  <h6 class="mb-2"><i class="fas fa-info-circle"></i> Password Requirements</h6>
  <small>Your password must include:</small>
  <ul class="mb-0 small">
    <li>At least 8 characters</li>
    <li>At least one uppercase letter (A-Z)</li>
    <li>At least one lowercase letter (a-z)</li>
    <li>At least one number (0-9)</li>
    <li>At least one special character (@, $, !, %, *, ?, &)</li>
  </ul>
</div>
```

#### 4. OTP Verification Form Fix
**Issue**: JavaScript in OTP verification template was preventing form submission to backend.
**Solution**: Removed client-side validation and ensured proper form submission.

**Files Modified**:
- `home/templates/accounts/verify_token.html`:
  - Removed faulty JavaScript OTP validation
  - Changed form action to proper Django URL
  - Added Django messages display for user feedback
  - Ensured form submits to backend properly

```html
<form action="{% url 'verifyEmail' %}" method="POST">
  {% csrf_token %}
  
  <!-- Django Messages Display -->
  {% if messages %}
    {% for message in messages %}
      <div class="alert alert-{{ message.tags }} alert-dismissible fade show" role="alert">
        {{ message }}
        <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close">×</button>
      </div>
    {% endfor %}
  {% endif %}

  <div class="mb-3">
    <input type="text" class="form-control" name="otp" id="otp" placeholder="Enter OTP" required />
  </div>

  <button type="submit" class="btn btn-primary" style="width: 100%">
    Activate Account
  </button>
</form>
```

### Current Authentication Flow

1. **Sign-up**: User registers → Email validation → OTP verification → **Redirects to Login Page**
2. **Login**: User signs in (no reCAPTCHA) → OTP verification → **Redirects to Profile Page**
3. **Password Requirements**: Clearly displayed with validation feedback
4. **Error Handling**: Improved user feedback throughout the process

#### 5. Login Redirect to Profile
**Issue**: After successful login, users were redirected to the home page.
**Solution**: Modified login flow to redirect users to their profile page for better user experience.

**Files Modified**:
- `home/views.py` - Line ~503:
```python
# Changed from: return redirect('/')
# To:
return redirect('/profile')
```

- `core/settings.py` - Line ~276:
```python
# Changed from: LOGIN_REDIRECT_URL = '/'
# To:
LOGIN_REDIRECT_URL = '/profile'
```

### Benefits

- **Improved User Experience**: Clear flow from sign-up to login
- **Resolved Blocking Issues**: reCAPTCHA no longer prevents login
- **Better Error Feedback**: Users understand what's required
- **Streamlined Process**: Logical flow from registration to authentication

### Notes

- reCAPTCHA remains active on other forms (contact, join project, etc.)
- All reCAPTCHA code is commented out (not deleted) for easy re-enablement if needed
- Login debugging messages are included for troubleshooting

## Security Considerations

1. **Change default passwords** in production
2. **Use environment variables** for sensitive data
3. **Restrict PostgreSQL port** access in production (remove port mapping)
4. **Regular backups** of the PostgreSQL volume
5. **Use SSL/TLS** for database connections in production
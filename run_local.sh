#!/bin/bash
# Script to run Django application locally with PostgreSQL

echo "Starting Django application with local PostgreSQL..."

# Check if .env file exists
if [ ! -f .env ]; then
    echo "Creating .env file from env.sample..."
    cp env.sample .env
    echo ""
    echo "⚠️  IMPORTANT: Please edit .env file with your database credentials!"
    echo "Example configuration:"
    echo "DB_NAME=companywebsite_db"
    echo "DB_USER=django_user"
    echo "DB_PASSWORD=your_secure_password"
    echo "DB_HOST=localhost"
    echo "DB_PORT=5432"
    echo ""
    read -p "Press Enter after you've edited the .env file..."
fi

# Load environment variables
set -a
source .env
set +a

# Determine Python command
PYTHON_CMD="python3"

# Check if python3 is available, fallback to python
if ! command -v python3 > /dev/null 2>&1; then
    if command -v python > /dev/null 2>&1; then
        PYTHON_CMD="python"
    else
        echo "Neither python3 nor python found. Please install Python."
        exit 1
    fi
fi

echo "Using Python: $PYTHON_CMD"

# Create and activate virtual environment
VENV_DIR="venv"
if [ ! -d "$VENV_DIR" ]; then
    echo "Creating Python virtual environment..."
    $PYTHON_CMD -m venv $VENV_DIR
fi

echo "Activating virtual environment..."
source $VENV_DIR/bin/activate

# Upgrade pip in virtual environment
echo "Upgrading pip..."
pip install --upgrade pip

# Install Python requirements in virtual environment
echo "Installing Python dependencies in virtual environment..."
pip install -r requirements.txt

# Check if PostgreSQL is installed
if ! command -v psql > /dev/null 2>&1; then
    echo "PostgreSQL is not installed. Installing PostgreSQL..."
    
    # Detect the Linux distribution and install accordingly
    if command -v apt-get > /dev/null 2>&1; then
        # Ubuntu/Debian
        echo "Detected Ubuntu/Debian system. Installing PostgreSQL..."
        sudo apt-get update
        sudo apt-get install -y postgresql postgresql-contrib postgresql-client
    elif command -v yum > /dev/null 2>&1; then
        # CentOS/RHEL/Fedora
        echo "Detected RedHat-based system. Installing PostgreSQL..."
        sudo yum install -y postgresql-server postgresql-contrib
        sudo postgresql-setup initdb
    elif command -v dnf > /dev/null 2>&1; then
        # Fedora (newer versions)
        echo "Detected Fedora system. Installing PostgreSQL..."
        sudo dnf install -y postgresql-server postgresql-contrib
        sudo postgresql-setup --initdb
    elif command -v pacman > /dev/null 2>&1; then
        # Arch Linux
        echo "Detected Arch Linux system. Installing PostgreSQL..."
        sudo pacman -S postgresql
        sudo -u postgres initdb -D /var/lib/postgres/data
    else
        echo "Unsupported Linux distribution. Please install PostgreSQL manually."
        echo "Visit: https://www.postgresql.org/download/"
        exit 1
    fi
    
    echo "PostgreSQL installation completed!"
fi

# Check if PostgreSQL is running, if not try to start it
if ! pg_isready -h localhost -p 5432 > /dev/null 2>&1; then
    echo "PostgreSQL is not running on localhost:5432"
    echo "Attempting to start PostgreSQL service..."
    
    # Try different methods to start PostgreSQL
    if command -v systemctl > /dev/null 2>&1; then
        echo "Using systemctl to start PostgreSQL..."
        sudo systemctl enable postgresql
        sudo systemctl start postgresql
    elif command -v service > /dev/null 2>&1; then
        echo "Using service command to start PostgreSQL..."
        sudo service postgresql start
    else
        echo "Trying pg_ctlcluster method..."
        sudo pg_ctlcluster 12 main start 2>/dev/null || sudo pg_ctlcluster 13 main start 2>/dev/null || sudo pg_ctlcluster 14 main start 2>/dev/null || sudo pg_ctlcluster 15 main start 2>/dev/null || sudo pg_ctlcluster 16 main start
    fi
    
    # Wait a moment for PostgreSQL to start
    echo "Waiting for PostgreSQL to start..."
    sleep 5
    
    # Check again if PostgreSQL is now running
    if ! pg_isready -h localhost -p 5432 > /dev/null 2>&1; then
        echo "Failed to start PostgreSQL automatically."
        echo "Trying to initialize and start PostgreSQL..."
        
        # Try to initialize PostgreSQL if not initialized
        if command -v systemctl > /dev/null 2>&1; then
            sudo systemctl enable postgresql
            sudo systemctl start postgresql
        fi
        
        # Final check
        sleep 3
        if ! pg_isready -h localhost -p 5432 > /dev/null 2>&1; then
            echo "PostgreSQL still not running. Manual intervention required."
            echo "Please check PostgreSQL installation and configuration."
            exit 1
        fi
    fi
    
    echo "PostgreSQL started successfully!"
else
    echo "PostgreSQL is already running."
fi

# Ensure PostgreSQL user and database exist
echo "Setting up PostgreSQL database and user..."

# Check if environment variables are set
if [ -z "$DB_NAME" ] || [ -z "$DB_USER" ]; then
    echo ""
    echo "❌ Error: DB_NAME or DB_USER not set in .env file"
    echo ""
    echo "Please edit your .env file to include:"
    echo "DB_NAME=companywebsite_db"
    echo "DB_USER=django_user"
    echo "DB_PASSWORD=your_secure_password"
    echo "DB_HOST=localhost"
    echo "DB_PORT=5432"
    echo ""
    echo "Then run this script again."
    exit 1
else
    echo "Creating database user: $DB_USER"
    echo "Creating database: $DB_NAME"
    
    # Create user (will prompt for password)
    sudo -u postgres createuser --interactive --pwprompt $DB_USER 2>/dev/null || echo "User $DB_USER already exists"
    
    # Create database
    sudo -u postgres createdb -O $DB_USER $DB_NAME 2>/dev/null || echo "Database $DB_NAME already exists"
fi

# Run migrations
echo "Running database migrations..."
$PYTHON_CMD manage.py migrate

# Collect static files
echo "Collecting static files..."
$PYTHON_CMD manage.py collectstatic --noinput

# Start the development server
echo ""
echo "🚀 Starting Django development server..."
echo "The server will be available at: http://localhost:8000"
echo "To stop the server, press Ctrl+C"
echo ""
$PYTHON_CMD manage.py runserver
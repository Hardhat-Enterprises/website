#!/bin/bash

# Script to check Docker hardening compliance for Hardhat Enterprises website in the current directory

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
NC='\033[0m' # No Color

# Variables
REPO_DIR="$(pwd)"  # Use current working directory
DOCKERFILE_PATH="$REPO_DIR/Dockerfile"
DOCKERIGNORE_PATH="$REPO_DIR/.dockerignore"
COMPOSE_FILE="$REPO_DIR/docker-compose.yml"
IMAGE_NAME_DJANGO="django_app"
IMAGE_NAME_NGINX="nginx"
COMPLIANCE_STATUS=0  # 0 for compliant, 1 for non-compliant
CHECK_IMAGES=false

# Array to store compliance results
declare -A RESULTS

# Function to check terminal color support
check_color_support() {
    if [ -z "$TERM" ] || [ "$TERM" = "dumb" ] || ! command -v tput > /dev/null 2>&1 || [ "$(tput colors)" -lt 8 ]; then
        echo "Warning: Terminal does not support colors or tput is not available. Output will be plain text."
        RED=""
        GREEN=""
        NC=""
    fi
}

# Function to print help screen
print_help() {
    echo "Usage: $0 <command> [options]"
    echo "Commands:"
    echo "  compliance [--images]  Check hardening compliance of Docker files and optionally images"
    echo "  build                  Build and run the Docker images (not implemented in this mode)"
    echo "  help                   Display this help screen"
    echo "Options:"
    echo "  --images              Include Docker image inspection in compliance check"
    echo "Example:"
    echo "  $0 compliance         # Check file compliance only"
    echo "  $0 compliance --images  # Check files and images"
    exit 0
}

# Function to print compliance result
print_result() {
    local check=$1
    local status=$2
    local message=$3
    RESULTS["$check"]="$status|$message"
    if [ "$status" == "FAIL" ]; then
        COMPLIANCE_STATUS=1
    fi
}

# Function to print compliance table
print_compliance_table() {
    echo
    echo "======================================================================"
    echo "Docker Hardening Compliance Report"
    echo "======================================================================"
    printf "%-35s | %-6s | %-50s\n" "Check" "Status" "Details"
    printf "%-35s | %-6s | %-50s\n" "-----------------------------------" "------" "--------------------------------------------------"

    for check in "${!RESULTS[@]}"; do
        IFS='|' read -r status message <<< "${RESULTS[$check]}"
        if [ "$status" == "PASS" ]; then
            status_colored="${GREEN}PASS${NC}"
        else
            status_colored="${RED}FAIL${NC}"
        fi
        printf "%-35s | %-6b | %-50s\n" "$check" "$status_colored" "$message"
    done

    echo "======================================================================"
    if [ "$COMPLIANCE_STATUS" -eq 0 ]; then
        echo -e "Overall Hardening Status: ${GREEN}Hardened${NC}"
    else
        echo -e "Overall Hardening Status: ${RED}Not Hardened${NC}"
    fi
    echo "======================================================================"
}

# Check terminal color support
check_color_support

# Parse command-line arguments
if [ $# -eq 0 ]; then
    print_help
fi

COMMAND=$1
shift

while [ $# -gt 0 ]; do
    case "$1" in
        --images)
            CHECK_IMAGES=true
            shift
            ;;
        *)
            echo "Unknown option: $1"
            print_help
            ;;
    esac
done

case "$COMMAND" in
    help)
        print_help
        ;;
    compliance)
        # Check if current directory contains requirements.txt
        if [ ! -f "$REPO_DIR/requirements.txt" ]; then
            echo "Error: No requirements.txt found in $REPO_DIR. Ensure you're in the correct repository directory."
            exit 1
        fi

        echo "Checking Docker hardening compliance in $REPO_DIR..."
        echo "=========================================="

        # Step 1: Check Dockerfile compliance
        echo "Checking Dockerfile ($DOCKERFILE_PATH)..."
        if [ ! -f "$DOCKERFILE_PATH" ]; then
            print_result "Dockerfile Existence" "FAIL" "Dockerfile not found at $DOCKERFILE_PATH."
        else
            # Check for minimal base image
            if grep -q "FROM python:3.12-slim" "$DOCKERFILE_PATH"; then
                print_result "Minimal Base Image" "PASS" "Dockerfile uses python:3.12-slim as the base image."
            else
                print_result "Minimal Base Image" "FAIL" "Dockerfile does not use python:3.12-slim."
            fi

            # Check for non-root user
            if grep -q "USER appuser" "$DOCKERFILE_PATH" && grep -q "useradd.*appuser" "$DOCKERFILE_PATH"; then
                print_result "Non-Root User" "PASS" "Dockerfile creates and uses non-root user (appuser)."
            else
                print_result "Non-Root User" "FAIL" "Dockerfile does not define or use a non-root user."
            fi

            # Check for dependency cleanup
            if grep -q "apt-get clean" "$DOCKERFILE_PATH" && grep -q "rm -rf /var/lib/apt/lists" "$DOCKERFILE_PATH"; then
                print_result "Dependency Cleanup" "PASS" "Dockerfile includes cleanup of apt caches."
            else
                print_result "Dependency Cleanup" "FAIL" "Dockerfile does not clean up apt caches."
            fi
        fi

        # Step 2: Check .dockerignore compliance
        echo "Checking .dockerignore ($DOCKERIGNORE_PATH)..."
        if [ ! -f "$DOCKERIGNORE_PATH" ]; then
            print_result ".dockerignore Existence" "FAIL" ".dockerignore not found. Create one to exclude unnecessary files."
        else
            # Check for common exclusions
            expected_patterns=("__pycache__" "*.pyc" "*.pyo" "*.pyd" ".env" "*.log" "*.sqlite3" "staticfiles/" "media/" ".git")
            missing_patterns=()
            for pattern in "${expected_patterns[@]}"; do
                if ! grep -q "^$pattern$" "$DOCKERIGNORE_PATH"; then
                    missing_patterns+=("$pattern")
                fi
            done
            if [ ${#missing_patterns[@]} -eq 0 ]; then
                print_result ".dockerignore Content" "PASS" ".dockerignore includes key exclusions to reduce image size."
            else
                print_result ".dockerignore Content" "FAIL" ".dockerignore is missing patterns: ${missing_patterns[*]}."
            fi
        fi

        # Step 3: Check docker-compose.yml compliance
        echo "Checking docker-compose.yml ($COMPOSE_FILE)..."
        if [ ! -f "$COMPOSE_FILE" ]; then
            print_result "docker-compose.yml Existence" "FAIL" "docker-compose.yml not found at $COMPOSE_FILE."
        else
            # Check for minimal Nginx image
            if grep -q "image: nginx:alpine" "$COMPOSE_FILE"; then
                print_result "Minimal Nginx Image" "PASS" "docker-compose.yml uses nginx:alpine."
            else
                print_result "Minimal Nginx Image" "FAIL" "docker-compose.yml does not use nginx:alpine."
            fi

            # Check for non-root user in web service
            if grep -q "user:.*1000:1000" "$COMPOSE_FILE"; then
                print_result "Non-Root User (Compose)" "PASS" "docker-compose.yml specifies non-root user for web service."
            else
                print_result "Non-Root User (Compose)" "FAIL" "docker-compose.yml does not specify non-root user."
            fi

            # Check for read-only volume
            if grep -q "\.:/app:ro" "$COMPOSE_FILE"; then
                print_result "Read-Only Volume" "PASS" "docker-compose.yml mounts project code as read-only."
            else
                print_result "Read-Only Volume" "FAIL" "docker-compose.yml does not mount project code as read-only."
            fi
        fi

        # Step 4: Check Docker images (if --images flag is used)
        if [ "$CHECK_IMAGES" = true ]; then
            echo "Inspecting Docker images..."
            if docker images -q "$IMAGE_NAME_DJANGO" > /dev/null 2>&1; then
                # Check for non-root user in django_app image
                docker_run_user=$(docker inspect "$IMAGE_NAME_DJANGO" --format '{{.Config.User}}' 2>/dev/null)
                if [ "$docker_run_user" == "1000:1000" ] || [ "$docker_run_user" == "appuser" ]; then
                    print_result "Django Image Non-Root" "PASS" "Django image ($IMAGE_NAME_DJANGO) runs as non-root user."
                else
                    print_result "Django Image Non-Root" "FAIL" "Django image ($IMAGE_NAME_DJANGO) does not run as non-root user."
                fi
            else
                print_result "Django Image Existence" "FAIL" "Django image ($IMAGE_NAME_DJANGO) not found."
            fi

            if docker images -q "$IMAGE_NAME_NGINX" > /dev/null 2>&1; then
                # Check Nginx image base
                nginx_base=$(docker inspect "$IMAGE_NAME_NGINX" --format '{{.Config.Image}}' 2>/dev/null)
                if [ "$nginx_base" == "nginx:alpine" ]; then
                    print_result "Nginx Image Base" "PASS" "Nginx image ($IMAGE_NAME_NGINX) uses nginx:alpine."
                else
                    print_result "Nginx Image Base" "FAIL" "Nginx image ($IMAGE_NAME_NGINX) does not use nginx:alpine."
                fi
            else
                print_result "Nginx Image Existence" "FAIL" "Nginx image ($IMAGE_NAME_NGINX) not found."
            fi
        fi

        # Step 5: Print compliance table
        print_compliance_table
        ;;
    build)
        echo "Build command not implemented in this mode as per request."
        echo "To build and run, use a separate script or run 'docker-compose up --build -d' manually."
        exit 0
        ;;
    *)
        echo "Unknown command: $COMMAND"
        print_help
        ;;
esac

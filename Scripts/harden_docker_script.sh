#!/bin/bash

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
NC='\033[0m'

# Determine the repository directory based on script location
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_DIR="$(dirname "$SCRIPT_DIR")"
DOCKERFILE_PATH="$REPO_DIR/Dockerfile"
DOCKERFILE_PROD_PATH="$REPO_DIR/Dockerfile.prod"
DOCKERIGNORE_PATH="$REPO_DIR/.dockerignore"
COMPOSE_FILE="$REPO_DIR/docker-compose.yml"
COMPOSE_PROD_FILE="$REPO_DIR/docker-compose-prod.yml"
IMAGE_NAME_DJANGO="django_app"
IMAGE_NAME_NGINX="nginx"
COMPLIANCE_STATUS=0
CHECK_IMAGES=false

# Use a simple approach for storing results that works across bash versions
RESULTS_KEYS=""
RESULTS_VALUES=""

check_color_support() {
    if [ -z "$TERM" ] || [ "$TERM" = "dumb" ] || ! command -v tput > /dev/null 2>&1 || [ "$(tput colors)" -lt 8 ]; then
        echo "Warning: Terminal does not support colors or tput is not available. Output will be plain text."
        RED=""
        GREEN=""
        NC=""
    fi
}

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

print_result() {
    local check=$1
    local status=$2
    local message=$3
    
    # Display result immediately
    if [ "$status" == "PASS" ]; then
        echo -e "${YELLOW}$check${NC} : ${GREEN}PASSED${NC}"
    else
        echo -e "${YELLOW}$check${NC} : ${RED}FAILED${NC}"
        if [ -n "$message" ]; then
            echo -e "${YELLOW}Reason${NC} : $message"
        fi
        COMPLIANCE_STATUS=1
    fi
}

print_compliance_table() {
    echo
    echo "======================================================================"
    echo "Docker Hardening Compliance Report"
    echo "======================================================================"
    echo 

    echo "Note: Individual compliance checks are performed during script execution."
    echo "Review the output above for detailed pass/fail results."

    echo "======================================================================"
    if [ "$COMPLIANCE_STATUS" -eq 0 ]; then
        echo -e "Overall Hardening Status : ${GREEN}Hardened${NC}"
    else
        echo -e "Overall Hardening Status : ${RED}Not Hardened${NC}"
    fi
    echo "======================================================================"
}


check_color_support

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
        if [ ! -f "$REPO_DIR/requirements.txt" ]; then
            echo "Error: No requirements.txt found in $REPO_DIR. Ensure you're in the correct repository directory."
            exit 1
        fi
        echo -e "\n=========================================="
        echo "Checking Docker hardening compliance in \"$REPO_DIR\""
        echo "=========================================="

        echo -e "Checking ${YELLOW}Dockerfile ($DOCKERFILE_PATH)${NC}"
        if [ ! -f "$DOCKERFILE_PATH" ]; then
            print_result "Dockerfile Existence" "FAIL" "Dockerfile not found at $DOCKERFILE_PATH."
        else
            if grep -q "FROM python:3.12-slim" "$DOCKERFILE_PATH"; then
                print_result "Minimal Base Image" "PASS" "Dockerfile uses python:3.12-slim as the base image."
            else
                print_result "Minimal Base Image" "FAIL" "Dockerfile does not use python:3.12-slim."
            fi

            if grep -q "USER appuser" "$DOCKERFILE_PATH" && grep -q "useradd.*appuser" "$DOCKERFILE_PATH"; then
                print_result "Non-Root User" "PASS" "Dockerfile creates and uses non-root user (appuser)."
            else
                print_result "Non-Root User" "FAIL" "Dockerfile does not define or use a non-root user."
            fi

            if grep -q "apt-get clean" "$DOCKERFILE_PATH" && grep -q "rm -rf /var/lib/apt/lists" "$DOCKERFILE_PATH"; then
                print_result "Dependency Cleanup" "PASS" "Dockerfile includes cleanup of apt caches."
            else
                print_result "Dependency Cleanup" "FAIL" "Dockerfile does not clean up apt caches."
            fi
        fi

        echo -e "Checking ${YELLOW}.dockerignore ($DOCKERIGNORE_PATH)${NC}"
        if [ ! -f "$DOCKERIGNORE_PATH" ]; then
            print_result ".dockerignore Existence" "FAIL" ".dockerignore not found. Create one to exclude unnecessary files."
        else
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

        echo -e "Checking ${YELLOW}docker-compose.yml ($COMPOSE_FILE)${NC}"
        if [ ! -f "$COMPOSE_FILE" ]; then
            print_result "docker-compose.yml Existence" "FAIL" "docker-compose.yml not found at $COMPOSE_FILE."
        else
            print_result "docker-compose.yml Existence" "PASS" "docker-compose.yml found for development."
            
            # Check development-specific configurations
            if grep -q "DEBUG=1" "$COMPOSE_FILE"; then
                print_result "Development Config" "PASS" "docker-compose.yml properly configured for development."
            else
                print_result "Development Config" "FAIL" "docker-compose.yml missing development configuration."
            fi
        fi

        echo -e "Checking ${YELLOW}docker-compose-prod.yml ($COMPOSE_PROD_FILE)${NC}"
        if [ ! -f "$COMPOSE_PROD_FILE" ]; then
            print_result "docker-compose-prod.yml Existence" "FAIL" "docker-compose-prod.yml not found at $COMPOSE_PROD_FILE."
        else
            print_result "docker-compose-prod.yml Existence" "PASS" "docker-compose-prod.yml found for production."
            
            # Check production-specific configurations
            if grep -q "DEBUG=0" "$COMPOSE_PROD_FILE"; then
                print_result "Production Config" "PASS" "docker-compose-prod.yml properly configured for production."
            else
                print_result "Production Config" "FAIL" "docker-compose-prod.yml missing production configuration."
            fi

            if grep -q "gunicorn" "$COMPOSE_PROD_FILE"; then
                print_result "Production Server" "PASS" "docker-compose-prod.yml uses Gunicorn for production."
            else
                print_result "Production Server" "FAIL" "docker-compose-prod.yml does not use Gunicorn."
            fi
        fi

        if [ "$CHECK_IMAGES" = true ]; then
            echo -e "Inspecting ${YELLOW}Docker images${NC}"
            if docker images -q "$IMAGE_NAME_DJANGO" > /dev/null 2>&1; then
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

        print_compliance_table
        ;;
    build)
        echo -e "\n${GREEN}Docker Build Help Command:${NC}"
        echo -e "=========================================="
        echo -e "To build and run, use a separate script or run ${GREEN}'docker-compose up --build -d'${NC} manually."
        echo -e "=========================================="
        exit 0
        ;;
    *)
        echo "Unknown command: $COMMAND"
        print_help
        ;;
esac

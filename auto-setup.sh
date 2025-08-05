#!/bin/bash

# One-click Developer Setup Script
# Author: Hamza Shahid
# Description: Performs dry-run checks and launches Dockerized Django application (There is still room for improvement)

APP_NAME="Hardhat Enterprises Web App"
ENV_FILE=".env"
ENV_SAMPLE_FILE="env.sample"
COMPOSE_FILE="docker-compose.yml"
HEALTHCHECK_URL="http://localhost:80/health"

# Colors & symbols
GREEN="\033[0;32m"
RED="\033[0;31m"
NC="\033[0m"
TICK="${GREEN}✅${NC}"
CROSS="${RED}❌${NC}"

# Help
show_help() {
  echo "Usage: $0 [OPTION]"
  echo
  echo "  --dry-run     Only perform environment checks"
  echo "  --setup       Run checks and start dockerized app"
  echo "  --help        Show this help message"
}

# Table headers
show_table_header() {
  echo "🔧 Running checks for $APP_NAME..."
  echo
  printf "%-40s | %-10s\n" "Check" "Status"
  printf "%-40s-+-%-10s\n" "$(printf '%.0s-' {1..40})" "$(printf '%.0s-' {1..10})"
}

# Command check
check_command() {
  if command -v "$1" >/dev/null 2>&1; then
    printf "%-40s | %b\n" "$2" "$TICK"
    return 0
  else
    printf "%-40s | %b\n" "$2" "$CROSS"
    return 1
  fi
}

# Docker daemon check
check_docker_running() {
  if docker info >/dev/null 2>&1; then
    printf "%-40s | %b\n" "Docker daemon running" "$TICK"
    return 0
  else
    printf "%-40s | %b\n" "Docker daemon running" "$CROSS"
    echo -e "${RED}❗ Docker is installed but not running. Please start Docker.${NC}"
    return 1
  fi
}

# File check
check_file() {
  [ -f "$1" ] && printf "%-40s | %b\n" "$2" "$TICK" || printf "%-40s | %b\n" "$2" "$CROSS"
}

# Health check
check_health() {
  if curl -s --head --request GET "$HEALTHCHECK_URL" | grep "200 OK" >/dev/null; then
    printf "%-40s | %b\n" "Healthcheck endpoint ($HEALTHCHECK_URL)" "$TICK"
    return 0
  else
    printf "%-40s | %b\n" "Healthcheck endpoint ($HEALTHCHECK_URL)" "$CROSS"
    return 1
  fi
}

# Perform all checks
run_checks() {
  show_table_header

  check_command git "Git installed"
  check_command python3 "Python 3 installed"
  check_command pip3 "pip3 installed"
  check_command docker "Docker installed"
  check_docker_running
  check_command docker-compose "Docker Compose installed"

  check_file "$ENV_SAMPLE_FILE" "env.sample present"
  check_file "$ENV_FILE" ".env present"
  check_file "$COMPOSE_FILE" "docker-compose.yml present"

  check_health
}

# Run setup
run_setup() {
  echo -e "\n🔄 Starting Docker containers...\n"
  docker-compose up --build -d

  echo -e "\n⏳ Waiting for health endpoint..."
  sleep 5

  if check_health; then
    echo -e "\n🎉 ${GREEN}Setup complete. Visit your app at http://localhost:80/health\n"
  else
    echo -e "\n${RED}❌ Setup ran but app is not healthy. Please check logs using 'docker-compose logs'.${NC}\n"
  fi
}

# Main
case "$1" in
  --dry-run)
    run_checks
    ;;
  --setup)
    run_checks
    run_setup
    ;;
  --help | *)
    show_help
    ;;
esac

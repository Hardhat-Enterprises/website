#!/bin/bash

# One-click Developer Setup Script
# Author: Hamza Shahid
# Description: Performs dry-run checks and launches Dockerized Django application (There is still room for improvement)

APP_NAME="Hardhat Enterprises Web App"
ENV_FILE=".env"
ENV_SAMPLE_FILE="env.sample"
COMPOSE_FILE="docker-compose.yml"

# Dynamic health check URLs - will try multiple combinations
DJANGO_URLS=("http://127.0.0.1:8000/health" "http://localhost:8000/health")
NGINX_URLS=("http://127.0.0.1:8080/health" "http://localhost:8080/health")

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

# Health check - tries Django dev server first, then nginx (both localhost and 127.0.0.1)
check_health() {
  # Try Django development server URLs first
  for url in "${DJANGO_URLS[@]}"; do
    if curl -s --head --request GET "$url" | grep "200 OK" >/dev/null; then
      printf "%-40s | %b\n" "Django health endpoint ($url)" "$TICK"
      ACTIVE_HEALTHCHECK_URL="$url"
      return 0
    fi
  done
  
  # Try nginx URLs if Django isn't responding
  for url in "${NGINX_URLS[@]}"; do
    if curl -s --head --request GET "$url" | grep "200 OK" >/dev/null; then
      printf "%-40s | %b\n" "Nginx health endpoint ($url)" "$TICK"
      ACTIVE_HEALTHCHECK_URL="$url"
      return 0
    fi
  done
  
  # No endpoints responded
  printf "%-40s | %b\n" "Health endpoints (localhost/127.0.0.1)" "$CROSS"
  return 1
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
    echo -e "\n🎉 ${GREEN}Setup complete. Active endpoint: $ACTIVE_HEALTHCHECK_URL${NC}"
    echo -e "${GREEN}Available URLs:${NC}"
    echo -e "${GREEN}  Django app: http://localhost:8000 or http://127.0.0.1:8000${NC}"
    echo -e "${GREEN}  Nginx proxy: http://localhost:8080 or http://127.0.0.1:8080${NC}\n"
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

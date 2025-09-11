#!/bin/bash

APP_NAME="Hardhat Enterprises Web App"
ENV_FILE=".env"
ENV_SAMPLE_FILE="env.sample"
COMPOSE_FILE="docker-compose.yml"
HEALTHCHECK_URL="http://localhost:80/health"

GREEN="\033[0;32m"
RED="\033[0;31m"
YELLOW='\033[0;33m'
NC="\033[0m"

show_help() {
  echo "Usage: $0 [OPTION]"
  echo
  echo "  --dry-run     Only perform environment checks"
  echo "  --setup       Run checks and start dockerized app"
  echo "  --help        Show this help message"
}

TICK="${GREEN}Passed${NC}"
CROSS="${RED}Failed${NC}"

show_table_header() {
  echo -e "\n======================================================"
  echo -e "${YELLOW}  Running checks for \"$APP_NAME\"${NC}"
  echo -e "======================================================\n"
}

check_command() {
  if command -v "$1" >/dev/null 2>&1; then
    echo -e "$2 : $TICK"
    return 0
  else
    echo -e "$2 : $CROSS"
    return 1
  fi
}

check_docker_running() {
  if docker info >/dev/null 2>&1; then
    echo -e "Docker daemon running : $TICK"
    return 0
  else
    echo -e "Docker daemon running : $CROSS"
    echo -e "${YELLOW}Docker is installed but not running. Please start Docker.${NC}"
    return 1
  fi
}

check_file() {
  if [ -f "$1" ]; then
    echo -e "$2 : $TICK"
  else
    echo -e "$2 : $CROSS"
  fi
}

check_health() {
  if curl -s --head --request GET "$HEALTHCHECK_URL" | grep "200 OK" >/dev/null; then
    echo -e "Healthcheck endpoint ($HEALTHCHECK_URL) : $TICK"
    return 0
  else
    echo -e "Healthcheck endpoint ($HEALTHCHECK_URL) : $CROSS"
    return 1
  fi
}

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

run_setup() {
  echo -e "\n ${YELLOW}Starting Docker containers...\n${NC}"
  docker-compose up --build -d

  echo -e "\n ${YELLOW}Waiting for health endpoint...${NC}"
  sleep 5

  if check_health; then
    echo -e "\n${GREEN}Setup complete. Visit your app at http://localhost:80/health\n"
  else
    echo -e "\n${RED}Setup ran but app is not healthy. Please check logs using 'docker-compose logs'.${NC}\n"
  fi
}

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

#!/bin/bash

APP_NAME="Hardhat Enterprises Web App"
ENV_FILE=".env"
ENV_SAMPLE_FILE="env.sample"

# Default to development mode
MODE="dev"
COMPOSE_FILE="docker-compose.yml"
HEALTHCHECK_URLS=("http://localhost:8000/health" "http://127.0.0.1:8000/health" "http://localhost:8080/health" "http://127.0.0.1:8080/health")

GREEN="\033[0;32m"
RED="\033[0;31m"
YELLOW='\033[0;33m'
NC="\033[0m"

show_help() {
  echo "Usage: $0 [OPTION]"
  echo
  echo "  --dry-run     Only perform environment checks"
  echo "  --dev         Run checks and start development environment (default)"
  echo "  --prod        Run checks and start production environment"
  echo "  --setup       Run checks and start dockerized app (legacy - uses dev mode)"
  echo "  --help        Show this help message"
  echo
  echo "Development mode (--dev):"
  echo "  - Uses docker-compose.yml"
  echo "  - Django dev server on port 8000"
  echo "  - Nginx proxy on port 8080"
  echo "  - PostgreSQL on port 5433"
  echo "  - Health checks: http://localhost:8000/health, http://localhost:8080/health"
  echo
  echo "Production mode (--prod):"
  echo "  - Uses docker-compose-prod.yml"
  echo "  - Gunicorn server behind Nginx on port 80"
  echo "  - PostgreSQL on port 5432"
  echo "  - Health check: http://localhost/health"
}

TICK="${GREEN}Passed${NC}"
CROSS="${RED}Failed${NC}"

set_mode_config() {
  if [ "$MODE" = "prod" ]; then
    COMPOSE_FILE="docker-compose-prod.yml"
    HEALTHCHECK_URLS=("http://localhost/health" "http://127.0.0.1/health")
    echo -e "${YELLOW}Production mode selected${NC}"
  else
    COMPOSE_FILE="docker-compose.yml"
    HEALTHCHECK_URLS=("http://localhost:8000/health" "http://127.0.0.1:8000/health" "http://localhost:8080/health" "http://127.0.0.1:8080/health")
    echo -e "${YELLOW}Development mode selected${NC}"
  fi
}

show_table_header() {
  echo -e "\n======================================================"
  echo -e "${YELLOW}  Running checks for \"$APP_NAME\" ($MODE mode)${NC}"
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
  local health_found=false
  local active_url=""
  
  for url in "${HEALTHCHECK_URLS[@]}"; do
    if curl -s --head --request GET "$url" | grep "200 OK" >/dev/null; then
      echo -e "Health endpoint ($url) : $TICK"
      health_found=true
      active_url="$url"
      break
    fi
  done
  
  if [ "$health_found" = false ]; then
    echo -e "Health endpoints (${HEALTHCHECK_URLS[*]}) : $CROSS"
    return 1
  fi
  
  return 0
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
  
  if [ "$MODE" = "prod" ]; then
    check_file "$COMPOSE_FILE" "docker-compose-prod.yml present"
  else
    check_file "$COMPOSE_FILE" "docker-compose.yml present"
  fi

  check_health
}

run_setup() {
  echo -e "\n ${YELLOW}Starting Docker containers ($MODE mode)...\n${NC}"
  
  if [ "$MODE" = "prod" ]; then
    docker-compose -f docker-compose-prod.yml up --build -d
  else
    docker-compose up --build -d
  fi

  echo -e "\n ${YELLOW}Waiting for health endpoint...${NC}"
  sleep 10

  if check_health; then
    if [ "$MODE" = "prod" ]; then
      echo -e "\n${GREEN}✅ Production setup complete!${NC}"
      echo -e "${GREEN}🌐 Application available at: http://localhost${NC}"
      echo -e "${GREEN}📊 Health check: http://localhost/health${NC}\n"
    else
      echo -e "\n${GREEN}✅ Development setup complete!${NC}"
      echo -e "${GREEN}🌐 Django app: http://localhost:8000${NC}"
      echo -e "${GREEN}🌐 Nginx proxy: http://localhost:8080${NC}"
      echo -e "${GREEN}📊 Health checks available at both URLs${NC}\n"
    fi
  else
    echo -e "\n${RED}❌ Setup ran but app is not healthy.${NC}"
    if [ "$MODE" = "prod" ]; then
      echo -e "${RED}Please check logs using 'docker-compose -f docker-compose-prod.yml logs'.${NC}\n"
    else
      echo -e "${RED}Please check logs using 'docker-compose logs'.${NC}\n"
    fi
  fi
}

# Parse arguments
case "$1" in
  --prod)
    MODE="prod"
    set_mode_config
    run_checks
    run_setup
    ;;
  --dev)
    MODE="dev" 
    set_mode_config
    run_checks
    run_setup
    ;;
  --setup)
    # Legacy option - defaults to dev mode
    MODE="dev"
    set_mode_config
    run_checks
    run_setup
    ;;
  --dry-run)
    # Use default mode for dry run, but allow override with second argument
    if [ "$2" = "--prod" ]; then
      MODE="prod"
    fi
    set_mode_config
    run_checks
    ;;
  --help | *)
    show_help
    ;;
esac

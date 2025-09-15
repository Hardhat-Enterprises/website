#!/bin/bash
set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
NC='\033[0m'

check_color_support() {
    if [ -z "$TERM" ] || [ "$TERM" = "dumb" ] || ! command -v tput > /dev/null 2>&1 || [ "$(tput colors)" -lt 8 ]; then
        echo "Warning: Terminal doesnt support colors or tput is not available. Output will be plain text."
        RED=""
        GREEN=""
        YELLOW=""
        BLUE=""
        NC=""
    fi
}

show_help() {
  echo "Usage: $0 [option]"
  echo
  echo "Options:"
  echo "  --install        Install pre-commit and set up git hooks"
  echo "  --check          Verify if pre-commit hooks are installed"
  echo "  --run            Run pre-commit on staged files"
  echo "  --run-all        Run pre-commit on all files"
  echo "  --update         Update all hooks to latest version"
  echo "  --uninstall      Remove pre-commit hooks"
  echo "  --list           Show all hooks configured in .pre-commit-config.yaml"
  echo "  --config         Display contents of .pre-commit-config.yaml"
  echo "  --help           Show this help message"
  echo
}

case "$1" in
  --install)
    echo -e "\n${YELLOW}Installing pre-commit...${NC}"

    if command -v pipx >/dev/null 2>&1; then
      pipx install pre-commit --force
      echo -e "${GREEN}Installed with pipx${NC}"

    elif command -v pip >/dev/null 2>&1; then
      if grep -qi "Debian" /etc/os-release 2>/dev/null || grep -qi "Ubuntu" /etc/os-release 2>/dev/null; then
        pip install pre-commit --break-system-packages --force
      else
        pip install pre-commit --force
      fi
      echo -e "${GREEEN}Installed with pip${NC}"

    elif command -v pip3 >/dev/null 2>&1; then
      if grep -qi "Debian" /etc/os-release 2>/dev/null || grep -qi "Ubuntu" /etc/os-release 2>/dev/null; then
        pip3 install pre-commit --break-system-packages --force
      else
        pip3 install pre-commit --force
      fi
      echo -e "${GREEN}Installed with pip3${NC}"

    else
      echo -e "${RED}No pipx, pip, or pip3 found.${NC} Please install Python."
      exit 1
    fi

    pre-commit install
    echo -e "${GREEN}Pre-commit installed and hooks configured.${NC}"
    ;;
  --run)
    echo -e "\n${YELLOW}Running pre-commit on staged files...${NC}"
    pre-commit run
    ;;

  --run-all)
    echo -e "${YELLOW}Running pre-commit on all files...${NC}"
    pre-commit run --all-files
    ;;

  --update)
    echo -e "${YELLOW}Updating pre-commit hooks...${NC}"
    pre-commit autoupdate
    ;;

  --uninstall)
    echo -e "${YELLOW}Removing pre-commit hooks...${NC}"
    pre-commit uninstall
    ;;

  --list)
    if [ -f "../.pre-commit-config.yaml" ]; then
      echo -e "\n${GREEN}Configured hooks from (.pre-commit-config.yaml):${NC}"
      grep "id:" ../.pre-commit-config.yaml | awk '{print ("➜  " $3)}'
    else
      echo -e "${YELLOW}No .pre-commit-config.yaml found!${NC}"
    fi
    ;;

  --check)
    if [ -f "../.git/hooks/pre-commit" ]; then
      echo -e "\n${GREEN}Pre-commit is installed.${NC} Path: ../.git/hooks/pre-commit"
    else
      echo -e "${RED}Pre-commit is NOT installed.${NC} Run with --install"
    fi
    ;;

  --config)
    if [ -f "../.pre-commit-config.yaml" ]; then
      echo -e "\n${YELLOW}Config File \".pre-commit-config.yaml\" contents:${NC}\n"
      cat ../.pre-commit-config.yaml
    else
      echo -e "\n${YELLOW}No .pre-commit-config.yaml found!${NC}"
    fi
    ;;

  --help|*)
    show_help
    check_color_support
    ;;
esac

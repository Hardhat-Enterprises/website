#!/bin/bash
set -e

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
    echo "🔧 Installing pre-commit..."

    # Prefer pipx if available (best for cross-OS app installs)
    if command -v pipx >/dev/null 2>&1; then
      pipx install pre-commit --force
      echo "✅ Installed with pipx"

    # Else try pip
    elif command -v pip >/dev/null 2>&1; then
      if grep -qi "Debian" /etc/os-release 2>/dev/null || grep -qi "Ubuntu" /etc/os-release 2>/dev/null; then
        pip install pre-commit --break-system-packages --force
      else
        pip install pre-commit --force
      fi
      echo "✅ Installed with pip"

    # Else try pip3
    elif command -v pip3 >/dev/null 2>&1; then
      if grep -qi "Debian" /etc/os-release 2>/dev/null || grep -qi "Ubuntu" /etc/os-release 2>/dev/null; then
        pip3 install pre-commit --break-system-packages --force
      else
        pip3 install pre-commit --force
      fi
      echo "✅ Installed with pip3"

    else
      echo "❌ No pipx, pip, or pip3 found. Please install Python."
      exit 1
    fi

    pre-commit install
    echo "✅ Pre-commit installed and hooks configured."
    ;;
  --run)
    echo "▶ Running pre-commit on staged files..."
    pre-commit run
    ;;

  --run-all)
    echo "▶ Running pre-commit on all files..."
    pre-commit run --all-files
    ;;

  --update)
    echo "⬆️ Updating pre-commit hooks..."
    pre-commit autoupdate
    ;;

  --uninstall)
    echo "🗑️ Removing pre-commit hooks..."
    pre-commit uninstall
    ;;

  --list)
    if [ -f ".pre-commit-config.yaml" ]; then
      echo "📋 Configured hooks from (.pre-commit-config.yaml):"
      grep "id:" .pre-commit-config.yaml | awk '{print ("➜  " $3)}'
    else
      echo "⚠️ No .pre-commit-config.yaml found!"
    fi
    ;;

  --check)
    if [ -f ".git/hooks/pre-commit" ]; then
      echo "✅ Pre-commit is installed."
    else
      echo "❌ Pre-commit is NOT installed. Run with --install"
    fi
    ;;

  --config)
    if [ -f ".pre-commit-config.yaml" ]; then
      echo "📜 .pre-commit-config.yaml contents:"
      cat .pre-commit-config.yaml
    else
      echo "⚠️ No .pre-commit-config.yaml found!"
    fi
    ;;

  --help|*)
    show_help
    ;;
esac

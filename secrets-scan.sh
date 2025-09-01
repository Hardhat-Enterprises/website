#!/bin/bash
# ==================================================
# Universal TruffleHog Secrets Scanner
# Cross-platform pre-push hook installer
# Auto-detects install paths and permissions
# ==================================================

HOOK_FILE=".git/hooks/pre-push"

# --- Colors ---
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
BOLD='\033[1m'
RESET='\033[0m'

error()   { echo -e "${RED}${BOLD}ERROR:${RESET} $*"; }
success() { echo -e "${GREEN}${BOLD}SUCCESS:${RESET} $*"; }
warn()    { echo -e "${YELLOW}${BOLD}WARNING:${RESET} $*"; }
info()    { echo -e "${BLUE}${BOLD}INFO:${RESET} $*"; }

# --- Determine platform ---
OS=$(uname | tr '[:upper:]' '[:lower:]')

# --- Install TruffleHog ---
install_trufflehog() {
    if command -v trufflehog &>/dev/null; then
        success "TruffleHog already installed."
        return
    fi

    warn "Installing TruffleHog..."

    # --- Linux/macOS ---
    if [[ "$OS" == "linux" || "$OS" == "darwin" ]]; then
        if [ -w /usr/local/bin ]; then
            INSTALL_DIR="/usr/local/bin"
        else
            INSTALL_DIR="$HOME/.local/bin"
            mkdir -p "$INSTALL_DIR"
            export PATH=$PATH:$INSTALL_DIR
        fi

        curl -sSfL https://raw.githubusercontent.com/trufflesecurity/trufflehog/main/scripts/install.sh \
            | sudo sh -s -- -b "$INSTALL_DIR"

    # --- Windows Git Bash / WSL ---
    elif [[ "$OS" == *"mingw"* || "$OS" == *"msys"* || "$OS" == *"cygwin"* ]]; then
        INSTALL_DIR="$USERPROFILE/AppData/Local/Programs/trufflehog"
        mkdir -p "$INSTALL_DIR"
        curl -sSfL https://raw.githubusercontent.com/trufflesecurity/trufflehog/main/scripts/install.sh \
            | sudo sh -s -- -b "$INSTALL_DIR"
        export PATH=$PATH:$INSTALL_DIR
    else
        error "Unsupported OS: $OS"
        exit 1
    fi

    if command -v trufflehog &>/dev/null; then
        success "TruffleHog installed in $INSTALL_DIR."
    else
        error "Failed to install TruffleHog."
        exit 1
    fi
}

# --- Install pre-push hook ---
install_hook() {
    install_trufflehog

    if [ -f "$HOOK_FILE" ]; then
        warn "Pre-push hook already exists."
        return
    fi

    cat > "$HOOK_FILE" <<'EOF'
#!/bin/bash
RED='\033[0;31m'; GREEN='\033[0;32m'; YELLOW='\033[0;33m'; BOLD='\033[1m'; RESET='\033[0m'
error()   { echo -e "${RED}${BOLD}ERROR:${RESET} $*"; }
success() { echo -e "${GREEN}${BOLD}SUCCESS:${RESET} $*"; }
warn()    { echo -e "${YELLOW}${BOLD}WARNING:${RESET} $*"; }
info()    { echo -e "${BOLD}INFO:${RESET} $*"; }

info "Running TruffleHog on staged files..."
STAGED_FILES=$(git diff --cached --name-only)
if [ -z "$STAGED_FILES" ]; then
    info "No staged files."
    exit 0
fi

FAILED=0
for file in $STAGED_FILES; do
    if [ -f "$file" ]; then
        trufflehog filesystem "$file" --no-update || FAILED=1
    fi
done

if [ $FAILED -ne 0 ]; then
    error "Secrets detected! Push blocked."
    exit 1
fi

success "No secrets detected."
EOF

    chmod +x "$HOOK_FILE"
    success "Pre-push hook installed."
}

# --- Status check ---
status_hook() {
    if [ -f "$HOOK_FILE" ]; then
        success "Pre-push hook is installed."
    else
        error "No pre-push hook found."
    fi
}

# --- Uninstall hook ---
uninstall_hook() {
    if [ -f "$HOOK_FILE" ]; then
        rm "$HOOK_FILE"
        sudo rm /usr/local/bin/trufflehog
        success "Pre-push hook removed."
    else
        warn "No pre-push hook to remove."
    fi
}

# --- Manual scan ---
scan_path() {
    TARGET="${1:-.}"
    install_trufflehog
    info "Scanning $TARGET for secrets..."
    trufflehog filesystem "$TARGET" --no-update
}

# --- Help menu ---
show_help() {
    echo "Usage: $0 {install|status|uninstall|scan <PATH>}"
    echo
    echo "Commands:"
    echo "  install        Install pre-push hook and TruffleHog"
    echo "  status         Check if pre-push hook is installed"
    echo "  uninstall      Remove pre-push hook"
    echo "  scan PATH      Scan a directory or file manually (defaults to current dir)"
}

# --- Main ---
case "$1" in
    install) install_hook ;;
    status) status_hook ;;
    uninstall) uninstall_hook ;;
    scan) scan_path "$2" ;;
    *) show_help ;;
esac

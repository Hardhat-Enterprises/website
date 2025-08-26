#!/bin/bash
# ==================================================
# 🔐 Universal TruffleHog Secrets Scanner
# Cross-platform pre-push hook installer
# Auto-detects install paths and permissions
# ==================================================

HOOK_FILE=".git/hooks/pre-push"

# --- Determine platform ---
OS=$(uname | tr '[:upper:]' '[:lower:]')

# --- Install TruffleHog ---
install_trufflehog() {
    if command -v trufflehog &>/dev/null; then
        echo "✅ TruffleHog already installed."
        return
    fi

    echo "⚠️  Installing TruffleHog..."

    # --- Linux/macOS ---
    if [[ "$OS" == "linux" || "$OS" == "darwin" ]]; then
        # Check if /usr/local/bin is writable
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
        echo "❌ Unsupported OS: $OS"
        exit 1
    fi

    if command -v trufflehog &>/dev/null; then
        echo "✅ TruffleHog installed in $INSTALL_DIR."
    else
        echo "❌ Failed to install TruffleHog."
        exit 1
    fi
}

# --- Install pre-push hook ---
install_hook() {
    install_trufflehog

    if [ -f "$HOOK_FILE" ]; then
        echo "⚠️  Pre-push hook already exists."
        return
    fi

    cat > "$HOOK_FILE" <<'EOF'
#!/bin/bash
echo "🔍 Running TruffleHog on staged files..."

STAGED_FILES=$(git diff --cached --name-only)
if [ -z "$STAGED_FILES" ]; then
    echo "ℹ️  No staged files."
    exit 0
fi

FAILED=0
for file in $STAGED_FILES; do
    if [ -f "$file" ]; then
        trufflehog filesystem "$file" --no-update || FAILED=1
    fi
done

if [ $FAILED -ne 0 ]; then
    echo "❌ Secrets detected! Push blocked."
    exit 1
fi

echo "✅ No secrets detected."
EOF

    chmod +x "$HOOK_FILE"
    echo "✅ Pre-push hook installed."
}

# --- Status check ---
status_hook() {
    if [ -f "$HOOK_FILE" ]; then
        echo "✅ Pre-push hook is installed."
    else
        echo "❌ No pre-push hook found."
    fi
}

# --- Uninstall hook ---
uninstall_hook() {
    if [ -f "$HOOK_FILE" ]; then
        rm "$HOOK_FILE"
        sudo rm /usr/local/bin/trufflehog
        echo "✅ Pre-push hook removed."
    else
        echo "⚠️  No pre-push hook to remove."
    fi
}

# --- Manual scan ---
scan_path() {
    TARGET="${1:-.}"
    install_trufflehog
    echo "🔍 Scanning $TARGET for secrets..."
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

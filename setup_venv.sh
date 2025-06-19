#!/bin/bash

pipx install poetry
poetry config virtualenvs.in-project true
eval "$(poetry env activate)"
poetry install

# Setup interpreter which uses Python from the virtual env
# Ensure jq is available
if ! command -v jq &> /dev/null; then
    echo "❌ 'jq' is required but not installed. Install it with: sudo apt install jq"
    exit 1
fi

# Get the Python interpreter path from Poetry
VENV_PYTHON=$(poetry run which python)

# Ensure the .vscode directory exists
mkdir -p .vscode

SETTINGS_FILE=".vscode/settings.json"

# If settings.json exists, update it; else, create a new one
if [ -f "$SETTINGS_FILE" ]; then
    # Use jq to update or add the key
    jq --arg pythonPath "$VENV_PYTHON" \
       '. + { "python.defaultInterpreterPath": $pythonPath }' \
       "$SETTINGS_FILE" > "${SETTINGS_FILE}.tmp" && mv "${SETTINGS_FILE}.tmp" "$SETTINGS_FILE"
else
    # Create new settings file with just the interpreter
    cat > "$SETTINGS_FILE" <<EOF
{
  "python.defaultInterpreterPath": "$VENV_PYTHON"
}
EOF
fi

echo "✅ VS Code Python interpreter set to: $VENV_PYTHON"
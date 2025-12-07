#!/bin/bash
# gitbro installer

set -e

VENV_PATH="venv"

echo "🧠 Installing gitbro - AI-Powered Git CLI Tool"
echo ""

# Check prerequisites
command -v git >/dev/null 2>&1 || { echo "❌ Git is required"; exit 1; }
command -v python3 >/dev/null 2>&1 || { echo "❌ Python 3 is required"; exit 1; }

# Create virtual environment
if [ ! -d "$VENV_PATH" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv "$VENV_PATH"
fi

# Activate and install
source "$VENV_PATH/bin/activate"
echo "📥 Installing dependencies..."
pip install --quiet --upgrade pip
pip install --quiet -r requirements.txt

# Make executable
chmod +x bin/gitbro

deactivate

echo ""
echo "✅ Installation complete!"
echo ""
echo "📋 Quick Start:"
echo "   1. Setup provider:  ./bin/gitbro setup"
echo "   2. Generate commit: ./bin/gitbro commit"
echo ""
echo "🔧 Add to PATH for global access:"
echo "   export PATH=\"\$PATH:$(pwd)/bin\""
echo ""
echo "💡 Or install with pip (recommended):"
echo "   pip install -e ."

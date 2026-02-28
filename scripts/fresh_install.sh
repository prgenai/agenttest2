#!/bin/bash
# Fresh installation script for Jack
# This script sets up the database and ensures all tables are created properly

set -e  # Exit on any error

echo "🦆 Jack Fresh Installation"
echo "================================="

# Get the project root directory
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$PROJECT_ROOT"

echo "📁 Project root: $PROJECT_ROOT"

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found. Please create it first:"
    echo "   python -m venv venv"
    echo "   source venv/bin/activate"
    echo "   pip install -r requirements.txt"
    exit 1
fi

# Activate virtual environment
source venv/bin/activate

echo "🗄️  Setting up database..."

# Remove existing database if it exists (for fresh install)
if [ -f "data/jack.db" ]; then
    echo "⚠️  Removing existing database..."
    rm data/jack.db
fi

# Run database migrations
echo "🔄 Running database migrations..."
alembic upgrade head

# Verify database setup
echo "✅ Verifying database setup..."
python scripts/setup_database.py

echo ""
echo "🎉 Fresh installation completed successfully!"
echo ""
echo "🚀 You can now start Jack:"
echo "   # Backend (in one terminal):"
echo "   source venv/bin/activate"
echo "   python run.py"
echo ""
echo "   # Frontend (in another terminal):"
echo "   cd frontend"
echo "   npm install"
echo "   npm run dev"
echo ""
echo "🌐 Then visit http://localhost:5173"
echo "📧 Default login: admin@example.com / admin"
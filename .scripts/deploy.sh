#!/bin/bash
set -euo pipefail

echo "🚀 Deployment started at $(date)"

APP_DIR="/home/ubuntu/jagyat"  # Set your project path here
VENV_DIR="$APP_DIR/venv"           # Virtual environment directory

cd "$APP_DIR"
echo "📂 Changed to project directory: $APP_DIR"

# Ensure Git is clean before pulling
echo "🔄 Pulling latest code from GitHub..."
git reset --hard HEAD
git pull origin main
echo "✅ Code updated."

# Activate Virtual Env
if [ -f "$VENV_DIR/bin/activate" ]; then
  source "$VENV_DIR/bin/activate"
  echo "🟢 Virtual environment activated!"
else
  echo "❌ Virtual environment not found!"
  exit 1
fi

# Install dependencies safely
echo "📦 Installing dependencies..."
# pip install --upgrade pip
# pip install -r requirements.txt

# Collect static files
# echo "🎨 Collecting static files..."
# python manage.py collectstatic --noinput

# Apply migrations
echo "🛠️ Running migrations..."
python manage.py makemigrations --noinput
python manage.py migrate --noinput

# Optional: Restart services like Gunicorn or Supervisor
echo "🔁 Restarting Gunicorn..."
sudo systemctl restart jagyat.gunicorn

# Reload application (alternative method)
# touch "$APP_DIR/miniblog/wsgi.py"

# Deactivate
deactivate
echo "🔴 Virtual environment deactivated."

echo "✅ Deployment finished at $(date) - KuldeepSaini65"

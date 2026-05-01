#!/bin/bash

echo "🚀 Starting MindEase Development Servers..."
echo ""

echo "📦 Installing frontend dependencies (if needed)..."
cd frontend && npm install
echo ""

echo "✅ Starting Django backend on http://localhost:8000"
cd ../prutha
./venv/bin/python manage.py runserver &
DJANGO_PID=$!

sleep 3

echo "✅ Starting React frontend on http://localhost:5173"
cd ../frontend
npm run dev &
REACT_PID=$!

echo ""
echo "🎉 Both servers are running!"
echo "   - Django Backend: http://localhost:8000"
echo "   - React Frontend: http://localhost:5173"
echo ""
echo "Press Ctrl+C to stop both servers"
echo ""

trap "kill $DJANGO_PID $REACT_PID" EXIT

wait

# MindEase React Frontend

A modern, animated React frontend for the MindEase mental health counseling platform.

## Features

- Built with React + Vite
- Smooth animations using Framer Motion
- Modern, responsive design
- Gradient accents and professional styling
- Integrates with existing Django backend

## Tech Stack

- React 18
- Vite
- Framer Motion (animations)
- React Router DOM
- Lucide React (icons)
- Axios (API calls)

## Getting Started

1. Install dependencies:
```bash
cd frontend
npm install
```

2. Start the development server:
```bash
npm run dev
```

The frontend will run on `http://localhost:5173`

3. Make sure the Django backend is running on `http://localhost:8000`

## Project Structure

```
frontend/
├── src/
│   ├── components/       # Reusable components
│   │   ├── Navigation.jsx
│   │   ├── Hero.jsx
│   │   ├── Features.jsx
│   │   ├── Benefits.jsx
│   │   └── Footer.jsx
│   ├── pages/           # Page components
│   │   └── HomePage.jsx
│   ├── styles/          # CSS modules
│   │   ├── Navigation.css
│   │   ├── Hero.css
│   │   ├── Features.css
│   │   ├── Benefits.css
│   │   └── Footer.css
│   ├── App.jsx          # Main app component
│   └── main.jsx         # Entry point
├── index.html
└── vite.config.js       # Vite configuration
```

## Integration with Django

The React frontend communicates with the Django backend through proxied requests configured in `vite.config.js`. All Django URLs are preserved and work seamlessly with the new frontend.

## Design Highlights

- Cyan (#06b6d4) and Purple (#7c3aed) gradient theme
- Smooth scroll animations
- Floating elements with parallax effects
- Professional card-based layouts
- Mobile-responsive design

## Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run preview` - Preview production build

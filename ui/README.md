# UI for Distributed Seat Reservation System

This directory contains the user interface (UI) components for the Distributed Seat Reservation System. The UI is built using Typescript, React, Tailwindcss and Vite.

## Prerequisites

Before you begin, ensure you have met the following requirements:

- You have Flask server running for backend services. Without the backend, the UI will show blank page.

## Getting Started

To get started with the UI, follow these steps:

1. **Install Dependencies**: Navigate to the `ui` directory and run `npm install` to install all necessary dependencies.
2. **Run the Development Server**: Use `npm run dev` to start the development server. This will allow you to view the UI in your web browser at `http://localhost:5173`.

Check main.tsx for available routes. Following routes are available:

- `/` - Home page (empty)
- `/movies` - List of movies
- `/showtimes` - List of showtimes
- `/movies/:id` - Movie details
- `/movies/:id/seats` - Seat selection for a movie

# Meeting Preparation Assistant - React Frontend

This React application provides a user-friendly interface for the PrepForMeeting CrewAI project. It allows users to input meeting details and generate preparation materials using the CrewAI backend.

## Features

- Input form for meeting details (participants, company, context, objective, prior interactions)
- Real-time progress tracking
- Display of generated meeting preparation materials
- Download option for PowerPoint presentations

## Installation

### Prerequisites

- Node.js (v14 or later)
- npm or yarn
- Python 3.10-3.13 (for the backend)

### Setup

1. Install frontend dependencies:

```bash
cd react-frontend
npm install
```

2. Install backend dependencies:

```bash
pip install flask flask-cors
```

## Running the Application

### Start the Backend API Server

```bash
cd api
python server.py
```

This will start the Flask API server on port 5000.

### Start the React Frontend

In a separate terminal:

```bash
cd react-frontend
npm start
```

This will start the React development server on port 3000. The application will be available at http://localhost:3000.

## How It Works

1. The React frontend collects user input for meeting preparation
2. When the form is submitted, it sends the data to the Flask API
3. The API creates a temporary environment with the user's inputs
4. The API runs the CrewAI application with these inputs
5. Progress is tracked and displayed to the user
6. When complete, the generated materials are displayed and available for download

## Integration with CrewAI

The application integrates with the existing CrewAI project by:

1. Creating a temporary modified version of main.py that reads from environment variables
2. Passing user inputs through environment variables
3. Running the CrewAI process with the modified main.py
4. Capturing the output (report.md or PowerPoint files)
5. Serving these files back to the frontend

## Customization

You can customize the application by:

- Modifying the UI components in `App.js`
- Adding additional input fields as needed
- Changing the styling using Material-UI themes
- Extending the backend API in `server.py` to support additional features

## Troubleshooting

- If you encounter CORS issues, ensure the Flask server has CORS enabled
- Check that the CrewAI application is properly installed and configured
- Verify that the paths in server.py match your project structure
- Check the Flask server logs for any errors during execution

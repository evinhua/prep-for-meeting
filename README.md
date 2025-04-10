# PrepForMeeting Crew

Welcome to the PrepForMeeting Crew project, powered by [crewAI](https://crewai.com). This template is designed to help you set up a multi-agent AI system with ease, leveraging the powerful and flexible framework provided by crewAI. Our goal is to enable your agents to collaborate effectively on complex tasks, maximizing their collective intelligence and capabilities.

## Installation

Ensure you have Python >=3.10 <=3.13 installed on your system. This project uses [UV](https://docs.astral.sh/uv/) for dependency management and package handling, offering a seamless setup and execution experience.

First, if you haven't already, install uv:

```bash
pip install uv
```

Next, navigate to your project directory and install the dependencies:

1. First lock the dependencies and then install them:
```bash
uv lock
```
```bash
uv sync
```
### Customizing

**Add your `OPENAI_API_KEY` into the `.env` file**

- Modify `src/prep_for_meeting/config/agents.yaml` to define your agents
- Modify `src/prep_for_meeting/config/tasks.yaml` to define your tasks
- Modify `src/prep_for_meeting/crew.py` to add your own logic, tools and specific args
- Modify `src/prep_for_meeting/main.py` to add custom inputs for your agents and tasks

## Running the Project

To kickstart your crew of AI agents and begin task execution, run this from the root folder of your project:

```bash
$ crewai run
```
or
```bash
uv run prep_for_meeting
```

This command initializes the prep-for-meeting Crew, assembling the agents and assigning them tasks as defined in your configuration.

This example, unmodified, will create a `report.md` file with the output of research on LLMs in the root folder. The report now includes a PowerPoint presentation outline embedded within it.

## Understanding Your Crew

The prep-for-meeting Crew is composed of multiple AI agents, each with unique roles, goals, and tools. These agents collaborate on a series of tasks, defined in `config/tasks.yaml`, leveraging their collective skills to achieve complex objectives. The `config/agents.yaml` file outlines the capabilities and configurations of each agent in your crew.

## React Frontend Deployment

This project includes a React frontend that provides a user-friendly interface for interacting with the CrewAI backend. To deploy the frontend:

### Prerequisites

- Node.js (v14 or later)
- npm or yarn

### Setup and Installation

1. Navigate to the react-frontend directory:
```bash
cd react-frontend
```

2. Install dependencies:
```bash
npm install
```

3. Start the development server:
```bash
npm start
```

The React application will be available at http://localhost:3000.

### Production Deployment

To build the React application for production:

```bash
cd react-frontend
npm run build
```

This creates a `build` directory with optimized production files that can be deployed to any static hosting service like AWS S3, Netlify, Vercel, or GitHub Pages.

### Backend API Integration

The React frontend communicates with a Flask API backend. To run the backend:

```bash
cd api
python server.py
```

The API server will start on port 5000. Make sure both the frontend and backend are running for the application to work properly.

For more detailed information about the React frontend, see the [README-FRONTEND.md](README-FRONTEND.md) file.

## Support

For support, questions, or feedback regarding the PrepForMeeting Crew or crewAI.
- Visit our [documentation](https://docs.crewai.com)
- Reach out to us through our [GitHub repository](https://github.com/joaomdmoura/crewai)
- [Join our Discord](https://discord.com/invite/X4JWnZnxPb)
- [Chat with our docs](https://chatg.pt/DWjSBZn)

Let's create wonders together with the power and simplicity of crewAI.

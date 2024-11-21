# Chatbot Solution

This project is a chatbot application designed to run on multiple platforms, including Jetson Nano, Linux, Windows, and macOS. The project includes a backend and frontend, as well as additional services like Chroma and Ollama for AI processing and management of the chatbot's tasks.

## Requirements

- [Docker](https://docs.docker.com/get-docker/) (Ensure Docker and Docker Compose are installed)
- GPU support for Ollama (if applicable)

## Quick Start

You can start the chatbot application by following the steps below based on your platform.

### Run Chatbot Application

#### On Jetson Nano:

To run the chatbot on a Jetson Nano, use the following command:

```bash
docker compose -f docker-compose-jetson.yml up --build
```

#### On Linux, Windows, or macOS:

To run the chatbot on Linux, Windows, or macOS, use the following command:

```bash
docker compose -f docker-compose.yml up --build
```

This command will build and run the chatbot using the appropriate Docker Compose configuration for your system.

## Folder Structure

Below is the folder structure of the project and a detailed explanation of its contents:

```bash
.
├── backend/
│   ├── Dockerfile.backend           # Dockerfile for building the backend service
│   ├── main.py                      # Entry point for the backend chatbot logic
│   ├── pyproject.toml               # Python project configuration for backend
│   ├── requirements-dev.lock        # Backend development dependency lock file
│   ├── requirements.lock            # Backend production dependency lock file
│   └── src/
│       ├── AI_Book.pdf              # Document for knowledge base
│       ├── bot.py                   # Core logic of the chatbot, including AI-related operations
│       ├── __init__.py              # Marks the `src` directory as a Python module
├── docker-compose-jetson.yml        # Docker Compose configuration for Jetson Nano
├── docker-compose.yml               # Docker Compose configuration for Linux, Windows, and macOS
├── frontend/
│   ├── Dockerfile.frontend           # Dockerfile for building the frontend service
│   ├── app.py                        # Entry point for the frontend, handling user interaction
│   ├── pyproject.toml                # Python project configuration for frontend
│   ├── requirements-dev.lock         # Frontend development dependency lock file
│   └── requirements.lock             # Frontend production dependency lock file
├── README_CHATBOT.md                # Instructions for running the chatbot application
└── run_ollama.sh                    # Shell script to run and configure Ollama service
```

### Explanation of Folders and Files:

- **backend/**: Contains the backend code and dependencies. The backend handles the core logic for the chatbot, including AI processing.
    - **Dockerfile.backend**: Dockerfile for building the backend service.
    - **main.py**: Main entry point for the backend, likely initializing the chatbot and managing backend operations.
    - **pyproject.toml**: Python configuration file for backend dependencies.
    - **requirements-dev.lock**: Lock file for development dependencies of the backend.
    - **requirements.lock**: Lock file for production dependencies of the backend.
    - **src/**: Contains source code for the backend service.
        - **AI_Book.pdf**: Document to embedd and index into chroma vector store.
        - **bot.py**: Contains core chatbot logic, managing conversation flow, AI interaction, etc.
        - **__init__.py**: Initializes the `src` directory as a Python module.

- **frontend/**: Contains the frontend code and dependencies. The frontend handles user interaction, likely through a web interface.
    - **Dockerfile.frontend**: Dockerfile for building the frontend service.
    - **app.py**: Entry point for the frontend service, handling user interactions via a web UI.
    - **pyproject.toml**: Python configuration file for frontend dependencies.
    - **requirements-dev.lock**: Lock file for development dependencies of the frontend.
    - **requirements.lock**: Lock file for production dependencies of the frontend.

- **docker-compose-jetson.yml**: Docker Compose configuration file for running the chatbot application on a Jetson Nano.

- **docker-compose.yml**: Docker Compose configuration file for running the application on Linux, Windows, or macOS.

- **run_ollama.sh**: Shell script to set up and run the Ollama service.

---

## Docker Compose Overview

The `docker-compose-jetson.yml` file orchestrates the different services of the chatbot, such as the frontend, backend, and AI-related services like Chroma and Ollama. Below is a breakdown of each service and how they are set up:

```yaml
version: '3'

services:
  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile.frontend
    ports:
      - "7860:7860"
    container_name: frontend
    depends_on:
      - backend
    networks:
      - app-network

  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile.backend
    ports:
      - "5001:5001"
    container_name: backend
    depends_on:
      - chroma
      - ollama
    networks:
      - app-network
    volumes:
      - ./backend:/app 

  chroma:
    image: chromadb/chroma
    volumes:
      - ./chroma:/chroma/.chroma/index
    ports:
      - "8000:8000"
    container_name: chroma
    networks:
      - app-network

  ollama:
    image: dustynv/ollama:r36.2.0
    ports:
      - 11434:11434
    volumes:
      - ./ollama/ollama:/root/.ollama
      - ./run_ollama.sh:/run_ollama.sh
    container_name: ollama
    tty: true
    entrypoint: ["/bin/bash"]
    command: ["/run_ollama.sh"]
    environment:
      - OLLAMA_KEEP_ALIVE=24h
      - OLLAMA_HOST=0.0.0.0
    networks:
      - app-network

networks:
  app-network:
    driver: bridge
```

### Explanation of Services

1. **frontend**:
   - **Build**: Built from the `frontend` directory using `Dockerfile.frontend`.
   - **Ports**: Exposes port `7860` for frontend access.
   - **Depends On**: Ensures the backend service is running before starting the frontend.
   - **Networks**: Connected to the `app-network` for communication with other services.

2. **backend**:
   - **Build**: Built from the `backend` directory using `Dockerfile.backend`.
   - **Ports**: Exposes port `5001` for backend API access.
   - **Depends On**: Ensures Chroma and Ollama services are running before starting the backend.
   - **Volumes**: Maps the local `backend` directory to the container for code sharing.
   - **Networks**: Connected to the `app-network` for communication with other services.

3. **chroma**:
   - **Image**: Uses the official `chroma` Docker image.
   - **Volumes**: Maps the local `chroma` directory for persistent data storage.
   - **Ports**: Exposes port `8000` for external access to the Chroma service.
   - **Networks**: Connected to the `app-network`.

4. **ollama**:
   - **Image**: Uses the `dustynv/ollama:r36.2.0` image.
   - **Ports**: Exposes port `11434` for Ollama interactions.
   - **Volumes**: Maps the local Ollama configuration and script for persistent setup.
   - **Command**: Runs the Ollama service and executes the chatbot model via the `run_ollama.sh` script.
   - **Environment**: Configures the environment to keep Ollama alive and bind it to host `0.0.0.0` for external access.
   - **Networks**: Connected to the `app-network`.

---

## Network Configuration

- **app-network**: A **bridge** network that allows seamless communication between the frontend, backend, Chroma, and Ollama services. This internal network isolates the services from the external environment while allowing them to interact within Docker.
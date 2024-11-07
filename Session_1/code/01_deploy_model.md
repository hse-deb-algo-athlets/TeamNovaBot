## Deploying a Large Language Model (LLM) on Jetson Orin Nano with Ollama

### Overview

This guide provides a streamlined approach to deploying and running a Large Language Model (LLM) on the Jetson Orin Nano using Ollama, a powerful framework for running LLMs locally. You will learn how to set up the environment, deploy a pre-built Docker container, and interact with the model inside the container.

For more detailed documentation, visit the official guide here: [Jetson AI Lab Ollama Tutorial](https://www.jetson-ai-lab.com/tutorial_ollama.html).

---

### Building and Deploying the Ollama Container from Scratch

#### 1. Clone the Container Repository

Start by cloning the repository that contains Jetson-compatible Docker containers, optimized for Nvidia Jetson devices.

```bash
git clone https://github.com/dusty-nv/jetson-containers
```

This repository includes pre-configured containers designed for the Jetson Orin Nano and other Jetson devices.

#### 2. Install the Containers

Next, install the necessary dependencies and prepare your environment by running the installation script provided in the repository.

```bash
bash jetson-containers/install.sh
```

This script will install required components and configure your system for running LLMs in Docker containers on Jetson hardware.

#### 3. Run the Ollama Container

Now you can start the Ollama container, optimized for Jetson Orin Nano. To do so, use the following command from the terminal (outside VS Code):

```bash
jetson-containers run --name ollama $(autotag ollama) -Y
```

- `jetson-containers run`: Starts the container using configurations from the cloned repository.
- `--name ollama`: Names the container "ollama" for easy identification.
- `$(autotag ollama)`: Automatically tags and pulls the latest Ollama container image optimized for Jetson Orin Nano.

The container's shell should launch after this command.

---

### Manually Download and Run a LLM in the Ollama Container

To manually download and run a model like Llama 3.2 inside the Ollama container, use the following command outside the container shell:

```bash
docker exec -it ollama ollama run llama3.2
```

If you are already inside the container shell, you can simply run:

```bash
ollama run llama3.2
```

---

### Automatically Download and Run a LLM in the Ollama Container

You can also automatically download and run the LLM model using this command:

```bash
jetson-containers run $(autotag ollama) bash -c "/bin/ollama serve & sleep 5; ollama run llama3"
```

---

### Access the Container Shell

To troubleshoot or manage the container manually, access its shell using:

```bash
docker exec -it ollama sh
```

This opens an interactive shell within the running Ollama container.

---

### Interact with Ollama in the Container Shell

Once inside the container, you can interact with Ollama via its CLI. Here are some basic commands:

#### General Command Format:

```bash
ollama [command] [flags]
```

#### Available Commands:

- **serve**: Start Ollama's service.
- **create**: Create a model from a Modelfile.
- **show**: Display model information.
- **run**: Execute a model.
- **pull**: Download a model from a registry.
- **push**: Upload a model to a registry.
- **list**: List all available models.
- **ps**: List currently running models.
- **cp**: Copy a model.
- **rm**: Remove a model.
- **help**: Get help for any command.

#### Example Commands:

1. **Run a Model**:
   ```bash
   ollama run llama3.2
   ```

2. **List Available Models**:
   ```bash
   ollama list
   ```

3. **Pull a Model from a Registry**:
   ```bash
   ollama pull llama3.2
   ```

---

### Alternative Deployment Using a Pre-Built Container

Alternatively, you can pull a pre-built Ollama container from Docker Hub: [dustynv/ollama](https://hub.docker.com/r/dustynv/ollama).

Pre-built images are available for different Jetpack versions:

- **Jetpack 5**: `dustynv/ollama:r35.4.1`
- **Jetpack 6**: `dustynv/ollama:r36.4.0`

#### Steps:

1. **Check the installed Jetpack version**:

   ```bash
   sudo apt-cache show nvidia-jetpack
   ```

2. **Pull the appropriate Docker image** based on your Jetpack version:

   ```bash
   docker pull dustynv/ollama:r36.4.0
   ```

3. **Run the container**:

   ```bash
   docker run -d -v ollama:/root/.ollama -p 11434:11434 --name ollama dustynv/ollama:r36.4.0
   ```

4. **Execute the model inside the running container**:

   ```bash
   docker exec -it ollama ollama run llama3.2
   ```

---

## Final Check

Execute the following command in a bash while the ollama container is running.

```bash
curl http://localhost:11434/api/generate -d '{
  "model": "llama3.2:1b",
  "prompt": "Why is the sky blue?"
}'
```

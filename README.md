### Redis, a caching server
This is a simple project, I wanted to try what is redis as opposed to python in-build caching functionality (see cache project on my github)

We need to install redis (I used the docker desktop option)
Here is a guide on how to install and run a Redis server using Docker Desktop, along with alternative instructions for native installation on different operating systems.

### Installing Redis with Docker Desktop

Using Docker is the ideal way to run Redis because it simplifies setup, avoids conflicts with other software, and makes it easy to manage your Redis instance [3][10].

**Prerequisites**
*   You must have Docker Desktop installed and running on your system. You can download it from the official Docker website [10][11].
    
**Step 1: Pull the Official Redis Image**

First, open your terminal (Command Prompt or PowerShell on Windows, Terminal on macOS/Linux) and download the official Redis image from Docker Hub. This image is a lightweight, pre-configured package containing everything needed to run Redis [3].
(did it from docker desktop, just enter redis in the search window)
```bash
docker pull redis
```

This command downloads the latest stable version of Redis [6][10].

**Step 2: Start the Redis Container**

Once the image is downloaded, you can start a Redis server instance by running it inside a Docker container.

```bash
docker run --name my-redis-container -p 6379:6379 -d redis
```

Let's break down this command:
*   `docker run`: The command to create and start a new container [5].
*   `--name my-redis-container`: Assigns a memorable name to your container for easier management [3].
*   `-p 6379:6379`: This maps port 6379 on your local machine to port 6379 inside the container. Redis listens on port 6379 by default, so this allows your applications to connect to Redis at `localhost:6379` [4][8].
*   `-d`: Runs the container in "detached" mode, meaning it runs in the background and doesn't block your terminal [3][5].
*   `redis`: Specifies that the container should be created from the `redis` image you pulled earlier.

**Step 3: Verify the Installation**

You can verify that your Redis container is running correctly in two ways:

1.  **Check Docker's list of running containers**:
    ```bash
    docker ps
    ```
    You should see `my-redis-container` listed, confirming that it is up and running [5][11].

2.  **Connect with the Redis CLI**:
    The definitive test is to send a command to the Redis server. You can do this by running the Redis Command-Line Interface (CLI) inside your running container.
    ```bash
    docker exec -it my-redis-container redis-cli
    ```
    This command opens an interactive shell within your Redis container and starts the `redis-cli` tool [4][5]. You will see a prompt like `127.0.0.1:6379>`. Now, test the connection by typing `ping`:
    ```
    127.0.0.1:6379> ping
    PONG
    ```
    Receiving a `PONG` response confirms your Redis server is working correctly [1]. You can type `exit` to leave the Redis CLI.

Your Redis server is now installed and ready to be used by your applications.

### Alternative: Native Installation
-didn't do this but leaving here this info
If you prefer not to use Docker, you can install Redis directly on your operating system.

**On macOS (with Homebrew)**
Homebrew is the easiest way to install Redis on a Mac [2].
```bash
# Update Homebrew
brew update

# Install Redis
brew install redis
```

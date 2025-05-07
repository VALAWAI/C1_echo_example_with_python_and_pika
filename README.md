# C1_echo_example_with_python_and_pika

This is a simple C1 component that echo the received messages. It is implemente using Python
and Pika. You can read more about in the [VALAWAI documentation](https://valawai.github.io/docs/tutorials/how_python_component/example).

## Summary

 - Type: C1
 - Name: Echo example with Python and Pika
 - Version: 1.0.0 (May 7, 2025)
 - API: [1.0.0 (May 7, 2025)](https://raw.githubusercontent.com/VALAWAI/C1_echo_example_with_python_and_pika/ASYNCAPI_1.0.0/asyncapi.yml)
 - VALAWAI API: [1.2.0 (March 9, 2024)](https://raw.githubusercontent.com/valawai/MOV/ASYNCAPI_1.2.0/asyncapi.yml)
 - Developed By: [IIIA-CSIC](https://www.iiia.csic.es)
 - License: [GPL 3](LICENSE)


## Generate Docker image

The recommended way to create a Docker image for this component is to run the script:
 
 ```
./buildDockerImages.sh
```

This script will build the image and tag it with the component's version 
(e.g., `valawai/c1_echo_example_with_python_and_pika:1.0.0`).

The script offers several options for customization:

* **Build without cache:** Use `-nc` or `--no-cache` to skip using the cached
 image layers during the build process.
* **Specify tag:** Use `-t <tag>` or `--tag <tag>` to assign a custom tag name 
to the image (e.g., `./buildDockerImages.sh -t my-custom-image-name`).
* **Target architectures:** Use `-p <platforms>` or `--platform <platforms>` to specify
 the architectures (CPU types) for which the image should be built 
 (e.g., `./buildDockerImages.sh -p linux/arm64`). By default, the script builds 
 for `linux/arm64` and `linux/amd64` (both ARM and AMD processors).
* **Use default platforms:** Use `-dp` or `--default-platforms` to explicitly instruct
 the script to use the default architectures (linux/arm64 and linux/amd64).
* **Help message:** Use `-h` or `--help` to display a detailed explanation 
of all available options.

For example, to build an image with the tag `latest`, run:

```bash
./buildDockerImages.sh -t latest
```

This will create the container named `valawai/c1_echo_example_with_python_and_pika:latest`.


### Docker environment variables

The following environment variables configure the Docker image's behavior, categorized by function:

#### I. RabbitMQ Connection Parameters:

These variables govern the connection to the RabbitMQ message broker.

*   `RABBITMQ_HOST`: Specifies the hostname or IP address of the RabbitMQ server. The default
 value is `mov-mq`.
*   `RABBITMQ_PORT`: Defines the port number used for communication with RabbitMQ. The default
 value is `5672`.
*   `RABBITMQ_USERNAME`: Sets the username for authenticating with the RabbitMQ server. 
The default value is `mov`.
*   `RABBITMQ_PASSWORD`: Sets the password for authenticating with the RabbitMQ server. 
The default value is `password`. *Note: For production environments, it is strongly advised 
to avoid storing passwords directly in environment variables. Consider using secrets management
 solutions.*
*   `RABBITMQ_MAX_RETRIES`: Determines the maximum number of attempts to establish a connection
 to RabbitMQ. The default value is `100`.
*   `RABBITMQ_RETRY_SLEEP`: Specifies the delay, in seconds, between connection attempts to 
RabbitMQ. The default value is `3`.

#### II. Logging Configuration:

These variables control the logging behavior of the application.

*   `LOG_CONSOLE_LEVEL`: Sets the minimum log level for messages displayed on the console.
 Possible values, in increasing order of severity, are `DEBUG`, `INFO`, `WARNING`, `ERROR`,
  `FATAL`, and `CRITICAL`. The default value is `INFO`.
*   `LOG_FILE_LEVEL`: Sets the minimum log level for messages written to the log file. 
Possible values are the same as `LOG_CONSOLE_LEVEL`. The default value is `DEBUG`.
*   `LOG_FILE_MAX_BYTES`: Defines the maximum size, in bytes, of the log file before it
 is rolled over (renamed and a new file created). The default value is `1000000`.
*   `LOG_FILE_BACKUP_COUNT`: Specifies the number of rolled-over log files to retain. Older
 files are deleted when this limit is exceeded. The default value is `5`.
*   `LOG_DIR`: Specifies the directory where log files are stored. The default value 
is `logs`.
*   `LOG_FILE_NAME`: Defines the base filename for the log file within the `LOG_DIR`. The default
 value is `c1_echo_example_with_python_and_pika.txt`.

#### III. Component Identification:

This variable manages the storage of the component's unique identifier.

*   `COMPONET_ID_FILE_NAME`: Defines the filename (within the `LOG_DIR`) where the component's
 identifier, obtained during registration with the MOV, is stored. The default value is `component_id.json`.

 
### Docker health check

The component stores its registration details in a file. Unless overridden by the **COMPONET_ID_FILE_NAME**
environment variable, this file is located at **/app/${LOG_DIR:-logs}/${COMPONET_ID_FILE_NAME:-component_id.json}**.
This file is deleted when the component is unregistered. Therefore, checking the file's existence and size
provides a straightforward health check. The following Docker Compose snippet illustrates a health check
configuration:

```
    healthcheck:
      test: ["CMD-SHELL", "test -s /app/logs/component_id.json"]
      interval: 1m
      timeout: 10s
      retries: 5
      start_period: 1m
      start_interval: 5s
```


## Deploying the Component

This section shows you how to get the C2 Treatment Nonmaleficence Valuator up 
and running using Docker Compose.

### What you'll need:

*   **Docker:** This is a tool that lets you run software in isolated "containers."
 You can download it from [https://www.docker.com/get-started](https://www.docker.com/get-started).
*   **Docker Compose:** This tool helps you manage multiple Docker containers
 at once. It's usually included with Docker Desktop, or you can install it separately. 
 See the Docker documentation for instructions.

### Let's get started!

1.  **Get the code:** The project's files are on GitHub: 
[https://github.com/VALAWAI/C1_echo_example_with_python_and_pika](https://github.com/VALAWAI/C1_echo_example_with_python_and_pika).
 You'll need to download or "clone" this repository to your computer. If you're not familiar with Git, 
 you can simply download the repository as a ZIP file.

2.  **Start the application:** Open your terminal or command prompt, 
navigate to the directory where you downloaded the project, and run this command:

    ```bash
    COMPOSE_PROFILES=mov docker compose up -d
    ```

    This command tells Docker Compose to start the application in the background (`-d`).
     The `mov` part tells it to start the C2 component along with a related system called MOV.

3.  **Check if it's working:**

    *   Open your web browser and go to [http://localhost:8080](http://localhost:8080). 
    You should see the [Master of valawai (MOV)](/tutorials/mov) user interface.
    *   (Optional) You can also check the RabbitMQ message queue by going to
     [http://localhost:8081](http://localhost:8081). The default login is `mov` for the username 
     and `password` for the password. **Important:** Don't use these default logins if you're setting this 
     up for real use (like on a public server). They are only for testing.

### Making changes (if you need to):

If you want to change some settings, you can create a file named `.env` 
in the same folder as the `docker-compose.yml` file. Here's how it works:

1.  Create a new file named `.env` in your text editor.
2.  Add lines like this to change settings:

    ```
    MQ_HOST=my.custom.rabbitmq.server
    MQ_PASSWORD=my_secret_password
    ```

    This example changes the message queue server and the password.

Here's a list of the settings you can change in the `.env` file:

*   `C1_echo_example_with_python_and_pika_TAG` (usually leave this as `latest`)
*   `MQ_HOST` (the address of the message queue)
*   `MQ_PORT` (the port of the message queue, usually 5672)
*   `MQ_UI_PORT` (the port of the message queue web interface, usually 8081)
*   `MQ_USER` (the username for the message queue)
*   `MQ_PASSWORD` (the password for the message queue - **Important:** Change this for real use!)
*   `RABBITMQ_TAG` (usually leave this as `management`)
*   `MONGODB_TAG` (usually leave this as `latest`)
*   `MONGO_PORT` (the port for the database, usually 27017)
*   `MONGO_ROOT_USER` (the database root username)
*   `MONGO_ROOT_PASSWORD` (the database root password - **Important:** Change this for real use!)
*   `MONGO_LOCAL_DATA` (where the database files are stored on your computer)
*   `MOV_DB_NAME` (the name of the database MOV uses)
*   `MOV_DB_USER_NAME` (the username MOV uses to access the database)
*   `MOV_DB_USER_PASSWORD` (the password MOV uses to access the database - **Important:** Change this for real use!)
*   `MOV_TAG` (usually leave this as `latest`)
*   `MOV_UI_PORT` (the port for the MOV web interface, usually 8080)
*   `LOG_LEVEL` (how much logging information you see; usually `INFO`)

### If you change database settings:

If you change any of the settings that start with `MONGO_`, you'll need to reset the database:

1.  Find the folder on your computer that `MONGO_LOCAL_DATA` points to (it's usually `~/mongo_data/movDB`).
2.  Delete that folder.
3.  Run `COMPOSE_PROFILES=mov docker-compose up -d` again.

### To stop everything:

When you're finished, you can stop all the running parts with this command:

```bash
COMPOSE_PROFILES=mov docker-compose up -d
```
  
## Development

This guide explains how to set up a development environment to work
on the C2 Treatment Nonmaleficence Valuator code.

### Prerequisites:

* Ensure you have Docker and Docker Compose installed on your system.

### Starting the Development Environment:

1.  **Run the development script:**

    ```bash
    ./startDevelopmentEnvironment.sh
    ```

    This script starts the development environment using Docker Compose. 
    It includes various tools and services needed for development.

2.  **Interact with the Python code:**

    Once the script finishes, you'll have a bash shell where you can interact with the Python code.

### Available Commands:

The development environment provides several commands for common actions:

* **run:** Starts the C2 Treatment Nonmaleficence Valuator component.
* **testAll:** Runs all unit tests for the codebase.
* **test test/test_something.py:** Runs the unit tests defined in
 the file `test_something.py`.
* **test test/test_something.py::TestClassName::test_do_something:** Runs 
a specific unit test named `test_do_something` defined within the class `TestClassName` 
in the file `test_something.py`.
* **coverage:** Runs all unit tests and generates a coverage report.
* **fmt:** Runs a static code analyzer to check for formatting and style issues.

### Development Tools and Services:

The development environment also starts several tools and services:

* **RabbitMQ:** A message broker server used for communication between
 components. You can access its management UI at 
 [http://localhost:8081](http://localhost:8081) with credentials `mov:password` 
 (**Caution:** Avoid these default credentials in production environments).
* **MongoDB:** A NoSQL database used by the MOV component. The database is
 named `movDB`, and the credentials are `mov:password` (**Caution:** Avoid these 
 default credentials in production environments). You can access its management UI
  (MongoDB) at [http://localhost:8081](http://localhost:8081) with the same credentials.
* **Mongo express:** A web UI for interacting with the MongoDB database. You can access
 it at [http://localhost:8082](http://localhost:8082).
* **Master Of VALAWAI (MOV):** The web UI for interacting with the MOV component. 
You can access it at [http://localhost:8083](http://localhost:8083).

### Important:

The credentials `mov:password` used for RabbitMQ, MongoDB, and MOV should
be changed for secure deployments in production environments.


## Links

 - [C2 Treatment nonmaleficence valuator documentation](https://valawai.github.io/docs/components/C2/treatment_nonmaleficence_valuator)
 - [Master Of VALAWAI tutorial](https://valawai.github.io/docs/tutorials/mov)
 - [VALWAI documentation](https://valawai.github.io/docs/)
 - [VALAWAI project web site](https://valawai.eu/)
 - [Twitter](https://twitter.com/ValawaiEU)
 - [GitHub](https://github.com/VALAWAI)
# To-do list using FastAPI

This project implements a to-do list using FastAPI.

## Getting Started

### Prerequisites

The following dependencies are expected to be installed on your machine:

- [Python 3.12][python]
- [PostgreSQL][postgresql]
- [PDM][pdm]

#### MacOS Users

MacOS users are recommended to use [Homebrew][homebrew], a package manager that simplifies the installation of software on MacOS and Linux systems, to easily install the required dependencies for this project. If Homebrew is not yet installed, follow the instructions on its [homepage][homebrew].

Once Homebrew is installed, the project dependencies can be installed by running the following command in the terminal:

```bash
brew install python3 postgresql pdm
```

### Database Setup

Before the project setup, follow these steps for database setup:

1. Start the PostgreSQL service. The command may vary depending on the operating system:
    - [Windows][postgres-windows]
    - [Linux][postgres-linux]

    #### MacOS

    ```bash
    brew services start postgresql
    ```

2. Connect to the default `postgres` database:
    ```bash
    psql postgres
    ```

3. If the `postgres` user does not exist, create a new user named `postgres` with password `postgres`:
    ```sql
    CREATE USER postgres WITH PASSWORD 'postgres';
    ```
   If the `postgres` user already exists, set the password for this user to 'postgres':
    ```sql
    ALTER USER postgres WITH PASSWORD 'postgres';
    ```

4. Create a new database named `planner` owned by the `postgres` user:
    ```sql
    CREATE DATABASE planner OWNER postgres;
    ```

5. Exit the PostgreSQL shell:
    ```sql
    \q
    ```

## Project Setup

After the database setup, the following steps are followed to set up the project:

1. Clone the repository:
    ```bash
    git clone https://github.com/lmiguelvargasf/planner.git
    ```

2. Navigate into the project directory:
    ```bash
    cd planner
    ```

3. Install the project dependencies using PDM:
    ```bash
    pdm install
    ```

4. Copy the `.env.example` file to `.env`:
    ```bash
    cp .env.example .env
    ```
   Open the `.env` file and replace the placeholders in the `DATABASE_URL` with the appropriate values. The connection string should reflect the values used in the Database Setup section. For example:
    ```
    DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5432/planner
    ```
    In this example, `postgres` is the username and password, `localhost` is the host, `5432` is the port (default PostgreSQL port), and `planner` is the database.

5. Run the project:
    ```bash
    pdm run start
    ```

6. Open a web browser and navigate to [`localhost:8000`](http://localhost:8000). The follwing response should be seen:
    ```
    {"status": "up"}
    ```

[homebrew]: https://brew.sh/
[pdm]: https://pdm-project.org/latest/
[postgres-linux]: https://askubuntu.com/questions/1206416/how-to-start-postgresql
[postgres-windows]: https://stackoverflow.com/questions/36629963/how-can-i-start-postgresql-on-windows
[postgresql]: https://www.postgresql.org/
[python]: https://www.python.org/

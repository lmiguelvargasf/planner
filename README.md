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

[homebrew]: https://brew.sh/
[pdm]: https://pdm-project.org/latest/
[postgres-linux]: https://askubuntu.com/questions/1206416/how-to-start-postgresql
[postgres-windows]: https://stackoverflow.com/questions/36629963/how-can-i-start-postgresql-on-windows
[postgresql]: https://www.postgresql.org/
[python]: https://www.python.org/

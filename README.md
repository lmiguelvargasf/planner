# To-do list using FastAPI

This project implements a to-do list using FastAPI.

## Getting Started

### Prerequisites

The following dependencies are expected to be installed:

- [Python 3.12][python]
- [PostgreSQL][postgresql]
- [pre-commit][]
- [PDM][pdm]

#### MacOS Users

MacOS users are recommended to use [Homebrew][homebrew], a package manager that simplifies the installation of software on MacOS and Linux systems, to easily install the required dependencies for this project. If Homebrew is not yet installed, follow the instructions on its [homepage][homebrew].

Once Homebrew is installed, the project dependencies can be installed by running the following command in the terminal:

```bash
brew install python3 postgresql pre-commit pdm
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

1. Connect to the default `postgres` database:
    ```bash
    psql postgres
    ```

1. If the `postgres` user does not exist, create a new user named `postgres` with password `postgres`:
    ```sql
    CREATE USER postgres WITH PASSWORD 'postgres';
    ```
   If the `postgres` user already exists, set the password for this user to 'postgres':
    ```sql
    ALTER USER postgres WITH PASSWORD 'postgres';
    ```

1. Create two databases named `planner` and `planner_test` owned by the `postgres` user:
    ```sql
    CREATE DATABASE planner OWNER postgres;
    CREATE DATABASE planner_test OWNER postgres;
    ```
    `planner` is used for the main application, while `planner_test` is used for running tests.

1. Set the timezone of the databases to UTC:
    ```sql
    ALTER DATABASE planner SET timezone TO 'UTC';
    ALTER DATABASE planner_test SET timezone TO 'UTC';
    ```

1. Exit the PostgreSQL shell:
    ```bash
    \q
    ```

### Project Setup

After the database setup, the following steps are followed to set up the project:

1. Clone the repository:
    ```bash
    git clone https://github.com/lmiguelvargasf/planner.git
    ```

1. Navigate into the project directory:
    ```bash
    cd planner
    ```

1. Install the project dependencies using PDM:
    ```bash
    pdm install
    ```

1. Install the pre-commit hooks for the repository:
    ```bash
    pre-commit install
    ```

1. Copy the `.env.example` file to `.env`:
    ```bash
    cp .env.example .env
    ```
   Open the `.env` file and replace the placeholders in the `DATABASE_URL` with the appropriate values. The connection string should reflect the values used in the [Database Setup](#database-setup) section. For example:
    ```
    DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5432/planner
    ```
    In this example, `postgres` is the username and password, `localhost` is the host, `5432` is the port (default PostgreSQL port), and `planner` is the database.

1. Run the project:
    ```bash
    pdm run start
    ```

1. Access the application by clicking on the following link: [`localhost:8000`](http://localhost:8000). The following response should be seen:
    ```
    {"status": "up"}
    ```

## Jupyter Notebook Usage

It is encouraged the use of Jupyter notebooks for data analysis and exploration
to facilitate interactive development and data visualization.

- **Storage:** Please place all notebooks in the [`./notebooks`](./notebooks/) directory.
- **Naming Convention:** Name the notebooks using the format `YYYY-MM-DD_brief_description.ipynb`.
This convention organizes notebooks chronologically and provides a quick insight into their contents.

#### Pre-commit Hook: `nbstripout`

To maintain a clean repository, the [`nbstripout`][nbstripout] pre-commit hook is used to strip outputs from Jupyter notebooks, which can significantly reduce file sizes.

### Launching JupyterLab

JupyterLab can be launched using the following command:

```bash
dotenv run jupyter lab --notebook-dir=./notebooks
```

It can also be initiated through pdm scripts:

```bash
pdm run lab
```

Executing either command starts the JupyterLab server, enabling access to notebooks via the web interface.


[homebrew]: https://brew.sh/
[nbstripout]: https://github.com/kynan/nbstripout
[pdm]: https://pdm-project.org/latest/
[postgres-linux]: https://askubuntu.com/questions/1206416/how-to-start-postgresql
[postgres-windows]: https://stackoverflow.com/questions/36629963/how-can-i-start-postgresql-on-windows
[postgresql]: https://www.postgresql.org/
[pre-commit]: https://pre-commit.com/
[python]: https://www.python.org/

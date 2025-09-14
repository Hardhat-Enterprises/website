# Hardhat Enterprises Web App Automation and Security Scripts

This Folder Contains the Automation and Security Scripts used each for individual purpose i.e. Helper Script for Developer, Secret Scanning Script ensures Security and Code Quality of Hardhat Enterprises Web App. Each script is detailed below in its own section, including the commands available and their functionality.

## Table Of Content
- Auto-Setup.sh
- precommit.sh
- secrets-scan.sh
- harden_docker_script.sh
- Prerequisites

## Auto-Setup.sh

The Hardhat Enterprises Web App's environment setup and verification are automated by the `Auto-Setup.sh` script. It launches the Dockerized program, verifies that the relevant configuration files are present, and looks for any necessary dependencies.

### Commands and Usage

- **`--dry-run`**
  - Performs the checks related to enviornment without even starting the application.
  - Check and Verify the presence of `Git`, `Python 3`, `pip3`, `Docker`, `Docker Compose` (i.e. `.env`,`docker-compose.yaml` etc)
  - Checks the health endpoint located at `http://localhost:80/health`.
  - **Example**: `./Auto-setup.sh --dry-run`
- **`--setup`**
  - Uses `docker-compose up --build -d` to launch the Docker containers and performs all environment checks.
  - Awaits confirmation from the health endpoint that the application is operating properly.
  - Feedback on setup success or failure is given, along with recommendations for log checks if necessary.
  - **Example**: `./Auto-Setup.sh --setup`
- **`--help`**
  -  Displays a help message with the instructions and options available.
  - **Example**: `./Auto-Setup.sh --help`

## precommit.sh
The `precommit.sh` script administers Git pre-commit hooks to ensure code quality prior to commits.

### Commands and Usage
- **`--install`**
   - Installs the pre-commit tool utilising `pipx`, `pip`, or `pip3`, and configures Git hooks.
   - Sets up the repository to execute pre-commit hooks automatically during commits.
   - **Example**: `./precommit.sh --install`.
- **`--check`**
   - Verifies the installation of pre-commit hooks by inspecting the presence of the .git/hooks/pre-commit file.
   - **Example**: `./precommit.sh --check`
- **`--run`**
   - Executes pre-commit hooks on staged files to uphold code quality.
   - **Example:** `./precommit.sh --run`
- **`--run-all`**
   - Executes pre-commit hooks on all files within the repository, rather than solely on staged files.
   - **Example**: `./precommit.sh --run-all`
- **`--update`**
   - Upgrades all pre-commit hooks to their most recent versions.
   - **Example**: `./precommit.sh --update`
- **`--uninstall`**
   - Eliminates pre-commit hooks from the repository.
   - **Example**: `./precommit.sh --uninstall`
- **`--list`**
   - Enumerates all hooks configured in .pre-commit-config.yaml.
   - **Example**: ⁠ `./precommit.sh --list`
- **`--config`**
   - Exhibits the contents of the.pre-commit-config.yaml ⁠ file.
   - **Example**: `./precommit.sh --config`
- **`--help`**
   - Display a help message detailing usage instructions and available options.
   - **Example**: `./precommit.sh --help`

## secrets-scan.sh
The `secrets-scan.sh` script incorporates TruffleHog to detect secrets within files and avert their inclusion in the repository.

### Commands and Usage
- **`install`**
  - Installs TruffleHog and sets up a pre-push Git hook to scan staged files for secrets before pushing to the repository.
  - **Example**: `./secrets-scan.sh install`
- **`status`**
  - Checks if the pre-push hook is installed.
  - **Example**: `./secrets-scan.sh status`
- **`uninstall`**
  - Removes the pre-push hook and TruffleHog binary from the system.
  - **Example**: `./secrets-scan.sh uninstall`
- **`scan [PATH]`**
  - Conducts a manual scan of a designated directory or file (defaulting to the current directory) for secrets utilising TruffleHog.
  - **Example**: `./secrets-scan.sh scan ./src`
- **`(No argument)`**
  - Display a help message detailing usage instructions and available options.
  - **Example**: `./secrets-scan.sh`

## harden_docker_script.sh
The `harden_docker_script.sh` script evaluates Docker settings for security compliance, verifying adherence to best practices like minimal base images, non-root users, and appropriate cleanup procedures.

- **`compliance`** 
  - Checks `Dockerfile`, `.dockerignore`, and `docker-compose.yml` for security compliance.                                                           - Validates the use of minimal base images (`python:3.12-slim`, `nginx:alpine`), non-root user configurations, dependency cleanup, and read-only >  - Generates a compliance report with pass/fail results for each check.
  - **Example**: `./harden_docker_script.sh compliance`
- **`compliance --images`**
  - Expands the `complianc` directive to encompass the examination of constructed Docker images (`django_app` and `nginx`).
  - Confirms that images operate as non-root users and utilise the appropriate base images.
  - **Example**: `./harden_docker_script.sh compliance --images`
- **`help`**
  - Display a help message detailing usage instructions and available options.
  - **Example**: `./harden_docker_script.sh help`
- **`build`**
  - Offers instructions for constructing and executing Docker images, instructing users to manually execut d `docker-compose up --build -d`.
  - **Example**: `./harden_docker_script.sh build`

## Prerequisites
- **`Git`**: Required for version control and repository management.
- **`Python 3 and pip/pip3/pipx`**: Needed for installing `pre-commit` and running scripts.
- **`Docker and Docker Compose`**: Necessary for running the containerized application.
- **`TruffleHog`**: Automatically installed by `secrets-scan.sh` for secrets scanning.
- **`Operating System`**: Compatible with Linux, macOS, or Windows (with Git Bash).

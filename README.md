# Git Maintainer Backend

This project is the backend for an AI-driven GitHub assistant that helps users with coding tasks and GitHub repository management. It is built using Django Rest Framework and is designed to automate specific GitHub-related actions based on user prompts.

## Features

- **Account Creation and Login**: Users can create an account and log in securely.
- **GitHub Integration**: Users can provide their GitHub username and authentication token to allow the backend to interact with their GitHub account.
- **AI-Driven Coding Assistance**: The AI agent takes coding-related prompts from users, processes them, and performs related actions on GitHub repositories.
- **GitHub Commits**: Users can specify coding-related questions, and the AI agent will:
  - Check if the specified GitHub repository exists.
  - If the repository does not exist, it will create a new private repository with the provided name.
  - Solve the coding question and create a file with the solution.
  - Push the changes to the repository with meaningful commit messages.

## Current Features

- **Create Repository**: If a user provides a repository name that does not exist, the backend will automatically create a new private repository.
- **Push Code**: Based on user prompts, the AI will generate code, create files, and push them to the specified repository with descriptive commit messages.

## Work In Progress

This backend is currently under development. The functionality for GitHub commits is active, but there are plans to add more features in the future, such as:
- More comprehensive support for different GitHub operations (e.g., creating issues, managing pull requests).
- Enhanced AI capabilities for solving more advanced coding queries.

## Technology Stack

- **Django Rest Framework**: The backend is built using Django Rest Framework for efficient API development.
- **GitHub API**: To interact with user GitHub accounts, manage repositories, commits, and other GitHub actions.

## Installation

To get started with this project, clone the repository and set up the environment:

1. Clone the repository:
    ```bash
    git clone https://github.com/chnoumanejaz/git-maintainer-backend.git
    ```

2. Navigate into the project directory:
    ```bash
    cd git-maintainer-backend
    ```

3. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

4. Apply migrations:
    ```bash
    python manage.py migrate
    ```

5. Create a superuser for admin access (optional):
    ```bash
    python manage.py createsuperuser
    ```

6. Run the server:
    ```bash
    python manage.py runserver
    ```

## Usage

1. **Create an Account & Login**: Use the endpoints provided to create an account and log in. Authentication will require a username and password.
2. **Connect to GitHub**: Provide your GitHub username and authentication token to link your GitHub account.
3. **Submit a Prompt**: Provide a coding-related question along with a repository name. The backend will check for the repository and handle the commit process automatically.

## Contributing

Contributions are welcome! Feel free to fork this repository and submit a pull request with improvements, bug fixes, or new features. Please follow the existing code style and write tests for any new features or changes.

## License

This project is open-source and available under the MIT License.


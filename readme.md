# FileFlow: Effortless File Sharing

FileFlow is a web-based file sharing service designed to simplify file sharing between individuals and groups by removing the need for user accounts or logins. It provides an extremely convenient way to share files quickly. Please note that FileFlow is not designed for secure file transfer and does not encrypt files; it offers a trade-off between convenience and security.

⚠️ **Disclaimer**: FileFlow is intended for temporary and non-sensitive file sharing. Do not use FileFlow to share confidential or sensitive information.

## Features

- **No Login Required**: Share files without the need to create an account or log in.
- **Unique Numeric Identifier**: Assign a unique number to your file for easy sharing.
- **Quick Access**: Directly access files using a URL pattern.
- **Simple Interface**: Minimalist design focused on ease of use.

### API Documentation

For detailed information on the API endpoints and usage, please refer to the [API Documentation](API.md).

## Getting Started

These instructions will help you get a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

Ensure you have the following installed:

- **Python 3.6+**
- **MongoDB**
- **Redis**
- **Node.js and npm**
- **Docker and Docker Compose** (optional, for Docker installation)

### Installation

#### Option 1: Using Docker

1. **Clone the repository:**

   ```bash
   git clone https://github.com/BellaZ0317/FileFlow.git
   cd FileFlow
   ```

2. **Start the application using Docker Compose:**

   ```bash
   docker-compose up --build
   ```

   This command builds and starts all the services defined in the `docker-compose.yml` file.

#### Option 2: Manual Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/BellaZ0317/FileFlow.git
   cd FileFlow
   ```

2. **Set up a virtual environment:**

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install Python dependencies:**

   ```bash
   pip install -r app/requirements.txt
   ```

4. **Install Node.js dependencies:**

   Navigate to the `app` directory and run:

   ```bash
   npm install
   ```

5. **Install frontend dependencies using Bower:**

   **Note:** If you don't have Bower installed globally, install it first:

   ```bash
   npm install -g bower
   ```

   Then, install the dependencies:

   ```bash
   bower install
   ```

6. **Build frontend assets using Gulp:**

   ```bash
   gulp
   ```

7. **Start MongoDB and Redis servers:**

   - **MongoDB:** Follow the [MongoDB installation guide](https://docs.mongodb.com/manual/installation/) for your operating system.
   - **Redis:** Follow the [Redis installation guide](https://redis.io/topics/quickstart).

8. **Start the Celery worker:**

   In a new terminal window, navigate to the `app` directory and run:

   ```bash
   celery -A models worker --loglevel=info
   ```

9. **Run the application:**

   ```bash
   python app/server.py
   ```

   The application will start on `http://0.0.0.0:4000`.

### Running the Application

- Access the application at `http://localhost:4000` in your web browser.

## Usage

### Uploading Files

1. **Open the FileFlow homepage.**
2. **Create a Space:**

   - In the "Create a Space" section, enter a numeric identifier (e.g., "123"). If the space number is already taken, a new number will be suggested.
   - Click the "Choose File" button to select the file you want to upload.
   - Click the "Upload" button.

3. **Share the Space Number:**

   - After uploading, you will receive a confirmation with the space number.
   - Share this number with anyone you want to have access to the file.

### Downloading Files

1. **Open the FileFlow homepage.**
2. **Open a Space:**

   - Enter the space number provided to you in the "Open a Space" section.
   - Click the "Download" button.

3. **Receive the File:**

   - The file associated with that space number will be downloaded to your device.

## Development

### Directory Structure

- **app/**: Contains the Flask application and all Python code.
  - **templates/**: HTML templates for rendering web pages.
  - **static/**: Static files (CSS, JavaScript, images).
    - **js/**: Compiled JavaScript files.
    - **jsx/**: React JSX source files.
    - **sass/**: SASS stylesheets.
- **nginx/**: Nginx configuration for serving the application.
- **docs/**: Documentation and guides.
- **docker-compose.yml**: Configuration file for Docker Compose.
- **Makefile**: Contains common tasks for building and running the application.
- **requirements.txt**: Python dependencies.

### Running Tests

Tests are located in the `app/tests/` directory. To run the tests:

```bash
cd app/tests
python -m unittest unittest.py
```

### Environment Variables

Environment variables can be set in the `development.env` and `production.env` files.

## Contributing

Contributions are welcome! If you're interested in contributing to FileFlow, please follow these steps:

1. **Fork the repository** on GitHub.
2. **Create a new branch** for your feature or bug fix:

   ```bash
   git checkout -b feature/your_cool_feature_name
   ```

3. **Commit your changes** with clear and descriptive commit messages.
4. **Push your branch** to your forked repository:

   ```bash
   git push origin feature/your_cool_feature_name
   ```

5. **Create a Pull Request** to the `master` branch of the main repository.

Please make sure to follow the existing code style and include tests for new functionality.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

By adopting FileFlow, you agree to use it responsibly and acknowledge that it is not intended for transferring sensitive or confidential information.

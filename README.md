# Driver Stores

## Features
- **User Authentication**: Secure user login and registration via Firebase authentication, with email verification and password reset functionality.
- **File Management**: Users can upload, create, delete, and organize files and folders within their personal storage area.
- **Folder Security**: Ensures folder and file access are restricted to authenticated users only.
- **File Download**: Users can download individual files from their storage.
- **Dynamic Navigation**: Allows users to navigate folders and files dynamically.
- **Error Handling and Logging**: Logs errors and warnings for failed operations and authentication issues.

## Project Structure
```plaintext
├── app.py                # Main application file
├── templates/            # HTML templates for rendering pages
│   ├── index.html        # Homepage (login page)
│   ├── profile.html      # User profile and file management page
│   ├── reset.html        # Password reset page
│   ├── register.html     # Registration page
│   ├── files.html        # Dynamic folder view
├── static/               # Folder for static files (CSS, JS, images)
├── func.py               # Contains helper functions like `generate_header`
└── requirements.txt      # List of project dependencies
```

## Prerequisites
- Python 3.x
- Flask and Flask-Compress libraries
- Firebase configuration for authentication
- `requirements.txt` with project dependencies

## Installation

1. **Clone the Repository**:
    ```bash
    git clone [https://github.com/geekyfaahad/driver-store.git](https://github.com/geekyfaahad/drive-store)
    cd driver-store
    ```

2. **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

3. **Firebase Setup**:
   - Replace the Firebase configuration in `config` with your own Firebase project settings.

4. **Run the Application**:
    ```bash
    python app.py
    ```

   Access the app at `http://localhost:4000`.

## Usage
1. **Login/Register**: Access the homepage to log in or register a new account.
2. **File Upload**: Once logged in, navigate to the user profile to upload, delete, or organize files.
3. **Folder Operations**: Create and manage folders directly within your storage area.
4. **Download Files**: Use the download option to retrieve files from your storage.
5. **Logout**: Clear the session and return to the login page.

## License
Distributed under the MIT License. See `LICENSE` for more information.

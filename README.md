# Hospital Website API

## Overview

This project is a hospital management website built using Flask and PostgreSQL. It provides various functionalities such as patient registration, doctor login, appointment scheduling, and profile management. This README includes information about the API endpoints available in this project.

## Features

- User registration and profile management
- Doctor login and appointment scheduling
- Contact us form
- Profile updates and viewing appointment history

## Installation

To run this project locally, follow these steps:

1. **Clone the repository:**

   ```bash
   git clone https://github.com/your-username/your-repository.git
   cd your-repository
   ```

2. **Set up a virtual environment:**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install the required dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Configure the database:**
   - Ensure PostgreSQL is installed and running.
   - Create a database named `hospital`.
   - Update the `database_session` configuration in `app.py` with your PostgreSQL credentials.

5. **Run the application:**

   ```bash
   python app.py
   ```

   The application will be accessible at `http://localhost:5001`.

## API Documentation

The API provides endpoints for various functionalities in the hospital management system. Below is a summary of the available endpoints:

### Authentication

- **POST /login**
  - **Description:** Allows patients to log in.
  - **Request Body:** `email`, `password`
  - **Response:** Patient details and appointment information

- **POST /drlogin**
  - **Description:** Allows doctors to log in.
  - **Request Body:** `email`, `password`
  - **Response:** Doctor details and appointments

### Patient Registration

- **POST /signup**
  - **Description:** Registers a new patient.
  - **Request Body:** `name`, `email`, `password`, `age`, `blood`, `profile_picture`
  - **Response:** Success or error message

### Appointment Management

- **POST /submit**
  - **Description:** Allows patients to schedule an appointment.
  - **Request Body:** `doctor`, `date`, `time`
  - **Response:** Success or error message

- **GET /update**
  - **Description:** Updates patient profile and retrieves appointment information.
  - **Response:** Updated profile and appointments

### Contact Us

- **POST /contactus**
  - **Description:** Allows users to send complaints or messages.
  - **Request Body:** `name`, `email`, `phonenumber`, `message`
  - **Response:** Success or error message

### Profile Management

- **POST /update_profile**
  - **Description:** Updates patient profile details.
  - **Request Body:** `patient_name`, `email`, `age`
  - **Response:** Updated profile and appointments

## Files and Directories

- `app.py`: Main application file
- `static/`: Directory for static files (e.g., profile images)
- `templates/`: Directory for HTML templates
- `requirements.txt`: File listing Python package dependencies

## Contributing

Contributions are welcome! Please open an issue or submit a pull request to contribute to this project.


## Contact

For any questions or feedback, please contact [Omar Ahmed](mailto:omarref3at2031@gmail.com).
```

### How to Use This Template:

1. **Replace placeholders** like `your-username`, `your-repository`, and `your-email@example.com` with actual values.
2. **Add additional sections** if necessary, such as testing instructions, deployment details, or acknowledgments.
3. **Save the file** as `README.md` and place it in the root directory of your project.

This README file will help users and collaborators understand how to set up, use, and contribute to your project.

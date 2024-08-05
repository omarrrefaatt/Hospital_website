## Hospital Website API Documentation

### 1. Introduction

This API documentation covers the endpoints for the hospital website, including functionalities for patient registration, login, appointment management, and doctor login.

**Base URL:**
`http://localhost:5001/api`

### 2. Authentication

**Authentication Method:**
- **Session Cookies:** After successful login, a session is created.

### 3. API Endpoints

#### a. Home

- **Endpoint:** `/`
- **Method:** GET
- **Description:** Serves the home page.

**Response:**
- **200 OK**
  - Returns the HTML content for the home page.

#### b. Patient Registration

- **Endpoint:** `/signup`
- **Method:** POST
- **Description:** Registers a new patient.

**Request Parameters:**
- `name` (string, required)
- `email` (string, required)
- `password` (string, required)
- `age` (integer, required)
- `blood` (string, required)
- `profile_picture` (file, optional)

**Example Request:**
```http
POST /signup
Content-Type: multipart/form-data

{
  "name": "Jane Doe",
  "email": "jane.doe@example.com",
  "password": "password123",
  "age": 30,
  "blood": "O+",
  "profile_picture": <file>
}
```

**Response:**
- **200 OK** (if successful)
  ```json
  {
    "message": "You have successfully registered."
  }
  ```
- **400 Bad Request** (if account already exists)
  ```json
  {
    "message": "Account already exists!"
  }
  ```

#### c. Doctor Login

- **Endpoint:** `/drlogin`
- **Method:** POST
- **Description:** Logs in a doctor.

**Request Parameters:**
- `email` (string, required)
- `password` (string, required)

**Example Request:**
```http
POST /drlogin
Content-Type: application/x-www-form-urlencoded

{
  "email": "doctor@example.com",
  "password": "password123"
}
```

**Response:**
- **200 OK** (if successful)
  ```json
  {
    "doctor_id": 1,
    "doctor_name": "Dr. John Smith",
    "specialization": "Cardiology",
    "department": "Heart Department",
    "doctor_image_path": "/images/dr_john_smith.jpg"
  }
  ```
- **401 Unauthorized** (if credentials are incorrect)
  ```json
  {
    "message": "Please enter correct email/password."
  }
  ```

#### d. Patient Login

- **Endpoint:** `/login`
- **Method:** POST
- **Description:** Logs in a patient.

**Request Parameters:**
- `email` (string, required)
- `password` (string, required)

**Example Request:**
```http
POST /login
Content-Type: application/x-www-form-urlencoded

{
  "email": "patient@example.com",
  "password": "password123"
}
```

**Response:**
- **200 OK** (if successful)
  ```json
  {
    "patient_name": "Jane Doe",
    "email": "jane.doe@example.com",
    "patient_id": 1,
    "blood_type": "O+",
    "age": 30,
    "profile_picture": "/images/profile.jpg"
  }
  ```
- **401 Unauthorized** (if credentials are incorrect)
  ```json
  {
    "message": "Please enter correct email/password."
  }
  ```

#### e. Contact Us

- **Endpoint:** `/contactus`
- **Method:** POST
- **Description:** Submits a contact us form.

**Request Parameters:**
- `name` (string, required)
- `email` (string, required)
- `phonenumber` (string, required)
- `message` (string, required)

**Example Request:**
```http
POST /contactus
Content-Type: application/x-www-form-urlencoded

{
  "name": "John Doe",
  "email": "john.doe@example.com",
  "phonenumber": "1234567890",
  "message": "I have an issue."
}
```

**Response:**
- **200 OK** (if successful)
  ```json
  {
    "message": "You have successfully sent your complaint."
  }
  ```
- **400 Bad Request** (if no account found)
  ```json
  {
    "message": "You do not have an account. Please sign up."
  }
  ```

#### f. Update Patient Profile

- **Endpoint:** `/update_profile`
- **Method:** POST
- **Description:** Updates patient profile information.

**Request Parameters:**
- `patient_name` (string, required)
- `email` (string, required)
- `age` (integer, required)

**Example Request:**
```http
POST /update_profile
Content-Type: application/x-www-form-urlencoded

{
  "patient_name": "Jane Doe",
  "email": "jane.doe@example.com",
  "age": 31
}
```

**Response:**
- **200 OK** (if successful)
  ```json
  {
    "message": "Profile updated successfully."
  }
  ```

#### g. Book Appointment

- **Endpoint:** `/submit`
- **Method:** POST
- **Description:** Books an appointment with a doctor.

**Request Parameters:**
- `doctor` (integer, required)
- `date` (string, required, format: `YYYY-MM-DD`)
- `time` (string, required, format: `HH:MM`)

**Example Request:**
```http
POST /submit
Content-Type: application/x-www-form-urlencoded

{
  "doctor": 1,
  "date": "2024-08-10",
  "time": "10:00"
}
```

**Response:**
- **200 OK** (if successful)
  ```json
  {
    "message": "Appointment booked successfully."
  }
  ```
- **400 Bad Request** (if doctor is busy or date is in the past)
  ```json
  {
    "message": "Doctor is busy or date has passed. Please select another date or time."
  }
  ```

### 4. Error Codes

- **400 Bad Request:** The request was invalid or missing parameters.
- **401 Unauthorized:** Authentication failed or incorrect credentials.
- **404 Not Found:** Resource not found.
- **500 Internal Server Error:** Server error occurred.

### 5. Example Requests

**Register Patient:**
```http
POST /signup
Content-Type: multipart/form-data

{
  "name": "Jane Doe",
  "email": "jane.doe@example.com",
  "password": "password123",
  "age": 30,
  "blood": "O+",
  "profile_picture": <file>
}
```

**Login:**
```http
POST /login
Content-Type: application/x-www-form-urlencoded

{
  "email": "patient@example.com",
  "password": "password123"
}
```




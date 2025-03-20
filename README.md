# Medicare-Connect
A comprehensive healthcare platform connecting patients with doctors, offering seamless appointment scheduling, prescription management, and personalized care.

## Prerequisites

Before you begin, ensure you have met the following requirements:
- Python 3.11 or higher
- Other dependencies are listed in the requirements.txt file

## Local Dev Setup
##### Steps to install and run application on your local machine.
* Run `$ cd ..` command for jump out from the project directory
* Run `$ python3.11 -m venv env` command to Create Virtual environment
* Run `$ source env/bin/activate` command to activate virtual environment
* Run `$ cd Medicare-Connect` command for jump into the project directory
* Run `$ pip install -r requirements.txt` command to Install project requirement file
* Run `$ python manage.py migrate` command to apply migrations on your local machine
* Run `$ python manage.py runserver` command to run project on your local machine
* Run `$ python manage.py test` command to run the unittest case on your local machine

## API Endpoints
### User Registration
- **Endpoint**: `POST http://127.0.0.1:8000/medlink/user-registration/`
- **Request Body**:
    ```
  {"email": "abc@xyz.com",
  "password": "secret_password"
  "role": "doctor/patient"}
  ```
- **Response**:
    ```
  {"message": "User created successfully",
    "role": "doctor/patient"}
  ```
  
### Generate User Access Token
- **Endpoint**: `POST http://127.0.0.1:8000/api/token/`
- **Request Body**:
    ```
  {"username": "abc@xyz.com",
  "password": "secret_password"}
  ```
- **Response**:
    ```
  {"refresh": "encrypted_refresh_token",
  "access": "encrypted_access_token"}
  ```
  
### Generate Refresh Token
- **Endpoint**: `POST http://127.0.0.1:8000/api/token/refresh/`
- **Request Body**:
    ```
  {"refresh": "encrypted_refresh_token"}
  ```
- **Response**:
    ```
  {"access": "encrypted_access_token"}
  ```
  
### Register patient
- **Endpoint**: `POST http://127.0.0.1:8000/medlink/patients/create/`
- **Request Body**:
    ```
  {"patient": "abc@xyz.com"}
  ```
- **Headers**:
    ```
  {"Authorization": "Bearer encrypted_access_token"}
  ```
- **Response**:
    ```
    {"message": "Patient created successfully"}
  ```
  
### Fetch Patient List
- **Endpoint**: `GET http://127.0.0.1:8000/medlink/patients/list/`
- **Headers**:
    ```
  {"Authorization": "Bearer encrypted_access_token"}
  ```
- **Response**:
    ```
    [{"id": 1,
    "patient_email": "abc@xyz.com"},
    {"id": 2,
    "patient_email": "pqr@abc.com"}]
  ```
  
### Assign Prescription to Patient
- **Endpoint**: `POST http://127.0.0.1:8000/medlink/patient/prescriptions/create/`
- **Request Body**:
    ```
  {"patient_username": "abc@xyz.com",
  "medication": "medicine_name",
  "dosage": "usage count",
  "instruction": "usage detail"}
  ```
- **Headers**:
    ```
  {"Authorization": "Bearer encrypted_access_token"}
  ```
- **Response**:
    ```
    {"message": "Prescription created successfully"}
  ```
  
### Patient Prescription List
- **Endpoint**: `GET http://127.0.0.1:8000/medlink/patient/prescriptions/list/`
- **Request params**:
    ```
  {"patient_username": "abc@xyz.com"}
  ```
- **Headers**:
    ```
  {"Authorization": "Bearer encrypted_access_token"}
  ```
- **Response**:
    ```
    [{"id": 1,
    "patient_username": "abc@xyz.com"
    "doctor_username": "gef@zzz.com"
    "date_prescribed": "01-01-2025"},
    {"id": 2,
    "patient_username": "abc@xyz.com"
    "doctor_username": "gef@zzz.com"
    "date_prescribed": "01-01-2025"}]
  ```

### Patient Prescription Detail
- **Endpoint**: `GET http://127.0.0.1:8000/medlink/patient/prescriptions/1/`
- **Headers**:
    ```
  {"Authorization": "Bearer encrypted_access_token"}
  ```
- **Response**:
    ```
    {"id": 1,
    "patient_username": "abc@xyz.com",
    "doctor_username": "pqr@zzz.com",
    "medication": "medicina_name",
    "dosage": "Once a day",
    "instructions": "Morning",
    "date_prescribed": "01-01-2025"}
  ```
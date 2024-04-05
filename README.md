# Ceral API management.
This project provides a toy example of an API solution for tracking the nutritional content of cereals. The API is built using FastAPI and connects to a locally hosted MySQL database.

## Overview

FastAPI is a modern web framework for building APIs with Python 3.7+ based on standard Python type hints. It is designed for high performance, easy development, and automatic OpenAPI documentation generation. Leveraging FastAPI's capabilities, this project aims to showcase the creation of a RESTful API that enables users to manage and query nutritional data for various types of cereals.

## Features

- **RESTful API:** Utilizing FastAPI's intuitive syntax, the API adheres to the principles of REST architecture, providing endpoints for common HTTP methods such as GET, POST, PUT, and DELETE.
  
- **MySQL Integration:** The API connects to a local MySQL database to store and retrieve data related to cereal nutrition, allowing for efficient data management and persistence.
  
- **OpenAPI Documentation:** FastAPI automatically generates interactive API documentation based on the OpenAPI specification, offering developers a comprehensive guide to available endpoints and their usage. This can be found using the following link, assuming the server is run locally `http://localhost:8000/docs`.

## Usage

To interact with the API, users can send HTTP requests to the provided endpoints using tools like cURL, Postman, or by making direct requests from their applications. The API supports operations such as fetching cereal data, adding new cereals, updating existing entries, and deleting records.


## Installation Guide

### Prerequisites:
- Anaconda installed.
- pip installed (usually comes with Anaconda).
- MySQL server installed.
- Cereal.csv in a folder called `data/`. The data can be found here: `https://drive.google.com/file/d/1TyFq6OzCBfGUVMAqISIp1LwcT-FoBwtM/view?usp=drive_link`

### Steps:

1. **Clone the Repository:**
`git clone https://github.com/soeren97/Cereal`

2. **Navigate to the Repository Directory:**
`cd */Cereal`

3. **Create a Virtual Environment (Optional but Recommended):**
`conda create -n your-env-name python=3.11`

4. **Activate the Virtual Environment:**
`conda activate your-env-name`

5. **Install Required Packages:**
`pip install .`

6. **Verify Installation:**
Ensure all dependencies are installed successfully without any errors.

7. **Deactivate Virtual Environment (If Created):**
`conda deactivate`

8. **Create config.json.**
Create a file containing the fields username and password in the repocetory directory.


### Additional Notes:

- **Virtual Environment:** Creating a virtual environment is a good practice to isolate project dependencies from other projects and the system Python environment.
- **pip Install:** The `pip install .` command installs the necessary packages specified in the `setup.py` file from the current directory.
- **requirements** The required packages can be found in the `setup.py` file as the variable `INSTALL_REQQUIRES`.

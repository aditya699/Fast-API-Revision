# README

# FastAPI with MongoDB: PDF Processing Project

This project was developed to enhance understanding of FastAPI in conjunction with MongoDB, specifically focusing on a PDF upload and processing setup. The application allows users to upload their resumes in PDF format, which are then processed to extract relevant information such as user name, email, primary skill set, and years of experience. This data is subsequently stored in a MongoDB database.

## Project Structure

- **index.html**: The main HTML file that provides the user interface for uploading resumes. It includes a form for file uploads and utilizes Tailwind CSS for styling.
  
- **route.py**: This file contains the FastAPI routes for handling PDF uploads. It reads the uploaded PDF, extracts text, and invokes a language model to parse the information.

- **pdf_str.py**: This module defines the data model for storing PDF-related information and includes a function to insert this data into the MongoDB database.

- **utils.py**: Contains utility functions for session verification, ensuring that user sessions are valid.

- **users.py**: Manages user-related database operations, including inserting and updating user information.

## Technologies Used

- **FastAPI**: A modern web framework for building APIs with Python 3.6+ based on standard Python type hints.
- **MongoDB**: A NoSQL database used for storing user and PDF data.
- **Pydantic**: Data validation and settings management using Python type annotations.
- **PyPDF2**: A library for reading PDF files and extracting text.

## Getting Started

1. Clone the repository:
   ```bash
   git clone <repository-url>
   ```

2. Install the required dependencies:
   ```bash
   pip install fastapi[all] pymongo pydantic PyPDF2 langchain_google_genai
   ```

3. Set up your MongoDB connection string in the environment variable `MONGO_CON`.

4. Run the FastAPI application:
   ```bash
   uvicorn app.route:app --reload
   ```

5. Access the application at `http://127.0.0.1:8000`.

## Conclusion

This project serves as a practical exercise in using FastAPI with MongoDB, providing insights into handling file uploads and data processing in a web application context. It is a stepping stone for further exploration of more complex functionalities within FastAPI and database interactions.

Feel free to explore and modify the code to suit your learning needs!


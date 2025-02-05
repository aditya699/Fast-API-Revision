import os
from fastapi import APIRouter, UploadFile, File
from fastapi.responses import HTMLResponse
from PyPDF2 import PdfReader
from app.db.pdf_str import insert_pdf
from langchain_google_genai import ChatGoogleGenerativeAI
from io import BytesIO
import json
import uuid

router = APIRouter(prefix="/pdf")

os.environ["GOOGLE_API_KEY"]=os.getenv("GEMINI_API_KEY")
@router.post("/upload", response_class=HTMLResponse)
async def upload_pdf(pdf_file: UploadFile = File(...)):
    # Read the PDF file
    pdf_content = await pdf_file.read()
    
    # Create a BytesIO object from the PDF content
    pdf_file_obj = BytesIO(pdf_content)
    
    # Extract text from the PDF using the file-like object
    reader = PdfReader(pdf_file_obj)
    text = ""
    for page in reader.pages:
        text += page.extract_text() + "\n"

    prompt = f"""
    Extract the following information from the resume:
    1. user_name
    2. email
    3. primary_skill_set
    4. years_of_experience

    Output should be in the following format:(Strictly follow this format , no other text or explanation is needed)
    [
        {{
            "user_name": "John Doe",
            "email": "john.doe@example.com",
            "primary_skill_set": "Python, SQL, AWS",
            "years_of_experience": "5 years"
        }}
    ]

    Resume:
    {text}
    """
    
    llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0)
    response = llm.invoke(prompt)
    print(response.content)



    # Parse the JSON response
    try:
        # Extract data using string manipulation since response.content may not be valid JSON
        content = response.content.strip()
        # Remove any leading/trailing brackets and split into lines
        content = content.replace("[", "").replace("]", "").strip()
        # Parse as individual fields
        fields = {}
        for line in content.split("\n"):
            line = line.strip()
            if ":" in line:
                key, value = line.split(":", 1)
                key = key.strip().strip('"')
                value = value.strip().strip('",')
                fields[key] = value
        parsed_data = [fields]
        if parsed_data and len(parsed_data) > 0:
            data = parsed_data[0]
            await insert_pdf(
                pdf_id=str(uuid.uuid4()),
                user_name=data["user_name"],
                email=data["email"], 
                primary_skill_set=data["primary_skill_set"],
                years_of_experience=data["years_of_experience"]
            )
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON: {e}")
        return HTMLResponse(content="<h1>Error processing PDF</h1>", status_code=500)
    except Exception as e:
        print(f"Error: {e}")
        return HTMLResponse(content="<h1>Error processing PDF</h1>", status_code=500)

  
    return HTMLResponse(content="<h1>PDF uploaded and processed successfully!</h1>", status_code=200)

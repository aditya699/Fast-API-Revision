# main.py
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from app.auth.router import router as auth_router
from app.pdf.route import router as pdf_router
from starlette.middleware.sessions import SessionMiddleware
from starlette.responses import RedirectResponse
from app.auth.utils import verify_session  # Import our verify function
import os
from dotenv import load_dotenv
load_dotenv()


app = FastAPI(title="Job-Dundo.AI")
app.include_router(auth_router)
app.include_router(pdf_router)
# Add session middleware to handle user sessions more effectively, using session middleware is a abstract implementation of middleware so that we do not have to manage the session manually
app.add_middleware(SessionMiddleware, secret_key=os.getenv("SECRET_KEY"), max_age=86400)  # 1 DAY

# Mount static and template directories
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/login")
async def login_page(request: Request):
    # If already logged in, redirect to home
    if verify_session(request):
        return RedirectResponse(url="/")
    # We must include the request in the template response so that we can use it in the template(also even we are not using it in the template, we must include it)
    return templates.TemplateResponse("login.html", {"request": request})

@app.get("/")
async def home(request: Request):
    # Check if user is logged in
    if not verify_session(request):
        return templates.TemplateResponse("index.html", {
            "request": request,
            "user": "We respect your privacy"
        })
    

    # Get user info for template
    user_info = request.session.get("user_info")
    #in index.html we are using the user info to display the user's name
    return templates.TemplateResponse("index.html", {
        "request": request,
        "user": user_info
    })

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", reload=True)
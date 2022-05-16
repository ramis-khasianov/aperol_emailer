import os

from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from fastapi import FastAPI, UploadFile, File, BackgroundTasks, Request, Form
from pydantic import EmailStr, BaseModel
from typing import List, Optional
from starlette.responses import JSONResponse


conf = ConnectionConfig(
    MAIL_USERNAME=os.environ.get('MAIL_USERNAME'),
    MAIL_PASSWORD=os.environ.get('MAIL_PASSWORD'),
    MAIL_FROM=os.environ.get('MAIL_FROM'),
    MAIL_PORT=os.environ.get('MAIL_PORT'),
    MAIL_SERVER=os.environ.get('MAIL_SERVER'),
    MAIL_FROM_NAME=os.environ.get('MAIL_FROM_NAME'),
    MAIL_TLS=os.environ.get('MAIL_TLS'),
    MAIL_SSL=os.environ.get('MAIL_SSL'),
    USE_CREDENTIALS=os.environ.get('USE_CREDENTIALS'),
    VALIDATE_CERTS=os.environ.get('VALIDATE_CERTS'),
)

fm = FastMail(conf)
app = FastAPI()


class EmailSchema(BaseModel):
    email: List[EmailStr]
    subject: str
    body: str


@app.post("/send_email")
async def send_email(email: EmailSchema) -> JSONResponse:

    message = MessageSchema(
        subject=email.dict().get('subject'),
        recipients=email.dict().get('email'),
        body=email.dict().get('body')
    )

    await fm.send_message(message)

    return JSONResponse(status_code=200, content={"message": "email has been sent"})


@app.post("/send_file")
async def send_file(
        file: UploadFile = File(...),
        emails: List[EmailStr] = Form(...),
) -> JSONResponse:

    message = MessageSchema(
        subject="Express delivery",
        recipients=emails,
        body="Simple background task ",
        attachments=[file]
    )

    await fm.send_message(message)

    return JSONResponse(status_code=200, content={"message": "email has been sent"})


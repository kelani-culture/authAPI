from fastapi import (BackgroundTasks, UploadFile, File, Form,
                     Depends, HTTPException, status)

from typing import List
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from jose import jwt
from app.config import settings

conf = ConnectionConfig(
    MAIL_USERNAME=settings.mail_username,
    MAIL_PASSWORD=settings.password,
    MAIL_FROM=settings.mail_username,
    MAIL_PORT = 587,
    MAIL_SERVER="smtp.gmail.com",
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
    USE_CREDENTIALS=True
)

async def send_email(email: List, token_data: dict):
    access_token = jwt.encode(token_data, settings.secret_key, settings.algorithm)
    template = f""" 
    <!DOCTYPE html>
    <html>
        <head>
            <body>
                <div style = "display: flex; align-items: center; justify-content: center; flex-direction: column">
                <h3> Account Verification </h3>
                <br>
                <p> please click on the button below to verify your account</p>
                <a style="margin-top: 1rem; padding: 1rem;; border-radius: 0.5rem; font-size: 1rem; text-decoration: none; background; #077b8a; color: white;" href=http://localhost:8000/verification/?token={access_token}>Verify your email</a>
                <p> Please kindly ignore this email if you did not register to authpy Thanks</p>
            </body>
        </head>
    </html>
    """

    message = MessageSchema(
        subject="authpy verification Email",
        recipients= email,
        body=template,
        subtype="html"
    )
    fm = FastMail(conf)
    await fm.send_message(message=message)
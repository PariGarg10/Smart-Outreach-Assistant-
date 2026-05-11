from typing import Any

from fastapi import Body, FastAPI, File, Form, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import sessionmaker

from ai_engine import generate_email
from csv_handler import read_csv
from database import engine
from email_service import send_email
from models import Outreach

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Session = sessionmaker(bind=engine)
session = Session()


@app.get("/")
def home() -> dict[str, str]:
    return {"message": "Smart Outreach Assistant Running"}


@app.post("/upload-csv/")
async def upload_csv(file: UploadFile = File(...)) -> list[dict[str, Any]]:
    return read_csv(file.file)


def add_to_db(person: dict[str, Any]) -> None:
    entry = session.query(Outreach).filter_by(email=person["email"]).first()
    if entry:
        entry.name = person["name"]
        entry.company = person["company"]
        entry.role = person["role"]
        entry.status = "pending"
    else:
        entry = Outreach(
            email=person["email"],
            name=person["name"],
            company=person["company"],
            role=person["role"],
            status="pending",
        )
        session.add(entry)
    session.commit()


def mark_as_sent(email: str) -> None:
    record = session.query(Outreach).filter_by(email=email).first()
    if record:
        record.status = "sent"
        session.commit()

def build_email_body(person: dict[str, Any], openai_api_key: str | None = None) -> str:
    try:
        return generate_email(
            person["name"],
            person["company"],
            person["role"],
            api_key=openai_api_key,
        )
    except Exception:
        return (
            f"Dear {person['name']},\n\n"
            "Most applications try to convince you why they are a good fit.\n"
            "This one is structured so you can decide that yourself.\n\n"
            "---\n\n"
            "### Product: Pari Garg (SDE Candidate v1.0)\n\n"
            f"**Category:** {person['role']}\n"
            "**Core Functionality:** Builds, optimizes, and occasionally automates things before being asked\n\n"
            "---\n\n"
            "### Overview\n\n"
            "I am a Computer Science undergraduate with a strong foundation in Data Structures, Algorithms, and software development.\n\n"
            "What does that translate to beyond coursework?\n"
            "Building systems that actually work, scale, and solve real problems.\n\n"
            "Over time, I have focused on projects that reflect both technical depth and practical impact - from full-stack platforms to machine learning systems.\n\n"
            "---\n\n"
            "### Why Company\n\n"
            "What kind of environment brings out the best in an engineer?\n"
            "One that values ownership, learning, and building meaningful solutions.\n\n"
            f"That is what draws me to {person['company']}.\n\n"
            "If you are looking for someone who can contribute from day one while continuously learning and improving, I would value the opportunity to be part of your team.\n\n"
            "My resume is attached for a more structured overview of my work.\n\n"
            "Thank you for your time and consideration.\n\n"
            "Best regards,\nPari Garg\n{{Phone}}\n{{Email}}\n{{LinkedIn}} | {{GitHub}}"
        )


@app.post("/send-mails/")
def send_mails(data: list[dict[str, Any]] = Body(...)) -> dict[str, Any]:
    sent_count = 0
    for person in data:
        try:
            add_to_db(person)
            email_body = build_email_body(person)
            send_email(person["email"], "Internship Application", email_body)
            mark_as_sent(person["email"])
            sent_count += 1
        except Exception as exc:
            raise HTTPException(status_code=500, detail=str(exc)) from exc

    return {"status": "Emails Sent", "sent_count": sent_count}


@app.post("/upload-csv-and-send/")
async def upload_csv_and_send(
    file: UploadFile = File(...),
    smtp_email: str = Form(""),
    smtp_app_password: str = Form(""),
    openai_api_key: str = Form(""),
) -> dict[str, Any]:
    data = read_csv(file.file)
    if not data:
        raise HTTPException(status_code=400, detail="CSV has no rows.")

    sent_count = 0
    failures: list[dict[str, str]] = []

    for person in data:
        try:
            add_to_db(person)
            email_body = build_email_body(person, openai_api_key.strip() or None)
            send_email(
                person["email"],
                "Internship Application",
                email_body,
                smtp_email=smtp_email.strip() or None,
                smtp_password=smtp_app_password.strip() or None,
            )
            mark_as_sent(person["email"])
            sent_count += 1
        except Exception as exc:
            failures.append(
                {"email": str(person.get("email", "")), "error": str(exc)}
            )

    return {
        "status": "completed",
        "total_rows": len(data),
        "sent_count": sent_count,
        "failed_count": len(failures),
        "failures": failures,
    }


@app.get("/status/")
def get_status() -> list[dict[str, Any]]:
    return session.query(Outreach).all()


@app.get("/metrics/")
def get_metrics() -> dict[str, int]:
    total = session.query(Outreach).count()
    sent = session.query(Outreach).filter_by(status="sent").count()
    pending = session.query(Outreach).filter_by(status="pending").count()
    return {"total": total, "sent": sent, "pending": pending}
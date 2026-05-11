import os
from openai import OpenAI


def _role_focus(role: str) -> str:
    role_lower = (role or "").lower()
    if "data" in role_lower or "analyst" in role_lower:
        return (
            "data-driven problem solving, dashboarding, experimentation, and clear business insights"
        )
    if "backend" in role_lower or "api" in role_lower:
        return "scalable backend APIs, clean architecture, performance, and reliability"
    if "frontend" in role_lower or "react" in role_lower:
        return "clean UI, responsive frontend development, and user-focused product thinking"
    if "ml" in role_lower or "ai" in role_lower:
        return "machine learning experimentation, model evaluation, and practical AI features"
    if "software" in role_lower or "developer" in role_lower or "engineer" in role_lower:
        return "full-stack engineering, ownership mindset, and shipping high-quality features"
    return "strong problem solving, fast learning, and building practical, high-impact solutions"


def _role_feature_lines(role: str) -> tuple[str, str, str]:
    role_lower = (role or "").lower()

    # These three lines are placed under the "Key Features" section.
    if "frontend" in role_lower or "react" in role_lower:
        return (
            "Built responsive web applications designed with usability and performance in mind",
            "Developed interactive user experiences by integrating APIs and optimizing UI performance",
            "Designed an automated outreach tool that processes structured CSV data to trigger personalized email workflows",
        )

    if "backend" in role_lower or "api" in role_lower:
        return (
            "Built scalable backend services and REST APIs designed with reliability and performance in mind",
            "Implemented robust data processing pipelines using structured CSV inputs to power automation workflows",
            "Designed an automated outreach tool that processes structured CSV data to trigger personalized email workflows",
        )

    if "data" in role_lower or "analyst" in role_lower:
        return (
            "Built analytics-focused data workflows and dashboards with decision-ready clarity in mind",
            "Developed a machine learning-based depression detection system using LSTM models and feature engineering",
            "Designed an automated outreach tool that processes structured CSV data to trigger personalized email workflows",
        )

    if "ml" in role_lower or "ai" in role_lower:
        return (
            "Developed machine learning models using LSTM architectures along with feature engineering",
            "Evaluated and improved model performance through experimentation and iterative tuning",
            "Designed an automated outreach tool that processes structured CSV data to trigger personalized email workflows",
        )

    return (
        "Built scalable web applications designed with usability and performance in mind",
        "Developed a machine learning-based depression detection system using LSTM models and feature engineering",
        "Designed an automated outreach tool that processes structured CSV data to trigger personalized email workflows",
    )


def _structured_template(name: str, company: str, role: str) -> str:
    key1, key2, key3 = _role_feature_lines(role)

    recruiter_name = os.getenv("RECRUITER_NAME", "Recruiter")
    phone = os.getenv("SENDER_PHONE", "7838589023")
    sender_email = os.getenv("SENDER_EMAIL", "pari10garg@gmail.com")
    role_display = (role or "").strip()

    # NOTE: Keep this formatting consistent with the exact template user provided.
    return (
        f"Dear {recruiter_name},\n\n"
        "Most applications try to convince you why they're a good fit.\n"
        "This one is structured so you can decide that yourself.\n\n"
        f"Product:  Pari Garg ({role_display} Candidate v1.0)\n\n"
        f"Category: {role_display}\n"
        "Core Functionality: Builds, optimizes, and occasionally automates things before being asked\n"
        "Overview\n\n"
        "I am a Computer Science undergraduate with a strong foundation in Data Structures, Algorithms, and software development.\n\n"
        "What does that translate to beyond coursework?\n"
        "Building systems that actually work, scale, and solve real problems.\n\n"
        "Over time, I've focused on projects that reflect both technical depth and practical impact  from full-stack platforms to machine learning systems.\n\n"
        "Key Features\n\n"
        f"{key1}\n"
        f"{key2}\n"
        f"{key3}\n\n"
        "What happens when problem-solving meets curiosity?\n"
        "You get someone who doesn't just complete tasks, but improves them.\n\n"
        "I also bring strong command over Java, Python, and modern development frameworks, along with consistent practice in writing optimized and clean code.\n\n\n"
        "Performance Add-ons\n\n"
        "Leadership experience as a co-secretary and mentor\n\n"
        "Can code alone build impact?\n"
        "Probably not. That's where collaboration, communication, and adaptability come in.\n\n"
        "I've worked closely with teams, guided newcomers, and learned how to break down complex ideas into simple, actionable solutions.\n\n\n\n"
        "Known Limitations\n\n"
        " Tends to spend extra time refining solutions beyond the minimum requirement\n"
        "Has a habit of automating repetitive tasks whenever possible\n\n"
        "Is that always a bad thing?\n"
        "Depends on whether you value efficiency.\n\n"
        " Occasionally treats debugging like a puzzle that must be solved immediately\n\n"
        f"Why {company}\n\n"
        "What kind of environment brings out the best in an engineer?\n"
        "One that values ownership, learning, and building meaningful solutions.\n\n"
        f"That's what draws me to {company}.\n\n"
        "If you are looking for someone who can contribute from day one while continuously learning and improving, I would value the opportunity to be part of your team.\n\n"
        "My resume is attached for a more structured overview of my work.\n\n"
        "Thank you for your time and consideration.\n\n"
        "Best regards,\n"
        "Pari Garg\n"
        f"{phone}\n"
        f"{sender_email}"
    )


def _fallback_email(name: str, company: str, role: str) -> str:
    return _structured_template(name, company, role)


def generate_email(name, company, role, api_key=None):
    # Since you want the content to match a specific template exactly, we generate
    # the email deterministically. OpenAI is intentionally not used here to avoid
    # drift in wording/formatting.
    return _fallback_email(name, company, role)
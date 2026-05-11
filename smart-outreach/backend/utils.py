from datetime import datetime, timedelta

# ⏳ Check if 5 days passed → send follow-up
def should_send_followup(last_sent_date):
    return datetime.now() - last_sent_date > timedelta(days=5)

# 📧 Generate probable email from name + domain
def generate_email_pattern(name, domain):
    first, last = name.split()
    return f"{first.lower()}.{last.lower()}@{domain}"
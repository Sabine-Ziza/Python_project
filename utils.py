import smtplib
from email.mime.text import MIMEText


def format_result(result):
    url = result["url"]
    status = result["status"]
    code = result["status_code"]
    response_time = result["response_time"]

    if status == "TIMEOUT":
        return f"{url} — TIMEOUT"

    if status == "DOWN":
        return f"{url} — DOWN ({code})"

    line = f"{url} — OK ({code}) — {response_time}ms"

    if status == "SLOW":
        line += " [slow]"

    return line


def send_alert(failed_services):

    if not failed_services:
        return

    sender_email = "ingabirezizas@gmail.com"
    to_email = "sabineingabire68@gmail.com"

    # Replace with your NEW Gmail App Password
    app_password = "fobb zzyh mlsj kqrs"

    body = "Failed Services:\n\n"
    body += "\n".join(failed_services)

    msg = MIMEText(body)
    msg["Subject"] = "Server Health Alert"
    msg["From"] = sender_email
    msg["To"] = to_email

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()

        server.login(sender_email, app_password)

        server.sendmail(
            sender_email,
            to_email,
            msg.as_string()
        )

        server.quit()

        print("Alert email sent successfully!")

    except Exception as e:
        print(f"Failed to send email: {e}")
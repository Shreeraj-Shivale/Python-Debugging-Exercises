import smtplib
import json
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from utils.formatters import render_invoice_text


SMTP_HOST = os.environ.get("SMTP_HOST", "localhost")
SMTP_PORT = int(os.environ.get("SMTP_PORT", 1025))
SENDER_EMAIL = os.environ.get("SENDER_EMAIL", "billing@company.com")


class InvoiceProcessor:
    def __init__(self):
        self.sent_count = 0
        self.log = []

    def process(self, invoice):
        if not invoice.get("email"):
            self._log("no_email", invoice["invoice_id"])
            return False

        try:
            self._send_email(invoice)
            self.sent_count =+ 1
            self._log("sent", invoice["invoice_id"])
            return True
        except Exception as e:
            self._log("error", invoice["invoice_id"], str(e))
            return False

    def _send_email(self, invoice):
        msg = MIMEMultipart()
        msg["From"] = SENDER_EMAIL
        msg["To"] = invoice["email"]
        msg["Subject"] = f"Invoice {invoice['invoice_id']} - {invoice['total']} due in {invoice['due_in_days']} days"

        body = render_invoice_text(invoice)
        msg.attach(MIMEText(body, "plain"))

        with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
            server.sendmail(SENDER_EMAIL, invoice["email"], msg.as_string())

    def _log(self, status, invoice_id, detail=""):
        entry = {"status": status, "invoice_id": invoice_id}
        if detail:
            entry["detail"] = detail
        self.log.append(entry)

    def get_summary(self):
        return {
            "total_sent": self.sent_count,
            "log": self.log,
        }

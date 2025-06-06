"""
I probably should have used something like Twilio to send the messages, but I did not 
want to pay for it (even if its only like less than $5 a year). 
"""
from config import GMAIL_ADDRESS, GOOGLE_APP_PASSWORD, PHONE_NUMBER
from notifier.logger import logger
import smtplib
from email.message import EmailMessage

def send_message(msg, sender=GMAIL_ADDRESS, recipient=PHONE_NUMBER):
    """
    Sends a text message/email to a given recipient. To send text messages you must end the phone number with an "@carrier.com"

    :param msg: The plaintext EmailMessage obj message to send
    :param sender: The sender of the message
    :param recipient: The recipient of the message
    """
    if not msg:
        logger.error("No message while trying to send the text")
        raise ValueError("No message while trying to send the text")
    
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(GMAIL_ADDRESS, GOOGLE_APP_PASSWORD)
    server.send_message(
        msg=msg, 
        from_addr=sender, 
        to_addrs=recipient
    )
    server.quit()
    logger.info(f"Successfully sent message to {recipient}")


def send_sms_message(message, sender=GMAIL_ADDRESS, recipient=PHONE_NUMBER):
    """
    Creates an SMS message and sends it

    :param msg: The string message to send
    :param sender: The sender of the message
    :param recipient: The recipient of the message
    """
    if not message:
        logger.error("No message while trying to send the text")
        raise ValueError("No message while trying to send the text")
    
    msg = EmailMessage()
    msg.set_content(message, subtype="plain", cte="7bit")
    msg["Subject"] = "" # the SMS doesnt like it when I dont include this
    msg["From"] = sender
    msg["To"] = recipient

    send_message(msg, GMAIL_ADDRESS, PHONE_NUMBER)

 
if __name__ == "__main__":
    send_sms_message("Test message", GMAIL_ADDRESS, PHONE_NUMBER)
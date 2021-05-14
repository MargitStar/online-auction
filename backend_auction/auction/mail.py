from backend_auction.settings import DEFAULT_FROM_EMAIL
from django.core.mail import send_mail


def send_email(user):
    mail_from = DEFAULT_FROM_EMAIL
    text = f'Dear {user.username}! You have just bought an auction! Congrats!'
    msg = send_mail(
        "Margosha's Auctions LLC",
        text,
        mail_from,
        [user.email]
    )


def offer_rejection_email(user):
    mail_from = DEFAULT_FROM_EMAIL
    text = f'Dear {user.username}! Your offer was rejected by another user!'
    msg = send_mail(
        "Margosha's Auctions LLC",
        text,
        mail_from,
        [user.email]
    )

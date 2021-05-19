from django.contrib.auth import get_user_model

from auction.models import Auction
from auction.mail import send_email, offer_rejection_email
from backend_auction.celery import app

User = get_user_model()


@app.task(name="start_auction")
def start_auction(auction_id):
    auction = Auction.objects.get(pk=auction_id)
    auction.status = Auction.Status.IN_PROGRESS
    auction.current_price = auction.opening_price
    auction.save()


@app.task(name="close_auction")
def close_auction(auction_id):
    auction = Auction.objects.get(pk=auction_id)
    auction.status = Auction.Status.CLOSED
    auction.save()


@app.task(name="update_price")
def update_price(auction_id, times):
    auction = Auction.objects.get(pk=auction_id)
    delta_price = auction.auction_type.delta_price(auction)
    auction.current_price -= delta_price
    auction.save()
    keep_running = True if auction.status == Auction.Status.IN_PROGRESS else False
    if keep_running:
        run_again = auction.opening_date + auction.auction_type.frequency * times
        times += 1
        update_price.apply_async((auction.pk, times), eta=run_again, task_id=auction.updating_price_task_id)


@app.task(name='send_email')
def send_email_buying_auction(user_id):
    user = User.objects.get(pk=user_id)
    send_email(user)


@app.task(name='offer_rejection_email')
def send_email_offer_rejection(user_id):
    user = User.objects.get(pk=user_id)
    offer_rejection_email(user)

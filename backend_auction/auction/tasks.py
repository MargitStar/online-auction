from auction.models import Auction
from backend_auction.celery import app


@app.task(name="start_auction")
def start_auction(auction_id):
    auction = Auction.objects.get(pk=auction_id)
    auction.status = Auction.Status.IN_PROGRESS
    auction.save()


@app.task(name="close_auction")
def close_auction(auction_id):
    auction = Auction.objects.get(pk=auction_id)
    auction.status = Auction.Status.CLOSED
    auction.save()
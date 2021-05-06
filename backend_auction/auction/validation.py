from rest_framework.exceptions import ValidationError

from auction.models import Auction


def validate_auction_price(lot, serializer):
    if serializer.validated_data['price'] <= lot.auction.current_price:
        raise ValidationError("Price is less than it should be")
    return True


def validate_auction_status(lot):
    if lot.auction.status == Auction.Status.PENDING:
        raise ValidationError('Auction has not opened yet!')
    elif lot.auction.status == Auction.Status.CLOSED:
        raise ValidationError('Auction has already closed!')
    return True


def validate_auction_buy_it_now_price(lot):
    if lot.auction.current_price > lot.auction.auction_type.buy_it_now:
        raise ValidationError("Price is higher now!")
    return True

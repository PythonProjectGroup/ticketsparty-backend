class NoAvailableTickets(Exception):
    pass


class UserHasExceededTheTicketAmountLimit(Exception):
    pass


class InvalidAmount(Exception):
    pass


class PurchaseNotAvailableInThisPeriod(Exception):
    pass

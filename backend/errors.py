class NoAvailableTickets(Exception):
    pass


class UserHasExceededTheTicketAmountLimit(Exception):
    pass


class InvalidAmount(Exception):
    pass


class PurchaseNotAvailableInThisPeriod(Exception):
    pass


class InvalidDate(Exception):
    pass


class InvalidData(Exception):
    pass

from threading import Event, Lock


class TicketOrderSynchronizer:
    def __init__(self):
        self.has_ticket_been_called = {}
        self.has_ticket_been_called_lock = Lock()

        self.has_order_been_made = {}
        self.has_order_been_made_lock = Lock()

    def call_ticket_owner(self, ticket_num):
        self.search_ticket_in_dict(
            ticket_num, self.has_ticket_been_called, self.has_ticket_been_called_lock
        )
        self.has_ticket_been_called[ticket_num].set()

    def block_until_ticket_is_called(self, ticket_num):
        self.search_ticket_in_dict(
            ticket_num, self.has_ticket_been_called, self.has_ticket_been_called_lock
        )
        self.has_ticket_been_called[ticket_num].wait()

    def make_order(self, ticket_num):
        self.search_ticket_in_dict(
            ticket_num, self.has_order_been_made, self.has_order_been_made_lock
        )
        self.has_order_been_made[ticket_num].set()

    def block_until_order_is_made(self, ticket_num):
        self.search_ticket_in_dict(
            ticket_num, self.has_order_been_made, self.has_order_been_made_lock
        )
        self.has_order_been_made[ticket_num].wait()

    def search_ticket_in_dict(self, ticket_num, dict_to_verify, dict_lock):
        with dict_lock:
            if ticket_num not in dict_to_verify:
                dict_to_verify[ticket_num] = Event()

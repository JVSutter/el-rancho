from threading import Event, Lock


class TicketOrderSynchronizer:
    """Classe responsável por sincronizar o fluxo de pedidos e chamadas de tickets."""

    def __init__(self):
        self.has_ticket_been_called = {}
        self.has_ticket_been_called_lock = Lock()

        self.has_order_been_made = {}
        self.has_order_been_made_lock = Lock()

    """Avisa a thread do cliente que o ticket foi chamado."""
    def call_ticket_owner(self, ticket_num):
        self.search_ticket_in_dict(
            ticket_num, self.has_ticket_been_called, self.has_ticket_been_called_lock
        )
        self.has_ticket_been_called[ticket_num].set()

    """Bloqueia a thread do cliente até que o ticket seja chamado."""
    def block_until_ticket_is_called(self, ticket_num):
        self.search_ticket_in_dict(
            ticket_num, self.has_ticket_been_called, self.has_ticket_been_called_lock
        )
        self.has_ticket_been_called[ticket_num].wait()

    """Avisa a thread do funcionário que o pedido foi feito."""
    def make_order(self, ticket_num):
        self.search_ticket_in_dict(
            ticket_num, self.has_order_been_made, self.has_order_been_made_lock
        )
        self.has_order_been_made[ticket_num].set()

    """Bloqueia a thread do funcionário até que o pedido seja feito."""
    def block_until_order_is_made(self, ticket_num):
        self.search_ticket_in_dict(
            ticket_num, self.has_order_been_made, self.has_order_been_made_lock
        )
        self.has_order_been_made[ticket_num].wait()

    """Verifica se o ticket está no dicionário e, caso não esteja, adiciona-o."""
    def search_ticket_in_dict(self, ticket_num, dict_to_verify, dict_lock):
        with dict_lock:
            if ticket_num not in dict_to_verify:
                dict_to_verify[ticket_num] = Event()

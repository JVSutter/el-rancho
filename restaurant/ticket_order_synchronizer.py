from threading import Event, Lock
from typing import Dict
from queue import Queue


class TicketOrderSynchronizer:
    """Classe responsável por sincronizar o fluxo de pedidos e chamadas de tickets."""

    def __init__(self, num_clients: int) -> None:
        self.has_ticket_been_called: Dict[int, Event] = {}
        self.has_ticket_been_called_lock = Lock()

        self.has_order_been_made: Dict[int, Event] = {}
        self.has_order_been_made_lock = Lock()

        self.has_chef_cooked_order: Dict[int, Event] = {}
        self.has_chef_cooked_order_lock = Lock()

        self.orders: Queue[int] = Queue()
        self.orders_left = num_clients

    """Avisa a thread do cliente que o ticket foi chamado."""

    def signal_client_ticket_has_been_called(self, ticket_num: int) -> None:
        self.search_ticket_in_dict(
            ticket_num, self.has_ticket_been_called, self.has_ticket_been_called_lock
        )
        self.has_ticket_been_called[ticket_num].set()

    """Bloqueia a thread do cliente até que o ticket seja chamado."""

    def block_until_ticket_is_called(self, ticket_num: int) -> None:
        self.search_ticket_in_dict(
            ticket_num, self.has_ticket_been_called, self.has_ticket_been_called_lock
        )
        self.has_ticket_been_called[ticket_num].wait()

    """Avisa a thread do funcionário que o pedido foi feito"""

    def signal_crew_order_has_been_made(self, ticket_num: int) -> None:
        self.search_ticket_in_dict(
            ticket_num, self.has_order_been_made, self.has_order_been_made_lock
        )
        self.has_order_been_made[ticket_num].set()

    """Bloqueia a thread do funcionário até que o pedido seja feito."""

    def block_until_order_has_been_made(self, ticket_num: int) -> None:
        self.search_ticket_in_dict(
            ticket_num, self.has_order_been_made, self.has_order_been_made_lock
        )
        self.has_order_been_made[ticket_num].wait()

    """Avisa a thread do cliente que o pedido está pronto."""

    def signal_client_order_is_ready(self, ticket_num: int) -> None:
        self.search_ticket_in_dict(
            ticket_num, self.has_chef_cooked_order, self.has_chef_cooked_order_lock
        )
        self.has_chef_cooked_order[ticket_num].set()

    """Bloqueia a thread do cliente até que o pedido esteja pronto."""

    def block_until_order_is_ready(self, ticket_num: int) -> None:
        self.search_ticket_in_dict(
            ticket_num, self.has_chef_cooked_order, self.has_chef_cooked_order_lock
        )
        self.has_chef_cooked_order[ticket_num].wait()

    """Adiciona um pedido na fila."""

    def add_order(self, order: int) -> None:
        self.orders.put(order)

    """Método para o chef pegar o pedido na fila."""

    def get_order(self) -> int:
        if self.orders_left == 0:
            return -1  # Valor sentinela, indica que não há mais pedidos

        self.orders_left -= 1
        return self.orders.get()

    """Verifica se o ticket está no dicionário e, caso não esteja, adiciona-o."""

    def search_ticket_in_dict(
        self, ticket_num: int, dict_to_verify: Dict[int, Event], lock: Lock
    ) -> None:
        with lock:
            if ticket_num not in dict_to_verify:
                dict_to_verify[ticket_num] = Event()

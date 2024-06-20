# imports do Python
from threading import Thread
import restaurant.shared as shared


"""
    Não troque o nome das variáveis compartilhadas, a assinatura e o nomes das funções.
"""


class Crew(Thread):
    """Inicia o membro da equipe com um id (use se necessario)."""

    def __init__(self, id: int) -> None:
        super().__init__()
        self._id = id
        # Insira o que achar necessario no construtor da classe.

    """ O membro da equipe espera um cliente. """

    def wait(self) -> int:
        print("O membro da equipe {} está esperando um cliente.".format(self._id))
        shared.clients_waiting_crew_sem.acquire()  # Aguarda um cliente
        return shared.get_totem().get_priority_ticket()

    """ O membro da equipe chama o cliente da senha ticket."""

    def call_client(self, ticket: int) -> None:
        print("[CALLING] - O membro da equipe {} está chamando o cliente da senha {}.".format(self._id, ticket))
        shared.get_ticket_order_synchronizer().call_ticket_owner(ticket)

    def make_order(self, order: int) -> None:
        shared.get_ticket_order_synchronizer().block_until_order_is_made(order)
        print("[STORING] - O membro da equipe {} está anotando o pedido {} para o chef.".format(self._id, order))

    """ Thread do membro da equipe."""

    def run(self) -> None:
        while True:
            ticket = self.wait()
            if ticket == -1:
                break

            self.call_client(ticket)
            self.make_order(ticket)

# imports do Python
from threading import Thread
from time import sleep
from random import randint

import restaurant.shared as shared

"""
    Não troque o nome das variáveis compartilhadas, a assinatura e o nomes das funções.
"""
class Chef(Thread):
    def __init__(self) -> None:
        super().__init__()

        # Insira o que achar necessario no construtor da classe.
        self.current_order: int = None

    """ Chef prepara um dos pedido que recebeu do membro da equipe."""
    def cook(self) -> None:
        print("[COOKING] - O chefe esta preparando o pedido para a senha {}.".format(self.current_order))
        sleep(randint(1, 5))

    """ Chef serve o pedido preparado."""
    def serve(self) -> None:
        print("[READY] - O chefe está servindo o pedido para a senha {}.".format(self.current_order))
        shared.get_ticket_order_synchronizer().signal_client_order_is_ready(self.current_order)

    """ O chefe espera algum pedido vindo da equipe."""
    def wait_order(self) -> int:
        print("O chefe está esperando algum pedido.")
        self.current_order = shared.get_ticket_order_synchronizer().get_order()

    """ Thread do chefe."""
    def run(self) -> None:
        while True:
            self.wait_order()
            if self.current_order == -1:
                break

            self.cook()
            self.serve()

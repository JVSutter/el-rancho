# imports do Python
from random import randint
from threading import Thread, Event
from time import sleep

# imports do projeto
import restaurant.shared as shared

# Constantes
MIN_THINKING_TIME = 1
MAX_THINKING_TIME = 5
MIN_EATING_TIME = 1
MAX_EATING_TIME = 5

"""
    Não troque o nome das variáveis compartilhadas, a assinatura e o nomes das funções.
"""


class Client(Thread):
    """Inicializa o cliente."""

    def __init__(self, i: int) -> None:
        self._id = i
        super().__init__()

        # Insira o que achar necessario no construtor da classe.
        self.ticket = -1 # valor default para não inciializar com 'None'
        self.thinking_time = randint(MIN_THINKING_TIME, MAX_THINKING_TIME)

    """ Pega o ticket do totem."""
    def get_my_ticket(self) -> None:
        self.ticket = shared.get_totem().generate_new_ticket()
        print(
            "[TICKET] - O cliente {} pegou o ticket {}.".format(self._id, self.ticket)
        )

    """ Espera ser atendido pela equipe. """
    def wait_crew(self) -> None:
        print("[WAIT] - O cliente {} esta aguardando atendimento.".format(self._id))
        shared.get_ticket_order_synchronizer().block_until_ticket_is_called(self.ticket)

    """ O cliente pensa no pedido."""
    def think_order(self) -> None:
        print("[THINK] - O cliente {} esta pensando no que pedir.".format(self._id))
        sleep(self.thinking_time)

    """ O cliente faz o pedido."""
    def order(self) -> None:
        shared.get_ticket_order_synchronizer().signal_crew_order_has_been_made(
            self.ticket
        )
        print("[ORDER] - O cliente {} pediu algo.".format(self._id))

    """ Espera pelo pedido ficar pronto. """
    def wait_chef(self) -> None:
        print("[WAIT MEAL] - O cliente {} esta aguardando o prato.".format(self._id))
        shared.get_ticket_order_synchronizer().block_until_order_is_ready(self.ticket)

    """ O cliente come por algum tempo."""
    def eating(self) -> None:
        print("[EATING] - O cliente {} esta comendo.".format(self._id))
        sleep(randint(MIN_EATING_TIME, MAX_EATING_TIME))

    """
        O cliente reserva o lugar e se senta.
        Lembre-se que antes de comer o cliente deve ser atendido pela equipe,
        ter seu pedido pronto e possuir um lugar pronto pra sentar.
    """
    def seat_and_eat(self) -> None:
        print(
            "[WAIT SEAT] - O cliente {} esta aguardando um lugar ficar livre".format(
                self._id
            )
        )
        shared.get_table().seat(self._id)

        self.eating()

    """ O cliente deixa o restaurante."""
    def leave(self) -> None:
        shared.get_table().leave(self._id)
        print("[LEAVE] - O cliente {} saiu do restaurante".format(self._id))

    """ Thread do cliente """
    def run(self) -> None:
        self.get_my_ticket()
        self.wait_crew()
        self.think_order()
        self.order()
        self.wait_chef()
        self.seat_and_eat()
        self.leave()

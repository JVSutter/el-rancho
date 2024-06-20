# imports do Python
from random import randint
from threading import Thread, Event
from time import sleep

# imports do projeto
import restaurant.shared as shared

# Constantes
MIN_THINKING_TIME = 1
MAX_THINKING_TIME = 5


"""
    Não troque o nome das variáveis compartilhadas, a assinatura e o nomes das funções.
"""


class Client(Thread):
    """Inicializa o cliente."""

    def __init__(self, i):
        self._id = i
        super().__init__()

        # Insira o que achar necessario no construtor da classe.
        self.ticket = None
        self.thinking_time = randint(MIN_THINKING_TIME, MAX_THINKING_TIME)

    """ Pega o ticket do totem."""

    def get_my_ticket(self):
        self.ticket = shared.get_totem().generate_new_ticket()
        print("[TICKET] - O cliente {} pegou o ticket {}.".format(self._id, self.ticket))

    """ Espera ser atendido pela equipe. """

    def wait_crew(self):
        print("[WAIT] - O cliente {} esta aguardando atendimento.".format(self._id))
        shared.get_ticket_order_synchronizer().block_until_ticket_is_called(self.ticket)

    """ O cliente pensa no pedido."""

    def think_order(self):
        print("[THINK] - O cliente {} esta pensando no que pedir.".format(self._id))
        sleep(self.thinking_time)

    """ O cliente faz o pedido."""

    def order(self):
        shared.get_ticket_order_synchronizer().make_order(self.ticket)
        print("[ORDER] - O cliente {} pediu algo.".format(self._id))

    """ Espera pelo pedido ficar pronto. """

    def wait_chef(self):
        print("[WAIT MEAL] - O cliente {} esta aguardando o prato.".format(self._id))

    """
        O cliente reserva o lugar e se senta.
        Lembre-se que antes de comer o cliente deve ser atendido pela equipe,
        ter seu pedido pronto e possuir um lugar pronto pra sentar.
    """

    def seat_and_eat(self):
        print("[WAIT SEAT] - O cliente {} esta aguardando um lugar ficar livre".format(self._id))
        print("[SEAT] - O cliente {} encontrou um lugar livre e sentou".format(self._id))

    """ O cliente deixa o restaurante."""

    def leave(self):
        print("[LEAVE] - O cliente {} saiu do restaurante".format(self._id))

    """ Thread do cliente """

    def run(self):
        self.get_my_ticket()
        self.wait_crew()
        self.think_order()
        self.order()
        self.wait_chef()
        self.seat_and_eat()
        self.leave()

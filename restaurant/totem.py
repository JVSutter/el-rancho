# imports do Python
from random import randint
from threading import Lock

import restaurant.shared as shared

"""
    Não troque o nome das variáveis compartilhadas, a assinatura e o nomes das funções.
"""
class Totem:
    def __init__(self, number_of_clients):
        super().__init__()
        self.already_sampled = list()
        self.maximum_ticket_number = number_of_clients * 5
        self.call = list()

        # Insira o que achar necessario no construtor da classe.
        self.number_of_clients = number_of_clients
        self.ticket_registry_lock = Lock()

    """
        A função get_ticket não pode ser alterada.
        Ela garante que um ticket aleatório (não repetido) seja criado e que a equipe seja chamada para atendê-lo.
    """
    def get_ticket(self):
        # Gera um ticket aleatório
        ticket_number = randint(1, self.maximum_ticket_number)

        # Garante que o ticket não foi chamado anteriormente
        while ticket_number in self.already_sampled:
            ticket_number = randint(1, self.maximum_ticket_number)
        self.already_sampled.append(ticket_number)

        # Adiciona o ticket na lista de chamadas
        self.call.append(ticket_number)

        self.call_crew()

        return ticket_number

    """Insira sua sincronização."""
    def call_crew(self):
        shared.clients_waiting_crew_sem.release()  # Aciona alguém da equipe
        print("[CALLING] - O totem chamou a equipe para atender o pedido da senha {}.".format(self.already_sampled[-1]))

    """
        Gera um ticket novo e verifica se o cliente atual é o último a ser atendido.
        Caso seja o último, aciona toda a equipe para que finalizem suas threads.
    """
    def generate_new_ticket(self):
        with self.ticket_registry_lock:
            if len(self.already_sampled) == self.number_of_clients - 1:
                self.trigger_all_crew_members()

            return self.get_ticket()

    def trigger_all_crew_members(self):
        for _ in range(shared.crew_size):
            shared.clients_waiting_crew_sem.release()

    def get_priority_ticket(self):
        with self.ticket_registry_lock:
            return min(self.call)

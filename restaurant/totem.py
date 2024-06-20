# imports do Python
from random import randint
from typing import List

import restaurant.shared as shared

"""
    Não troque o nome das variáveis compartilhadas, a assinatura e o nomes das funções.
"""
class Totem:
    def __init__(self, number_of_clients: int) -> None:
        super().__init__()
        self.already_sampled: List[int] = list()
        self.maximum_ticket_number: int = number_of_clients * 5
        self.call: List[int] = list()

        # Insira o que achar necessario no construtor da classe.
        self.number_of_clients: int = number_of_clients

    """
        A função get_ticket não pode ser alterada.
        Ela garante que um ticket aleatório (não repetido) seja criado e que a equipe seja chamada para atendê-lo.
    """
    def get_ticket(self) -> int:
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
    def call_crew(self) -> None:
        shared.clients_waiting_crew_sem.release()  # Aciona alguém da equipe
        print("[CALLING] - O totem chamou a equipe para atender o pedido da senha {}.".format(self.already_sampled[-1]))

    """
        Gera um ticket novo e verifica se o cliente atual é o último a ser atendido.
        Caso seja o último, aciona toda a equipe para que finalizem suas threads.
    """
    def generate_new_ticket(self) -> int:
        if len(self.already_sampled) == self.number_of_clients - 1:  # Se for o último cliente
            self.trigger_all_crew_members()

        return self.get_ticket()

    def trigger_all_crew_members(self) -> None:
        for _ in range(shared.get_crew_size()):
            shared.clients_waiting_crew_sem.release()

    def get_priority_ticket(self) -> int:
        # Se todos os clientes já foram chamados, retorna -1 (valor sentinela)
        if len(self.call) == 0 and len(self.already_sampled) == self.number_of_clients:
            return -1

        priority_ticket = min(self.call)  # O ticket com menor valor é o mais prioritário
        self.call.remove(priority_ticket)

        return priority_ticket

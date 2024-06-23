from threading import Semaphore, Lock
"""
    Não troque o nome das variáveis compartilhadas, a assinatura e o nomes das funções.
"""
class Table:
    """ Inicia a mesa com um número de lugares """
    def __init__(self, number: int) -> None:
        # Insira o que achar necessario no construtor da classe.
        self.seats_sem = Semaphore(number)  # Semáforo para controlar o acesso aos lugares
        self.clients_sitting = []  # Lista de clientes sentados
        self.print_clients_sitting_lock = Lock()

    """ O cliente se senta na mesa."""
    def seat(self, client: int) -> None:
        self.seats_sem.acquire()  # Aguarda um lugar livre
        self.clients_sitting.append(client)

        print(
            "[SEAT] - O cliente {} encontrou um lugar livre e sentou".format(client)
        )
        print("[TABLE] - Clientes na mesa: {}.".format(self.clients_sitting))

    """ O cliente deixa a mesa."""
    def leave(self, client: int):
        self.clients_sitting.remove(client)
        self.seats_sem.release()  # Libera um lugar
        print("[TABLE] - Clientes na mesa: {}.".format(self.clients_sitting))

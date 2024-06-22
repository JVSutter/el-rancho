from threading import Semaphore
"""
    Não troque o nome das variáveis compartilhadas, a assinatura e o nomes das funções.
"""
class Table:
    """ Inicia a mesa com um número de lugares """
    def __init__(self, number: int) -> None:
        self._number = number
        # Insira o que achar necessario no construtor da classe.
        self._seats_sem = Semaphore(number)
        self._clients = []

    """ O cliente se senta na mesa."""
    def seat(self, client: int) -> None:
        self._clients.append(client)
        self._seats_sem.acquire()
        print(
            "[SEAT] - O cliente {} encontrou um lugar livre e sentou".format(client)
        )

        print("[TABLE] - Clientes na mesa: {}.".format(self._clients))

    """ O cliente deixa a mesa."""
    def leave(self, client: int):
        self._clients.remove(client)
        self._seats_sem.release()
        if len(self._clients) == 0:
            print("[TABLE] - Não há clientes na mesa.")
            return

        print("[TABLE] - Clientes na mesa: {}.".format(self._clients))

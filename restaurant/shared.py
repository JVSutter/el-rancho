# Espaco reservado para voce inserir suas variaveis globais.
# Voce pode inserir como funcao (exemplo):
#
#  my_global_variable = 'Awesome value'
#  def get_my_global_variable():
#       global my_global_variable
#       return my_global_variable

totem = None  # Instância do totem

clients_waiting_crew_sem = None  # Semáforo cujo valor é igual ao n° de clientes esperando a equipe

ticket_order_synchronizer = None  # Sincronizador de pedidos e chamadas de tickets

crew_size = None  # Tamanho da equipe


def get_totem():
    global totem
    return totem


def get_clients_waiting_crew_sem():
    global clients_waiting_crew_sem
    return clients_waiting_crew_sem


def get_ticket_order_synchronizer():
    global ticket_order_synchronizer
    return ticket_order_synchronizer


def get_crew_size():
    global crew_size
    return crew_size

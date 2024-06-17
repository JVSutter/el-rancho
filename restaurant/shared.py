# Espaco reservado para voce inserir suas variaveis globais.
# Voce pode inserir como funcao (exemplo):
#
#  my_global_variable = 'Awesome value'
#  def get_my_global_variable():
#       global my_global_variable
#       return my_global_variable

totem = None  # Instância do totem

clients_waiting_crew_sem = None  # Semáforo cujo valor é igual ao n° de clientes esperando a equipe

crew_size = None  # Tamanho da equipe


def get_totem():
    global totem
    return totem


def get_clients_waiting_crew_sem():
    global clients_waiting_crew_sem
    return clients_waiting_crew_sem


def get_crew_size():
    global crew_size
    return crew_size

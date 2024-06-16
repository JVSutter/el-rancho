# Espaco reservado para voce inserir suas variaveis globais.
# Voce pode inserir como funcao (exemplo):
#
#  my_global_variable = 'Awesome value'
#  def get_my_global_variable():
#       global my_global_variable
#       return my_global_variable

totem = None

client_can_continue_events = None
clients_waiting_crew_sem = None

crew_size = None


def get_totem():
    global totem
    return totem


def get_client_can_continue_events():
    global client_can_continue_events
    return client_can_continue_events


def get_clients_waiting_crew_sem():
    global clients_waiting_crew_sem
    return clients_waiting_crew_sem

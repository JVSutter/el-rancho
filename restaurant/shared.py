# Espaco reservado para voce inserir suas variaveis globais.
# Voce pode inserir como funcao (exemplo):
#
#  my_global_variable = 'Awesome value'
#  def get_my_global_variable():
#       global my_global_variable
#       return my_global_variable

totem = None

def get_totem():
    global totem
    return totem

# imports do Python
from threading import Thread, Semaphore
from restaurant.shared import *
from restaurant.client import Client
"""
    Não troque o nome das variáveis compartilhadas, a assinatura e o nomes das funções.
"""
class Crew(Thread):
    
    """ Inicia o membro da equipe com um id (use se necessario)."""
    def __init__(self, id):
        super().__init__()
        self._id = id
        self._semaforo_espera_escolha = Semaphore(0) # Semáforo para esperar o cliente escolher o pedido
        self._ticket_atendendo_atual = None
        # Insira o que achar necessario no construtor da classe.

    """ O membro da equipe espera um cliente. """    
    def wait(self):
        print("O membro da equipe {} está esperando um cliente.".format(self._id))
        acquire_semaforo_espera_entrar() # Adquire o semáforo para que espere o cliente entrar no restaurante para continuar o funcionamento

    """ O membro da equipe chama o cliente da senha ticket."""
    def call_client(self, ticket):
        get_totem_restaurante().semaforo_alteracao.acquire() # Adquire o semáforo para previnir condição de corrida
        ticket_atendido = get_totem_restaurante().call.pop(0) # Pega o ticket que está na primeira posição da lista de chamadas
        #get_totem_restaurante().call.pop() # Remove o ticket da lista de chamadas
        get_totem_restaurante().semaforo_alteracao.release()
        print("[CALLING] - O membro da equipe {} está chamando o cliente da senha {}.".format(self._id, ticket_atendido))
        for client in lista_clientes:   # Procura o cliente com a senha igual a ticket
            if client.get_ticket_number() == ticket_atendido:
                self._ticket_atendendo_atual = ticket_atendido
                client.get_semaforo_wait_atendente().release() # Libera o semáforo para que o cliente seja atendido
                self._semaforo_espera_escolha.acquire() # Espera o cliente escolher o pedido

    def make_order(self, order):
        print("[STORING] - O membro da equipe {} está anotando o pedido {} para o chef.".format(self._id, order))

    """ Thread do membro da equipe."""
    def run(self):
        
        self.wait()
        self.call_client(get_totem_restaurante().call)
        self.make_order(0)
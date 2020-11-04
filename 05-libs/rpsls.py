#!/usr/bin/env python3

from random import choice


class Rpsls:

    def __init__(self):
        self.elements = {
            'piedra': ('lagarto', 'tijeras'),
            'papel': ('piedra', 'spock'),
            'tijeras': ('papel', 'lagarto'),
            'lagarto': ('spock', 'papel'),
            'spock': ('tijeras', 'piedra')    
        }

        self.choices = list(self.elements.keys())
        self.player_score = 0
        self.cpu_score = 0

    def player_choice(self):
        player_choice = None
        while player_choice not in self.choices:
            player_choice = input('Introduce tu elección [Piedra, Papel, Tijeras, Lagarto o Spock]: ').lower()
        return player_choice

    def cpu_choice(self):
        return choice(self.choices)

    def action(self, choice1, choice2):
        action = ''
        if choice1 == 'piedra':
            action = 'aplasta'
        elif choice1 == 'papel':
            action = 'cubre' if choice2 == 'piedra' else 'desaprueba'
        elif choice1 == 'tijeras':
            action = 'cortan' if choice2 == 'papel' else 'decapitan'
        elif choice1 == 'lagarto':
            action = 'envenena' if choice2 =='spock' else 'come'
        elif choice1 == 'spock':
            action = 'destruye' if choice2 == 'tijeras' else 'vaporiza'
        return action

    def result(self, player_choice, cpu_choice):
        if player_choice == cpu_choice:
            print('¡Empate!')
        elif player_choice in self.elements[cpu_choice]:
            action = self.action(cpu_choice, player_choice)
            self.cpu_score += 1
            print(f'{cpu_choice} {action} {player_choice}\n¡Has perdido!')
        else:
            action = self.action(player_choice, cpu_choice)
            self.player_score += 1
            print(f'{player_choice} {action} {cpu_choice}\n¡Has ganado!')

    def play(self):
        while True:
            player_choice = self.player_choice()
            cpu_choice = self.cpu_choice()
            print(f'\n[{player_choice}] vs [{cpu_choice}]\n')
            self.result(player_choice, cpu_choice)
            print('-' * 17)
            print(f'Puntuación: {self.player_score} - {self.cpu_score}\n')
            repeat = input('¿Quieres seguir jugando? [S/n] ').lower()
            if repeat in ['', 's', 'si']:
                print('\n' + '+' * 30 + '\n')
                continue
            else:
                exit()


if __name__ == '__main__':
    Rpsls().play()
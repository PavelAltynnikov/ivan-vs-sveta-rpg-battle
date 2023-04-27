import random
from typing import Protocol, Callable

from sveta_hero import SvetaHero
from hero_class import Hero


class HeroProtocol(Protocol):
    name: str

    def deal_damage(self):
        ...

    def take_damage(self, damage):
        ...

    def defense(self):
        ...

    def stop_defense(self):
        ...

    def rest(self):
        ...


class Action:
    def __init__(self, title: str, priority: int, method: Callable[..., None], playerTurn):
        self.title = title
        self.priority = priority
        self.method = method
        self.player_turn = playerTurn

    def __call__(self):
        return self.method()


class PlayerTurn:
    def __init__(self, player_name: str, character: HeroProtocol, enemy: HeroProtocol):
        self.player_name = player_name
        self._character = character
        self._enemy = enemy
        self._actions = {
            '1': Action('Атаковать', 1, self._attack_action, self),
            '2': Action('Защищаться', 2, self._defense_action, self),
            '3': Action('Отдыхать', 0, self._rest_action, self),
        }

    def ask_action(self) -> Action:
        print(f'\nЧто будет делать {self._character.name}?')

        for action_number, action in self._actions.items():
            print(f'{action_number}. {action.title}')

        return self._choose_action()

    def _choose_action(self) -> Action:
        while True:
            action_number = input('Ответ: ')
            if action_number in self._actions:
                return self._actions[action_number]
            print('Не корректный ввод данных. Нужно выбрать один из вариантов')

    def _attack_action(self):
        self._character.stop_defense()
        self._enemy.take_damage(self._character.deal_damage())

    def _defense_action(self):
        self._character.defense()

    def _rest_action(self):
        self._character.stop_defense()
        self._character.rest()


class Game:
    def __init__(self, hero_1: SvetaHero, hero_2: Hero):
        self.hero_1 = hero_1
        self.hero_2 = hero_2
        self.turn_hero_1 = PlayerTurn('Света', hero_1, hero_2)  # type: ignore
        self.turn_hero_2 = PlayerTurn('Иван', hero_2, hero_1)  # type: ignore
        self.winner = None
        self.is_game_over = False

    def show_intro(self):
        print('Добро пожаловать на поединок боевых героев созданных Иваном и Светой!!!')

    def start_game_loop(self):
        while not self.is_game_over:
            self._show_characters_characteristics()

            first_action, second_action = self._assign_actions_order(
                self.turn_hero_1.ask_action(),
                self.turn_hero_2.ask_action()
            )

            self._make_a_move(first_action, 'первым')
            self._assign_winner()

            self._make_a_move(second_action, 'вторым')
            self._assign_winner()

        self._announce_winner()
        self._show_characters_characteristics()

    def _assign_actions_order(self, action_1, action_2):
        if action_1.priority == action_2.priority:
            return random.sample((action_1, action_2), 2)

        if action_1.priority > action_2.priority:
            return action_1, action_2

        return action_2, action_1

    def _make_a_move(self, action: Action, order: str):
        self._announce_action(action, order)
        action()

    def _announce_action(self, action: Action, order: str):
        print(f'\n{action.player_turn.player_name} будет {action.title} {order}')

    def _assign_winner(self):
        if self.hero_1.health != 0 and self.hero_2.hp != 0:
            return

        if self.hero_1.health == 0:
            self.winner = self.hero_2
        else:
            self.winner = self.hero_1

        self.is_game_over = True

    def _announce_winner(self):
        if self.winner:
            print(f'\nВыиграл {self.winner.name}')
        else:
            print('Ничья')

    def _show_characters_characteristics(self):
        print(f'\nХарактеристики персонажей\n\n{self.hero_1}\n\n{self.hero_2}')


def main():
    halfling = SvetaHero('Серафима Подсветкина', 'Вор', 'Халфлинг')
    warrior = Hero('Волик', 'Воин', 'Человек', 100, 100, 12, 10)

    game = Game(halfling, warrior)
    game.show_intro()
    game.start_game_loop()


if __name__ == '__main__':
    main()

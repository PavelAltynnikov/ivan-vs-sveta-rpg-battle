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

    def rest(self):
        ...


class Action:
    def __init__(self, title: str, priority: int, method: Callable[..., None]):
        self.title = title
        self.priority = priority
        self.method = method

    def __call__(self):
        return self.method()


class PlayerTurn:
    def __init__(self, character: HeroProtocol, enemy: HeroProtocol):
        self._character = character
        self._enemy = enemy
        self._actions = {
            '1': Action('Атаковать', 1, self._attack_action),
            '2': Action('Защищаться', 2, self._defense_action),
            '3': Action('Отдыхать', 0, self._rest_action),
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
        damage = self._character.deal_damage()
        self._enemy.take_damage(damage)

    def _defense_action(self):
        self._character.defense()

    def _rest_action(self):
        self._character.rest()


halfling = SvetaHero('Серафима Подсветкина', 'Вор', 'Халфлинг')
warrior = Hero('Волик', 'Воин', 'Человек', 100, 100, 12, 10)

sveta_turn = PlayerTurn(halfling, warrior)  # type: ignore
ivan_turn = PlayerTurn(warrior, halfling)  # type: ignore

game_over = False

print('Добро пожаловать на поединок боевых героев созданных Иваном и Светой!!!')

while not game_over:
    print(f'\nХарактеристики персонажей\n\n{halfling}\n\n{warrior}')

    sveta_action = sveta_turn.ask_action()
    ivan_action = ivan_turn.ask_action()

    if sveta_action.priority > ivan_action.priority:
        print(f'\n{halfling.name} будет {sveta_action.title} первым')
        sveta_action()
        print(f'{warrior.name} будет {ivan_action.title} вторым')
        ivan_action()
    else:
        print(f'\n{warrior.name} будет {ivan_action.title} первым')
        ivan_action()
        print(f'{halfling.name} будет {sveta_action.title} вторым')
        sveta_action()

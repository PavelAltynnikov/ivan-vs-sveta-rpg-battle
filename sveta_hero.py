class SvetaHero:
    def __init__(self, name, classN, race) -> None:
        self.name = name
        self.classN = classN
        self.race = race
        self.health = 100
        self.stamina = 1
        self.moneyPocket = []
        self.coordinates = (0, 0)
        self.armor = 50
        self.weapon = 10
        self.is_defense = False

    def movement(self, new_coordinates):
        self.coordinates = new_coordinates

    def get_coin(self, coin):
        self.moneyPocket.append(coin)

    def deal_damage(self):
        self.is_defense = False

        if self.stamina <= 0:
            return 0

        fatigue = 0.1
        self.stamina -= fatigue

        return self.weapon * self.stamina

    def take_damage(self, damage):
        damage, fatigue = self._try_to_defeat(damage)

        self.stamina -= fatigue
        new_health = self.health - damage

        if new_health < 0:
            self.health = 0
        else:
            self.health = new_health

    def _try_to_defeat(self, damage):
        fatigue = 0.1

        if self.is_defense:
            fatigue = 0.2
            damage -= self.armor
            if damage < 0:
                damage = 0

        return damage, fatigue

    def defense(self):
        if self.stamina >= 0:
            self.is_defense = True
        else:
            self.is_defense = False

    def stop_defense(self):
        self.is_defense = False

    def rest(self):
        if self.stamina == 1:
            return

        new_value = self.stamina + 0.3
        if new_value >= 1:
            self.stamina = 1
        else:
            self.stamina = new_value

    def __str__(self):
        return '\n'.join(f'{attr}: {value}' for attr, value in self.__dict__.items())


if __name__ == '__main__':
    h_1 = SvetaHero('Garik', 'shaman', 'ork')
    h_2 = SvetaHero('Vitek', 'kuharka', 'niger')
    print(h_1.name)
    print(h_2.name)
    print(h_1.deal_damage())
    print(h_1.deal_damage())
    print(h_1.deal_damage())
    print(h_1.deal_damage())
    print(h_1.deal_damage())
    print(h_1.deal_damage())
    print(h_1.deal_damage())
    print(h_1.deal_damage())
    print(h_1.deal_damage())

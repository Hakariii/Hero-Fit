class Enemy:
    def __init__(self,hp,damage,name):
        self._hp = hp
        self._damage = damage
        self._name = name
    def get_health(self):
        return self._hp
    def get_damage(self):
        return self._damage
    def get_name(self):
        return self._name

global Enemies
Enemies = []
with open("Enemies.txt", "r") as file:
    for line in file:
        currentline = line.strip().split(",")
        Enemies.append(Enemy(int(currentline[0]),int(currentline[1]),str(currentline[2])))



for enemy in Enemies:
    print(enemy.get_name())

% Факты с одним аргументом

% Измерения

world(overworld).
world(nether).
world(end).

% Мобы

mob(creeper).
mob(zombie).
mob(piglin).
mob(enderman).
mob(villager).

% Свойства мобов

hostile(creeper).
hostile(zombie).
hostile(piglin).
hostile(enderman).

neutral(villager).

trader(piglin).
trader(villager).

% Ресурсы

resource(diamond).
resource(iron).
resource(gold).
resource(emerald).
resource(obsidian).
resource(gunpowder).
resource(ender_pearl).

% Руды

ore(diamond).
ore(iron).
ore(gold).

% Оружие

weapon(diamond_sword).
weapon(iron_sword).

% Броня

armor(diamond_armor).

% Редкие ресурсы

rare(diamond).
rare(emerald).
rare(ender_pearl).

% Создаваемые предметы

craftable(diamond_sword).
craftable(iron_sword).
craftable(diamond_armor).




% Факты с двумя аргументами

% Места обитания мобов

lives_in(creeper, overworld).
lives_in(zombie, overworld).
lives_in(piglin, nether).
lives_in(enderman, end).
lives_in(villager, overworld).

% Места нахождения ресурсов

found_in(diamond, overworld).
found_in(iron, overworld).
found_in(gold, nether).
found_in(obsidian, nether).

% Предметы и ресурсы для их создания

crafted_from(diamond_sword, diamond).
crafted_from(iron_sword, iron).
crafted_from(diamond_armor, diamond).

% Предметы, получаемые с мобов

drops(creeper, gunpowder).
drops(zombie, iron).
drops(piglin, gold).
drops(enderman, ender_pearl).

% Торговля

trades(villager, emerald).
trades(piglin, gold).




% Правила

% 1. Определяем измерения, в которых существуют враждебные мобы.

dangerous_world(World) :-
    hostile(Mob),
    lives_in(Mob, World).


% 2. Определяем редкие предметы, которые можно получить после убийства моба.

rare_drop(Mob, Item) :-
    drops(Mob, Item),
    rare(Item).


% 3. Определяем предметы, которые можно создать из редких ресурсов.

rare_craft(Item) :-
    craftable(Item),
    crafted_from(Item, Resource),
    rare(Resource).


% 4. Определяем торговцев, которые находятся в Незере.

nether_trader(Mob) :-
    trader(Mob),
    lives_in(Mob, nether).


% 5. Определяем предметы, которые можно получить использовать в торговле 
% и которые являются редкими ресурсами.

valuable_trade(Mob, Item) :-
    trades(Mob, Item),
    rare(Item).
"""
    Data for database demonstrations
"""


def get_furniture_data():
    """
    demonstration data
    """

    furniture_data = [
        {
            'product_type': 'Couch',
            'color': 'Red',
            'description': 'Leather low back',
            'monthly_rental_cost': 12.99,
            'in_stock_quantity': 10
        },
        {
            'product_type': 'Couch',
            'color': 'Blue',
            'description': 'Cloth high back',
            'monthly_rental_cost': 9.99,
            'in_stock_quantity': 3
        },
        {
            'product_type': 'Coffee Table',
            'color': 'Brown',
            'description': 'Plastic',
            'monthly_rental_cost': 2.50,
            'in_stock_quantity': 25
        },
        {
            'product_type': 'Couch',
            'color': 'Red',
            'description': 'Leather high back',
            'monthly_rental_cost': 15.99,
            'in_stock_quantity': 17
        },
        {
            'product_type': 'Recliner',
            'color': 'Blue',
            'description': 'Leather high back',
            'monthly_rental_cost': 19.99,
            'in_stock_quantity': 6
        },
        {
            'product_type': 'Chair',
            'color': 'Brown',
            'description': 'Plastic',
            'monthly_rental_cost': 1.00,
            'in_stock_quantity': 45
        },
        {
            'product_type': 'Recliner',
            'color': 'Red',
            'description': 'Leather high back',
            'monthly_rental_cost': 19.99,
            'in_stock_quantity': 6
        },
        {
            'product_type': 'Couch',
            'color': 'Green',
            'description': 'Cloth high back',
            'monthly_rental_cost': 15.99,
            'in_stock_quantity': 3
        },
    ]
    return furniture_data


def get_pokemon_flying_data():
    """
    for pickle demonstration
    """

    pokemon_flying_data = {
        "name": "flying",
        "generation": {
            "url": "https://pokeapi.co/api/v2/generation/1/",
            "name": "generation-i"
        },
        "damage_relations": {
            "half_damage_from": [
                {
                    "url": "https://pokeapi.co/api/v2/type/2/",
                    "name": "fighting"
                },
                {
                    "url": "https://pokeapi.co/api/v2/type/7/",
                    "name": "bug"
                },
                {
                    "url": "https://pokeapi.co/api/v2/type/12/",
                    "name": "grass"
                }
            ],
            "no_damage_from": [
                {
                    "url": "https://pokeapi.co/api/v2/type/5/",
                    "name": "ground"
                }
            ],
            "half_damage_to": [
                {
                    "url": "https://pokeapi.co/api/v2/type/6/",
                    "name": "rock"
                },
                {
                    "url": "https://pokeapi.co/api/v2/type/9/",
                    "name": "steel"
                },
                {
                    "url": "https://pokeapi.co/api/v2/type/13/",
                    "name": "electric"
                }
            ],
            "double_damage_from": [
                {
                    "url": "https://pokeapi.co/api/v2/type/6/",
                    "name": "rock"
                },
                {
                    "url": "https://pokeapi.co/api/v2/type/13/",
                    "name": "electric"
                },
                {
                    "url": "https://pokeapi.co/api/v2/type/15/",
                    "name": "ice"
                }
            ],
            "no_damage_to": [],
            "double_damage_to": [
                {
                    "url": "https://pokeapi.co/api/v2/type/2/",
                    "name": "fighting"
                },
                {
                    "url": "https://pokeapi.co/api/v2/type/7/",
                    "name": "bug"
                },
                {
                    "url": "https://pokeapi.co/api/v2/type/12/",
                    "name": "grass"
                }
            ]
        },
        "game_indices": [
            {
                "generation": {
                    "url": "https://pokeapi.co/api/v2/generation/1/",
                    "name": "generation-i"
                },
                "game_index": 2
            },
            {
                "generation": {
                    "url": "https://pokeapi.co/api/v2/generation/2/",
                    "name": "generation-ii"
                },
                "game_index": 2
            },
            {
                "generation": {
                    "url": "https://pokeapi.co/api/v2/generation/3/",
                    "name": "generation-iii"
                },
                "game_index": 2
            },
            {
                "generation": {
                    "url": "https://pokeapi.co/api/v2/generation/4/",
                    "name": "generation-iv"
                },
                "game_index": 2
            },
            {
                "generation": {
                    "url": "https://pokeapi.co/api/v2/generation/5/",
                    "name": "generation-v"
                },
                "game_index": 2
            },
            {
                "generation": {
                    "url": "https://pokeapi.co/api/v2/generation/6/",
                    "name": "generation-vi"
                },
                "game_index": 2
            }
        ],
        "move_damage_class": {
            "url": "https://pokeapi.co/api/v2/move-damage-class/2/",
            "name": "physical"
        },
        "moves": [
            {
                "url": "https://pokeapi.co/api/v2/move/16/",
                "name": "gust"
            },
            {
                "url": "https://pokeapi.co/api/v2/move/17/",
                "name": "wing-attack"
            },
            {
                "url": "https://pokeapi.co/api/v2/move/19/",
                "name": "fly"
            },
            {
                "url": "https://pokeapi.co/api/v2/move/64/",
                "name": "peck"
            },
            {
                "url": "https://pokeapi.co/api/v2/move/65/",
                "name": "drill-peck"
            },
            {
                "url": "https://pokeapi.co/api/v2/move/119/",
                "name": "mirror-move"
            },
            {
                "url": "https://pokeapi.co/api/v2/move/143/",
                "name": "sky-attack"
            },
            {
                "url": "https://pokeapi.co/api/v2/move/177/",
                "name": "aeroblast"
            },
            {
                "url": "https://pokeapi.co/api/v2/move/297/",
                "name": "feather-dance"
            },
            {
                "url": "https://pokeapi.co/api/v2/move/314/",
                "name": "air-cutter"
            },
            {
                "url": "https://pokeapi.co/api/v2/move/332/",
                "name": "aerial-ace"
            },
            {
                "url": "https://pokeapi.co/api/v2/move/340/",
                "name": "bounce"
            },
            {
                "url": "https://pokeapi.co/api/v2/move/355/",
                "name": "roost"
            },
            {
                "url": "https://pokeapi.co/api/v2/move/365/",
                "name": "pluck"
            },
            {
                "url": "https://pokeapi.co/api/v2/move/366/",
                "name": "tailwind"
            },
            {
                "url": "https://pokeapi.co/api/v2/move/403/",
                "name": "air-slash"
            },
            {
                "url": "https://pokeapi.co/api/v2/move/413/",
                "name": "brave-bird"
            },
            {
                "url": "https://pokeapi.co/api/v2/move/432/",
                "name": "defog"
            },
            {
                "url": "https://pokeapi.co/api/v2/move/448/",
                "name": "chatter"
            },
            {
                "url": "https://pokeapi.co/api/v2/move/507/",
                "name": "sky-drop"
            },
            {
                "url": "https://pokeapi.co/api/v2/move/512/",
                "name": "acrobatics"
            },
            {
                "url": "https://pokeapi.co/api/v2/move/542/",
                "name": "hurricane"
            },
            {
                "url": "https://pokeapi.co/api/v2/move/613/",
                "name": "oblivion-wing"
            },
            {
                "url": "https://pokeapi.co/api/v2/move/620/",
                "name": "dragon-ascent"
            },
            {
                "url": "https://pokeapi.co/api/v2/move/626/",
                "name": "supersonic-skystrike--physical"
            },
            {
                "url": "https://pokeapi.co/api/v2/move/627/",
                "name": "supersonic-skystrike--special"
            },
            {
                "url": "https://pokeapi.co/api/v2/move/690/",
                "name": "beak-blast"
            }
        ],
        "pokemon": [
            {
                "slot": 2,
                "pokemon": {
                    "url": "https://pokeapi.co/api/v2/pokemon/6/",
                    "name": "charizard"
                }
            },
            {
                "slot": 2,
                "pokemon": {
                    "url": "https://pokeapi.co/api/v2/pokemon/12/",
                    "name": "butterfree"
                }
            },
            {
                "slot": 2,
                "pokemon": {
                    "url": "https://pokeapi.co/api/v2/pokemon/16/",
                    "name": "pidgey"
                }
            },
            {
                "slot": 2,
                "pokemon": {
                    "url": "https://pokeapi.co/api/v2/pokemon/17/",
                    "name": "pidgeotto"
                }
            },
            {
                "slot": 2,
                "pokemon": {
                    "url": "https://pokeapi.co/api/v2/pokemon/18/",
                    "name": "pidgeot"
                }
            },
            {
                "slot": 2,
                "pokemon": {
                    "url": "https://pokeapi.co/api/v2/pokemon/21/",
                    "name": "spearow"
                }
            },
            {
                "slot": 2,
                "pokemon": {
                    "url": "https://pokeapi.co/api/v2/pokemon/22/",
                    "name": "fearow"
                }
            },
            {
                "slot": 2,
                "pokemon": {
                    "url": "https://pokeapi.co/api/v2/pokemon/41/",
                    "name": "zubat"
                }
            },
            {
                "slot": 2,
                "pokemon": {
                    "url": "https://pokeapi.co/api/v2/pokemon/42/",
                    "name": "golbat"
                }
            },
            {
                "slot": 2,
                "pokemon": {
                    "url": "https://pokeapi.co/api/v2/pokemon/83/",
                    "name": "farfetchd"
                }
            },
            {
                "slot": 2,
                "pokemon": {
                    "url": "https://pokeapi.co/api/v2/pokemon/84/",
                    "name": "doduo"
                }
            },
            {
                "slot": 2,
                "pokemon": {
                    "url": "https://pokeapi.co/api/v2/pokemon/85/",
                    "name": "dodrio"
                }
            },
            {
                "slot": 2,
                "pokemon": {
                    "url": "https://pokeapi.co/api/v2/pokemon/123/",
                    "name": "scyther"
                }
            },
            {
                "slot": 2,
                "pokemon": {
                    "url": "https://pokeapi.co/api/v2/pokemon/130/",
                    "name": "gyarados"
                }
            },
            {
                "slot": 2,
                "pokemon": {
                    "url": "https://pokeapi.co/api/v2/pokemon/142/",
                    "name": "aerodactyl"
                }
            },
            {
                "slot": 2,
                "pokemon": {
                    "url": "https://pokeapi.co/api/v2/pokemon/144/",
                    "name": "articuno"
                }
            },
            {
                "slot": 2,
                "pokemon": {
                    "url": "https://pokeapi.co/api/v2/pokemon/145/",
                    "name": "zapdos"
                }
            },
            {
                "slot": 2,
                "pokemon": {
                    "url": "https://pokeapi.co/api/v2/pokemon/146/",
                    "name": "moltres"
                }
            },
            {
                "slot": 2,
                "pokemon": {
                    "url": "https://pokeapi.co/api/v2/pokemon/149/",
                    "name": "dragonite"
                }
            },
            {
                "slot": 2,
                "pokemon": {
                    "url": "https://pokeapi.co/api/v2/pokemon/163/",
                    "name": "hoothoot"
                }
            },
            {
                "slot": 2,
                "pokemon": {
                    "url": "https://pokeapi.co/api/v2/pokemon/164/",
                    "name": "noctowl"
                }
            },
            {
                "slot": 2,
                "pokemon": {
                    "url": "https://pokeapi.co/api/v2/pokemon/165/",
                    "name": "ledyba"
                }
            },
            {
                "slot": 2,
                "pokemon": {
                    "url": "https://pokeapi.co/api/v2/pokemon/166/",
                    "name": "ledian"
                }
            },
            {
                "slot": 2,
                "pokemon": {
                    "url": "https://pokeapi.co/api/v2/pokemon/169/",
                    "name": "crobat"
                }
            },
            {
                "slot": 2,
                "pokemon": {
                    "url": "https://pokeapi.co/api/v2/pokemon/176/",
                    "name": "togetic"
                }
            },
            {
                "slot": 2,
                "pokemon": {
                    "url": "https://pokeapi.co/api/v2/pokemon/177/",
                    "name": "natu"
                }
            },
            {
                "slot": 2,
                "pokemon": {
                    "url": "https://pokeapi.co/api/v2/pokemon/178/",
                    "name": "xatu"
                }
            },
            {
                "slot": 2,
                "pokemon": {
                    "url": "https://pokeapi.co/api/v2/pokemon/187/",
                    "name": "hoppip"
                }
            },
            {
                "slot": 2,
                "pokemon": {
                    "url": "https://pokeapi.co/api/v2/pokemon/188/",
                    "name": "skiploom"
                }
            },
            {
                "slot": 2,
                "pokemon": {
                    "url": "https://pokeapi.co/api/v2/pokemon/189/",
                    "name": "jumpluff"
                }
            },
            {
                "slot": 2,
                "pokemon": {
                    "url": "https://pokeapi.co/api/v2/pokemon/193/",
                    "name": "yanma"
                }
            },
            {
                "slot": 2,
                "pokemon": {
                    "url": "https://pokeapi.co/api/v2/pokemon/198/",
                    "name": "murkrow"
                }
            },
            {
                "slot": 2,
                "pokemon": {
                    "url": "https://pokeapi.co/api/v2/pokemon/207/",
                    "name": "gligar"
                }
            },
            {
                "slot": 2,
                "pokemon": {
                    "url": "https://pokeapi.co/api/v2/pokemon/225/",
                    "name": "delibird"
                }
            },
            {
                "slot": 2,
                "pokemon": {
                    "url": "https://pokeapi.co/api/v2/pokemon/226/",
                    "name": "mantine"
                }
            },
            {
                "slot": 2,
                "pokemon": {
                    "url": "https://pokeapi.co/api/v2/pokemon/227/",
                    "name": "skarmory"
                }
            },
            {
                "slot": 2,
                "pokemon": {
                    "url": "https://pokeapi.co/api/v2/pokemon/249/",
                    "name": "lugia"
                }
            },
            {
                "slot": 2,
                "pokemon": {
                    "url": "https://pokeapi.co/api/v2/pokemon/250/",
                    "name": "ho-oh"
                }
            },
            {
                "slot": 2,
                "pokemon": {
                    "url": "https://pokeapi.co/api/v2/pokemon/267/",
                    "name": "beautifly"
                }
            },
            {
                "slot": 2,
                "pokemon": {
                    "url": "https://pokeapi.co/api/v2/pokemon/276/",
                    "name": "taillow"
                }
            },
            {
                "slot": 2,
                "pokemon": {
                    "url": "https://pokeapi.co/api/v2/pokemon/277/",
                    "name": "swellow"
                }
            },
            {
                "slot": 2,
                "pokemon": {
                    "url": "https://pokeapi.co/api/v2/pokemon/278/",
                    "name": "wingull"
                }
            },
            {
                "slot": 2,
                "pokemon": {
                    "url": "https://pokeapi.co/api/v2/pokemon/279/",
                    "name": "pelipper"
                }
            },
            {
                "slot": 2,
                "pokemon": {
                    "url": "https://pokeapi.co/api/v2/pokemon/284/",
                    "name": "masquerain"
                }
            },
            {
                "slot": 2,
                "pokemon": {
                    "url": "https://pokeapi.co/api/v2/pokemon/291/",
                    "name": "ninjask"
                }
            },
            {
                "slot": 2,
                "pokemon": {
                    "url": "https://pokeapi.co/api/v2/pokemon/333/",
                    "name": "swablu"
                }
            },
            {
                "slot": 2,
                "pokemon": {
                    "url": "https://pokeapi.co/api/v2/pokemon/334/",
                    "name": "altaria"
                }
            },
            {
                "slot": 2,
                "pokemon": {
                    "url": "https://pokeapi.co/api/v2/pokemon/357/",
                    "name": "tropius"
                }
            },
            {
                "slot": 2,
                "pokemon": {
                    "url": "https://pokeapi.co/api/v2/pokemon/373/",
                    "name": "salamence"
                }
            },
            {
                "slot": 2,
                "pokemon": {
                    "url": "https://pokeapi.co/api/v2/pokemon/384/",
                    "name": "rayquaza"
                }
            },
            {
                "slot": 2,
                "pokemon": {
                    "url": "https://pokeapi.co/api/v2/pokemon/396/",
                    "name": "starly"
                }
            },
            {
                "slot": 2,
                "pokemon": {
                    "url": "https://pokeapi.co/api/v2/pokemon/397/",
                    "name": "staravia"
                }
            },
            {
                "slot": 2,
                "pokemon": {
                    "url": "https://pokeapi.co/api/v2/pokemon/398/",
                    "name": "staraptor"
                }
            },
            {
                "slot": 2,
                "pokemon": {
                    "url": "https://pokeapi.co/api/v2/pokemon/414/",
                    "name": "mothim"
                }
            },
            {
                "slot": 2,
                "pokemon": {
                    "url": "https://pokeapi.co/api/v2/pokemon/415/",
                    "name": "combee"
                }
            },
            {
                "slot": 2,
                "pokemon": {
                    "url": "https://pokeapi.co/api/v2/pokemon/416/",
                    "name": "vespiquen"
                }
            },
            {
                "slot": 2,
                "pokemon": {
                    "url": "https://pokeapi.co/api/v2/pokemon/425/",
                    "name": "drifloon"
                }
            },
            {
                "slot": 2,
                "pokemon": {
                    "url": "https://pokeapi.co/api/v2/pokemon/426/",
                    "name": "drifblim"
                }
            },
            {
                "slot": 2,
                "pokemon": {
                    "url": "https://pokeapi.co/api/v2/pokemon/430/",
                    "name": "honchkrow"
                }
            },
            {
                "slot": 2,
                "pokemon": {
                    "url": "https://pokeapi.co/api/v2/pokemon/441/",
                    "name": "chatot"
                }
            },
            {
                "slot": 2,
                "pokemon": {
                    "url": "https://pokeapi.co/api/v2/pokemon/458/",
                    "name": "mantyke"
                }
            },
            {
                "slot": 2,
                "pokemon": {
                    "url": "https://pokeapi.co/api/v2/pokemon/468/",
                    "name": "togekiss"
                }
            },
            {
                "slot": 2,
                "pokemon": {
                    "url": "https://pokeapi.co/api/v2/pokemon/469/",
                    "name": "yanmega"
                }
            },
            {
                "slot": 2,
                "pokemon": {
                    "url": "https://pokeapi.co/api/v2/pokemon/472/",
                    "name": "gliscor"
                }
            },
            {
                "slot": 2,
                "pokemon": {
                    "url": "https://pokeapi.co/api/v2/pokemon/519/",
                    "name": "pidove"
                }
            },
            {
                "slot": 2,
                "pokemon": {
                    "url": "https://pokeapi.co/api/v2/pokemon/520/",
                    "name": "tranquill"
                }
            },
            {
                "slot": 2,
                "pokemon": {
                    "url": "https://pokeapi.co/api/v2/pokemon/521/",
                    "name": "unfezant"
                }
            },
            {
                "slot": 2,
                "pokemon": {
                    "url": "https://pokeapi.co/api/v2/pokemon/527/",
                    "name": "woobat"
                }
            },
            {
                "slot": 2,
                "pokemon": {
                    "url": "https://pokeapi.co/api/v2/pokemon/528/",
                    "name": "swoobat"
                }
            },
            {
                "slot": 2,
                "pokemon": {
                    "url": "https://pokeapi.co/api/v2/pokemon/561/",
                    "name": "sigilyph"
                }
            },
            {
                "slot": 2,
                "pokemon": {
                    "url": "https://pokeapi.co/api/v2/pokemon/566/",
                    "name": "archen"
                }
            },
            {
                "slot": 2,
                "pokemon": {
                    "url": "https://pokeapi.co/api/v2/pokemon/567/",
                    "name": "archeops"
                }
            },
            {
                "slot": 2,
                "pokemon": {
                    "url": "https://pokeapi.co/api/v2/pokemon/580/",
                    "name": "ducklett"
                }
            },
            {
                "slot": 2,
                "pokemon": {
                    "url": "https://pokeapi.co/api/v2/pokemon/581/",
                    "name": "swanna"
                }
            },
            {
                "slot": 2,
                "pokemon": {
                    "url": "https://pokeapi.co/api/v2/pokemon/587/",
                    "name": "emolga"
                }
            },
            {
                "slot": 2,
                "pokemon": {
                    "url": "https://pokeapi.co/api/v2/pokemon/627/",
                    "name": "rufflet"
                }
            },
            {
                "slot": 2,
                "pokemon": {
                    "url": "https://pokeapi.co/api/v2/pokemon/628/",
                    "name": "braviary"
                }
            },
            {
                "slot": 2,
                "pokemon": {
                    "url": "https://pokeapi.co/api/v2/pokemon/629/",
                    "name": "vullaby"
                }
            },
            {
                "slot": 2,
                "pokemon": {
                    "url": "https://pokeapi.co/api/v2/pokemon/630/",
                    "name": "mandibuzz"
                }
            },
            {
                "slot": 1,
                "pokemon": {
                    "url": "https://pokeapi.co/api/v2/pokemon/641/",
                    "name": "tornadus-incarnate"
                }
            },
            {
                "slot": 2,
                "pokemon": {
                    "url": "https://pokeapi.co/api/v2/pokemon/642/",
                    "name": "thundurus-incarnate"
                }
            },
            {
                "slot": 2,
                "pokemon": {
                    "url": "https://pokeapi.co/api/v2/pokemon/645/",
                    "name": "landorus-incarnate"
                }
            },
            {
                "slot": 2,
                "pokemon": {
                    "url": "https://pokeapi.co/api/v2/pokemon/661/",
                    "name": "fletchling"
                }
            },
            {
                "slot": 2,
                "pokemon": {
                    "url": "https://pokeapi.co/api/v2/pokemon/662/",
                    "name": "fletchinder"
                }
            },
            {
                "slot": 2,
                "pokemon": {
                    "url": "https://pokeapi.co/api/v2/pokemon/663/",
                    "name": "talonflame"
                }
            },
            {
                "slot": 2,
                "pokemon": {
                    "url": "https://pokeapi.co/api/v2/pokemon/666/",
                    "name": "vivillon"
                }
            },
            {
                "slot": 2,
                "pokemon": {
                    "url": "https://pokeapi.co/api/v2/pokemon/701/",
                    "name": "hawlucha"
                }
            },
            {
                "slot": 1,
                "pokemon": {
                    "url": "https://pokeapi.co/api/v2/pokemon/714/",
                    "name": "noibat"
                }
            },
            {
                "slot": 1,
                "pokemon": {
                    "url": "https://pokeapi.co/api/v2/pokemon/715/",
                    "name": "noivern"
                }
            },
            {
                "slot": 2,
                "pokemon": {
                    "url": "https://pokeapi.co/api/v2/pokemon/717/",
                    "name": "yveltal"
                }
            },
            {
                "slot": 2,
                "pokemon": {
                    "url": "https://pokeapi.co/api/v2/pokemon/722/",
                    "name": "rowlet"
                }
            },
            {
                "slot": 2,
                "pokemon": {
                    "url": "https://pokeapi.co/api/v2/pokemon/723/",
                    "name": "dartrix"
                }
            },
            {
                "slot": 2,
                "pokemon": {
                    "url": "https://pokeapi.co/api/v2/pokemon/731/",
                    "name": "pikipek"
                }
            },
            {
                "slot": 2,
                "pokemon": {
                    "url": "https://pokeapi.co/api/v2/pokemon/732/",
                    "name": "trumbeak"
                }
            },
            {
                "slot": 2,
                "pokemon": {
                    "url": "https://pokeapi.co/api/v2/pokemon/733/",
                    "name": "toucannon"
                }
            },
            {
                "slot": 2,
                "pokemon": {
                    "url": "https://pokeapi.co/api/v2/pokemon/741/",
                    "name": "oricorio-baile"
                }
            },
            {
                "slot": 2,
                "pokemon": {
                    "url": "https://pokeapi.co/api/v2/pokemon/774/",
                    "name": "minior-red-meteor"
                }
            },
            {
                "slot": 2,
                "pokemon": {
                    "url": "https://pokeapi.co/api/v2/pokemon/797/",
                    "name": "celesteela"
                }
            },
            {
                "slot": 2,
                "pokemon": {
                    "url": "https://pokeapi.co/api/v2/pokemon/10006/",
                    "name": "shaymin-sky"
                }
            },
            {
                "slot": 2,
                "pokemon": {
                    "url": "https://pokeapi.co/api/v2/pokemon/10011/",
                    "name": "rotom-fan"
                }
            },
            {
                "slot": 1,
                "pokemon": {
                    "url": "https://pokeapi.co/api/v2/pokemon/10019/",
                    "name": "tornadus-therian"
                }
            },
            {
                "slot": 2,
                "pokemon": {
                    "url": "https://pokeapi.co/api/v2/pokemon/10020/",
                    "name": "thundurus-therian"
                }
            },
            {
                "slot": 2,
                "pokemon": {
                    "url": "https://pokeapi.co/api/v2/pokemon/10021/",
                    "name": "landorus-therian"
                }
            },
            {
                "slot": 2,
                "pokemon": {
                    "url": "https://pokeapi.co/api/v2/pokemon/10035/",
                    "name": "charizard-mega-y"
                }
            },
            {
                "slot": 2,
                "pokemon": {
                    "url": "https://pokeapi.co/api/v2/pokemon/10040/",
                    "name": "pinsir-mega"
                }
            },
            {
                "slot": 2,
                "pokemon": {
                    "url": "https://pokeapi.co/api/v2/pokemon/10042/",
                    "name": "aerodactyl-mega"
                }
            },
            {
                "slot": 2,
                "pokemon": {
                    "url": "https://pokeapi.co/api/v2/pokemon/10073/",
                    "name": "pidgeot-mega"
                }
            },
            {
                "slot": 2,
                "pokemon": {
                    "url": "https://pokeapi.co/api/v2/pokemon/10079/",
                    "name": "rayquaza-mega"
                }
            },
            {
                "slot": 2,
                "pokemon": {
                    "url": "https://pokeapi.co/api/v2/pokemon/10089/",
                    "name": "salamence-mega"
                }
            },
            {
                "slot": 2,
                "pokemon": {
                    "url": "https://pokeapi.co/api/v2/pokemon/10123/",
                    "name": "oricorio-pom-pom"
                }
            },
            {
                "slot": 2,
                "pokemon": {
                    "url": "https://pokeapi.co/api/v2/pokemon/10124/",
                    "name": "oricorio-pau"
                }
            },
            {
                "slot": 2,
                "pokemon": {
                    "url": "https://pokeapi.co/api/v2/pokemon/10125/",
                    "name": "oricorio-sensu"
                }
            },
            {
                "slot": 2,
                "pokemon": {
                    "url": "https://pokeapi.co/api/v2/pokemon/10130/",
                    "name": "minior-orange-meteor"
                }
            },
            {
                "slot": 2,
                "pokemon": {
                    "url": "https://pokeapi.co/api/v2/pokemon/10131/",
                    "name": "minior-yellow-meteor"
                }
            },
            {
                "slot": 2,
                "pokemon": {
                    "url": "https://pokeapi.co/api/v2/pokemon/10132/",
                    "name": "minior-green-meteor"
                }
            },
            {
                "slot": 2,
                "pokemon": {
                    "url": "https://pokeapi.co/api/v2/pokemon/10133/",
                    "name": "minior-blue-meteor"
                }
            },
            {
                "slot": 2,
                "pokemon": {
                    "url": "https://pokeapi.co/api/v2/pokemon/10134/",
                    "name": "minior-indigo-meteor"
                }
            },
            {
                "slot": 2,
                "pokemon": {
                    "url": "https://pokeapi.co/api/v2/pokemon/10135/",
                    "name": "minior-violet-meteor"
                }
            },
            {
                "slot": 2,
                "pokemon": {
                    "url": "https://pokeapi.co/api/v2/pokemon/10136/",
                    "name": "minior-red"
                }
            },
            {
                "slot": 2,
                "pokemon": {
                    "url": "https://pokeapi.co/api/v2/pokemon/10137/",
                    "name": "minior-orange"
                }
            },
            {
                "slot": 2,
                "pokemon": {
                    "url": "https://pokeapi.co/api/v2/pokemon/10138/",
                    "name": "minior-yellow"
                }
            },
            {
                "slot": 2,
                "pokemon": {
                    "url": "https://pokeapi.co/api/v2/pokemon/10139/",
                    "name": "minior-green"
                }
            },
            {
                "slot": 2,
                "pokemon": {
                    "url": "https://pokeapi.co/api/v2/pokemon/10140/",
                    "name": "minior-blue"
                }
            },
            {
                "slot": 2,
                "pokemon": {
                    "url": "https://pokeapi.co/api/v2/pokemon/10141/",
                    "name": "minior-indigo"
                }
            },
            {
                "slot": 2,
                "pokemon": {
                    "url": "https://pokeapi.co/api/v2/pokemon/10142/",
                    "name": "minior-violet"
                }
            }
        ],
        "id": 3,
        "names": [
            {
                "name": "ひこう",
                "language": {
                    "url": "https://pokeapi.co/api/v2/language/1/",
                    "name": "ja-Hrkt"
                }
            },
            {
                "name": "비행",
                "language": {
                    "url": "https://pokeapi.co/api/v2/language/3/",
                    "name": "ko"
                }
            },
            {
                "name": "Vol",
                "language": {
                    "url": "https://pokeapi.co/api/v2/language/5/",
                    "name": "fr"
                }
            },
            {
                "name": "Flug",
                "language": {
                    "url": "https://pokeapi.co/api/v2/language/6/",
                    "name": "de"
                }
            },
            {
                "name": "Volador",
                "language": {
                    "url": "https://pokeapi.co/api/v2/language/7/",
                    "name": "es"
                }
            },
            {
                "name": "Volante",
                "language": {
                    "url": "https://pokeapi.co/api/v2/language/8/",
                    "name": "it"
                }
            },
            {
                "name": "Flying",
                "language": {
                    "url": "https://pokeapi.co/api/v2/language/9/",
                    "name": "en"
                }
            }
        ]
    }

    return pokemon_flying_data

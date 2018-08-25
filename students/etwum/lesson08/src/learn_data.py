"""
    Data for database demonstrations
"""


def get_furniture_data():
    """
    demonstration data
    """

    furniture_data = [
        {
            'product type': 'Couch',
            'color': 'Red',
            'description': 'Leather low back',
            'monthly_rental_cost': 12.99,
            'in_stock_quantity': 10
        },
        {
            'product type': 'Couch',
            'color': 'Blue',
            'description': 'Cloth high back',
            'monthly_rental_cost': 9.99,
            'in_stock_quantity': 3
        },
        {
            'product type': 'Coffee table',
            'color': 'Brown',
            'description': 'Plastic',
            'monthly_rental_cost': 2.50,
            'in_stock_quantity': 25
        },
        {
            'product type': 'Couch',
            'color': 'Red',
            'description': 'Leather high back',
            'monthly_rental_cost': 15.99,
            'in_stock_quantity': 17
        },
        {
            'product type': 'Recliner',
            'color': 'Blue',
            'description': 'Leather high back',
            'monthly_rental_cost': 19.99,
            'in_stock_quantity': 6
        },
        {
            'product type': 'Chair',
            'color': 'Black',
            'description': 'Plastic',
            'monthly_rental_cost': 1.00,
            'in_stock_quantity': 45
        },
        {
            'product type': 'TV stand',
            'color': 'Black',
            'description': 'Wood',
            'monthly_rental_cost': 10.00,
            'in_stock_quantity': 15
        },
        {
            'product type': 'Bookcase',
            'color': 'Black',
            'description': 'Wood',
            'monthly_rental_cost': 15.00,
            'in_stock_quantity': 30
        }
    ]
    return furniture_data


def get_player_data():

    player_data = [
        {'team': 'Barcelona',
         'forward': 'Messi',
         'midfield': 'Busquets',
         'defense': 'Pique',
         'goalkeeper': 'Ter Stegen'},

        {'team': 'Madrid',
         'forward': 'Bale',
         'midfield': 'Modric',
         'defense': 'Ramos',
         'goalkeeper': 'Courtois'},

        {'team': 'Manchester United',
         'forward': 'Lukaku',
         'midfield': 'Pogba',
         'defense': 'Smalling',
         'goalkeeper': 'De Gea'},

        {'team': 'Manchester City',
         'forward': 'Aguero',
         'midfield': 'De Bruyne',
         'defense': 'Mendy',
         'goalkeeper': 'Ederson'},

        {'team': 'Liverpool',
         'forward': 'Salah',
         'midfield': 'Keita',
         'defense': 'Lovren',
         'goalkeeper': 'Alisson'},

        {'team': 'Arsenal',
         'forward': 'Ozil',
         'midfield': 'Ramsey',
         'defense': 'Xhaka',
         'goalkeeper': 'Cech'},

        {'team': 'Tottenham',
         'forward': 'Kane',
         'midfield': 'Alli',
         'defense': 'Trippier',
         'goalkeeper': 'Lloris'},

        {'team': 'Chelsea',
         'forward': 'Hazard',
         'midfield': 'Wilian',
         'defense': 'Cahill',
         'goalkeeper': 'Caballero'},

        {'team': 'AC Milan',
         'forward': 'Higuian',
         'midfield': 'Laxalt',
         'defense': 'Zapata',
         'goalkeeper': 'Donnarumma'},

        {'team': 'Inter Milan',
         'forward': 'Icardi',
         'midfield': 'Asamoah',
         'defense': 'Miranda',
         'goalkeeper': 'Berni'}
    ]
    return player_data

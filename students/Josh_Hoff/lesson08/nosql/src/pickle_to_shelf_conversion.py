"""
Simple program that pulls pickle data and saves it in shelf format
"""

import pickle
import shelve

import pprint

def conversion():
    """
    Saves in pickle, reads from pickle, saves as shelf, then reads from shelf
    """
    wine_data = [
        {'label_name': 'Sutter Home',
            'grape': 'Cabernet Sauvignon',
            'region': 'California',
            'retail_price': 7.99,
            'alcohol_percentage': 13.5
        },
        {'label_name': 'Boomtown',
            'grape': 'Syrah',
            'region': 'Washington',
            'retail_price': 15.99,
            'alcohol_percentage': 14.7
        },
        {'label_name': 'Pundit',
            'grape': 'Syrah',
            'region': 'Washington',
            'retail_price': 19.99,
            'alcohol_percentage': 14.5
        },
        {'label_name': 'Red Schooner',
            'grape': 'Malbec',
            'region': 'California',
            'retail_price': 49.99,
            'alcohol_percentage': 15.2
        },
        {'label_name': 'Intrinsic',
            'grape': 'Cabernet Sauvignon',
            'region': 'Washington',
            'retail_price': 24.99,
            'alcohol_percentage': 14.0
        },
        {'label_name': 'Red Diamond',
            'grape': 'Red Blend',
            'region': 'California',
            'retail_price': 9.99,
            'alcohol_percentage': 13.5
        },
        {'label_name': 'Kim Crawford',
            'grape': 'Sauvignon Blanc',
            'region': 'New Zealand',
            'retail_price': 17.99,
            'alcohol_percentage': 13.2
        },
        {'label_name': 'Erath',
            'grape': 'Pinot Noir',
            'region': 'Oregon',
            'retail_price': 15.99,
            'alcohol_percentage': 14.0
        },
        {'label_name': 'Mer Soleil',
            'grape': 'Chardonnay',
            'region': 'California',
            'retail_price': 29.99,
            'alcohol_percentage': 13.9
        },
        {'label_name': 'Meiomi',
            'grape': 'Chardonnay',
            'region': 'California',
            'retail_price': 27.99,
            'alcohol_percentage': 14.1
        }]
        
    pickle.dump(wine_data, open('../data/data.pkl', 'wb'))
    
    read_data = pickle.load(open('../data/data.pkl', 'rb'))
    
    assert read_data == wine_data
    print('PRINTING PICKLE DATA')
    pprint.pprint(read_data)
    
    shelf_file = shelve.open('../data/shelve.dat')
    shelf_file['key'] = read_data
    read_items = shelf_file['key']
    assert read_items == wine_data
    print('PRINTING SHELF DATA')
    pprint.pprint(read_items)
    del shelf_file['key']
    shelf_file.close()
    return
    
if __name__ == '__main__':
    conversion()
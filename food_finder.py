"""Food Search

Usage:
    food_finder.py find <food_name>
    food_finder.py -h | --help
    food_finder.py --version

Options:
    -h --help    show help
    --version    show version of the application
"""

from docopt import docopt
from app.authenticate import Api
from app.restuarant import Restaurant


def main(args):
    if args['find'] and args['<food_name>']:
        api = Api()
        food = args['<food_name>']
        query_params = {'query': food}

        data = api.get_data(query_params)
        restaurants = create_restaurants(data)
        display_top_four(restaurants, food)
    else:
        print 'Notice: Please run food_finder.py --help to learn the usage pattern.'


def create_restaurants(data):
    restaurants = []
    venues = data['response']['venues']
    for json_venue in venues:
        restaurants.append(Restaurant.from_json(json_venue))
    return restaurants


def display_top_four(restaurants, food):
    if len(restaurants) > 0:
        print 'Top 4 venues serving {0} in Kampala'.format(food)
        print '_______________________________'
        print
        for restaurant in restaurants:
            print restaurant
    else:
        print 'No venues serving {0} in Kampala found.'.format(food)


if __name__ == '__main__':
    arguments = docopt(__doc__, argv=None, help=True, version='Food Finder v0.1', options_first=False)
    main(arguments)



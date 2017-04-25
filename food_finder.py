"""Food Search

Usage:
    food_finder.py find <food_name>
    food_finder.py -i | -interactive
    food_finder.py -h | --help
    food_finder.py --version

Options:
    -i --interactive  Interactive Mode
    -h --help    show help
    --version    show version of the application
"""

import sys, cmd
from docopt import docopt, DocoptExit
from app.authenticate import Api
from app.restuarant import Restaurant


def docopt_cmd(func):
    """
    This decorator is used to simplify the try/except block and pass the result
    of the docopt parsing to the called action.
    """
    def fn(self, arg):
        try:
            opt = docopt(fn.__doc__, arg)

        except DocoptExit as e:
            # The DocoptExit is thrown when the args do not match.
            # We print a message to the user and the usage block.
            print('Invalid Command!')
            print(e)
            return

        except SystemExit:
            # The SystemExit exception prints the usage for --help
            # We do not need to do the print here.
            return

        return func(self, opt)

    fn.__name__ = func.__name__
    fn.__doc__ = func.__doc__
    fn.__dict__.update(func.__dict__)
    return fn


class MyInteractive(cmd.Cmd):
    intro = 'Welcome to Food Finder!' \
            + ' (type help for a list of commands.)'
    prompt = '(food_finder) '
    file = None

    @docopt_cmd
    def do_find(self, arg):
        """Usage: find <food_name>"""
        api = Api()
        food = arg['<food_name>']
        query_params = {'query': food}

        data = api.get_data(query_params)
        restaurants = self.create_restaurants(data)
        self.display_top_four(restaurants, food)

    def do_quit(self, arg):
        """Quits out of Interactive Mode."""
        print('Good Bye!')
        exit()

    def create_restaurants(self, data):
        restaurants = []
        venues = data['response']['venues']
        for json_venue in venues:
            restaurants.append(Restaurant.from_json(json_venue))
        return restaurants

    def display_top_four(self, restaurants, food):
        if len(restaurants) > 0:
            print 'Top 4 venues serving {0} in Kampala'.format(food)
            print '_______________________________'
            print
            for restaurant in restaurants:
                print restaurant
        else:
            print 'No venues serving {0} in Kampala found.'.format(food)

if __name__ == '__main__':
    opt = docopt(__doc__, sys.argv[1:])
    if opt['--interactive'] or opt['-i']:
        MyInteractive().cmdloop()




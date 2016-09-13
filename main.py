import os 
import sys

import argparse
#import ConfigParser
import connection_manager
import scores_adder

tables = ['provinces', 'forts', 'income', 'gem_income', 'research', 'dominion',
        'army_size', 'victory_points']
dom4folder = os.path.expanduser('~/dominions4')
current_games = [] 
game_name = ''

nation_list = []

def setup():
    """ gets the database settings and file locations
        does sanity checking on inputs and allows user to choose
        which game/folder to use
        to select what game, program checks savedgame folder for 
        what games exist. Includes games that may be over
        :return: path of database file
    """ 
    #config = ConfigParser.ConfigParser()
    #config.read('dom4db.conf')
    #dom4folder = ConfigReader()
    global current_games, game_name, nation_list
    saved_games_folder = os.path.join(dom4folder, 'savedgames')
    current_games = get_subdirs(saved_games_folder)
    games_to_int = range(len(current_games))
    games_to_int = dict(zip(games_to_int, current_games))

    print 'games found:'
    for k, v in games_to_int.items():
        print str(k) + ": " + v

    game_selected = False
    while not game_selected:
        game_int = _get_game()
        if game_int == 'q':
            print 'bye bye'
            sys.exit(0)

        game_int = _run_checks(game_int)
        if game_int != None:
            game_name = games_to_int[game_int]
            game_selected = True

    nation_list = _get_nations()
    print 'nations retrieved: ' + ', '.join(nation_list)

    return os.path.join(saved_games_folder, game_name, "scores_list")

def populate_nation_table(conn):
    """populates the nation table with the nations found for the game
        :param conn: database connection
     """
    print 'populating nation list' 
    for i in range(len(nation_list)):
        print nation_list[i]
        connection_manager.insert_into(conn, "Nations",  ['id', 'name'], (i, nation_list[i]))
    
def main(options):
    """ runs setup and then creates necessary tables if they do not exist
        runs table populator afterwards
    """
    database_file = setup() 

    if not options.skip:
        create_score_tables(database_file)

    if options.populate:
        #populate stuff here
        score_file = os.join(dom4folder, game_name, 'scores.html')
        score_adder.set_score_file(score_file)


def create_score_tables(database_file):
    """ Create connection to database and create tables in database
    :param database_file: location of database to connect to
    """
    conn = connection_manager.create_connection(database_file)

    create_nation_table = (
        'CREATE TABLE IF NOT EXISTS Nations ( '
        'id INTEGER PRIMARY KEY, '
        'name TEXT NOT NULL );')
    print 'executing following sql query:'
    print create_nation_table
    if conn is not None: 
        connection_manager.create_table(conn, create_nation_table)
        connection_manager.commit(conn)
        print 'nation table created'
        populate_nation_table(conn)
        connection_manager.commit(conn)
        print 'nation table populated'
        print connection_manager.select_all_from(conn, 'nations') 

    table_creation_string= ( 
        'CREATE TABLE IF NOT EXISTS {} ( '
        'id INTEGER NOT NULL, '
        'Value INTEGER NOT NULL, '
        'FOREIGN KEY (id) REFERENCES Nation(id));')
    
    for t in tables:
        print 'executing following sql query:'
        print table_creation_string.format(t)
        connection_manager.create_table(conn, table_creation_string.format(t)) 
    print 'database and tables created, run script for populating tables'
    connection_manger.commit(conn)
    
    connection_manager.close_connection(conn)

"""
HELPER FUNCTIONS
"""
def _get_game():
    """ retrieves game selection from user
    :return: user selection as a string
    """
    return raw_input('Please select the game you would like to create a ' + \
        'database for or type "q" to exit: \n')

def _get_nations():
    """ gets nation names by reading turn values in savedgame folder
    :return: array with nation list
    """
    game_folder = os.path.join(dom4folder, 'savedgames', game_name)
    print 'retrieving nations from '+game_folder
    nation_list = filter(lambda w: w.endswith(".2h"), [name for name in os.listdir(game_folder)])
    return map(lambda w: w.split('_')[1][:-3], nation_list)
    
def _run_checks(game_int):
    """runs validation checks on game_integer
        :return: game_int as integer if valid, else None
    """
    try:
        game_int = int(game_int)
    except ValueError:
        print str(game_int) + 'is not an integer, please try a valid input'
        return None

    if game_int >= current_games:
        print 'invalid option, integer too large' 
        return None
    return game_int
    
def ConfigReader(section):
    option_dict = {}
    options = Config.options(section)
    for option in options:
        try:
            option_dict[option] = Config.get(section, option)
            if option_dict[option] == -1:
                pass
        except:
            print 'exception on {}'.format(option)
            option_dict = None

    return option_dict

def get_subdirs(path):
    return [name for name in os.listdir(path) if os.path.isdir(os.path.join(path, name))]

def _parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--skip', help='skip database and table creation', 
        action='store_true')
    parser.add_argument('-p', '--populate', help='populate tables using score.html', 
        action='store_true')

    return parser.parse_args()


"""
runner
"""
if __name__ == "__main__":
    main(_parse_args())


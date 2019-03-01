#!python3
import time
import random

import os, sys

import mysql.connector

"""
esportsuser
cscs1
"""

usr = 'esportsuser'
pwd = 'cscs1'
h = 'muppet' #'10.210.195.69'
db = 'esports'
p = 3306

#query = ""
#query2 = "SELECT Game, Score, User, Timestamp FROM gamescores WHERE user = 'Hubble'"

# Select data from table using SQL query.
#num_rows = cursor.execute(query)

#cursor.execute(query2)
#for (Game, Score, User, Timestamp) in cursor:
#  print(Game, Score, User, Timestamp)

#print(num_rows)
#cnx.commit()
#cursor.close()
#cnx.close()


def foo():
    print ("foo");


class User_Profile():
    def __init__(self , username_in):
        self.username = username_in
        self.start = 0
        self.end = 0
        self.score = 0

        self.db = None
        self.cursor = None

    def update_score(self , score_in):
        self.score = score_in

    def start_timer(self):
        self.start = time.time()

    def end_timer(self):
        self.end = time.time()

    def open_file(self , filename):
        self.file.open_file(filename)


    def save(self):
        self.file.open_file(None)
        self.file.save(None) # make a local copy.
        game = self.file
    '''
    def profile_user_get(self):
        pathname = os.path.dirname(sys.argv[0])
        if pathname == "ENTER PATH HERE": #CHANGE
            return(True)
        else:
            return(False)
    ''' 
    def add_game_record(self , game):
        
        try:
            #self.file.add_record([game , self.score])

            self.db = mysql.connector.connect(user=usr, password=pwd, host=h, database=db, port=p) # connect to database
            self.cursor = self.db.cursor()

            self.cursor.execute("INSERT INTO gamescores (User, Game, Score) VALUES('{0}' , '{1}' , {2})".format(self.username , game , self.score)) # execute insert command
            self.db.commit() # commit changes.

            self.cursor.close()
            self.db.close()
        except:
            #error_log = csv_edit.CSV_File_Write("")
            #error_log.add_record([str(err)])
            #error_log.save("Z:\\" + self.username + "_error_log.esp")
            print("Error: Database credientials incorrect")
            
        
    
'''
def play_game():
    print ("playing game")
    return (random.randint(10 , 100))

def play_games(profile):
    profile.update_score(play_game())
    profile.add_game_record("robots")
        
profile = User_Profile("spam")
play_games(profile)
'''


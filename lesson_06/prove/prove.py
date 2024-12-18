"""
Course: CSE 251
Lesson Week: 06
File: prove.py
Author: Dallin Olson
Purpose: Processing Plant
Instructions:
- Implement the classes to allow gifts to be created.
"""

import random
import multiprocessing as mp
import os.path
import time
import datetime

# Include cse 251 common Python files - Don't change
from cse251 import *
CONTROL_FILENAME = './settings.txt'
BOXES_FILENAME   = './boxes.txt'
# Settings consts
MARBLE_COUNT = 'marble-count'
CREATOR_DELAY = 'creator-delay'
NUMBER_OF_MARBLES_IN_A_BAG = 'bag-count'
BAGGER_DELAY = 'bagger-delay'
ASSEMBLER_DELAY = 'assembler-delay'
WRAPPER_DELAY = 'wrapper-delay'

# No Global variables

class Bag():
    """ bag of marbles - Don't change """

    def __init__(self):
        self.items = []

    def add(self, marble):
        self.items.append(marble)

    def get_size(self):
        return len(self.items)

    def __str__(self):
        return str(self.items)

class Gift():
    """ Gift of a large marble and a bag of marbles - Don't change """

    def __init__(self, large_marble, marbles):
        self.large_marble = large_marble
        self.marbles = marbles

    def __str__(self):
        marbles = str(self.marbles)
        marbles = marbles.replace("'", "")
        return f'Large marble: {self.large_marble}, marbles: {marbles[1:-1]}'


class Marble_Creator(mp.Process):
    """ This class "creates" marbles and sends them to the bagger """

    colors = ('Gold', 'Orange Peel', 'Purple Plum', 'Blue', 'Neon Silver', 
        'Tuscan Brown', 'La Salle Green', 'Spanish Orange', 'Pale Goldenrod', 'Orange Soda', 
        'Maximum Purple', 'Neon Pink', 'Light Orchid', 'Russian Violet', 'Sheen Green', 
        'Isabelline', 'Ruby', 'Emerald', 'Middle Red Purple', 'Royal Orange', 'Big Dip O’ruby', 
        'Dark Fuchsia', 'Slate Blue', 'Neon Dark Green', 'Sage', 'Pale Taupe', 'Silver Pink', 
        'Stop Red', 'Eerie Black', 'Indigo', 'Ivory', 'Granny Smith Apple', 
        'Maximum Blue', 'Pale Cerulean', 'Vegas Gold', 'Mulberry', 'Mango Tango', 
        'Fiery Rose', 'Mode Beige', 'Platinum', 'Lilac Luster', 'Duke Blue', 'Candy Pink', 
        'Maximum Violet', 'Spanish Carmine', 'Antique Brass', 'Pale Plum', 'Dark Moss Green', 
        'Mint Cream', 'Shandy', 'Cotton Candy', 'Beaver', 'Rose Quartz', 'Purple', 
        'Almond', 'Zomp', 'Middle Green Yellow', 'Auburn', 'Chinese Red', 'Cobalt Blue', 
        'Lumber', 'Honeydew', 'Icterine', 'Golden Yellow', 'Silver Chalice', 'Lavender Blue', 
        'Outrageous Orange', 'Spanish Pink', 'Liver Chestnut', 'Mimi Pink', 'Royal Red', 'Arylide Yellow', 
        'Rose Dust', 'Terra Cotta', 'Lemon Lime', 'Bistre Brown', 'Venetian Red', 'Brink Pink', 
        'Russian Green', 'Blue Bell', 'Green', 'Black Coral', 'Thulian Pink', 
        'Safety Yellow', 'White Smoke', 'Pastel Gray', 'Orange Soda', 'Lavender Purple',
        'Brown', 'Gold', 'Blue-Green', 'Antique Bronze', 'Mint Green', 'Royal Blue', 
        'Light Orange', 'Pastel Blue', 'Middle Green')

    def __init__(self, pipe, delay, marble_count):
        mp.Process.__init__(self)
        # TODO Add any arguments and variables here
        self.pipe = pipe
        self.delay = delay
        self.marble_count = marble_count

    def run(self):
        '''
        for each marble:
            send the marble (one at a time) to the bagger
              - A marble is a random name from the colors list above
            sleep the required amount
        Let the bagger know there are no more marbles
        '''
        for _ in range(self.marble_count):
            marble = random.choice(Marble_Creator.colors)
            self.pipe.send(marble)
            time.sleep(self.delay)

        self.pipe.send(None)


class Bagger(mp.Process):
    """ Receives marbles from the marble creator, then there are enough
        marbles, the bag of marbles are sent to the assembler """
    def __init__(self, recv_pipe, send_pipe, bag_count, delay):
        mp.Process.__init__(self)
        # TODO Add any arguments and variables here
        self.recv_pipe = recv_pipe
        self.send_pipe = send_pipe
        self.bag_count = bag_count
        self.delay = delay

    def run(self):
        '''
        while there are marbles to process
            collect enough marbles for a bag
            send the bag to the assembler
            sleep the required amount
        tell the assembler that there are no more bags
        '''
        while True:
            bag = Bag()
            for _ in range(self.bag_count):
                marble = self.recv_pipe.recv()
                if marble is None:
                    break
                bag.add(marble)

            
            if bag.get_size() > 0:
                self.send_pipe.send(bag)
                time.sleep(self.delay)

            
            if marble is None:
                break

        
        self.send_pipe.send(None)



class Assembler(mp.Process):
    """ Take the set of marbles and create a gift from them.
        Sends the completed gift to the wrapper """
    marble_names = ('Lucky', 'Spinner', 'Sure Shot', 'Big Joe', 'Winner', '5-Star', 'Hercules', 'Apollo', 'Zeus')

    def __init__(self, recv_pipe, send_pipe, delay):
        mp.Process.__init__(self)
        # TODO Add any arguments and variables here
        self.recv_pipe = recv_pipe
        self.send_pipe = send_pipe
        self.delay = delay



    def run(self):
        '''
        while there are bags to process
            create a gift with a large marble (random from the name list) and the bag of marbles
            send the gift to the wrapper
            sleep the required amount
        tell the wrapper that there are no more gifts
        '''
        while True:
            bag = self.recv_pipe.recv()
            if bag is None:
                break
            large_marble = random.choice(Assembler.marble_names)
            gift = Gift(large_marble, bag)
            self.send_pipe.send(gift)
            time.sleep(self.delay)
        self.send_pipe.send(None)


class Wrapper(mp.Process):
    """ Takes created gifts and wraps them by placing them in the boxes file """
    def __init__(self, recv_pipe, filename, delay):
        mp.Process.__init__(self)
        # TODO Add any arguments and variables here
        self.recv_pipe = recv_pipe
        self.filename = filename
        self.delay = delay
    def run(self):
        '''
        open file for writing
        while there are gifts to process
            save gift to the file with the current time
            sleep the required amount
        '''
        with open(self.filename, 'w') as file:
            while True:
                gift = self.recv_pipe.recv()
                if gift is None:
                    break
                timestamp = datetime.now().time()
                file.write(f"Created - {timestamp}: {str(gift)}\n")
                time.sleep(self.delay)

def display_final_boxes(filename, log):
    """ Display the final boxes file to the log file -  Don't change """
    if os.path.exists(filename):
        log.write(f'Contents of {filename}')
        with open(filename) as boxes_file:
            for line in boxes_file:
                log.write(line.strip())
    else:
        log.write_error(f'The file {filename} doesn\'t exist.  No boxes were created.')



def main():
    """ Main function """

    log = Log(show_terminal=True)

    log.start_timer()

    # Load settings file
    settings = load_json_file(CONTROL_FILENAME)
    if settings == {}:
        log.write_error(f'Problem reading in settings file: {CONTROL_FILENAME}')
        return

    log.write(f'Marble count     = {settings[MARBLE_COUNT]}')
    log.write(f'Marble delay     = {settings[CREATOR_DELAY]}')
    log.write(f'Marbles in a bag = {settings[NUMBER_OF_MARBLES_IN_A_BAG]}') 
    log.write(f'Bagger delay     = {settings[BAGGER_DELAY]}')
    log.write(f'Assembler delay  = {settings[ASSEMBLER_DELAY]}')
    log.write(f'Wrapper delay    = {settings[WRAPPER_DELAY]}')

    
    if os.path.exists(BOXES_FILENAME):
        os.remove(BOXES_FILENAME)
    open(BOXES_FILENAME, 'w').close()

    # TODO: create Pipes between creator -> bagger -> assembler -> wrapper
    creator_to_bagger, bagger_from_creator = mp.Pipe()
    bagger_to_assembler, assembler_from_bagger = mp.Pipe()
    assembler_to_wrapper, wrapper_from_assembler = mp.Pipe()

    # TODO create variable to be used to count the number of gifts
    # The boxes file handling has been adjusted to ensure it's present when needed

    log.write('Create the processes')

    # TODO Create the processes (ie., classes above)
    marble_creator = Marble_Creator(creator_to_bagger, settings[CREATOR_DELAY], settings[MARBLE_COUNT])
    bagger = Bagger(bagger_from_creator, bagger_to_assembler, settings[NUMBER_OF_MARBLES_IN_A_BAG], settings[BAGGER_DELAY])
    assembler = Assembler(assembler_from_bagger, assembler_to_wrapper, settings[ASSEMBLER_DELAY])
    wrapper = Wrapper(wrapper_from_assembler, BOXES_FILENAME, settings[WRAPPER_DELAY])

    log.write('Starting the processes')
    # TODO add code here
    marble_creator.start()
    bagger.start()
    assembler.start()
    wrapper.start()
    
    log.write('Waiting for processes to finish')
    # TODO add code here
    marble_creator.join()
    bagger.join()
    assembler.join()
    wrapper.join()

    display_final_boxes(BOXES_FILENAME, log)
    
    with open(BOXES_FILENAME, 'r') as f:
        gift_count = sum(1 for _ in f)
    # TODO Log the number of gifts created.
    log.write(f"Number of gifts created: {gift_count}")

if __name__ == '__main__':
    main()
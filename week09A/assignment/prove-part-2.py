"""
Course: CSE 251 
Lesson Week: 09
File: prove-part-2.py 
Author: Dallin Olson

Purpose: Part 2 of assignment 09, finding the end position in the maze

Instructions:
- Do not create classes for this assignment, just functions.
- Do not use any other Python modules other than the ones included.
- Each thread requires a different color by calling get_color().


This code is not interested in finding a path to the end position,
However, once you have completed this program, describe how you could 
change the program to display the found path to the exit position.

What approach would you take?
The strategy revolves around the solve_find_end function, which orchestrates
a controlled deployment of multiple threads to explore the maze concurrently.
Each thread commences from the same starting point, navigating through 
the maze, accumulating movements, and testing various pathways.

Why is it effective?
This approach leverages parallelism effectively to expedite the maze-solving
process while ensuring that the number of active threads remains manageable.
A shared 'stop' flag and a locking mechanism are employed cleverly, allowing
all threads to halt once any one of them successfully reaches the end.

"""
import math
import threading 
from screen import Screen
from maze import Maze
import sys
import cv2

# Include cse 251 files
from cse251 import *

SCREEN_SIZE = 700
COLOR = (0, 0, 255)
COLORS = (
    (0,0,255),
    (0,255,0),
    (255,0,0),
    (255,255,0),
    (0,255,255),
    (255,0,255),
    (128,0,0),
    (128,128,0),
    (0,128,0),
    (128,0,128),
    (0,128,128),
    (0,0,128),
    (72,61,139),
    (143,143,188),
    (226,138,43),
    (128,114,250)
)
SLOW_SPEED = 100
FAST_SPEED = 0

# Globals
current_color_index = 0
thread_count = 0
stop = False
speed = SLOW_SPEED

def get_color():
    """ Returns a different color when called """
    global current_color_index
    if current_color_index >= len(COLORS):
        current_color_index = 0
    color = COLORS[current_color_index]
    current_color_index += 1
    return color
# sometimes i question my sanity

def solve_find_end(maze):
    global stop, thread_count
    stop = False
    thread_count = 0
    max_threads = 24
    successful_thread_color = [None]
    thread_lock = threading.Lock()

    def thread_search(start_pos, color):
        global stop
        stack = [start_pos]

        while stack and not stop:
            position = stack.pop()
            row, col = position

            if maze.at_end(row, col):
                with thread_lock:
                    if not stop:
                        stop = True
                        successful_thread_color[0] = color
                return

            if maze.can_move_here(row, col):
                current_color = successful_thread_color[0] if stop else color
                maze.move(row, col, current_color)
                stack.extend(maze.get_possible_moves(row, col))

            if not stop:
                maze.restore(row, col)

    threads = []
    start_pos = maze.get_start_pos()

    for _ in range(max_threads):
        color = get_color()
        thread = threading.Thread(target=thread_search, args=(start_pos, color))
        threads.append(thread)
        thread_count += 1
        thread.start()

    for thread in threads:
        thread.join()


def find_end(log, filename, delay):
    """ Do not change this function """

    global thread_count
    global speed

    # create a Screen Object that will contain all of the drawing commands
    screen = Screen(SCREEN_SIZE, SCREEN_SIZE)
    screen.background((255, 255, 0))

    maze = Maze(screen, SCREEN_SIZE, SCREEN_SIZE, filename, delay=delay)

    solve_find_end(maze)

    log.write(f'Number of drawing commands = {screen.get_command_count()}')
    log.write(f'Number of threads created  = {thread_count}')

    done = False
    while not done:
        if screen.play_commands(speed): 
            key = cv2.waitKey(0)
            if key == ord('1'):
                speed = SLOW_SPEED
            elif key == ord('2'):
                speed = FAST_SPEED
            elif key == ord('q'):
                exit()
            elif key != ord('p'):
                done = True
        else:
            done = True



def find_ends(log):
    """ Do not change this function """

    files = (
        ('verysmall.bmp', True),
        ('verysmall-loops.bmp', True),
        ('small.bmp', True),
        ('small-loops.bmp', True),
        ('small-odd.bmp', True),
        ('small-open.bmp', False),
        ('large.bmp', False),
        ('large-loops.bmp', False)
    )

    log.write('*' * 40)
    log.write('Part 2')
    for filename, delay in files:
        log.write()
        log.write(f'File: {filename}')
        find_end(log, filename, delay)
    log.write('*' * 40)


def main():
    """ Do not change this function """
    sys.setrecursionlimit(5000)
    log = Log(show_terminal=True)
    find_ends(log)



if __name__ == "__main__":
    main()
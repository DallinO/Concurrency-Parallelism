"""
Course: CSE 251
Lesson Week: 07
File: prove.py
Author: Dallin Olson
Purpose: Process Task Files

Instructions:  See I-Learn

TODO

Add your comments here on the pool sizes that you used for your assignment and
why they were the best choices.

TYPE_PRIME: mp.Pool(3),
TYPE_WORD: mp.Pool(1),
TYPE_UPPER: mp.Pool(1),
TYPE_SUM: mp.Pool(1),
TYPE_NAME: mp.Pool(2)

This odd configuration produced the best times. The prime and name prcesses take
the most amount of time to complete so I assigned more processes to those. I did
not go above 8 total processes because I only have 8 cores. When I did add more
processes it actually slowed the total time.
"""

from datetime import datetime, timedelta
import requests
import multiprocessing as mp
from matplotlib.pylab import plt
import numpy as np
import glob
import math 

# Include cse 251 common Python files - Dont change
from cse251 import *

TYPE_PRIME  = 'prime'
TYPE_WORD   = 'word'
TYPE_UPPER  = 'upper'
TYPE_SUM    = 'sum'
TYPE_NAME   = 'name'

# Global lists to collect the task results
result_primes = []
result_words = []
result_upper = []
result_sums = []
result_names = []

def is_prime(n: int):
    """Primality test using 6k+-1 optimization.
    From: https://en.wikipedia.org/wiki/Primality_test
    """
    if n <= 3:
        return n > 1
    if n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i ** 2 <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True

def task_prime(value, result_primes):
    """
    Use the is_prime() above
    Add the following to the global list:
        {value} is prime
            - or -
        {value} is not prime
    """
    if is_prime(value):
       return result_primes.append(f'{value:,} is prime')
    else:
       return result_primes.append(f'{value:,} is not prime')


def task_word(word, result_words):
    """
    search in file 'words.txt'
    Add the following to the global list:
        {word} Found
            - or -
        {word} not found *****
    """
    with open("words.txt") as file:
        words_set = set(file.read().splitlines())
    if word in words_set:
       return result_words.append(f'{word} Found')
    else:
       return result_words.append(f'{word} not found *****')

def task_upper(text, result_upper):
    """
    Add the following to the global list:
        {text} ==>  uppercase version of {text}
    """

    return result_upper.append(f'{text} ==> {text.upper()}')

def task_sum(start_value, end_value, result_sums):
    """
    Add the following to the global list:
        sum of {start_value:,} to {end_value:,} = {total:,}
    """

    n = end_value - start_value + 1
    total = n * (start_value + end_value) // 2
    return result_sums.append(f'sum of {start_value:,} to {end_value:,} = {total:,}')

def task_name(url, result_names):
    """
    use requests module
    Add the following to the global list:
        {url} has name <name>
            - or -
        {url} had an error receiving the information
    """
    response = requests.get(url)
    if response.status_code == 200:
        name = response.json().get('name', 'Name not found')
        return result_names.append(f'{url} has name {name}')
    else:
       return result_names.append(f'{url} had an error receiving the information')

def main(result_primes, result_words, result_upper, result_sums, result_names):
    log = Log(show_terminal=True)
    log.start_timer()

# TODO Create process pools
    pools = {
        TYPE_PRIME: mp.Pool(3),
        TYPE_WORD: mp.Pool(1),
        TYPE_UPPER: mp.Pool(1),
        TYPE_SUM: mp.Pool(1),
        TYPE_NAME: mp.Pool(2)
    }

    # TODO you can change the following

    count = 0
    task_files = glob.glob("*.task")
    for filename in task_files:
        task = load_json_file(filename)
        count += 1
        task_type = task['task']
        if task_type == TYPE_PRIME:
            pools[TYPE_PRIME].apply_async(task_prime, args=(task['value'], result_primes))
        elif task_type == TYPE_WORD:
            pools[TYPE_WORD].apply_async(task_word, args=(task['word'], result_words))
        elif task_type == TYPE_UPPER:
            pools[TYPE_UPPER].apply_async(task_upper, args=(task['text'], result_upper))
        elif task_type == TYPE_SUM:
            pools[TYPE_SUM].apply_async(task_sum, args=(task['start'], task['end'], result_sums))
        elif task_type == TYPE_NAME:
            pools[TYPE_NAME].apply_async(task_name, args=(task['url'], result_names))
        else:
            log.write(f'Error: unknown task type {task_type}')
    # TODO start and wait pools
    # this was better in creating all those pools
    for pool in pools.values():
        pool.close()
        pool.join()


    # Do not change the following code (to the end of the main function)
    def log_list(lst, log):
        for item in lst:
            log.write(item)
        log.write(' ')
    
    log.write('-' * 80)
    log.write(f'Primes: {len(result_primes)}')
    log_list(result_primes, log)

    log.write('-' * 80)
    log.write(f'Words: {len(result_words)}')
    log_list(result_words, log)

    log.write('-' * 80)
    log.write(f'Uppercase: {len(result_upper)}')
    log_list(result_upper, log)

    log.write('-' * 80)
    log.write(f'Sums: {len(result_sums)}')
    log_list(result_sums, log)

    log.write('-' * 80)
    log.write(f'Names: {len(result_names)}')
    log_list(result_names, log)

    log.write(f'Number of Primes tasks: {len(result_primes)}')
    log.write(f'Number of Words tasks: {len(result_words)}')
    log.write(f'Number of Uppercase tasks: {len(result_upper)}')
    log.write(f'Number of Sums tasks: {len(result_sums)}')
    log.write(f'Number of Names tasks: {len(result_names)}')
    log.stop_timer(f'Finished processes {count} tasks')

if __name__ == '__main__':
    with mp.Manager() as manager:
        result_primes = manager.list()
        result_words = manager.list()
        result_upper = manager.list()
        result_sums = manager.list()
        result_names = manager.list()
        
        main(result_primes, result_words, result_upper, result_sums, result_names)
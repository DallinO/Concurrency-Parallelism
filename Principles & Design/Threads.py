# THREADS (PYTHON)

'''
A thread is the smallest unit of execution within a process. A process, in turn,
is an independent program that runs in its own memory space. Threads within a 
process share the same resources, including memory space, but each thread has 
its own execution context, such as program counter and register values.

Key points about threads include:

Concurrency: Threads enable concurrent execution within a process, allowing
multiple tasks to progress independently. Each thread has its own sequence of
instructions and can run concurrently with other threads.

Resource Sharing: Threads within the same process share resources like memory
space, file descriptors, and code segments. This shared access allows for more
efficient communication and coordination between threads.

Lightweight: Threads are generally considered lightweight compared to processes.
Creating and switching between threads is typically faster than doing the same
with processes.

Independence: Threads within the same process can run independently, allowing for
parallelism. However, developers need to consider synchronization to avoid
conflicts when multiple threads access shared data concurrently.

States: Threads can exist in different states such as running, ready, and blocked.
The operating system scheduler manages the execution of threads based on their
states and priorities.

Task Parallelism: Threads are often used to achieve task parallelism by breaking
down a larger task into smaller subtasks that can be executed concurrently.
'''

import threading        # We must import the threading module.
import os

def main():
    os.system('cls')
    print('END')

if __name__ == '__main__':
    main()
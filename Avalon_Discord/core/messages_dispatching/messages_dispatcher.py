import logging

from collections import deque

from .task import Task
from .helper_client_executor import HelperClientExecutor
from.task_queue import TaskQueue

MAX_NUMBER_OF_HELPING_CLIENTS = 3

HELPING_THREAD_NAME_TEMPLATE = 'HelperThread-{id}'

class MessagesDispatcher:
    _tasks_queues      = None
    _clients_executors = None
    _clients_token     = None


    def __init__(self, clients_token):
        self._clients_token = clients_token

        self._clients_executors = list()
        self._tasks_queues      = deque()

        helper_thread_id = 0

        for _ in range (0, MAX_NUMBER_OF_HELPING_CLIENTS):
            new_queue           = TaskQueue()
            new_helper_executor = HelperClientExecutor(
                new_queue, 
                clients_token)

            self._clients_executors.append(new_helper_executor)

            new_helper_executor.start(
                HELPING_THREAD_NAME_TEMPLATE.format(id = helper_thread_id))
            self._tasks_queues.append(new_queue)
            helper_thread_id += 1

            

    def order_task_to_execute(
        self, 
        task: Task)\
                                  -> type(None):
        
        most_free_task_queue = self._tasks_queues[0]
        self._tasks_queues.rotate()
        logging.info('Adding a task to queue...')
        most_free_task_queue.add_task(task)
        logging.info('Task added to queue.')

    # TODO Consider to add stop functionality?
            

# import sched
# import time
# import random
# import config as cfg
# import messages as ms
# from typing import Callable
# import node as nd
# import params as pm
# from threading import Thread
# import codes as cd

# class Query:
#     """
#     A class used to track and handle all of the node's open queries
#     Queries are used to handle communications with the sequencer.
#     Once sent, the open query is stored and dropped once a response is received or the query times out.
#     Once a response is received, the query can run a processing function to handle the response.
#     """

#     def __init__(
#         self,
#         query_type: bytes,
#         processing_function: Callable | None = None,
#         data: bytes = b"",
#         alloted_time: float = 1,
#         max_retries: int = 4,
#     ):
#         self.alloted_time = alloted_time
#         self.response = None
#         self.query_type = query_type
#         self.processing_function = processing_function
#         self.data = data
#         self.max_retries = max_retries
#         self.retries = 0
#         while True:
#             self.query_id = random.randint(0, 2 ** (pm.DB_INT_LENGTH * 8))
#             if self.query_id not in nd.open_queries.keys():
#                 break

#         self.scheduler = sched.scheduler(time.time, time.sleep)
#         self.scheduler.enter(self.alloted_time, 0, self.retry)
#         # self.scheduler.run()
#         t_retry = Thread(target=self.scheduler.run, name="delete")
#         t_retry.start()

#         nd.open_queries[self.query_id] = self
#         self.send_query()

#     def send_query(self) -> None:
#         """send message to sequencer with info for query"""
#         query_id = self.query_id.to_bytes(4, "big")
#         message = ms.format_message(self.query_type, query_id, self.data)
#         cfg.client_socket.send(message)

#     def retry(self) -> None:
#         """retry sending the query"""
#         if self.retries > self.max_retries:
#             self.delete()
#             return
#         if self.query_id in nd.open_queries.keys():
#             self.scheduler.enter(
#                 self.alloted_time * 2**self.retries * random.uniform(0.5, 1),
#                 0,
#                 self.retry,
#             )
#             self.retries += 1
#             t_retry = Thread(target=self.scheduler.run, name="delete")
#             t_retry.start()
#         self.send_query()

#     def delete(self) -> None:
#         if self.query_id in nd.open_queries.keys():
#             del nd.open_queries[self.query_id]

#     def process_query_response(self, response: bytes):
#         """process the query response and delete the query"""
#         if self.processing_function is not None:
#             self.processing_function(response, self.data)
#         self.delete()


import sched
import time
import random
import config as cfg
import messages as ms
from typing import Callable
import node as nd
import params as pm
from threading import Thread
import codes as cd

class Query:
    """
    A class used to track and handle all of the node's open queries
    Queries are used to handle communications with the sequencer.
    Once sent, the open query is stored and dropped once a response is received or the query times out.
    Once a response is received, the query can run a processing function to handle the response.
    """

    def __init__(   
        self,
        query_type: bytes,
        processing_function: Callable | None = None,
        data: bytes = b"",
        alloted_time: float = 1,
        max_retries: int = 0,
    ):
        self.alloted_time = alloted_time
        self.response = None
        self.query_type = query_type
        self.processing_function = processing_function
        self.data = data
        self.max_retries = max_retries
        self.retries = 0

        # if self.alloted_time is not None:
        self.scheduler = sched.scheduler(time.time, time.sleep)
        self.scheduler.enter(self.alloted_time, 0, self.retry)
        # self.scheduler.run()
        # t_del = Thread(target=self.scheduler.run, name="delete")
        # t_del.start()
        t_retry = Thread(target=self.scheduler.run, name="retry")
        t_retry.start()

        while True:
            self.query_id = random.randint(0, 2**(pm.DB_INT_LENGTH*8))
            if self.query_id not in nd.open_queries.keys():
                break
        # print("created", self.query_id)
        nd.open_queries[self.query_id] = self
        self.send_query()

    def send_query(self) -> None:
        """send message to sequencer with info for query"""
        query_id = self.query_id.to_bytes(4, "big")
        message = ms.format_message(self.query_type, query_id, self.data)
        cfg.client_socket.send(message)

    def retry(self) -> None:
        if self.query_id in nd.open_queries.keys():
            if self.retries >= self.max_retries:
                self.delete()
                return
            self.scheduler.enter(self.alloted_time, 0, self.retry)
            self.retries += 1
            self.send_query()
            t = cd.reverse[self.query_type]
            print("query unresponsive, retrying", t, self.data, self.query_id)
            t_retry = Thread(target=self.scheduler.run, name="retry")
            t_retry.start()


    def delete(self, p= True) -> None:
        if self.query_id in nd.open_queries.keys():
            del nd.open_queries[self.query_id]
            if p:
                t = cd.reverse[self.query_type]
                if t not in {"REQUEST_ALIAS","REQUEST_ALIAS_UPDATE","REQUEST_NYM_UPDATE","REQUEST_BC"}:
                    print("query unresponsive, deleting", t, self.data, self.query_id)
        

    def process_query_response(self, response: bytes):
        """process the query response and delete the query"""
        # print("processed", self.query_id)
        if self.processing_function is not None:
            self.processing_function(response, self.data)
        self.delete(False)


# import sched
# import time
# import random
# import config as cfg
# import messages as ms
# from typing import Callable
# import node as nd
# import params as pm
# from threading import Thread
# import codes as cd

# class Query:
#     """
#     A class used to track and handle all of the node's open queries
#     Queries are used to handle communications with the sequencer.
#     Once sent, the open query is stored and dropped once a response is received or the query times out.
#     Once a response is received, the query can run a processing function to handle the response.
#     """

#     def __init__(
#         self,
#         query_type: bytes,
#         processing_function: Callable | None = None,
#         data: bytes = b"",
#         alloted_time: float = 1,
#         max_retries: int = 4,
#     ):
#         self.alloted_time = alloted_time
#         self.response = None
#         self.query_type = query_type
#         self.processing_function = processing_function
#         self.data = data
#         self.max_retries = max_retries
#         self.retries = 0
#         while True:
#             self.query_id = random.randint(0, 2 ** (pm.DB_INT_LENGTH * 8))
#             if self.query_id not in nd.open_queries.keys():
#                 break

#         self.scheduler = sched.scheduler(time.time, time.sleep)
#         self.scheduler.enter(self.alloted_time, 0, self.retry)
#         # self.scheduler.run()
#         t_retry = Thread(target=self.scheduler.run, name="delete")
#         t_retry.start()

#         nd.open_queries[self.query_id] = self
#         self.send_query()

#     def send_query(self) -> None:
#         """send message to sequencer with info for query"""
#         query_id = self.query_id.to_bytes(4, "big")
#         message = ms.format_message(self.query_type, query_id, self.data)
#         cfg.client_socket.send(message)

#     def retry(self) -> None:
#         """retry sending the query"""
#         if self.retries > self.max_retries:
#             self.delete()
#             return
#         if self.query_id in nd.open_queries.keys():
#             self.scheduler.enter(
#                 self.alloted_time * 2**self.retries * random.uniform(0.5, 1),
#                 0,
#                 self.retry,
#             )
#             self.retries += 1
#             t_retry = Thread(target=self.scheduler.run, name="delete")
#             t_retry.start()
#         self.send_query()

#     def delete(self) -> None:
#         if self.query_id in nd.open_queries.keys():
#             del nd.open_queries[self.query_id]

#     def process_query_response(self, response: bytes):
#         """process the query response and delete the query"""
#         if self.processing_function is not None:
#             self.processing_function(response, self.data)
#         self.delete()


# import sched
# import time
# import random
# import config as cfg
# import messages as ms
# from typing import Callable
# import node as nd
# import params as pm
# from threading import Thread

# class Query:
#     """
#     A class used to track and handle all of the node's open queries
#     Queries are used to handle communications with the sequencer.
#     Once sent, the open query is stored and dropped once a response is received or the query times out.
#     Once a response is received, the query can run a processing function to handle the response.
#     """

#     def __init__(
#         self,
#         query_type: bytes,
#         processing_function: Callable | None = None,
#         data: bytes = b"",
#         alloted_time: float | None = 2,
#     ):
#         self.alloted_time = alloted_time
#         self.response = None
#         self.query_type = query_type
#         self.processing_function = processing_function
#         self.data = data

#         if self.alloted_time is not None:
#             self.scheduler = sched.scheduler(time.time, time.sleep)
#             self.scheduler.enter(self.alloted_time, 0, self.delete)
#             # self.scheduler.run()
#             t_del = Thread(target=self.scheduler.run, name="delete")
#             t_del.start()

#         while True:
#             self.query_id = random.randint(0, 2**(pm.DB_INT_LENGTH*8))
#             if self.query_id not in nd.open_queries.keys():
#                 break
#         # print("created", self.query_id)
#         nd.open_queries[self.query_id] = self
#         self.send_query()

#     def send_query(self) -> None:
#         """send message to sequencer with info for query"""
#         query_id = self.query_id.to_bytes(4, "big")
#         message = ms.format_message(self.query_type, query_id, self.data)
#         cfg.client_socket.send(message)

#     def delete(self, p= True) -> None:
#         if self.query_id in nd.open_queries.keys():
#             del nd.open_queries[self.query_id]
#             if p:
#                 t = cd.reverse[self.query_type]
#                 if t not in {"REQUEST_ALIAS","REQUEST_ALIAS_UPDATE","REQUEST_NYM_UPDATE","REQUEST_BC"}:
#                     print("query unresponsive, deleting", t, self.data, self.query_id)
        

#     def process_query_response(self, response: bytes):
#         """process the query response and delete the query"""
#         # print("processed", self.query_id)
#         if self.processing_function is not None:
#             self.processing_function(response, self.data)
#         self.delete(False)

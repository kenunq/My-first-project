import functools
import statistics
import time
from unittest.util import safe_repr

from django.core.signals import request_started
from django.db import connection, reset_queries
from django.test.utils import CaptureQueriesContext


class CaptureQueriesContext2(CaptureQueriesContext):
    """
    Замеряет количество запросов к бд внутри тела контекстного менеджера,
    выводит подробную информацию о замере,
    валидирует количество запросов.

    UseCase::

        with CaptureQueriesContext2():
            response = self.client.get(url)

   Queries count: 164  |  Execution time: 0.92s
 
     - assert_q_count: Ожидаемое количество запросов к БД иначе "AssertionError: N not less than or equal to N"
     - verbose: Отображение финальных результатов тестового замера
     - queries: Отображение сырых SQL запросов к БД
 
     Queries count: Количество запросов к БД внутри контекстного менеджера
     Execution time: Время выполнения запросов к БД внутри контекстного менеджера
     """  # noqa: E501
     def __init__(self, assert_q_count: int | None = None, verbose=True, queries=False):
         super().__init__(connection)
 
         self.assert_q_count = assert_q_count
         self.verbose = verbose
         self.queries = queries
 
     def __enter__(self):
         self.start = time.perf_counter()
         return super().__enter__()
 
     def __exit__(self, exc_type, exc_value, traceback):
         super().__exit__(exc_type, exc_value, traceback)
 
         end = time.perf_counter()
         execution_time = end - self.start
 
         if self.queries:
             for query in self.captured_queries:
                 print(query, end="\n\n")
 
         if self.verbose:
             print(f"Queries count: {self.final_queries}  |  Execution time: {execution_time:.2f}s")
 
         if self.assert_q_count is not None:
             standard_msg = (f"{safe_repr(self.final_queries)} not less than or equal to "
                             f"{safe_repr(self.assert_q_count)}")
             assert self.final_queries <= self.assert_q_count, standard_msg

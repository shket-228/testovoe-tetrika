from data import tests
import sys


# Or disconnection if is_join == False
class Connection:
    def __init__(self, time, is_join=True):
        self.time = time
        self.is_join = is_join

    # For sorting
    def __lt__(self, other):
        return self.time < other.time


# Translate list of ints to list of connections
def to_conn_list(interval):
    return [Connection(v, i % 2) for i, v in enumerate(interval, 1)]


# Union connection inervals of one client
#   For avoiding "one-client" merge conflict,
#   otherwise attedance could be > 3
def union_one_client(connections):
    result = []
    connections = sorted(connections)
    parallel = 0
    for conn in connections:
        if (parallel == 0 and conn.is_join) or (parallel == 1 and not conn.is_join):
            result.append(conn)
        parallel += 1 if conn.is_join else -1
    return result


# Common merging of multiple sorted sequences (from merge sort)
def merge_many_clients(all_conn):
    len_all_conn = sum(len(conns) for conns in all_conn)
    result = []
    el_indices = [0] * len(all_conn)

    while len(result) < len_all_conn:
        min_conn = Connection(sys.maxsize)
        for i in range(len(all_conn)):
            if el_indices[i] < len(all_conn[i]):
                conn = all_conn[i][el_indices[i]]
                if conn.time < min_conn.time:
                    min_conn = conn
                    min_i = i
        result.append(min_conn)
        el_indices[min_i] += 1

    return result


def appearance(intervals):
    # Merging connections of different clients to "one-client"
    all_conn = merge_many_clients(
        list(
            map(
                lambda interval: union_one_client(to_conn_list(interval)),
                intervals.values(),
            )
        )
    )

    # Counting time according to attendance
    answer = 0
    attendance = 0
    for conn in all_conn:
        if attendance == 3:  # Crucial condition ("one-client")
            answer += conn.time - prev_conn.time
        attendance += 1 if conn.is_join else -1
        prev_conn = conn
    return answer


if __name__ == "__main__":
    for i, test in enumerate(tests):
        test_answer = appearance(test["data"])
        assert (
            test_answer == test["answer"]
        ), f'Error on test case {i}, got {test_answer}, expected {test["answer"]}'

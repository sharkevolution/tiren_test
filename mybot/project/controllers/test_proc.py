
import logging
import psutil
import time
from multiprocessing import Process, Pipe, current_process


def f(conn):

    name = current_process().pid
    conn.send([name, ])

    while True:
        h = conn.recv()
        if h == 2:
            conn.send([42, name, 'hello'])
            time.sleep(5)
            conn.send([43, name, 'hello'])
            logging.info('ok1')
            conn.close()
            break


def main_proc():

    parent_conn, child_conn = Pipe()
    p = Process(target=f, args=(child_conn,))
    p.start()
    pd = parent_conn.recv()
    logging.info((pd[0]))

    parent_conn.send(1)   # prints "[42, None, 'hello']"

    pid = pd
    if psutil.pid_exists(pid[0]):
        logging.info("a process with pid %d exists" % pid[0])
    else:
        logging.info("a process with pid %d does not exist" % pid[0])

    parent_conn.send(2)
    logging.info(parent_conn.recv())
    # p.join()
    logging.info('ok')


if __name__ == '__main__':
    pass
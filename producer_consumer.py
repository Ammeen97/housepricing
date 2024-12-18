from threading import Semaphore, Event
import queue
import time

buffer = queue.Queue(maxsize=10)
empty = Semaphore(10)
full = Semaphore(0)
stop_event = Event()

def produce_data():
    return {"input_data": "some_value"}

def process_data(data):
    result = f"Processed result for {data}"
    return result

def producer(max_iterations=10):
    for _ in range(max_iterations):
        if stop_event.is_set():
            break
        empty.acquire()
        data = produce_data()
        buffer.put(data)
        print(f"Produced: {data}")
        full.release()
        time.sleep(1)

def consumer(max_iterations=10):
    for _ in range(max_iterations):
        if stop_event.is_set():
            break
        full.acquire()
        data = buffer.get()
        result = process_data(data)
        print(f"Consumed: {result}")
        empty.release()
        time.sleep(1)

from queue import Queue
from threading import Thread


class EventManager:

    def __init__(self):
        self._timeOut = 1
        self._eventQueue = Queue()
        self._activated = False
        self._thread = Thread(target=self._run)
        self._handler_dict = {}

    def _run(self):
        while self._activated:
            if not self._eventQueue.empty():
                event = self._eventQueue.get(block=True, timeout=self._timeOut)
                self._event_process(event)

    def _event_process(self, event):
        if event.type in self._handler_dict:
            for handler in self._handler_dict[event.type]:
                handler(event)

    def start(self):
        self._activated = True
        self._thread.start()

    def stop(self):
        self._activated = False
        self._thread.join()

    def add_event_listener(self, event_type, event_handler):
        handler_list = self._handler_dict.get(event_type) or []

        if event_handler not in handler_list:
            handler_list.append(event_handler)

        self._handler_dict[event_type] = handler_list

    def remove_event_listener(self, type_, handler):
        pass

    def send_event(self, event):
        self._eventQueue.put(event)


class Event:
    def __init__(self, type_):
        self.type = type_
        self.data = {}

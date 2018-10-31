from eventCustom.eventManage import EventManager, Event
import time

EVENT_ARTICLE = "Event_Article"


class Subscription:
    def __init__(self, event_manager):
        self._eventManager = event_manager

    def write_new_article(self):
        event = Event(type_=EVENT_ARTICLE)
        event.data["article"] = '如何写出更优雅的代码\n'

        self._eventManager.send_event(event)
        print('公众号发送新文章')


class Listener:
    def __init__(self, username):
        self._username = username

    def read_article(self, event):
        print('%s 收到新文章' % self._username)
        print('正在阅读新文章内容：%s' % event.data["article"])


def test():
    listener1 = Listener("ThinkRoom")
    listener2 = Listener("Steve")

    event_manager = EventManager()

    event_manager.add_event_listener(EVENT_ARTICLE, listener1.read_article)
    event_manager.add_event_listener(EVENT_ARTICLE, listener2.read_article)
    event_manager.start()

    subscription = Subscription(event_manager)
    while True:
        subscription.write_new_article()
        time.sleep(2)


if __name__ == '__main__':
    test()

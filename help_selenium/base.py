#!/usr/bin/env python3


# formal lib
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from abc import ABCMeta, abstractmethod
from threading import Thread
from inputimeout import inputimeout, TimeoutOccurred
# my lib


class AccessBase(object, metaclass=ABCMeta):
    def __init__(self, options_ins=None, size=(1440, 783),
                 implicit_wait=3):
        cond1 = options_ins is None
        cond2 = isinstance(options_ins, Options)
        if not (cond1 or cond2):
            raise TypeError("Use Options in selenium libraries.")
        self.driver = webdriver.Chrome(options=options_ins)
        self._set_windows_size(size)
        self._set_implicit_wtime(implicit_wait)

    def _set_windows_size(self, size=(1440, 783)):
        self.size = size

    def _set_implicit_wtime(self, implicit_time=5):
        self.implicit_time = implicit_time

    def _initial_access(self):
        self.driver.set_window_size(*self.size)
        self.driver.implicitly_wait(self.implicit_time)

    @classmethod
    @abstractmethod
    def access(self):
        raise NotImplementedError("")

    def wait(self, time=300):
        time.sleep(time)

    def quit(self):
        self.driver.quit()

    def input_wait(self, wtime=300):
        try:
            _ = inputimeout(
                        "waiting for {}:".format(wtime),
                        timeout=wtime)
        except TimeoutOccurred:
            pass
        self.quit()

    def input_wait_by_thread(self, wtime=300):
        t1 = Thread(target=self.input_wait, args=(wtime))
        t1.start()

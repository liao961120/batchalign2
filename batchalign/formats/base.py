from abc import ABC, abstractproperty, abstractmethod

class BaseFormat:

    @abstractproperty
    def doc(self):
        pass

    @abstractmethod
    def write(self, path):
        pass

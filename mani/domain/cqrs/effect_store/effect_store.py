from abc import abstractmethod, ABC


class EffectStore(ABC):
    @abstractmethod
    def append(self, effect):
        pass

    @abstractmethod
    def __iter__(self):
        pass

    @abstractmethod
    def clear(self):
        pass

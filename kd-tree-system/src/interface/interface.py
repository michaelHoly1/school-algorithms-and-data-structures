from abc import ABC, abstractmethod

class PodporujeRovnost(ABC):
    """
    Interface pre podporu logickeho operatora ==.
    """
    @abstractmethod
    def __eq__(self, porovnavany) -> bool:
        pass


class PodporujeLogickeOperatory(ABC):
    """
    Interface pre podporu logickych operatorov: <=, <, >, and ==.
    """
    @abstractmethod
    def __le__(self, porovnavany) -> bool:
        pass

    @abstractmethod
    def __lt__(self, porovnavany) -> bool:
        pass

    @abstractmethod
    def __gt__(self, porovnavany) -> bool:
        pass
    
    @abstractmethod
    def __eq__(self, porovnavany) -> bool:
        pass

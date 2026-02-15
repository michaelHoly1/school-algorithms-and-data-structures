from abc import ABC, abstractmethod
from bitarray import bitarray


class PodporujePracuSByteArray(ABC):
    """
    Interface pre podporu prace s byte array.
    """

    @abstractmethod
    def vrat_velkost(self) -> int:
        pass

    @abstractmethod
    def na_byte_array(self) -> bytearray:
        pass

    @abstractmethod
    def z_byte_array(self, byte_array: bytearray):
        pass

class IData(PodporujePracuSByteArray):
    """
    Interface pre podporu logickeho operatora ==, klonovania instancii vkladanych dat a podporu prace s byte array.
    """
    @abstractmethod
    def __eq__(self, porovnavany) -> bool:
        pass

    @abstractmethod
    def klonuj(self) -> 'IData':
        pass
    
    @abstractmethod
    def to_string(self) -> str: 
        pass


class IHashData(IData):
    """
    Interface pre podporu hashovania.
    """
    @abstractmethod
    def get_hash(self) -> bitarray:
        pass




    

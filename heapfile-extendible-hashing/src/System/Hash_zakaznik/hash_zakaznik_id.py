from System.Hash_zakaznik.hash_zakaznik import HashZakaznik
from Interface.interface import IHashData
from bitarray import bitarray


class HashZakaznikID(HashZakaznik):
    """
    Trieda HashZakaznikID reprezentuje zákazníka s adresou a ID.
    Atribúty:
        __id (int): ID zákazníka.
        __adresa (int): Adresa zákazníka.
    """

    def __init__(self, id: int, adresa: int):
        """
        Inicializuje objekt HashZakaznikID.
        """
        super().__init__(adresa)
        self.__id = id
        
        

    def get_id(self) -> int:
        """
        Vráti ID zákazníka.
        """
        return self.__id
    
    def set_id(self, id):
        """
        Nastaví ID zákazníka.
        """
        self.__id = id
    
    def vrat_velkost(self) -> int:
        """
        Vráti veľkosť záznamu v bajtoch.
        """
        return 8

    
    def na_byte_array(self) -> bytearray:
        """
        Konvertuje objekt na byte array.
        """
        byte_array = bytearray()
        byte_array += self.__id.to_bytes(4, byteorder='big', signed=True)
        byte_array += super().na_byte_array()
        return byte_array
        
            
    def z_byte_array(self, byte_array: bytearray):
        """
        Konvertuje byte array na objekt.
        """
        self.__id = int.from_bytes(byte_array[:4], byteorder='big', signed=True)
        super().z_byte_array(byte_array[4:])
        
    
    def __eq__(self, porovnavany) -> bool:
        """
        Porovnáva dva objekty HashZakaznikID podľa ID.
        """
        if isinstance(porovnavany, HashZakaznikID):
            return self.__id == porovnavany.get_id()
        return False

    
    def klonuj(self) -> IHashData:
        """
        Vytvorí klon zákazníka s prednastavenými hodnotami.
        """
        klon = HashZakaznikID(-1, -1)
        return klon
    
    
    def to_string(self) -> str:
        """
        Vráti reprezentáciu objektu HashZakaznikID vo forme stringu.
        """ 
        return f"ID: {self.__id} {super().to_string()} \n"
    

    def get_hash(self) -> bitarray:
        """
        Vráti hash zákazníka - čo je v tomto prípade prevod na bitové pole.
        """
        bit_array = bitarray(endian='little')
        bit_array.frombytes(self.__id.to_bytes(4, byteorder='little'))
        return bit_array
from Interface.interface import IHashData
from bitarray import bitarray

class HashZakaznik(IHashData):
    """
    Trieda HashZakaznik reprezentuje zákazníka s adresou.
    Atribúty:
        __adresa (int): Adresa zákazníka.
    """

    def __init__(self, adresa):
        """
        Inicializuje objekt HashZakaznik.
        Atribúty:
            adresa (int): Adresa zákazníka.
        """
        if not isinstance(adresa, int):
            raise TypeError("Adresa musi byt cislo")
        else:
            self.__adresa = adresa

        self.__adresa = adresa
    
    def get_adresa(self) -> int:
        """
        Vráti adresu zákazníka.
        """
        return self.__adresa
    
    def set_adresa(self, adresa):
        """
        Nastaví adresu zákazníka.
        """
        self.__adresa = adresa
    
    def vrat_velkost(self) -> int:
        """
        Vráti veľkosť záznamu v bajtoch.
        """
        return 4

    
    def na_byte_array(self) -> bytearray:
        """
        Konvertuje objekt na byte array.
        """
        byte_array = bytearray()
        byte_array += self.__adresa.to_bytes(4, byteorder='big', signed=True)
        return byte_array
        
            
    def z_byte_array(self, byte_array: bytearray):
        """
        Konvertuje byte array na objekt.
        """
        self.__adresa = int.from_bytes(byte_array[:4], byteorder='big', signed=True)
        
    
    def __eq__(self, porovnavany) -> bool:
        """
        Porovná dva objekty HashZakaznik podľa adresy.
        """
        pass

    
    def klonuj(self) -> IHashData:
        """
        Vytvorí klon zákazníka s prednastavenými hodnotami.
        """
        pass
    
    def get_hash(self) -> bitarray:
        """
        Vráti hash zákazníka.
        """
        pass

    def to_string(self) -> str: 
        """
        Vráti reprezentáciu objektu HashZakaznik v podobe stringu.
        """
        return f"Adr: {self.__adresa}"

    
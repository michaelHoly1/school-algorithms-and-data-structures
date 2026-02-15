from System.Hash_zakaznik.hash_zakaznik import HashZakaznik
from Interface.interface import IHashData
from bitarray import bitarray


class HashZakaznikECV(HashZakaznik):
    """
    Trieda HashZakaznikECV reprezentuje zákazníka s adresou a ECV.
    Atribúty:
        __ecv (str): Evidenčné číslo vozidla.
        __adresa (int): Adresa zákazníka.
    """

    def __init__(self, ecv: str, adresa: int):
        """
        Inicializuje objekt HashZakaznikECV.
        """
        if len (ecv) > 10:
            raise ValueError("Ecv moze mat maximalne 10 znakov")
        else:
            self.__pocet_platnych_znakov_v_ecv = len(ecv)
            self.__ecv = ecv
        super().__init__(adresa)
        

    def get_ecv(self) -> str:
        """
        Vrátí ECV zákazníka.
        """
        return self.__ecv
    
    def set_ecv(self, ecv):
        """
        Nastaví ECV zákazníka.
        """
        self.__ecv = ecv

    
    def vrat_velkost(self) -> int:
        """
        Vráti veľkosť záznamu v bajtoch.
        """
        return 15 #4 + 1 + 10 

    
    def na_byte_array(self) -> bytearray:
        """
        Konvertuje objekt na byte array.
        """
        byte_array = bytearray()
        byte_array += self.__pocet_platnych_znakov_v_ecv.to_bytes(1, byteorder='big')
        byte_array += self.__dopln_znaky_do_ecv().encode('utf-8')
        byte_array += super().na_byte_array()
        
        return byte_array
        
            
    def z_byte_array(self, byte_array: bytearray):
        """
        Konvertuje byte array na objekt.
        """
        self.__pocet_platnych_znakov_v_ecv = int.from_bytes(byte_array[:1], byteorder='big')
        self.__ecv = byte_array[1:11].decode('utf-8')
        self.__odstran_znaky_z_ecv(self.__ecv)
        super().z_byte_array(byte_array[11:])

    def __dopln_znaky_do_ecv(self) -> str:
        """
        Doplní ECV na dĺžku 10 znakov.
        """
        doplnene_ecv = self.__ecv
        while len(doplnene_ecv) < 10:
            doplnene_ecv += '*'
        return doplnene_ecv
    
    def __odstran_znaky_z_ecv(self, nacitane_ecv):
        """
        Odstráni doplnené znaky z ECV.
        """
        self.__ecv = nacitane_ecv[:self.__pocet_platnych_znakov_v_ecv]
        
    
    def __eq__(self, porovnavany) -> bool:
        """
        Porovnáva dva objekty HashZakaznikECV podľa ECV.
        """
        if isinstance(porovnavany, HashZakaznikECV):

            return self.__ecv[:4] == porovnavany.get_ecv()[:4]
        return False

    
    def klonuj(self) -> IHashData:
        """
        Vytvorí klon zákazníka s prednastavenými hodnotami.
        """
        klon = HashZakaznikECV("klon", -1)
        return klon
    
    
    def to_string(self) -> str: 
        """
        Vráti representáciu objektu ako string.
        """
        return f" ECV: {self.__ecv} {super().to_string()} \n"
    

    def get_hash(self) -> bitarray:
        """
        Vráti hash zákazníka - čo je v tomto prípade prevod na bitové pole.
        """
        bit_array = bitarray(endian='little')
        bit_array.frombytes(self.__ecv.encode('utf-8'))
        if len(bit_array) < 32:
            pocet_doplnenych_bitov = 32 - len(bit_array)
            bit_array.extend([False] * pocet_doplnenych_bitov)
        
        return bit_array[:32]
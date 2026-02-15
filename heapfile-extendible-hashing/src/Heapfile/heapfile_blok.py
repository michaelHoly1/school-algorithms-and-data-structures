from Heapfile.blok import Blok
from Interface.interface import IData

class HeapfileBlok(Blok):
    """
    Trieda HeapfileBlok reprezentuje blok v pamäti s dĺžkou bloku, záznamami a s adresami nasledovného a predchádzajúceho bloku.
    Atribúty:
        __velkost_bloku (int): Veľkosť bloku.
        __instancia_zaznamu (IData): Inštancia záznamu.
        __nasledovny_blok (int): Adresa nasledovného bloku.
        __predchadzajuci_blok (int): Adresa predchádzajúceho bloku.
    """

    def __init__(self, velkost_bloku, instancia_zaznamu : IData):
        """
        Inicializuje objekt HeapfileBlok.
        """
        super().__init__(velkost_bloku, instancia_zaznamu)
        self.__instancia_zaznamu = instancia_zaznamu
        self.__velkost_bloku = velkost_bloku
        self.__nasledovny_blok = -1
        self.__predchadzajuci_blok = -1

    def get_nasledovny_blok(self) -> int:
        """
        Vráti adresu nasledovného bloku.
        """
        return self.__nasledovny_blok

    def get_predchadzajuci_blok(self) -> int:
        """
        Vráti adresu predchádzajúceho bloku.
        """
        return self.__predchadzajuci_blok
    
    def set_nasledovny_blok(self, adresa):
        """
        Nastaví adresu nasledovného bloku.
        """
        self.__nasledovny_blok = adresa

    def set_predchadzajuci_blok(self, adresa):
        """
        Nastaví adresu predchádzajúceho bloku.
        """
        self.__predchadzajuci_blok = adresa
    
    def vrat_velkost(self) -> int:
        """
        Vráti veľkosť bloku v bajtoch.
        """
        return 8 + super().vrat_velkost()
    
    def get_maximalny_pocet_zaznamov(self) -> int:
        """
        Vráti maximálny počet záznamov v bloku.
        """
        minimalna_velkost = 8
        velkost_zaznamu = self.__instancia_zaznamu.vrat_velkost()
        maximalny_pocet_zaznamov = (self.__velkost_bloku - minimalna_velkost) // velkost_zaznamu
        return maximalny_pocet_zaznamov
        
    def na_byte_array(self) -> bytearray:
        """
        Konvertuje objekt na byte array.
        """
        byte_array = bytearray()
        byte_array += self.__nasledovny_blok.to_bytes(4, byteorder='big', signed=True)
        byte_array += self.__predchadzajuci_blok.to_bytes(4, byteorder='big', signed=True)

        byte_array += super().na_byte_array()

        
        return byte_array
    
    def z_byte_array(self, byte_array):
        """
        Konvertuje byte array na objekt.
        """
        self.__nasledovny_blok = int.from_bytes(byte_array[:4], byteorder='big', signed=True)
        self.__predchadzajuci_blok = int.from_bytes(byte_array[4:8], byteorder='big' , signed=True)
        super().z_byte_array(byte_array)

        

    def to_string(self) -> str:
        """
        Vráti string reprezentujúci objekt.
        """
        blok_na_string = ''
        pocet_platnych_zaznamov = self.get_pocet_platnych_zaznamov()
        blok_na_string += f'Pocet platnych zaznamov: {pocet_platnych_zaznamov}/{self.get_maximalny_pocet_zaznamov()}\n'
        blok_na_string += f'Nasledovny blok: {self.__nasledovny_blok}   Predchadzajuci blok: {self.__predchadzajuci_blok}\n'
        if pocet_platnych_zaznamov > 0:
            blok_na_string += 'Zaznamy:\n'
            for i in range(len(self._Blok__zaznamy)):
                if i < pocet_platnych_zaznamov:
                    blok_na_string += self._Blok__zaznamy[i].to_string()
                else:
                    blok_na_string += '|X| \n'
        else:
            blok_na_string += 'Blok neobsahuje ziadne zaznamy\n'
            

        return blok_na_string


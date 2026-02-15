from typing import List
from Interface.interface import PodporujePracuSByteArray, IData

class Blok(PodporujePracuSByteArray):
    """
    Trieda Blok reprezentuje blok v pamäti s dĺžkou bloku a záznamami.
    Atribúty:
        __velkost_bloku (int): Veľkosť bloku.
        __instancia_zaznamu (IData): Inštancia záznamu.
        __zaznamy (List[IData]): Zoznam záznamov v bloku.
        __pocet_platnych_zaznamov (int): Počet platných záznamov v bloku.
    """

    def __init__(self, velkost_bloku: int, instancia_zaznamu : IData):
        """
        Inicializuje objekt Blok.
        """
        self.__instancia_zaznamu = instancia_zaznamu
        self.__velkost_bloku = velkost_bloku
        self.__zaznamy : List[IData] = []
        self.__pocet_platnych_zaznamov = 0

    def get_velkost_bloku(self) -> int:
        """
        Vráti veľkosť bloku.
        """
        return self.__velkost_bloku

    def get_pocet_platnych_zaznamov(self) -> int:
        """
        Vráti počet platných záznamov v bloku.
        """
        return self.__pocet_platnych_zaznamov
    
    def get_zaznamy(self) -> List[IData]:
        """
        Vráti zoznam záznamov v bloku.
        """
        return self.__zaznamy
    
    def get_maximalny_pocet_zaznamov(self) -> int:
        """
        Vráti maximálny počet záznamov v bloku.
        """
        minimalna_velkost = 4
        velkost_zaznamu = self.__instancia_zaznamu.vrat_velkost()
        maximalny_pocet_zaznamov = (self.__velkost_bloku - minimalna_velkost) // velkost_zaznamu
        return maximalny_pocet_zaznamov
    
    def vymaz_zaznamy(self):
        """
        Vymaže všetky záznamy v bloku.
        """
        self.__zaznamy = []
        self.__pocet_platnych_zaznamov = 0
        
    
    def vrat_velkost(self) -> int:
        """
        Vráti veľkosť bloku v bajtoch.
        """
        if self.__zaznamy:
            return 4 + len(self.__zaznamy) * self.__instancia_zaznamu.vrat_velkost()
        else:
            return 4
        
    
    def na_byte_array(self) -> bytearray:
        """
        Konvertuje objekt na byte array.
        """
        byte_array = bytearray()
        byte_array += self.__pocet_platnych_zaznamov.to_bytes(4, byteorder='big')
        for zaznam in self.__zaznamy:
            byte_array += zaznam.na_byte_array()
        pocet_doplnenych_bytov = self.__velkost_bloku - self.vrat_velkost()

        for i in range(pocet_doplnenych_bytov):
            byte_array.append(0)

        return byte_array
    
    def z_byte_array(self, byte_array):
        """
        Konvertuje byte array na objekt.
        """
        aktualna_velkost = self.vrat_velkost()
        self.__pocet_platnych_zaznamov = int.from_bytes(byte_array[aktualna_velkost - 4:aktualna_velkost], byteorder='big')

        velkost_zaznamu = self.__instancia_zaznamu.vrat_velkost()
        

        while aktualna_velkost + velkost_zaznamu <= self.__velkost_bloku:
            nacitavany_zaznam = self.__instancia_zaznamu.klonuj()
            nacitavany_zaznam.z_byte_array(byte_array[aktualna_velkost: aktualna_velkost + velkost_zaznamu])
            self.__zaznamy.append(nacitavany_zaznam)
            aktualna_velkost += velkost_zaznamu


    def pridaj_zaznam(self, novy_zaznam : IData) -> bool:
        """
        Pridá záznam do bloku, ak je to možné.
        """
        if not self.__zaznamy:
            
            velkost_zaznamu = novy_zaznam.vrat_velkost()
            aktualna_velkost = self.vrat_velkost()

            if aktualna_velkost + velkost_zaznamu <= self.__velkost_bloku:
                self.__zaznamy.append(novy_zaznam)
                self.__pocet_platnych_zaznamov += 1
                aktualna_velkost += velkost_zaznamu
            
                while aktualna_velkost + velkost_zaznamu <= self.__velkost_bloku:
                    self.__zaznamy.append(novy_zaznam.klonuj())
                    aktualna_velkost += velkost_zaznamu

                return True

            else:
                return False

        else:
            klon = novy_zaznam.klonuj()
            for i in range (len(self.__zaznamy)):
                if self.__zaznamy[i] == klon:
                    self.__zaznamy[i] = novy_zaznam
                    self.__pocet_platnych_zaznamov += 1
                    return True
                
        return False
    
    def vrat_zaznam(self, hladany_zaznam) ->IData:
        """
        Vráti záznam na základe hľadaného záznamu.
        """
        for zaznam in self.__zaznamy:
            if zaznam == hladany_zaznam:
                return zaznam
            
        return None
    
    def aktualizuj_zaznam(self, novy_zaznam: IData) -> bool:
        """
        Aktualizuje záznam na základe nového záznamu.
        """
        for i in range(len(self.__zaznamy)):
            if self.__zaznamy[i] == novy_zaznam:
                self.__zaznamy[i] = novy_zaznam
                return True

        return False

    def vymaz_zaznam(self, zaznam: IData) -> bool:
        """
        Vymaže záznam a následne posunie ostatné záznamy aby boli neplatné záznamy na konci.
        """
        for i in range(len(self.__zaznamy)):
            if self.__zaznamy[i] == zaznam:
                self.__zaznamy[i] = zaznam.klonuj()
                self.__pocet_platnych_zaznamov -= 1

                if i != len(self.__zaznamy) - 1:
                    klon = zaznam.klonuj()
                    
                    for j in range(i, len(self.__zaznamy)):
                        if j != len(self.__zaznamy) - 1:
                            self.__zaznamy[j] = self.__zaznamy[j + 1]
                        else:
                            self.__zaznamy[j] = klon

                return True
                    

        return False
    
    def ma_volne_zaznamy(self) -> bool:
        """
        Vráti True, ak blok má voľné záznamy.
        """
        return self.__pocet_platnych_zaznamov < self.get_maximalny_pocet_zaznamov()
    
    def to_string(self):
        """
        Vráti reprezentáciu objektu Blok ako string.
        """
        blok_na_string = ''
        blok_na_string += f'Pocet platnych zaznamov: {self.__pocet_platnych_zaznamov}/{self.get_maximalny_pocet_zaznamov()}\n'
        if self.__pocet_platnych_zaznamov > 0:
            blok_na_string += 'Zaznamy:\n'
            for i in range(len(self.__zaznamy)):
                if i < self.__pocet_platnych_zaznamov:
                    blok_na_string += self.__zaznamy[i].to_string()
                else:
                    blok_na_string += '|X| \n'
        else:
            blok_na_string += 'Blok neobsahuje ziadne zaznamy\n'
            
        return blok_na_string


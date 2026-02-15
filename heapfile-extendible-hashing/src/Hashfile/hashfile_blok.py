from Heapfile.blok import Blok
from Interface.interface import IHashData

class HashFileBlok(Blok):
    """
    Trieda HashFileBlok reprezentuje blok v pamäti s dĺžkou bloku a záznamami.
    Atribúty:
        __velkost_bloku (int): Veľkosť bloku.
        __instancia_zaznamu (IHashData): Inštancia záznamu.
        __zaznamy (List[IData]): Zoznam záznamov v bloku.
        __pocet_platnych_zaznamov (int): Počet platných záznamov v bloku.
    """

    def __init__(self, velkost_bloku, instancia_zaznamu: IHashData):
        """
        Inicializuje objekt HashFileBlok.
        """
        super().__init__(velkost_bloku, instancia_zaznamu) 
        
    
    
    
    
    

    
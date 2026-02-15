from interface.interface import PodporujeLogickeOperatory

class PoziciaGPS(PodporujeLogickeOperatory):
    """
    Trieda PoziciaGPS reprezentuje geografickú pozíciu ukladaním hodnôt zemepisnej šírky a dĺžky.
    Atribúty:
    __sirka (str): Zemepisná šírka ('N' pre severnú alebo 'S' pre južnú).
    __pozicia_sirky (float): Pozícia zemepisnej šírky v stupňoch.
    __dlzka (str): Zemepisná dĺžka ('E' pre východnú alebo 'W' pre západnú).
    __pozicia_dlzky (float): Pozícia zemepisnej dĺžky v stupňoch.
    """

    def __init__(self, sirka, pozicia_sirky, dlzka, pozicia_dlzky):
        """
        Inicializuje objekt PoziciaGPS.
        """
        self.set_sirka(sirka)
        self.set_dlzka(dlzka)
        self.set_pozicia_sirky(pozicia_sirky)
        self.set_pozicia_dlzky(pozicia_dlzky)

    # Gettery
    def get_sirka(self):
        return self.__sirka

    def get_pozicia_sirky(self):
        return self.__pozicia_sirky

    def get_dlzka(self):
        return self.__dlzka

    def get_pozicia_dlzky(self):
        return self.__pozicia_dlzky
    
    def get_suradnice(self):
        return (self.__pozicia_sirky, self.__pozicia_dlzky)

    # Settery
    def set_sirka(self, nastavovana_sirka):
        if nastavovana_sirka not in ('N', 'S'):
            raise ValueError('Nespravne zadany parameter pre sirku')
        self.__sirka = nastavovana_sirka

    def set_pozicia_sirky(self, nastavovana_pozicia):
        if nastavovana_pozicia < 0 or nastavovana_pozicia > 90:
            raise ValueError('Nespravne zadana pozicia pre sirku')
        
        if self.__sirka == 'N':
            self.__pozicia_sirky = nastavovana_pozicia
        else:
            self.__pozicia_sirky = -nastavovana_pozicia
        

    def set_dlzka(self, nastavovana_dlzka):
        if nastavovana_dlzka not in ('E', 'W'):
            raise ValueError('Nespravne zadany parameter pre dlzku')
        self.__dlzka = nastavovana_dlzka

    def set_pozicia_dlzky(self, nastavovana_pozicia):
        if nastavovana_pozicia < 0 or nastavovana_pozicia > 180:
            raise ValueError('Nespravne zadana pozicia pre dlzku')
        
        if self.__dlzka == 'E':
            self.__pozicia_dlzky = nastavovana_pozicia
        else:
            self.__pozicia_dlzky = -nastavovana_pozicia
        

    #Metody pre logicke porovnavanie
    def __le__(self, porovnavany):
        """
        Porovnáva, či je aktuálna pozícia menšia alebo rovná porovnávanej pozícii.
        """
        if self.__pozicia_sirky == porovnavany.get_pozicia_sirky():
            return self.__pozicia_dlzky <= porovnavany.get_pozicia_dlzky()
        else:
            return self.__pozicia_sirky <= porovnavany.get_pozicia_sirky()
        
    def __lt__(self, porovnavany):
        """
        Porovnáva, či je aktuálna pozícia menšia ako porovnávaná pozícia.
        """
        if self.__pozicia_sirky == porovnavany.get_pozicia_sirky():
            return self.__pozicia_dlzky < porovnavany.get_pozicia_dlzky()
        else:
            return self.__pozicia_sirky < porovnavany.get_pozicia_sirky()
    
    
    def __gt__(self, porovnavany):
        """
        Porovnáva, či je aktuálna pozícia väčšia ako porovnávaná pozícia.
        """
        if self.__pozicia_sirky == porovnavany.get_pozicia_sirky():
            return self.__pozicia_dlzky > porovnavany.get_pozicia_dlzky()
        else:
            return self.__pozicia_sirky > porovnavany.get_pozicia_sirky()
    
    def __eq__(self, porovnavany):
        """
        Porovnáva, či sú dve pozície rovnaké.
        """
        if self.__pozicia_sirky == porovnavany.get_pozicia_sirky():
            return self.__pozicia_dlzky == porovnavany.get_pozicia_dlzky()
        return False

    # Metódy na výpis
    def vypis(self):
        """
        Vypíše informácie o pozícii GPS.
        """
        print(f'PoziciaGPS ma atributy:\nSirka: {self.__sirka}\nPoziciaSirky: {self.__pozicia_sirky}'
              f'\nDlzka: {self.__dlzka}\nPoziciaDlzky: {self.__pozicia_dlzky}')
        
    def to_string(self):
        """
        Vráti reťazec reprezentujúci objekt PoziciaGPS.
        """
        return (f'S: {self.__pozicia_sirky} D: {self.__pozicia_dlzky}')
    
    def vypis_pre_csv(self):
        """
        Vráti reťazec pre CSV súbor.
        """
        return f'{self.__sirka};{abs(self.__pozicia_sirky)};{self.__dlzka};{abs(self.__pozicia_dlzky)}'
        


    


        
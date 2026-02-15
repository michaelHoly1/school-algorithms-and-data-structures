from interface.interface import PodporujeRovnost


class TestovacieData(PodporujeRovnost):

    """
    Trieda TestovacieData implementuje rozhranie PodporujeRovnost a slúži na uchovávanie a manipuláciu testovacích dát.
    Atribúty:
    __primarny_kluc (str): Primárny kľúč identifikujúci objekt o veľkosti 10 znakov.
    __x (int): X-ová súradnica - číslo od 1 - 50.
    __y (int): Y-ová súradnica - číslo od 1 - 50.
    """

    def __init__(self, string, x, y):
        """
        Inicializuje objekt s daným primárnym kľúčom, x a y súradnicami.
        """
        self.__primarny_kluc = string
        self.__x = x
        self.__y = y

    def __eq__(self, porovnavany):
        """
        Porovnáva dva objekty na základe ich primárneho kľúča.
        """
        return self.__primarny_kluc == porovnavany.get_primarny_kluc()
    
    def get_primarny_kluc(self):
        """
        Vráti primárny kľúč objektu.
        """
        return self.__primarny_kluc
    
    def get_x(self):
        """
        Vráti x-ovú súradnicu objektu.
        """
        return self.__x
    
    def get_y(self):
        """
        Vráti y-ovú súradnicu objektu.
        """
        return self.__y
    
    def get_suradnice(self):
        """
        Vráti súradnice objektu ako dvojicu (x, y).
        """
        return (self.__x, self.__y)
    
    def set_primarny_kluc(self, string):
        """
        Nastaví nový primárny kľúč objektu.
        """
        self.__primarny_kluc = string

    def set_x(self, x):
        """
        Nastaví novú x-ovú súradnicu objektu.
        """
        self.__x = x

    def set_y(self, y):
        """
        Nastaví novú y-ovú súradnicu objektu.
        """
        self.__y = y

    
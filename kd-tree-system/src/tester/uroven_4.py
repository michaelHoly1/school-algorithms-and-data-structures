from interface.interface import PodporujeLogickeOperatory

class Uroven4(PodporujeLogickeOperatory):
    """
    Trieda Uroven4, ktorá podporuje logické operátory.
    Atribúty:
    __atribut_string (str): Reťazcový atribút.
    __atribut_integer (int): Celý číselný atribút.
    """

    def __init__(self, string, integer):
        """
        Inicializuje objekt Uroven4 s reťazcom a celým číslom.
        """
        self.__atribut_string = string
        self.__atribut_integer = integer

    def get_atribut_string(self):
        return self.__atribut_string
    
    def get_atribut_integer(self):
        return self.__atribut_integer
    
    def set_atribut_string(self, string):
        self.__atribut_string = string

    def set_atribut_integer(self, integer):
        self.__atribut_integer = integer

    def __eq__(self, porovnavany):
        """
        Skontroluje, či sú dva objekty Uroven4 rovnaké na základe ich atribútov.
        """
        if self.__atribut_string == porovnavany.get_atribut_string():
            return self.__atribut_integer == porovnavany.get_atribut_integer()
        else:
            return False
        
    def __lt__(self, porovnavany):
        """
        Skontroluje, či je aktuálny objekt Uroven4 menší ako iný na základe ich atribútov.
        """
        if self.__atribut_string == porovnavany.get_atribut_string():
            return self.__atribut_integer < porovnavany.get_atribut_integer()
        else:
            return self.__atribut_string < porovnavany.get_atribut_string()
        
    def __gt__(self, porovnavany):
        """
        Skontroluje, či je aktuálny objekt Uroven4 väčší ako iný na základe ich atribútov.
        """
        if self.__atribut_string == porovnavany.get_atribut_string():
            return self.__atribut_integer > porovnavany.get_atribut_integer()
        else:
            return self.__atribut_string > porovnavany.get_atribut_string()
        
    def __le__(self, porovnavany):
        """
        Skontroluje, či je aktuálny objekt Uroven4 menší alebo rovný ako iný na základe ich atribútov.
        """
        if self.__atribut_string == porovnavany.get_atribut_string():
            return self.__atribut_integer <= porovnavany.get_atribut_integer()
        else:
            return self.__atribut_string <= porovnavany.get_atribut_string()
        
    def toString(self):
        """
        Vráti reťazcovú reprezentáciu objektu Uroven4.
        """
        return f"Uroven4: {self.__atribut_string}, {self.__atribut_integer}"

    


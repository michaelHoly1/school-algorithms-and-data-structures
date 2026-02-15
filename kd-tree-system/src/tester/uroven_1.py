from interface.interface import PodporujeLogickeOperatory


class Uroven1(PodporujeLogickeOperatory):
    """
    Trieda Uroven1, ktorá podporuje logické operátory implementovaním príslušného interfac-u.
    Atribúty:
        __atribut_double (float): Atribút typu float.
        __atribut_string (str): Atribút typu string.
        __epsilon (float): Malá hodnota používaná na porovnanie dátových typov float a double.
    """
    
    def __init__(self, double, string):
        """
        Inicializuje objekt Uroven1 s double a string.
        """
        self.__atribut_double = double
        self.__atribut_string = string
        self.__epsilon = 1e-7

    def get_atribut_double(self):
        return self.__atribut_double
    
    def get_atribut_string(self):
        return self.__atribut_string
    
    def set_atribut_double(self, double):
        self.__atribut_double = double

    def set_atribut_string(self, string):
        self.__atribut_string = string

    def __eq__(self, porovnavany):
        """
        Skontroluje, či je aktuálny objekt rovný porovnávanému objektu.
        """
        if abs(self.__atribut_double - porovnavany.get_atribut_double()) < self.__epsilon:
            return self.__atribut_string == porovnavany.get_atribut_string()
        else:
            return False
        
    def __lt__(self, porovnavany):
        """
        Skontroluje, či je aktuálny objekt menší ako porovnávaný objekt.
        """  
        if abs(self.__atribut_double - porovnavany.get_atribut_double()) < self.__epsilon:
            return self.__atribut_string < porovnavany.get_atribut_string()
        else:
            return self.__atribut_double < porovnavany.get_atribut_double()
        
    def __gt__(self, porovnavany):
        """
        Skontroluje, či je aktuálny objekt väčší ako porovnávaný objekt.
        """
        if abs(self.__atribut_double - porovnavany.get_atribut_double()) < self.__epsilon:
            return self.__atribut_string > porovnavany.get_atribut_string()
        else:
            return self.__atribut_double > porovnavany.get_atribut_double()
        
    def __le__(self, porovnavany):
        """
        Skontroluje, či je aktuálny objekt menší alebo rovný porovnávanému objektu.
        """
        if abs(self.__atribut_double - porovnavany.get_atribut_double()) < self.__epsilon:
            return self.__atribut_string <= porovnavany.get_atribut_string()
        else:
            return self.__atribut_double <= porovnavany.get_atribut_double()
        
    def toString(self):
        """
        Vráti reťazcovú reprezentáciu objektu.
        """
        return f"Uroven1: {self.__atribut_double}, {self.__atribut_string}"


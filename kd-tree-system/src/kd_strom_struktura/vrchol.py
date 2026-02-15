from interface.interface import PodporujeRovnost, PodporujeLogickeOperatory
from collections.abc import Iterable

class Vrchol:
    """
    Trieda Vrchol predstavuje uzol v dátovej štruktúre stromu.
    Atribúty:
    __data: Dáta uložené vo vrchole.
    __kluce: Kľúče spojené s vrcholom.
    __uroven: Úroveň vrcholu v strome.
    __otec: Referencia na rodičovský vrchol.
    __lavy_syn: Referencia na ľavého syna.
    __pravy_syn: Referencia na pravého syna.
    """

    def __init__(self, data, kluce):
        """
        Inicializuje vrchol s danými dátami a kľúčmi.
        """
        
        #ak sú dáta napr. samostatny objekt a nie su iterovatelne
        if not isinstance(data, Iterable):

            if type(data) not in (int, float, bool, str, bytes, tuple, list, dict, set, frozenset, complex):
                if not isinstance(data, PodporujeRovnost):
                    raise TypeError('Data musia podporovat logicky operator ==')
        else:
        #ak su iterovatelne, znamena to ze ich mozeme prechadzat napr. ako zoznam
            for objekt in data:
                if type(objekt) not in (int, float, bool, str, bytes, tuple, list, dict, set, frozenset, complex):
                    if not isinstance(objekt, PodporujeRovnost):
                        raise TypeError('Data musia podporovat logicky operator ==')

        if not isinstance(kluce, Iterable):
            raise TypeError('Kluce musia byt iterovatelne')
        else:
            for kluc in kluce:
                if type(kluc) not in (int, float, bool, str, bytes, tuple, list, dict, set, frozenset, complex):
                    if not isinstance(kluc, PodporujeLogickeOperatory):
                        raise TypeError('Kluce musia podporovat logicke operatory <=, <, > a ==')
                
        self.__data = data
        self.__kluce = kluce
        self.__uroven = 0
        self.__otec = None 
        self.__lavy_syn = None
        self.__pravy_syn = None

    # Gettery
    def get_data(self):
        return self.__data

    def get_kluce(self):
        return self.__kluce
    
    def get_uroven(self):
        return self.__uroven

    def get_otec(self):
        return self.__otec

    def get_lavy_syn(self):
        return self.__lavy_syn

    def get_pravy_syn(self):
        return self.__pravy_syn

    # Settery
    def set_data(self, data):
        self.__data = data

    def set_kluce(self, kluce):
        self.__kluce = kluce

    def set_uroven(self, uroven):
        self.__uroven = uroven

    def set_otec(self, otec):
        self.__otec = otec

    def set_lavy_syn(self, lavy_syn):
        self.__lavy_syn = lavy_syn

    def set_pravy_syn(self, pravy_syn):
        self.__pravy_syn = pravy_syn

    def nastav_syna(self, povodny_syn, novy_syn):
        if self.__lavy_syn == povodny_syn:
            self.__lavy_syn = novy_syn
        elif self.__pravy_syn == povodny_syn:
            self.__pravy_syn = novy_syn

    def vymaz_syna(self, vymazavany_syn):
        if self.__lavy_syn == vymazavany_syn:
            self.__lavy_syn = None
        elif self.__pravy_syn == vymazavany_syn:
            self.__pravy_syn = None

    def vymen_pozicie_vrcholov(self, vrchol):
        """
        Vymení pozície dvoch vrcholov.
        """
        povodna_uroven = vrchol.get_uroven()
        povodny_otec = vrchol.get_otec()
        povodny_lavy_syn = vrchol.get_lavy_syn()
        povodny_pravy_syn = vrchol.get_pravy_syn()

        # nastavenie nahradneho vrcholu na poziciu vymazavaneho vrcholu
        if self.__otec is not None:
            self.__otec.nastav_syna(self, vrchol)
        vrchol.set_uroven(self.__uroven)
        vrchol.set_otec(self.__otec)
        if self.__lavy_syn is vrchol:
            vrchol.set_lavy_syn(self)
        else:
            vrchol.set_lavy_syn(self.__lavy_syn)

        if self.__pravy_syn is vrchol:
            vrchol.set_pravy_syn(self)
        else:
            vrchol.set_pravy_syn(self.__pravy_syn)

        if self.__lavy_syn is not None and self.__lavy_syn is not vrchol:
            self.__lavy_syn.set_otec(vrchol)
        if self.__pravy_syn is not None and self.__pravy_syn is not vrchol:
            self.__pravy_syn.set_otec(vrchol)

        # nastavenie vymazavaneho vrcholu na poziciu nahradneho vrcholu
        if povodny_otec is self:
            self.set_otec(vrchol)
        else:
            self.set_otec(povodny_otec)
            if povodny_otec is not None:
                povodny_otec.nastav_syna(vrchol, self)
        self.set_uroven(povodna_uroven)
        self.set_lavy_syn(povodny_lavy_syn)
        self.set_pravy_syn(povodny_pravy_syn)

        if povodny_lavy_syn is not None:
            povodny_lavy_syn.set_otec(self)
        if povodny_pravy_syn is not None:
            povodny_pravy_syn.set_otec(self)




    def vrchol_je_list(self):
        """
        Skontroluje, či je vrchol list, to je vtedy, pokiaľ nemá žiadnych synov.
        """
        if self.__lavy_syn == None and self.__pravy_syn == None:
            return True
        else:
            return False
        




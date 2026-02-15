from Tester.tester import GeneratorOperacii


def main():
    
    
    generator = GeneratorOperacii("Subory/testovanie",3453)  #Zaznamy v: Heap - 1147; Hash_ECV - 15; Hash_ID - 8
    generator.generuj_operacie(5000) 
    

if __name__ == "__main__":
    main()
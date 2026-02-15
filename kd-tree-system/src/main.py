from tester.generator_operacii import GeneratorOperacii

def main():
    
    generator = GeneratorOperacii(20000, 2)
    generator.generuj_nahodne_operacie()
    #for i in range(100):
        #generator.generuj_vkladanie()
    
    #generator.test() 
    

if __name__ == "__main__":
    main()
    



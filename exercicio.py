# classe joia

class Joia:
    def __init__(self,nome, preco, quilate,pedra):
        self.nome = nome
        self.__preco = preco
        self.__quilate = quilate
        self.pedra = pedra

    def __str__(self):
        return f"joia: {self.nome},preco: {self.__preco},quilate: {self.__quilate},pedra: {self.pedra}"


joia1= Joia("colar",  "15000.00", "23K", "rubi")
print(joia1)


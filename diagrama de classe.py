from datetime import date

class historico:
    def __init__(self):
        self.transacoes = []

    def adicionar_transacao(self, transacao):
        self.transacoes.append(transacao)

    def extrato(self):
        if not self.transacoes:
            return "historico vazio"
        return "\n".join(
            f"{i} - {t}" for i, t in enumerate(self.transacoes, start=1)
        )

    def __str__(self):
        return self.extrato()


class transacao:
    def registrar(self, conta):
        raise NotImplementedError("implemente este metodo nas subclasses")


class deposito(transacao):
    def __init__(self, valor):
        self.valor = valor

    def registrar(self, conta):
        ok = conta.depositar(self.valor)
        if ok:
            conta.historico.adicionar_transacao(self)
        return ok

    def __str__(self):
        return f"deposito de {self.valor:.2f}"


class saque(transacao):
    def __init__(self, valor):
        self.valor = valor

    def registrar(self, conta):
        ok = conta.sacar(self.valor)
        if ok:
            conta.historico.adicionar_transacao(self)
        return ok

    def __str__(self):
        return f"saque de {self.valor:.2f}"


class conta:
    def __init__(self, cliente, numero, agencia):
        self._saldo = 0.0
        self.numero = numero
        self.agencia = agencia
        self.cliente = cliente
        self.historico = historico()

    def saldo(self):
        return self._saldo

    @classmethod
    def nova_conta(cls, cliente, numero, agencia):
        return cls(cliente, numero, agencia)

    def sacar(self, valor):
        if valor <= self._saldo:
            self._saldo -= valor
            return True
        return False

    def depositar(self, valor):
        if valor > 0:
            self._saldo += valor
            return True
        return False

    def __str__(self):
        return f"conta {self.numero}-{self.agencia}, saldo: {self._saldo:.2f}"


class contacorrente(conta):
    def __init__(self, cliente, numero, agencia, limite, limite_saques):
        super().__init__(cliente, numero, agencia)
        self.limite = limite
        self.limite_saques = limite_saques

    def sacar(self, valor):
        if valor <= (self._saldo + self.limite):
            self._saldo -= valor
            return True
        return False

    def __str__(self):
        return f"conta corrente {self.numero}-{self.agencia}, saldo: {self._saldo:.2f}, limite: {self.limite}, limite saques: {self.limite_saques}"


class cliente:
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []

    def realizar_transacao(self, conta, transacao):
        return transacao.registrar(conta)

    def adicionar_conta(self, conta):
        self.contas.append(conta)

    def __str__(self):
        return f"cliente (endereco: {self.endereco}, contas: {len(self.contas)})"


class pessoafisica(cliente):
    def __init__(self, cpf, nome, data_nascimento, endereco):
        super().__init__(endereco)
        self.cpf = cpf
        self.nome = nome
        self.data_nascimento = data_nascimento

    def __str__(self):
        return f"pessoa fisica: {self.nome}, cpf: {self.cpf}, nasc: {self.data_nascimento}, endereco: {self.endereco}, contas: {len(self.contas)}"


# exemplo de uso
c1 = pessoafisica("12345678900", "ana", date(2000, 5, 20), "rua a, 123")
cc = contacorrente(c1, 1, "0001", limite=500.0, limite_saques=3)
c1.adicionar_conta(cc)

print(c1)
print(cc)

d1 = deposito(1000)
c1.realizar_transacao(cc, d1)

s1 = saque(200)
c1.realizar_transacao(cc, s1)

print(cc)
print("historico:")
print(cc.historico)

from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Session
from sqlalchemy import Column
from sqlalchemy import func
from sqlalchemy import select
from sqlalchemy import create_engine
from sqlalchemy import inspect
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Float
from sqlalchemy import ForeignKey

Base = declarative_base()



# Gerando tabelas
class Cliente(Base):
    __tablename__ = "cliente"

    # atributos
    id = Column(Integer, primary_key=True)
    nome = Column(String)
    cpf = Column(String(9))
    endereco = Column(String(9))

    # Estabelecendo relacao id_conta com id_cliente
    conta = relationship(
        "Conta", back_populates="cliente", cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"Cliente(id={self.id}, name={self.nome}, cpf={self.cpf}, endereco={self.endereco})"


class Conta(Base):
     __tablename__ = "conta"

     #atributos
     id = Column(Integer, primary_key=True)
     tipo = Column(String)
     agencia = Column(String)
     num = Column(Integer)
     id_cliente = Column(Integer, ForeignKey("cliente.id"), nullable=False)
     saldo = Column(Float)

     # Estabelecendo relacao id_conta com id_cliente
     cliente = relationship(
         "Cliente", back_populates="conta"
     )

     def __repr__(self):
         return f"Conta(id={self.id}, tipo={self.tipo}, agencia={self.agencia}, num={self.num}, saldo={self.saldo}"



# criando conexao com base de dados
engine = create_engine("sqlite://")

# criando as classes e as tabelas dentro da base de dados
Base.metadata.create_all(engine)

# criando metodos

def existe_cpf(cpf):
    existe = select(Cliente).where(Cliente.cpf.in_(cpf))
    for cliente in Session(engine).scalars(existe):
        return True

    return False

def adicionar_conta():
    print("=-=-=-=-= Criando uma nova conta =-=-=-=-=")
    nome = str(input("Digite seu nome: "))
    cpf = str(input("Digite seu CPF: "))
    endereco = str(input("Digite seu endereco: "))
    return Cliente(nome=nome, cpf=cpf, endereco=endereco)
    if not existe_cpf([cpf]):
        endereco = str(input("Digite seu endereco: "))
        cliente = Cliente(nome=nome, cpf=cpf, endereco=endereco)
        adicionar_conta_db(cliente)
        return cliente
    else:
        print("CPF já cadastrado!\n\n")
        return None


def adicionar_conta_db(cliente):
    with Session(engine) as session:
        session.add(cliente)
        session.commit()
        session.close()

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
    name = Column(String)
    cpf = Column(String(9))
    endereco = Column(String(9))

    def __repr__(self):
        return f"Cliente(id={self.id}, name={self.name}, cpf={self.cpf}, endereco={self.endereco})"


    #Estabelecendo relacao id_conta com id_cliente
    conta = relationship(
        "Conta", back_populates="cliente", cascade="all, delete-orphan"
    )

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

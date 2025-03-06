from sqlalchemy import ForeignKey, Column, Integer, String, MetaData, Table
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base

convention = {
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
}
metadata = MetaData(naming_convention=convention)

Base = declarative_base(metadata=metadata)

dev_company = Table(
    'dev_companies',
    Base.metadata,
    Column('dev_id', ForeignKey('devs.id'), primary_key=True),
    Column('company_id', ForeignKey('companies.id'), primary_key=True),
    extend_existing=True,
)

class Company(Base):
    __tablename__ = 'companies'

    id = Column(Integer(), primary_key=True)
    name = Column(String())
    founding_year = Column(Integer())
    devs = relationship('Dev', secondary=dev_company, backref=backref('companies', lazy='dynamic'))
    freebies = relationship('Freebie', backref='company')

    def __repr__(self):
        return f'<Company {self.name}>'

    def give_freebie(self, dev, item_name, value):
        freebie = Freebie(item_name=item_name, value=value, dev=dev, company=self)
        return freebie
    
    @classmethod
    def oldest_company(cls, session):
        return session.query(cls).order_by(cls.founding_year).first()

class Dev(Base):
    __tablename__ = 'devs'

    id = Column(Integer(), primary_key=True)
    name = Column(String())
    freebies = relationship('Freebie', backref='dev')

    def __repr__(self):
        return f'<Dev {self.name}>'

    def received_one(self, item_name):
        return any(freebie.item_name == item_name for freebie in self.freebies)

    def give_away(self, dev, freebie):
        if freebie in self.freebies:
            freebie.dev = dev
            return True
        return False

class Freebie(Base):
    __tablename__ = 'freebies'
    id = Column(Integer(), primary_key=True)
    item_name = Column(String(), nullable=False)
    value = Column(Integer)
    dev_id = Column(Integer(), ForeignKey('devs.id'))
    company_id = Column(Integer(), ForeignKey('companies.id'))

    def print_details(self):
        return f"{self.dev.name} owns a {self.item_name} from {self.company.name}"

    def __repr__(self):
        return f"Freebie {self.id}: item_name={self.item_name}, value={self.value}"

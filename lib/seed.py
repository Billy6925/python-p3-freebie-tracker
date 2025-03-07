from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base,Dev,Company,Freebie
from faker import Faker
import random

engine = create_engine('sqlite:///freebies.db')
Session = sessionmaker(bind =engine)
session = Session()

faker = Faker()

#clear existing records
session.query(Dev).delete()
session.query(Company).delete()
session.query(Freebie).delete()
session.commit()


def seed_data():
    companies =[]
    devs = []
    freebies =[]

#create companies
    for i in range(10):
        company = Company(name = faker.company(), founding_year =faker.year())
        session.add(company)
        companies.append(company)

#create devs
    for i in range(50):
        dev = Dev(name = faker.name())
        session.add(dev)
        devs.append(dev)

#create freebies and set relationships
    for i in range (50):
        dev = random.choice(devs)
        company = random.choice(companies)
        freebie = Freebie(
            item_name = faker.name(),
            value = random.randint(0,100),
            dev =dev,#set the dev relationship
            company =company #set the company relationship
        )
        session.add(freebie)
        freebies.append(freebie)
    session.commit()

if __name__ == '__main__':
    seed_data()
    print('Seed data generated successfully...')

#Use ipdb for debugging
import ipdb; ipdb.set_trace()
    

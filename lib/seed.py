from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from faker import Faker
from models import Base, Dev, Company, Freebie
import random

engine = create_engine('sqlite:///freebies.db')
Session = sessionmaker(bind=engine)
session = Session()

faker = Faker()

print("Seeding data...")

def seed_data():
    # Clear existing records
    session.query(Freebie).delete()
    session.query(Dev).delete()
    session.query(Company).delete()
    session.commit()

    companies = []
    devs = []
    freebies = []

    # Create companies
    for i in range(10):
        company = Company(name=faker.company(), founding_year=faker.year())
        session.add(company)
        companies.append(company)

    # Create developers
    for i in range(50):
        dev = Dev(name=faker.name())
        session.add(dev)
        devs.append(dev)

    # Create freebies and set relationships
    for i in range(50):
        dev = random.choice(devs)
        company = random.choice(companies)
        freebie = Freebie(
            item_name=faker.name(),
            value=random.randint(0, 100),
            dev=dev,  # Set the dev relationship
            company=company  # Set the company relationship
        )
        session.add(freebie)
        freebies.append(freebie)

    session.commit()
    print("Seed data generated successfully!")

if __name__ == '__main__':
    seed_data()

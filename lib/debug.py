#!/usr/bin/env python3

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base,Company, Dev,Freebie
from seed import seed_data

if __name__ == '__main__':
    engine = create_engine('sqlite:///freebies.db')
    Session = sessionmaker(bind= engine)
    session = Session()

    #seed the database with the seed data
    seed_data()

    import ipdb; ipdb.set_trace()

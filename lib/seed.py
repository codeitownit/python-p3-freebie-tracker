#!/usr/bin/env python3

from faker import Faker
import random

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import Company, Dev, Freebie

if __name__ == '__main__':
    engine = create_engine('sqlite:///freebies.db')
    Session = sessionmaker(bind=engine)
    session = Session()

    session.query(Company).delete()
    session.query(Dev).delete()
    session.query(Freebie).delete()

    fake = Faker()

    items = ['T-shirt','hoodie', 'usb drive',
                 'charger', 'notebooks', 'caps']
    companies = []
    for i in range(50):
        company = Company(
            name=fake.company(),
            founding_year= fake.year(),
        )

        # add and commit individually to get IDs back
        session.add(company)
        session.commit()

        companies.append(company)


    devs = []
    for i in range(25):
        dev = Dev(
            name=fake.name(),
        )

        session.add(dev)
        session.commit()

        devs.append(dev)


    freebies = []
    for company in companies:
        for i in range(random.randint(1,5)):
            dev = random.choice(devs)
            if company not in dev.companies:
                dev.companies.append(company)
                session.add(dev)
                session.commit()
            
            freebie = Freebie(
                item_name=random.choice(items),
                value=random.randint(0, 10),
                company_id=company.id,
                dev_id=dev.id,
            )

            freebies.append(freebie)

    session.bulk_save_objects(freebies)
    session.commit()
    session.close()

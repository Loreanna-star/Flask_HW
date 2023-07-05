from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


engine = create_engine('postgresql://app:1234@127.0.0.1:5434/app')
Session = sessionmaker(bind=engine)
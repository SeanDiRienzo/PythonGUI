#Author Sean Di Rienzo
from PyQt5.QtCore import *
from PyQt5.QtSql import QSqlDatabase, QSqlTableModel

import pandas as pd
import numpy as np

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///canadianCheeseDirectory.sqlite', echo=True)
Base = declarative_base(engine)


def loadSession():
    Session = sessionmaker(bind=engine)
    session = Session()
    return session


class CheeseRecord:
    db_name = 'canadianCheeseDirectory.sqlite'
    working_table = 'cheeseData'

    def __init__(self):
        self.connection = engine.connect()
        self.session = loadSession()
        self.create_working_table()
        self.model = SQLTableModel()

    def create_working_table(self):
        """Create database table from csv file using declarative relational model base"""
        Base.metadata.create_all(engine)
        df = pd.read_csv("canadianCheeseDirectory.csv")
        df = df.replace(np.nan, '', regex=True)
        self.session.query(Record).delete()
        self.session.commit()
        for _, row in df.iterrows():
            record = Record(cheese_id=row["CheeseId"], cheese_name=row["CheeseNameEn"],
                            manuf_name_en=row["ManufacturerNameEn"],
                            manuf_prov_code=row["ManufacturerProvCode"], manuf_type=row["ManufacturingTypeEn"],
                            website=row["WebSiteEn"], fat_content=row["FatContentPercent"],
                            moisture=row["MoisturePercent"],
                            particularities=row["ParticularitiesEn"], flavour=row["FlavourEn"],
                            characteristics=row["CharacteristicsEn"], ripening=row["RipeningEn"],
                            organic=row["Organic"],
                            category=row["CategoryTypeEn"], milk=row["MilkTypeEn"],
                            milk_treatment=row["MilkTreatmentTypeEn"],
                            rind=row["RindTypeEn"], last_update=row["LastUpdateDate"])
            self.session.add(record)

        self.session.commit()


class Record(Base):
    """declarative base class for a database Record"""
    __tablename__ = "cheeseData"

    cheese_id = Column('CheeseId', Integer, primary_key=True)
    cheese_name = Column('CheeseNameEn', String)
    manuf_name_en = Column('ManufacturerNameEn', String)
    manuf_prov_code = Column('ManufacturerProvCode', String)
    manuf_type = Column('ManufacturingTypeEn', String)
    website = Column('WebSiteEn', String)
    fat_content = Column('FatContentPercent', String)
    moisture = Column('MoisturePercent', String)
    particularities = Column('ParticularitiesEn', String)
    flavour = Column('FlavourEn', String)
    characteristics = Column('CharacteristicsEn', String)
    ripening = Column('RipeningEn', String)
    organic = Column('Organic', String)
    category = Column('CategoryTypeEn', String)
    milk = Column('MilkTypeEn', String)
    milk_treatment = Column('MilkTreatmentTypeEn', String)
    rind = Column('RindTypeEn', String)
    last_update = Column('LastUpdateDate', String)

    def __init__(self, cheese_id, cheese_name, manuf_name_en, manuf_prov_code, manuf_type, website, fat_content,
                 moisture,
                 particularities, flavour, characteristics, ripening, organic, category, milk, milk_treatment, rind,
                 last_update):
        self.cheese_id = cheese_id
        self.cheese_name = str(cheese_name)
        self.manuf_name_en = str(manuf_name_en)
        self.manuf_prov_code = str(manuf_prov_code)
        self.manuf_type = str(manuf_type)
        self.website = str(website)
        self.fat_content = str(fat_content)
        self.moisture = str(moisture)
        self.particularities = str(particularities)
        self.flavour = str(flavour)
        self.characteristics = str(characteristics)
        self.ripening = str(ripening)
        self.organic = str(organic)
        self.category = str(category)
        self.milk = str(milk)
        self.milk_treatment = str(milk_treatment)
        self.rind = str(rind)
        self.last_update = str(last_update)


class SQLTableModel:
    """Class to create SQl model for model view controller"""

    def __init__(self):
        self.db = QSqlDatabase.addDatabase("QSQLITE")
        self.db.setDatabaseName("canadianCheeseDirectory.sqlite")
        self.db.open()
        self.model = QSqlTableModel()
        self.initializedModel()
        while self.model.canFetchMore():
            self.model.fetchMore()

    def initializedModel(self):
        """initialize the model to the database table we created"""
        self.model.setTable("cheeseData")
        self.model.setEditStrategy(QSqlTableModel.OnFieldChange)
        self.model.select()



    def closeEvent(self, event):
        self.db.close()

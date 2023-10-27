# External libraries
from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Laptop(Base):
    __tablename__ = 'laptops'

    id: int = Column(Integer, primary_key=True, autoincrement=True)
    manufacturer: str = Column(String)
    size: str = Column(String)
    resolution: str = Column(String)
    type: str = Column(String)
    touchscreen: bool = Column(String)
    processor_name: str = Column(String)
    physical_cores:int = Column(String)
    clock_speed: int = Column(String)
    ram: str = Column(String)
    storage: str = Column(String)
    disc_type: str = Column(String)
    graphic_card_name: str = Column(String)
    graphic_card_memory: str = Column(String)
    operating_system: str = Column(String)
    disc_reader: str = Column(String)
    
    @classmethod
    def add_table_to_db(cls, engine) -> None:
        cls.metadata.create_all(engine)
    
    @classmethod
    def get_all(cls, session) -> list:
        return [i.to_dict() for i in session.query(cls).all()]
    
    @classmethod
    def delete(cls, session) -> None:
        session.query(cls).delete()
        session.commit()
    
    def add(self, session) -> None:
        session.add(self)
        session.commit()
    
    def update(self, session, data: dict) -> None:
        for name, value in data.items():
            setattr(self, name, value)
        session.commit()
        
    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'manufacturer': self.manufacturer,
            'size': self.size,
            'resolution': self.resolution,
            'type': self.type, 
            'touchscreen': self.touchscreen,
            'processor_name': self.processor_name,
            'physical_cores': self.physical_cores,
            'clock_speed': self.clock_speed,
            'ram' : self.ram,
            'storage' : self.storage,
            'disc_type' : self.disc_type,
            'graphic_card_name' : self.graphic_card_name,
            'graphic_card_memory' : self.graphic_card_memory,
            'operating_system' : self.operating_system,
            'disc_reader' : self.disc_reader,
        }
        
    def __repr__(self) -> str:
        return f'Laptop(id: {self.id}, manufacturer: {self.manufacturer}, \
            size: {self.size}, resolution: {self.resolution}, type: {self.type}, \
            touchscreen: {self.touchscreen}, processor_name: {self.processor_name}, \
            physical_cores: {self.physical_cores}, clock_speed: {self.clock_speed}, \
            ram: {self.ram}, storage: {self.storage}, disk_type: {self.disc_type}, \
            graphic_card_name: {self.graphic_card_name}, graphic_card_memory: {self.graphic_card_memory}, \
            operating_system: {self.operating_system}, disk_reader: {self.disc_reader})'
# External libraries
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import xml.etree.ElementTree as ET
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QBrush, QColor
from PyQt5.QtWidgets import QApplication, QMainWindow, \
                            QFileDialog, QTableWidget, \
                            QTableWidgetItem, QPushButton, \
                            QStyleFactory, QLabel, QMessageBox

# Internal libraries
from desk_app.const_vars import COLUMN_NAMES, APP_TITLE, BUTTON_STYLE
from desk_app.models import Laptop

class FileManager(QMainWindow):
    red = QColor(255, 0, 0)
    gray = QColor(169, 169, 169)
    white = QColor(255, 255, 255)
    
    def __init__(self) -> None:
        super().__init__()
        self.configure_db() # Create database
        self.initUI() # Create window with components
        self.resize_column_width()
        self.message = QMessageBox()
        self.duplicates = []
        
    def configure_db(self) -> None:
        # DB creation
        engine = create_engine('sqlite:///mydatabase.db')  # Replace with your database URI
        Session = sessionmaker(bind=engine)
        self.session = Session()
        
        # Create the "Laptops" table in the database
        Laptop.add_table_to_db(engine)   
        
    def initUI(self) -> None:
        "Base display of window and its components"
        
        # Set style
        QApplication.setStyle(QStyleFactory.create('Fusion'))
        
        # Main app window
        self.setGeometry(100, 100, 1150, 550)
        self.setWindowTitle(APP_TITLE)

        # Table
        self.table = QTableWidget(self)
        self.table.setGeometry(50, 60, 1350, 500)
        self.table.setColumnCount(len(COLUMN_NAMES))
        
        self.table.setHorizontalHeaderLabels(COLUMN_NAMES)
        
        # Label for displaying information
        self.info_label = QLabel('Liczba nowych rekordów: 0, Liczba duplikatów: 0', self)
        self.info_label.setGeometry(50, 20, 400, 20)

        # Buttons - add
        load_txt_btn = QPushButton('Dodaj dane z pliku .txt', self)
        load_txt_btn.setGeometry(50, 600, 200, 40)
        load_txt_btn.clicked.connect(self.load_txt_file)
        load_txt_btn.setStyleSheet(BUTTON_STYLE)

        load_xml_btn = QPushButton('Dodaj dane z pliku .xml', self)
        load_xml_btn.setGeometry(280, 600, 200, 40)
        load_xml_btn.clicked.connect(self.load_xml_file)
        load_xml_btn.setStyleSheet(BUTTON_STYLE)

        # Buttons - save
        save_txt_btn = QPushButton('Zapisz do pliku .txt', self)
        save_txt_btn.setGeometry(510, 600, 200, 40)
        save_txt_btn.clicked.connect(self.save_txt_file)
        save_txt_btn.setStyleSheet(BUTTON_STYLE)

        save_xml_btn = QPushButton('Zapisz do pliku .xml', self)
        save_xml_btn.setGeometry(740, 600, 200, 40)
        save_xml_btn.clicked.connect(self.save_xml_file)
        save_xml_btn.setStyleSheet(BUTTON_STYLE)
        
        # Buttons - import and export to database
        import_db_btn = QPushButton('Importuj z bazy danych', self)
        import_db_btn.setGeometry(970, 600, 200, 40)
        import_db_btn.clicked.connect(self.import_data_from_db)
        import_db_btn.setStyleSheet(BUTTON_STYLE)
        
        export_db_btn = QPushButton('Eksportuj do bazy danych', self)
        export_db_btn.setGeometry(1200, 600, 200, 40)
        export_db_btn.clicked.connect(self.export_to_database)
        export_db_btn.setStyleSheet(BUTTON_STYLE)

        # Dict data structure to keep data from files
        self.data = {}
        
        # Safe current table
        self.get_current_table()
        
        # If element changed start cellChanged function
        self.table.itemChanged.connect(self.cellChanged)
        
    def update_label(self, new_records: int) -> None:
        self.info_label.setText(f'Liczba nowych rekordów: {new_records}, Liczba duplikatów: {len(self.duplicates)}')
        
    def get_old_table(self):
        old_table = []
        for row in range(self.table.rowCount()):
            temp = []
            for col in range(self.table.columnCount()):
                value = self.get_item(row, col) # Get value
                temp.append(value) # add value to the temp list
            old_table.append(temp[1:]) # Without id 
        return old_table
    
    def resize_column_width(self) -> None: 
        self.table.resizeColumnsToContents()
        for col in range(self.table.columnCount()):
            self.table.setColumnWidth(col, self.table.columnWidth(col) + 40)  # Dodatkowy margines dla tekstu
        
        # self.table.setColumnWidth(0, 0)
        
    def load_txt_file(self) -> None:
        "Function to handle loading data from .txt into the table"
        self.button_clicked = True
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, 'Wczytaj plik TXT', '', 'Pliki TXT (*.txt);;Wszystkie pliki (*)', options=options)
        if file_name:
            with open(file_name, 'r') as file:
                lines = file.readlines()
                # Empty the data structure
                self.data = {}
                # For each line in file
                for i, line in enumerate(lines):
                    # delete enters
                    line = line.replace(';\n', '')
                    # Split data by ';'
                    self.data[i] = line.split(';')
                # Put prepared data to the table
                self.display_data()
        self.button_clicked = False
                
    def save_txt_file(self) -> None:
        "Function to handle saving data to .txt from the table"
        
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getSaveFileName(self, 'Zapisz do pliku TXT', '', 'Pliki TXT (*.txt);;Wszystkie pliki (*)', options=options)
        if file_name:
            with open(file_name, 'w') as file:
                # For each row
                for row in range(self.table.rowCount()):
                    # For each column
                    for col in range(1, len(COLUMN_NAMES)+1):
                        # Get value item as <PyQt5.QtWidgets.QTableWidgetItem object ...>
                        value_item = self.table.item(row, col)
                        # Get its true value
                        if value_item:
                            value = value_item.text()
                        else:
                            value = ''
                        # Add it into the new file with ';' in the end
                        file.write(value + ';')
                    # In the end of the row add enter
                    file.write('\n')

    def load_xml_file(self) -> None:
        "Function handles loading data from .xml file into the table"
        
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, 'Wczytaj plik XML', '', 'Pliki XML (*.xml);;Wszystkie pliki (*)', options=options)
        if file_name:
            # Passing the path of the file
            tree = ET.parse(file_name)
            # getting the parent tag
            root = tree.getroot()
            # Empty the data structure
            self.data = {}
            # For each laptop in xml file
            for i, laptop in enumerate(root.findall('laptop')):
                
                screen = laptop.find('screen') # get screen info
                processor = laptop.find('processor') # get processor info
                disc = laptop.find('disc') # get disc into
                graphic_card = laptop.find('graphic_card') # get graphic card info

                # Put info into the data structure
                self.data[i] = [
                    # Producent
                    laptop.find('manufacturer').text if laptop.find('manufacturer') != None else '',
                    # Wielkość matrycy
                    screen.find('size').text if screen.find('size') != None else '', 
                    # Rozdzielczość
                    screen.find('resolution').text if screen.find('resolution') != None else '', 
                    # Typ matrycy
                    screen.find('type').text if screen.find('type') != None else '', 
                    # Czy dotykowy ekran 
                    screen.find('touchscreen').text if screen.find('touchscreen') != None else '',
                    # Procesor 
                    processor.find('name').text if processor.find('name') != None else '', 
                    # Liczba rdzeni fizycznych
                    processor.find('physical_cores').text if processor.find('physical_cores') != None else '', 
                    # Taktowanie
                    processor.find('clock_speed').text if processor.find('physical_cores') != None else '', 
                    # RAM
                    laptop.find('ram').text if laptop.find('ram') != None else '', 
                    # Pojemność dysku
                    disc.find('storage').text if disc.find('storage') != None else '', 
                    # Typ dysku
                    disc.find('type').text if disc.find('type') != None else '', 
                    # Karta graficzna
                    graphic_card.find('name').text if graphic_card.find('name') != None else '', 
                    # Pamięć karty graficznej
                    graphic_card.find('memory').text if graphic_card.find('memory') != None else '', 
                    # System operacyjny
                    laptop.find('os').text if laptop.find('os') != None else '', 
                    # Napęd optyczny
                    laptop.find('disc_reader').text if laptop.find('disc_reader') != None else '', 
                ]
                
            self.display_data()

    def save_xml_file(self) -> None:
        "Function handles saving data to the .xml file from the table"
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getSaveFileName(self, 'Zapisz do pliku XML', '', 'Pliki XML (*.xml);;Wszystkie pliki (*)', options=options)
        
        if file_name:
            root = ET.Element('laptops')
            for row in range(self.table.rowCount()):
                
                laptop = ET.SubElement(root, 'laptop')      
                ET.SubElement(laptop, 'manufacturer').text = self.get_item(row, 1) # Producent
                
                screen = ET.SubElement(laptop, 'screen')
                ET.SubElement(screen, 'size').text = self.get_item(row, 2) # Wielkość matrycy
                ET.SubElement(screen, 'resolution').text = self.get_item(row, 3) # Rozdzielczość
                ET.SubElement(screen, 'type').text = self.get_item(row, 4) # Typ matrycy
                ET.SubElement(screen, 'touchscreen').text = self.get_item(row, 5) # Czy dotykowy ekran 
                
                processor = ET.SubElement(laptop, 'processor')
                ET.SubElement(processor, 'name').text = self.get_item(row, 6) # Procesor
                ET.SubElement(processor, 'physical_cores').text = self.get_item(row, 7) # Liczba rdzeni fizycznych
                ET.SubElement(processor, 'clock_speed').text = self.get_item(row, 8) # Taktowanie
                
                ET.SubElement(laptop, 'ram').text = self.get_item(row, 9) # RAM
                
                disc = ET.SubElement(laptop, 'disc')
                ET.SubElement(disc, 'storage').text = self.get_item(row, 10) # Pojemność dysku
                ET.SubElement(disc, 'type').text = self.get_item(row, 11) # Typ dysku
                
                graphic_card = ET.SubElement(laptop, 'graphic_card')
                ET.SubElement(graphic_card, 'name').text = self.get_item(row, 12)
                ET.SubElement(graphic_card, 'memory').text = self.get_item(row, 13)
                
                ET.SubElement(laptop, 'os').text =  self.get_item(row, 14)
                ET.SubElement(laptop, 'disc_reader').text = self.get_item(row, 15)
                
            tree = ET.ElementTree(root)
            tree.write(file_name)
            
    def cellChanged(self, item):
        if not self.button_clicked:
            if item:
                row = item.row()
                column = item.column()
            
                element = self.current_table[row][column]
                if element != item.text():
                    for col in range(self.table.columnCount()):
                        el = self.table.item(row, col)
                        if el:
                            el.setBackground(self.white)
            
    def get_item(self, row: int, col: int) -> str:
        item = self.table.item(row, col)
        if item: 
            return item.text()
        return item
    
    def export_to_database(self) -> None:
        "Function to handle loading data from .txt into the table"

        for row in range(self.table.rowCount()):
            # Id from table
            id_item = self.get_item(row, 0)
            # Do not duplicate
            if row not in self.duplicates and not id_item:
                laptop = Laptop(
                    manufacturer = self.get_item(row, 1),
                    size = self.get_item(row, 2),
                    resolution = self.get_item(row, 3),
                    type = self.get_item(row, 4),
                    touchscreen = self.get_item(row, 5),
                    processor_name = self.get_item(row, 6),
                    physical_cores = self.get_item(row, 7),
                    clock_speed = self.get_item(row, 8),
                    ram = self.get_item(row, 9),
                    storage = self.get_item(row, 10),
                    disc_type = self.get_item(row, 11),
                    graphic_card_name = self.get_item(row, 12),
                    graphic_card_memory = self.get_item(row, 13),
                    operating_system = self.get_item(row, 14),
                    disc_reader = self.get_item(row, 15),
                )
                
                laptop.add(self.session)
        
    def showInfoMessage(self, message: str) -> None:
        # Ustawienie tytułu i tekstu alertu
        self.message.setWindowTitle("Alert!")
        self.message.setText(message)
        # Wyświetlenie alertu (bez możliwości wyboru)
        self.message.show()
    
    def get_current_table(self) -> dict:
        self.current_table = {}
        for row in range(self.table.rowCount()):
            values = []
            for col in range(self.table.columnCount()):
                item = self.table.item(row, col)
                if item:
                    values.append(item.text())
                else:
                    values.append('')  # or any default value if the cell is empty
            self.current_table[row] = values
    
    def import_data_from_db(self) -> None:
        "Function to handle displaying data"
        
        self.button_clicked = True
        
        # Get data from db
        laptops = Laptop.get_all(self.session)
        laptops_len = len(laptops)
        if laptops_len == 0:
            self.showInfoMessage('Baza danych jest pusta.')
        else:
            # Number of existing rows
            curr_count = self.table.rowCount()
            # Set cols and rows
            self.table.setRowCount(laptops_len+curr_count)
            # Get current table
            old_table = self.get_old_table()
            
            # For pairs in the self.data
            for row, laptop in enumerate(laptops):
                # Get each laptop values
                values = laptop.values()
                is_duplicate = False
                for col, val in enumerate(values):
                    # Put each value into the table
                    value = str(val) if val else ''
                    self.table.setItem(row+curr_count, col, QTableWidgetItem(value))
                    # If values exists color red
                    item = self.table.item(row+curr_count, col)
                    # If duplicate - color red else gray
                    if list(values)[1:] in old_table: 
                        item.setBackground(QBrush(self.red))
                        is_duplicate = True
                    else: 
                        item.setBackground(QBrush(self.gray))
                if is_duplicate:
                    self.duplicates.append(row+curr_count)
                
            # Safe current table
            self.get_current_table()
            # Wyświetl poprawiony label
            self.update_label(laptops_len)
            # Wyrównaj kolumny
            self.table.resizeColumnsToContents()
        self.button_clicked = False
        
    def display_data(self) -> None:
        "Function to handle displaying data"
        
        # Number of existing rows
        curr_count = self.table.rowCount()
        # Get current table
        old_table = self.get_old_table()
        # Set row count
        self.table.setRowCount(len(self.data)+curr_count)
        
        if len(self.data) == 0:
            self.showInfoMessage('Nie ma niczego do dodania.')
        
        # For pairs in the self.data
        for row, values in self.data.items():
            # For each value from the list in data.values() (with its id)
            self.table.setItem(row, 0, None)
            is_duplicate = False
            for col, val in enumerate(values):
                # Display value in the right place in the table
                value = str(val) if val else ''
                item = self.table.setItem(row+curr_count, col+1, QTableWidgetItem(value))
                # If values exists color red
                item = self.table.item(row+curr_count, col+1)
                # If duplicate - color red else gray
                if list(values) in old_table: 
                    item.setBackground(QBrush(self.red))
                    is_duplicate = True
                else: 
                    item.setBackground(QBrush(self.gray))
            if is_duplicate:
                self.duplicates.append(row+curr_count)
                
        # Safe current table
        self.get_current_table()
        # Wyświetl poprawiony label
        self.update_label(len(self.data))
        # Wyrównaj kolumny
        self.table.resizeColumnsToContents()
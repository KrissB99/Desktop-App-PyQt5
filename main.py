# External libraries
import sys
import xml.etree.ElementTree as ET
from PyQt5.QtWidgets import QApplication, QMainWindow, \
                            QFileDialog, QTableWidget, \
                            QTableWidgetItem, QPushButton, \
                            QStyleFactory

# Internal libraries
from const_vars import COLUMN_NAMES, APP_TITLE, BUTTON_GEOMETRY

class FileManager(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.initUI()
        
    def initUI(self) -> None:
        "Base display of window and its components"
        
        # Set style
        QApplication.setStyle(QStyleFactory.create('Fusion'))
        
        # Main app window
        self.setGeometry(100, 100, 800, 600)
        self.setWindowTitle(APP_TITLE)

        # Table
        self.table = QTableWidget(self)
        self.table.setGeometry(50, 50, 700, 400)
        self.table.setColumnCount(len(COLUMN_NAMES))
        
        self.table.setHorizontalHeaderLabels(COLUMN_NAMES)

        # Buttons - upload
        load_txt_btn = QPushButton('Wczytaj plik .txt', self)
        load_txt_btn.setGeometry(50, BUTTON_GEOMETRY['ay'], BUTTON_GEOMETRY['aw'], BUTTON_GEOMETRY['ah'])
        load_txt_btn.clicked.connect(self.load_txt_file)

        load_xml_btn = QPushButton('Wczytaj plik .xml', self)
        load_xml_btn.setGeometry(220, BUTTON_GEOMETRY['ay'], BUTTON_GEOMETRY['aw'], BUTTON_GEOMETRY['ah'])
        load_xml_btn.clicked.connect(self.load_xml_file)

        # Buttons - save
        save_txt_btn = QPushButton('Zapisz do pliku .txt', self)
        save_txt_btn.setGeometry(390, BUTTON_GEOMETRY['ay'], BUTTON_GEOMETRY['aw'], BUTTON_GEOMETRY['ah'])
        save_txt_btn.clicked.connect(self.save_txt_file)

        save_xml_btn = QPushButton('Zapisz do pliku .xml', self)
        save_xml_btn.setGeometry(560, BUTTON_GEOMETRY['ay'], BUTTON_GEOMETRY['aw'], BUTTON_GEOMETRY['ah'])
        save_xml_btn.clicked.connect(self.save_xml_file)

        # Dict data structure to keep data from files
        self.data = {}  

    def load_txt_file(self) -> None:
        "Function to handle loading data from .txt into the table"
        
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
                
    def save_txt_file(self) -> None:
        "Function to handle saving data to .txt from the table"
        
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getSaveFileName(self, 'Zapisz do pliku TXT', '', 'Pliki TXT (*.txt);;Wszystkie pliki (*)', options=options)
        if file_name:
            with open(file_name, 'w') as file:
                # For each row
                for row in range(self.table.rowCount()):
                    # For each column
                    for col in range(len(COLUMN_NAMES)):
                        # Get value item as <PyQt5.QtWidgets.QTableWidgetItem object ...>
                        value_item = self.table.item(row, col)
                        # Get its true value
                        value = value_item.text()
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
                ET.SubElement(laptop, 'manufacturer').text = self.table.item(row, 0).text() # Producent
                
                screen = ET.SubElement(laptop, 'screen')
                ET.SubElement(screen, 'size').text = self.table.item(row, 1).text() # Wielkość matrycy
                ET.SubElement(screen, 'resolution').text = self.table.item(row, 2).text() # Rozdzielczość
                ET.SubElement(screen, 'type').text = self.table.item(row, 3).text() # Typ matrycy
                ET.SubElement(screen, 'touchscreen').text = self.table.item(row, 4).text() # Czy dotykowy ekran 
                
                processor = ET.SubElement(laptop, 'processor')
                ET.SubElement(processor, 'name').text = self.table.item(row, 5).text() # Procesor
                ET.SubElement(processor, 'physical_cores').text = self.table.item(row, 6).text() # Liczba rdzeni fizycznych
                ET.SubElement(processor, 'clock_speed').text = self.table.item(row, 7).text() # Taktowanie
                
                ET.SubElement(laptop, 'ram').text = self.table.item(row, 8).text() # RAM
                
                disc = ET.SubElement(laptop, 'disc')
                ET.SubElement(disc, 'storage').text = self.table.item(row, 9).text() # Pojemność dysku
                ET.SubElement(disc, 'type').text = self.table.item(row, 10).text() # Typ dysku
                
                graphic_card = ET.SubElement(laptop, 'graphic_card')
                ET.SubElement(graphic_card, 'name').text = self.table.item(row, 11).text()
                ET.SubElement(graphic_card, 'memory').text = self.table.item(row, 12).text()
                
                ET.SubElement(laptop, 'os').text =  self.table.item(row, 13).text()
                ET.SubElement(laptop, 'disc_reader').text = self.table.item(row, 14).text()
                
            tree = ET.ElementTree(root)
            tree.write(file_name)

    def display_data(self) -> None:
        "Function to handle displaying data"
        
        self.table.setRowCount(len(self.data))
        # For pairs in the self.data
        for key, values in self.data.items():
            # For each value from the list in data.values() (with its id)
            for i, val in enumerate(values):
                # Display value in the right place in the table
                self.table.setItem(key, i, QTableWidgetItem(val))
  
if __name__ == '__main__':
    # Create application
    app = QApplication(sys.argv)
    # Create a window
    window = FileManager()
    # Show window
    window.show()
    sys.exit(app.exec_())
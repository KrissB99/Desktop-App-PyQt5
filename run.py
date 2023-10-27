# External libraries
import sys
from PyQt5.QtWidgets import QApplication

# Internal libraries 
from desk_app.main import FileManager

app = QApplication(sys.argv)
window = FileManager()

window.show()
sys.exit(app.exec_())
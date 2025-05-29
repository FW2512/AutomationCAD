from utils.json_loader import layers_config, beams_data, columns_data
from core.layer_manager import setup_layers
from core.beams import draw_beam_outline

def main():
    """The main runner function
    """
    
    # Layer Manager
    setup_layers(layers_config)
    
    # Beams Manager
    # draw_beam_outline(beams_data,layer_name="0")
    

"""
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel
from utils.messenger import Messenger, MultiMessenger
from gui.message_handler import QtMessenger
from utils.file_messager import FileMessenger

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("AutoCAD Beam Tool")

        # Set up status bar
        self.status = self.statusBar()
        self.status_label = QLabel("")
        self.status.addPermanentWidget(self.status_label)

        # Set Messenger handler
        Messenger.set_handler(
            MultiMessenger(
                QtMessenger(self.update_status),
                FileMessenger("logs/app.log)
            )
        )

        # Test the setup
        Messenger.send("Application started", level="info")

    def update_status(self, msg):
        self.status_label.setText(msg)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())

"""







    
if __name__ == "__main__":
    main()
   
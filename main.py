import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QHBoxLayout, QVBoxLayout, QPushButton, QLineEdit, QFileDialog
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
from PIL.Image import open as iopen
import pyzbar.pyzbar as pyzbar


class Interface(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(150, 150, 450, 500)
        self.setMinimumSize(450, 500)
        self.setMaximumSize(450, 500)
        self.setWindowTitle('Library Student Storage System')

        # Create layout for squares
        hbox1 = QHBoxLayout()
        hbox2 = QHBoxLayout()

        barcodes = ["147258369", "741852963", "789456123", "987654321"]

        # Create 4 squares with red circles and number 1
        for (i, Id) in zip(range(4), barcodes):
            # Create square label
            square = QLabel(self)
            square.setObjectName(f"square_{i}")
            square.setAlignment(Qt.AlignCenter)
            square.setFixedSize(200, 200)
            square.setStyleSheet('background-color: white; border: 1px solid black;')
            font = QFont()
            font.setPointSize(60)
            square.setFont(font)
            square.setText(str(i+1))

            # Create red circle label
            circle = QLabel(self)
            circle.setObjectName(Id)
            circle.setFixedSize(20, 20)
            circle.setStyleSheet('background-color: green; border-radius: 10px;')

            # Add circle to top-right of square
            vbox = QVBoxLayout()
            vbox.addWidget(circle)
            vbox.setAlignment(Qt.AlignTop | Qt.AlignRight)
            vbox.setContentsMargins(0, 10, 10, 0)  # right margin to separate from border
            square.setLayout(vbox)

            # Add square to layout
            if i < 2:
                hbox1.addWidget(square)
            else:
                hbox2.addWidget(square)

        # Create vertical layout for the two horizontal layouts
        vbox_squares = QVBoxLayout()
        vbox_squares.addLayout(hbox1)
        vbox_squares.addLayout(hbox2)

        # Add scan button and entry box
        scan_button = QPushButton('Scan', self)
        scan_button.setStyleSheet('background-color: green; color: white')
        scan_button.clicked.connect(self.on_press_scan)
        read_button = QPushButton('Read', self)
        read_button.setStyleSheet('background-color: green; color: white')
        read_button.clicked.connect(self.on_press_read)
        entry_box = QLineEdit(self)
        entry_box.setObjectName("entry_box")
        entry_box.setPlaceholderText("Enter barcode number")

        # Create horizontal layout for buttons
        hbox_buttons = QHBoxLayout()
        hbox_buttons.addWidget(scan_button)
        hbox_buttons.addWidget(read_button)

        # Create vertical layout for buttons and entry box
        vbox_bottom = QVBoxLayout()
        vbox_bottom.addLayout(hbox_buttons)
        vbox_bottom.addWidget(entry_box)

        # Add all layouts to main layout
        main_layout = QVBoxLayout()
        main_layout.addLayout(vbox_squares)
        main_layout.addLayout(vbox_bottom)
        self.setLayout(main_layout)
        self.show()

    def on_press_read(self):
        # Locate entry box
        entry = self.findChild(QLineEdit, "entry_box")

        # Locate label with the barcode address
        label = self.findChild(QLabel, entry.text())

        # invalid entry handling
        if not label:
            return

        # Change color of signal
        if "green" in label.styleSheet():
            label.setStyleSheet('background-color: red; border-radius: 10px;')
        else:
            label.setStyleSheet('background-color: green; border-radius: 10px;')

    def on_press_scan(self):
        # Open fileDialog to pick image
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(
            self, "Select Image", "", "Images (*.png *.xpm *.jpg *.bmp *.gif *.jpeg *.svg *.webp);;All Files (*)"
        )

        # invalid entry handling
        if fileName == "":
            return

        # Create reader object
        image = iopen(fileName)

        # Decode the barcode in the image
        barcodes = pyzbar.decode(image)

        # Locate label with the barcode address
        label = self.findChild(QLabel, barcodes[0].data.decode('utf-8'))

        # invalid entry handling
        if not label:
            return

        # Change color of signal
        if "green" in label.styleSheet():
            label.setStyleSheet('background-color: red; border-radius: 10px;')
        else:
            label.setStyleSheet('background-color: green; border-radius: 10px;')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    interface = Interface()
    sys.exit(app.exec_())

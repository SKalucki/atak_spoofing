import sys
from time import sleep

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter, QPixmap, QIcon, QDoubleValidator, QIntValidator, QFont
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QVBoxLayout, QGroupBox, QGridLayout, \
    QDialog, QLineEdit, QMessageBox


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.background_image = QPixmap('stacja_empty.png')
        self.init_ui()
        self.welcome()
        mainLayout = QVBoxLayout()

        self.smallerWindow = QDialog(self)
        self.enterWindow = QDialog(self)
        self.smallerWindow.setWindowTitle('Wybór kanału')
        self.enterWindow.setWindowTitle('Wybór wartości')

        self.smallerWindowLayout = QVBoxLayout(self.smallerWindow)
        self.smallerWindowLayout.addWidget(self.welcomeBox)

        mainLayout.addWidget(self.smallerWindow)
        sleep(0.05)
        self.smallerWindow.show()
        self.enterWindow.finished.connect(self.openSmallerWindow)  # Connect accepted signal to openSmallerWindow

    def openSmallerWindow(self):
        if self.smallerWindow is not None:
            sleep(0.15)
            self.smallerWindow.show()

    def init_ui(self):
        self.setMinimumSize(953, 643)
        self.setWindowTitle('Atak na stację pogodową')
        self.setFixedSize(self.size())
        self.setWindowIcon(QIcon('weather.png'))
        self.show()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.drawPixmap(self.rect(), self.background_image)

    def handleButtonClick(self):

        clickedButton = app.sender()
        self.enterValues()

        self.enterWindowLayout = QVBoxLayout(self.enterWindow)
        self.enterWindowLayout.addWidget(self.enterV)

        if clickedButton == self.select_channel1:
            self.smallerWindow.close()
            self.channel_value = 1
            self.enterWindow.setStyleSheet("background-color: #36D173")
            self.enterWindow.show()

        elif clickedButton == self.select_channel2:
            self.smallerWindow.close()
            self.channel_value = 2
            self.enterWindow.setStyleSheet("background-color: #ffab00")
            self.enterWindow.show()

        elif clickedButton == self.select_channel3:
            self.smallerWindow.close()
            self.channel_value = 3
            self.enterWindow.setStyleSheet("background-color: #44BCE9")
            self.enterWindow.show()


    def welcome(self):
        global close
        close = 1

        self.welcomeBox = QGroupBox()
        self.welcomeBox.setStyleSheet("QGroupBox { border: none; }")
        info = QLabel("Wybierz kanał, na który chcesz wykonać atak Spoofing.")
        info.setStyleSheet("height: 70px; width: 500px; font-weight: bold")
        info.setFont(QFont("Didot", 25))
        info.setStyleSheet("color: black")

        self.select_channel1 = QPushButton("Kanał 1")
        self.select_channel1.setStyleSheet("QPushButton {height: 70px; width: 220px; background-color: white; "
                                           "border-radius: 8px; border: 1px solid black}"
                                           "QPushButton:hover {background-color: #36D173;}")

        self.select_channel1.setFont(QFont("Didot", 20))

        self.select_channel2 = QPushButton("Kanał 2")
        self.select_channel2.setStyleSheet("QPushButton {height: 70px; width: 260px; background-color: white; "
                                           "border-radius: 8px; border: 1px solid black}"
                                           "QPushButton:hover {background-color: #ffab00;}")
        self.select_channel2.setFont(QFont("Didot", 20))

        self.select_channel3 = QPushButton("Kanał 3")
        self.select_channel3.setStyleSheet("QPushButton {height: 70px; width: 260px; background-color: white; "
                                           "border-radius: 8px; border: 1px solid black}"
                                           "QPushButton:hover {background-color: #44BCE9;}")
        self.select_channel3.setFont(QFont("Didot", 20))
        self.select_channel1.setCursor(Qt.PointingHandCursor)
        self.select_channel2.setCursor(Qt.PointingHandCursor)
        self.select_channel3.setCursor(Qt.PointingHandCursor)

        layout = QGridLayout()
        topLayout = QVBoxLayout()
        topLayout.addWidget(info)
        layout.addLayout(topLayout, 0, 0, 1, 3)
        layout.addWidget(self.select_channel1, 1, 0)
        layout.addWidget(self.select_channel2, 1, 1)
        layout.addWidget(self.select_channel3, 1, 2)

        self.select_channel1.clicked.connect(self.handleButtonClick)
        self.select_channel2.clicked.connect(self.handleButtonClick)
        self.select_channel3.clicked.connect(self.handleButtonClick)

        self.welcomeBox.setLayout(layout)

    def enterValues(self):
        self.enterV = QGroupBox()
        self.enterV.setStyleSheet("QGroupBox { border: none; }")
        valuesLayout = QGridLayout()

        temperatureLabel = QLabel("Temperatura")
        temperatureLabel2 = QLabel("(-40" + u"\N{DEGREE SIGN}" + " - 70" + u"\N{DEGREE SIGN})")
        temperatureLabel.setWordWrap(True)
        self.temperature = QLineEdit()
        humidityLabel = QLabel("Wilgotność")
        humidityLabel2 = QLabel("(20% - 95%)")
        humidityLabel.setWordWrap(True)
        self.humidity = QLineEdit()

        temperature_validator = QDoubleValidator(-40.0, 70.0, 1)
        humidity_validator = QIntValidator(20, 95)

        self.temperature.setValidator(temperature_validator)
        self.humidity.setValidator(humidity_validator)

        self.temperature.setFixedWidth(200)
        self.humidity.setFixedWidth(200)

        temperatureLabel.setStyleSheet("height: 70px; width: 500px; font-weight: bold")
        self.temperature.setStyleSheet("height: 70px; width: 300px; background-color: white;"
                                       " border-radius: 8px; border: 1px solid black")
        humidityLabel.setStyleSheet("height: 70px; width: 500px; font-weight: bold")
        self.humidity.setStyleSheet("height: 70px; width: 300px; background-color: white;"
                                    " border-radius: 8px; border: 1px solid black")

        temperatureLabel.setFont(QFont("Didot", 25))
        temperatureLabel2.setFont(QFont("Didot", 18))
        self.temperature.setFont(QFont("Didot", 25))
        humidityLabel.setFont(QFont("Didot", 25))
        humidityLabel2.setFont(QFont("Didot", 18))
        self.humidity.setFont(QFont("Didot", 25))

        self.temperature.textChanged.connect(self.validate_temperature)
        self.humidity.textChanged.connect(self.validate_humidity)

        button = QPushButton("Wygeneruj sygnał")
        button.setStyleSheet("QPushButton {height: 70px; width: 260px; background-color: white; "
                                           "border-radius: 8px; border: 1px solid black}"
                                           "QPushButton:hover {background-color: #90c5e8;}")
        button.setCursor(Qt.PointingHandCursor)
        button.setFont(QFont("Didot", 20))
        button.clicked.connect(self.create_signal)

        valuesLayout.setVerticalSpacing(15)
        valuesLayout.setHorizontalSpacing(15)
        valuesLayout.addWidget(temperatureLabel, 0, 0)
        valuesLayout.addWidget(temperatureLabel2, 1, 0)
        valuesLayout.addWidget(self.temperature, 2, 0)
        valuesLayout.addWidget(humidityLabel, 0, 1)
        valuesLayout.addWidget(humidityLabel2, 1, 1)
        valuesLayout.addWidget(self.humidity, 2, 1)
        valuesLayout.addWidget(button, 3, 0, 1, 0)

        self.enterV.setLayout(valuesLayout)

    def validate_temperature(self):
        temperature = self.sender()
        if temperature.hasAcceptableInput():
            temperature.setStyleSheet("height: 70px; width: 250px; background-color: LightGreen; border-radius: 5px")
        else:
            temperature.setStyleSheet("height: 70px; width: 250px; background-color: LightCoral; border-radius: 5px")

    def validate_humidity(self):
        humidity = self.sender()
        if humidity.hasAcceptableInput():
            humidity.setStyleSheet("height: 70px; width: 250px; background-color: LightGreen; border-radius: 5px")
        else:
            humidity.setStyleSheet("height: 70px; width: 250px; background-color: LightCoral; border-radius: 5px")

    def advance_progress_bar(self):
        curVal = self.progressBar.value()
        maxVal = self.progressBar.maximum()
        self.progressBar.setValue(curVal + (maxVal - curVal) / 100)

    def create_signal(self):
        if self.temperature.text() == '' or self.humidity.text() == '':
            error_message = QMessageBox()
            error_message.setIcon(QMessageBox.Warning)
            error_message.setWindowTitle("Błąd")
            error_message.setText("Nie wprowadzono wszystkich wartości!")
            error_message.setStyleSheet("QLabel {font-family: 'GFS Didot'; font-size: 20px} QMessageBox {}")
            error_message.exec_()
        else:
            temperature = self.temperature.text()
            if (temperature[2:] != ",5" or temperature[2:] != ",0"):
                temperature = temperature.replace(",", ".")
                temperature = float(temperature)
                temperature = temperature + 0.05
            else:
                pass
            humidity = int(self.humidity.text())

            if(humidity == 95):
                humidity = humidity - 0.001
            if ((temperature < -40 or temperature > 70) and (humidity > 95 or humidity < 20)):
                error_message = QMessageBox()
                error_message.setIcon(QMessageBox.Warning)
                error_message.setWindowTitle("Błąd")
                error_message.setText("Wprowadzona temperatury i wilgotności jest nieprawidłowa!")
                error_message.setStyleSheet("QLabel {font-family: 'GFS Didot'; font-size: 20px} QMessageBox {}")
                error_message.exec_()
            elif (temperature < -40 or temperature > 70):
                error_message = QMessageBox()
                error_message.setIcon(QMessageBox.Warning)
                error_message.setWindowTitle("Błąd")
                error_message.setText('Wprowadzona temperatury jest nieprawidłowa!')
                error_message.setStyleSheet("QLabel {font-family: 'GFS Didot'; font-size: 20px} QMessageBox {}")
                error_message.exec_()
            elif (humidity > 95 or humidity < 20):
                error_message = QMessageBox()
                error_message.setIcon(QMessageBox.Warning)
                error_message.setWindowTitle("Błąd")
                error_message.setText("Wprowadzona wilgotności jest nieprawidłowa!")
                error_message.setStyleSheet("QLabel {font-family: 'GFS Didot'; font-size: 20px} QMessageBox {}")
                error_message.exec_()
            else:
                create_signal(generate_bin(float(temperature), float(humidity), int(self.channel_value)))
                message = QMessageBox()
                message.setIcon(QMessageBox.Information)
                message.setWindowTitle("Generowanie sygnału.")
                message.setText("Sygnał wygenerowany pomyślnie.")
                message.setStyleSheet("QLabel {font-family: 'GFS Didot'; font-size: 20px} QMessageBox {}")
                message.exec_()


def crc4(message, nBytes, polynomial, init):
    remainder = init << 4  # LSBs are unused
    poly = polynomial << 4

    while nBytes:
        remainder ^= message[0]
        message = message[1:]

        for bit in range(8):
            if remainder & 0x80:
                remainder = (remainder << 1) ^ poly
            else:
                remainder = (remainder << 1)
        nBytes -= 1

    return (remainder >> 4) & 0x0F  # discard the LSBs


def generate_crc(msg):
    crc = crc4(msg, 4, 0x13, 0)  # Koopmann 0x9, CCITT-4; FP-4; ITU-T G.704
    crc ^= msg[4] >> 4
    return crc


def calc_temp(temp_c):
    temp_f = (temp_c * 9 / 5) + 32
    temp_raw = (temp_f / 0.1) + 900
    return hex(int(temp_raw))


# postac heksadecymalna
def generate_bin(temp_c, humidity, channel):
    bajt1 = 155  # 1 id

    temp = calc_temp(temp_c)

    bajt3 = temp[0:4]
    # if humidity == 20 or humidity == 21:
    #     humidity = 22
    if len(str(humidity)) == 1:
        humidity = "0" + str(humidity)
    else:
        humidity = str(humidity)
    bajt4 = "0x" + temp[-1] + humidity[0]
    bajt5 = "0x" + humidity[1] + str(channel)
    bajt2 = hex(channel) + str(2)

    data = [bajt1, hex2dec(bajt2), hex2dec(bajt3), hex2dec(bajt4), hex2dec(bajt5)]
    crc = generate_crc(data)

    bajt2 = bajt2.replace(bajt2[2], hex(crc)[2:], 1)
    data_dec = [bajt1, hex2dec(bajt2), hex2dec(bajt3), hex2dec(bajt4), hex2dec(bajt5)]

    data_bin = ""
    for x in data_dec:
        data_add = decimal_to_binary(x)
        data_bin += data_add

    return data_bin


def hex2dec(val):
    dec = int(val, base=16)
    return dec


def decimal_to_binary(val):
    return format(val, '08b').replace("0b", "")


def create_signal(data_bin):
    with open("bit1.raw", "rb") as file_bit1:
        bit1 = file_bit1.read()

    with open("bit0.raw", "rb") as file_bit0:
        bit0 = file_bit0.read()

    with open("preambula.raw", "rb") as file_preambula:
        preambula = file_preambula.read()

    signal_out = preambula

    for bit in data_bin:
        if bit == "1":
            signal_out = signal_out + bit1
        elif bit == "0":
            signal_out = signal_out + bit0

    signal_out = signal_out + bit1

    with open("generated_signal.raw", "wb") as file_out:
        file_out.write(signal_out)


if __name__ == '__main__':
    try:
        app = QApplication(sys.argv)
        mainWindow = MainWindow()
        sys.exit(app.exec_())
    except Exception as e:
        print("Wystąpił błąd: ", str(e))

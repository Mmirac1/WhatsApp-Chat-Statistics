import sys
from PyQt5 import QtWidgets
from wpCalculater_UI import Ui_Form
from PyQt5.QtWidgets import QFileDialog
import calculate_function
from os.path import exists
from PyQt5.QtWidgets import QTableWidgetItem

class Window(QtWidgets.QMainWindow):
    def __init__(self):
        super(Window, self).__init__()

        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.path = None
        self.select_language()
        self.control()

        self.ui.cmb_language.currentIndexChanged.connect(self.select_language)
        self.ui.le_dosyaYolu.textChanged.connect(self.path_changed)
        self.ui.le_dosyaYolu.returnPressed.connect(self.button_click)
        self.ui.btn_ok.clicked.connect(self.button_click)
        #self.ui.btn_filter.clicked.connect(self.filter)
        self.ui.gitHub_link.clicked.connect(self.open_gitHub)

        

    def control(self):
        if self.path == None:   self.ui.btn_ok.setText(btn_file)
        else :   self.ui.btn_ok.setText(btn_ok)
         
    def button_click(self):
        if not self.path == None:
            if exists(self.path):
                result = calculate_function.calculate(self.path)
                if result == 'eror':
                    self.change_info(fileEror)
                    self.control()
                else:   self.show_result(result)
            else:
                self.change_info(pathEror)
                self.path = None
                self.control()
        else:   self.file_select()


    def change_info(self, bilgi):   self.ui.lbl_info.setText(bilgi)

    def show_result(self, result):
        from resultPage_UI import Ui_MainWindow
        self.result_window = QtWidgets.QMainWindow()
        self.result_ui = Ui_MainWindow()
        self.result_ui.setupUi(self.result_window)
        self.result_window.show()
        self.result_ui.tableWidget.setHorizontalHeaderItem(0, QTableWidgetItem(resultText_name))
        self.result_ui.tableWidget.setHorizontalHeaderItem(1, QTableWidgetItem(resultText_messages))
        self.result_ui.tableWidget.setHorizontalHeaderItem(2, QTableWidgetItem(resultText_words))

        self.result_ui.tableWidget.setRowCount(len(result))
        totalMessage, totalWord = 0, 0
        row_index = 0
        for i in result:
            self.result_ui.tableWidget.setItem(row_index, 0, QTableWidgetItem('  '+i))
            self.result_ui.tableWidget.setItem(row_index, 1, QTableWidgetItem(str(result[i]['messages'])))
            self.result_ui.tableWidget.setItem(row_index, 2, QTableWidgetItem(str(result[i]['words'])))
            totalMessage += result[i]['messages']
            totalWord += result[i]['words']
            row_index+=1

        self.result_ui.statusBar.showMessage(f"{totalText}:   {totalMessage} {messageText},  {totalWord} {wordText}")
        win.hide()


    def file_select(self):
        self.ui.lbl_info.setText(' ')
        self.ui.le_dosyaYolu.setText(QFileDialog.getOpenFileName(self, file_select_message,"C:/","Text Files (*.txt)")[0])
    def path_changed(self):
        if not self.ui.le_dosyaYolu.text() == '':   self.path = self.ui.le_dosyaYolu.text()
        else:   self.path = None 
        self.control()


    def filter(self):
        from filterPage_UI import Ui_Settings_page
        self.filter_window = QtWidgets.QMainWindow()
        self.filter_ui = Ui_Settings_page()
        self.filter_ui.setupUi(self.filter_window)
        self.filter_window.show()

        def filter_aply():
            time = self.filter_ui.time_start.time()
            timeSpec = self.filter_ui.time_start.timeSpec()
            print(time)
            print(time.toPyTime())
            print(time.hour())
            print(time.minute())
            


        self.filter_ui.rdb_allTime.setChecked(True)
        self.filter_ui.btn_aply.clicked.connect(filter_aply)



    def select_language(self):
        global btn_file, btn_ok, pathEror, fileEror, notPath, file_select_message, resultText_name, resultText_messages, resultText_words, totalText, messageText, wordText
        language = self.ui.cmb_language.currentIndex()    # 0 = English / 1 = Turkish
        if language == 1: 
            self.ui.txt_bilgilendirmeEN.hide()
            self.ui.txt_bilgilendirmeTR.show()
            self.ui.Title.setText('Whatsapp Mesaj Sayıcı')
            btn_file, btn_ok = "Dosya seç", "Tamam"
            pathEror, fileEror, notPath = 'Dosya konumunu hatalı! Tekrar deneyin.', 'Seçtiğiniz metin dosyası bir Whatsapp sohbet yedeği değil veya hatalı! Lütfen talimatları okuyunuz.', 'Bir Whatsapp sohbet yedeği seçmelisiniz. (Gerekirse talimatlara göz atın)'
            file_select_message = "Bir whatsapp sohbet yedeği seçin"
            resultText_name, resultText_messages, resultText_words, totalText, messageText, wordText= "İsim", "Mesajlar", "Kelimeler", "Toplam", "mesaj", "kelime"
        else:
            self.ui.txt_bilgilendirmeTR.hide()
            self.ui.txt_bilgilendirmeEN.show()
            self.ui.Title.setText('Whatsapp Message Counter')
            self.ui.btn_ok.setText('OK')
            btn_file, btn_ok = "Select file", "Ok"
            pathEror, fileEror, notPath = 'Incorrect file location! Try again.', 'The text file you selected is not a Whatsapp chat backup! Please read the instructions.', 'You must choose a Whatsapp chat backup. (read the instructions if needed)'
            file_select_message = "Choose whatsapp chat backup"
            resultText_name, resultText_messages, resultText_words, totalText, messageText, wordText = "Name", "Messages", "Words", "Total", "messages", "words"
        self.control()

    def open_gitHub(self):
        try:
            from webbrowser import open
            open('https://github.com/Mmirac1')
        except: pass



def application():
    global win
    app = QtWidgets.QApplication(sys.argv)
    win = Window()
    win.show()
    sys.exit(app.exec_())

application()
# ///////////////////////////////////////////////////////////////

import sys
import os
import platform

# IMPORT / GUI AND MODULES AND WIDGETS
# ///////////////////////////////////////////////////////////////
from modules import *
from widgets import *
from database import *

os.environ["QT_FONT_DPI"] = "96" # FIX Problem for High DPI and Scale above 100%

# SET AS GLOBAL WIDGETS
# ///////////////////////////////////////////////////////////////
widgets = None

class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)

        # SET AS GLOBAL WIDGETS
        # ///////////////////////////////////////////////////////////////
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        global widgets
        widgets = self.ui

        # USE CUSTOM TITLE BAR | USE AS "False" FOR MAC OR LINUX
        # ///////////////////////////////////////////////////////////////
        Settings.ENABLE_CUSTOM_TITLE_BAR = True

        # APP NAME
        # ///////////////////////////////////////////////////////////////
        title = "Sistema de RH"
        description = "Sistema de Gerenciamento - SRH"
        # APPLY TEXTS
        self.setWindowTitle(title)
        widgets.titleRightInfo.setText(description)

        # TOGGLE MENU
        # ///////////////////////////////////////////////////////////////
        widgets.toggleButton.clicked.connect(lambda: UIFunctions.toggleMenu(self, True))

        # SET UI DEFINITIONS
        # ///////////////////////////////////////////////////////////////
        UIFunctions.uiDefinitions(self)

        # QLineEdit PARAMETERS
        # ///////////////////////////////////////////////////////////////

        
        # QTableWidget PARAMETERS
        # ///////////////////////////////////////////////////////////////
        widgets.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        widgets.tableWidget.setHorizontalHeaderLabels(['ID', 'Nome', 'Setor', 'Salario', 'Email'])
        createConnection('database.db')
        query = QSqlQuery("SELECT id, name, setor, salary, email, chave FROM sistemarh") # Adicionar decriptografia
        while query.next():
            rows = widgets.tableWidget.rowCount()
            widgets.tableWidget.setRowCount(rows + 1)
            widgets.tableWidget.setItem(rows, 0, QTableWidgetItem(str(query.value(0))))
            widgets.tableWidget.setItem(rows, 1, QTableWidgetItem(query.value(1)))
            widgets.tableWidget.setItem(rows, 2, QTableWidgetItem(query.value(2)))
            widgets.tableWidget.setItem(rows, 3, QTableWidgetItem(f'R$ {(query.value(3))}'))
            tuple_email_chave = (query.value(4), query.value(5))
            emailQuery = AppFunctions.decodificar_dados(tuple_email_chave)
            emailValue, *chaveValue = emailQuery
            if emailValue[-1] == 'z':
                emailValueN = emailValue.replace(emailValue[-1], '')
                self.ui.tableWidget.setItem(rows, 4, QTableWidgetItem(emailValueN))
            else:
                self.ui.tableWidget.setItem(rows, 4, QTableWidgetItem(emailValue))
        widgets.tableWidget.setRowCount(rows + 5)
        widgets.tableWidget.resizeColumnsToContents()
        
        # BUTTONS CLICK
        # ///////////////////////////////////////////////////////////////

        # LEFT MENUS
        widgets.btn_home.clicked.connect(self.buttonClick)
        widgets.btn_funcionarios.clicked.connect(self.buttonClick)
        widgets.btn_salarioLiquido.clicked.connect(self.buttonClick)
        widgets.btn_feriasLiquida.clicked.connect(self.buttonClick)
        widgets.btn_decimoTerceiro.clicked.connect(self.buttonClick)
        widgets.btn_exit.clicked.connect(self.buttonClick)
        widgets.btn_addFuncionario.clicked.connect(self.buttonClick)
        widgets.btn_remFuncionario.clicked.connect(self.buttonClick)
        widgets.btn_calcSalarioLiquido.clicked.connect(self.buttonClick)
        widgets.btn_calcFeriasLiquida.clicked.connect(self.buttonClick)
        widgets.btn_calcDecimoTerceiro.clicked.connect(self.buttonClick)

        # EXTRA LEFT BOX
        #def openCloseLeftBox():
        #    UIFunctions.toggleLeftBox(self, True)
        #widgets.toggleLeftBox.clicked.connect(openCloseLeftBox)
        #widgets.extraCloseColumnBtn.clicked.connect(openCloseLeftBox)

        # EXTRA RIGHT BOX
        #def openCloseRightBox():
        #    UIFunctions.toggleRightBox(self, True)
        #widgets.settingsTopBtn.clicked.connect(openCloseRightBox)


        # SHOW APP
        # ///////////////////////////////////////////////////////////////
        self.show()

        # SET HOME PAGE AND SELECT MENU
        # ///////////////////////////////////////////////////////////////
        widgets.stackedWidget.setCurrentWidget(widgets.home)
        widgets.btn_home.setStyleSheet(UIFunctions.selectMenu(widgets.btn_home.styleSheet()))
    
    # BUTTONS CLICK
    # Post here your functions for clicked buttons
    # ///////////////////////////////////////////////////////////////
    def buttonClick(self):
        # GET BUTTON CLICKED
        btn = self.sender()
        btnName = btn.objectName()
        valueNull = 0

        # Funcionarios
        valueID = widgets.lineID.text()
        valueName = widgets.lineName.text()
        valueSetor = widgets.lineSetor.text()
        valueSalary = widgets.lineSalary.text()
        valueEmail = widgets.lineEmail.text()

        # Sal??rio L??quido
        valueSID = widgets.idInputS.text()
        valueSBonus = widgets.bonusInputS.text()

        # F??rias L??quida
        valueFID = widgets.idInputF.text()
        valueFBonus = widgets.bonusInputF.text()
        valueFerias = widgets.dFeriasInputF.text()

        # Decimo Terceiro
        valueDID = widgets.idInputD.text()
        valueDBonus = widgets.bonusInputD.text()
        valueMeses = widgets.mesesInputD.text()

        # SHOW HOME PAGE
        if btnName == "btn_home":
            widgets.stackedWidget.setCurrentWidget(widgets.home)
            UIFunctions.resetStyle(self, btnName)
            btn.setStyleSheet(UIFunctions.selectMenu(btn.styleSheet()))

        # SHOW FUNCIONARIOS PAGE
        if btnName == "btn_funcionarios":
            widgets.stackedWidget.setCurrentWidget(widgets.funcionarios)
            UIFunctions.resetStyle(self, btnName)
            btn.setStyleSheet(UIFunctions.selectMenu(btn.styleSheet()))

        # SHOW SALARIO LIQUIDO PAGE
        if btnName == "btn_salarioLiquido":
            widgets.stackedWidget.setCurrentWidget(widgets.salarioLiquido)
            UIFunctions.resetStyle(self, btnName)
            btn.setStyleSheet(UIFunctions.selectMenu(btn.styleSheet()))

        # SHOW FERIAS LIQUIDA PAGE
        if btnName == "btn_feriasLiquida":
            widgets.stackedWidget.setCurrentWidget(widgets.feriasLiquida)
            UIFunctions.resetStyle(self, btnName)
            btn.setStyleSheet(UIFunctions.selectMenu(btn.styleSheet()))

        # SHOW DECIMO TERCEIRO PAGE
        if btnName == "btn_decimoTerceiro":
            widgets.stackedWidget.setCurrentWidget(widgets.decimoTerceiro)
            UIFunctions.resetStyle(self, btnName)
            btn.setStyleSheet(UIFunctions.selectMenu(btn.styleSheet()))

        if btnName == "btn_addFuncionario":
            if (valueName == '' or valueSetor == '' or valueSalary == '' or valueEmail == ''):
                return widgets.resultAdd.setText("Todos os valores devem ser preenchidos.")
            else:
                if (AppFunctions.stringTest(valueName)):
                    if (AppFunctions.stringTest(valueSetor)):
                        if(AppFunctions.valueTest(valueSalary)):
                            if(AppFunctions.emailTest(valueEmail)):
                                genchave = AppFunctions.gerar_chave()
                                emailtuple = AppFunctions.encripta????o(valueEmail, genchave)
                                emailencripto, chaves = emailtuple
                                AppFunctions.addFuncionario(valueName, valueSetor, valueSalary, emailencripto)
                                AppFunctions.addChave(emailencripto, chaves)
                                AppFunctions.reloadTable(self)
                                return widgets.resultAdd.setText("Sucesso!")
                            else:
                                return widgets.resultAdd.setText("Erro no Email")
                        else:
                            return widgets.resultAdd.setText("Erro no Sal??rio")
                    else:
                        return widgets.resultAdd.setText("Erro no Setor")
                else:
                    return widgets.resultAdd.setText("Erro no Nome")

        if btnName == "btn_remFuncionario":
            if (AppFunctions.idTest(valueID)):
                AppFunctions.remFuncionario(valueID)
                AppFunctions.reloadTable(self)
                widgets.resultRem.setText("Funcion??rio removido com sucesso!")
            else:
                widgets.resultRem.setText("Erro ao tentar remover funcion??rio.")

        if btnName == "btn_calcSalarioLiquido":
            if widgets.bonusCheckS.isChecked():
                if (valueSID == '' or valueSBonus == ''):
                    return widgets.sucessLabelS.setText("Todos os valores devem ser preenchidos.")
                else:
                    if (AppFunctions.idTest(valueSID)):
                        if (AppFunctions.valueTest(valueSBonus)):
                            AppFunctions.calcSalaryL(self, valueSID, valueSBonus)
                            widgets.sucessLabelS.setText("C??lculo feito com sucesso!")
                        else:
                            widgets.sucessLabelS.setText("B??nus deve ser um n??mero v??lido.")
                    else:
                        widgets.sucessLabelS.setText("ID n??o encontrado ou inv??lido.")
            else:
                if (valueSID == ''):
                    return widgets.sucessLabelS.setText("O ID n??o pode ser v??zio.")
                else:
                    if (AppFunctions.idTest(valueSID)):
                        AppFunctions.calcSalaryL(self, valueSID, valueNull)
                        widgets.sucessLabelS.setText("C??lculo feito com sucesso!")
                    else:
                        widgets.sucessLabelS.setText("ID n??o encontrado ou inv??lido.")
        
        if btnName == "btn_calcFeriasLiquida":
            if widgets.bonusCheckF.isChecked():
                if (valueFID == '' or valueFBonus == '' or valueFerias == ''):
                    return widgets.sucessLabelF.setText("Todos os valores devem ser preenchidos.")
                else:
                    if (AppFunctions.idTest(valueFID)):
                        if (AppFunctions.valueTest(valueFBonus)):
                            if (AppFunctions.valueTest(valueFerias)):
                                AppFunctions.calcFeriasL(self, valueFID, valueFBonus, valueFerias)
                                widgets.sucessLabelF.setText("C??lculo feito com sucesso!")
                            else:
                                widgets.sucessLabelF.setText("Dias de F??rias deve ser um n??mero v??lido!")
                        else:
                            widgets.sucessLabelF.setText("B??nus deve ser um n??mero v??lido.")
                    else:
                        widgets.sucessLabelF.setText("ID n??o encontrado ou inv??lido.")
            else:
                if (valueFID == '' or valueFerias == ''):
                    return widgets.sucessLabelF.setText("Todos os valores devem ser preenchidos.")
                else:
                    AppFunctions.calcFeriasL(self, valueFID, valueNull, valueFerias)
                    widgets.sucessLabelF.setText("C??lculo feito com sucesso!")

        if btnName == "btn_calcDecimoTerceiro":
            if widgets.bonusCheckD.isChecked():
                if (valueDID == '' or valueDBonus == '' or valueMeses == ''):
                    return widgets.sucessLabelD.setText("Todos os valores devem ser preenchidos.")
                else:
                    if (AppFunctions.idTest(valueDID)):
                        if (AppFunctions.valueTest(valueDBonus)):
                            if (AppFunctions.valueTest(valueMeses)):
                                AppFunctions.calcDecimoT(self, valueDID, valueDBonus, valueMeses)
                                widgets.sucessLabelD.setText("C??lculo feito com sucesso!")
                            else:
                                widgets.sucessLabelD.setText("Meses trabalhados deve ser um n??mero v??lido.")
                        else:
                            widgets.sucessLabelD.setText("B??nus deve ser um n??mero v??lido.")
                    else:
                        widgets.sucessLabelD.setText("ID n??o encontrado ou inv??lido.")
            else:
                if (valueFID == '' or valueMeses == ''):
                    return widgets.sucessLabelD.setText("Todos os valores devem ser preenchidos.")
                else:
                    AppFunctions.calcDecimoT(self, valueDID, valueNull, valueMeses)
                    widgets.sucessLabelD.setText("C??lculo feito com sucesso!")
        
        if btnName == "btn_exit":
            sys.exit()


    # RESIZE EVENTS
    # ///////////////////////////////////////////////////////////////
    def resizeEvent(self, event):
        # Update Size Grips
        UIFunctions.resize_grips(self)
    

    # MOUSE CLICK EVENTS
    # ///////////////////////////////////////////////////////////////
    def mousePressEvent(self, event):
        # SET DRAG POS WINDOW
        self.dragPos = event.globalPos()

        # PRINT MOUSE EVENTS
        #if event.buttons() == Qt.LeftButton:
        #    print('Mouse click: LEFT CLICK')
        #if event.buttons() == Qt.RightButton:
        #    print('Mouse click: RIGHT CLICK')

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon("icon.ico"))
    window = MainWindow()
    sys.exit(app.exec_())

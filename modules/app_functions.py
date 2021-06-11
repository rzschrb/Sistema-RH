# MAIN FILE
# ///////////////////////////////////////////////////////////////
from main import *
import random

# WITH ACCESS TO MAIN WINDOW WIDGETS
# ///////////////////////////////////////////////////////////////
class AppFunctions(MainWindow):
    
    ################################################################
    # Functions Add/Remove Funcionario
    ################################################################

    def addFuncionario(name, setor, salary, email):
        insertData = QSqlQuery()
        insertData.exec_(f"""INSERT INTO sistemarh (name, setor, salary, email) VALUES ('{name}', '{setor}', {salary}, '{email}')""")

    def addChave(email, key):
        insertData = QSqlQuery()
        insertData.exec_(f"""UPDATE sistemarh SET chave = '{key}' WHERE email = '{email}'""")

    def remFuncionario(id):
        removeData = QSqlQuery()
        removeData.exec_(f"""DELETE FROM sistemarh WHERE id = {id}""")

    ################################################################
    # RELOAD TABLE
    ################################################################

    def reloadTable(self): # adicionar decriptografia
        self.ui.tableWidget.clearContents()
        self.ui.tableWidget.setRowCount(0)
        query = QSqlQuery("SELECT id, name, setor, salary, email, chave FROM sistemarh")
        while query.next():
            rows = self.ui.tableWidget.rowCount()
            self.ui.tableWidget.setRowCount(rows + 1)
            self.ui.tableWidget.setItem(rows, 0, QTableWidgetItem(str(query.value(0))))
            self.ui.tableWidget.setItem(rows, 1, QTableWidgetItem(query.value(1)))
            self.ui.tableWidget.setItem(rows, 2, QTableWidgetItem(query.value(2)))
            self.ui.tableWidget.setItem(rows, 3, QTableWidgetItem(f'R$ {(query.value(3))}'))
            tuple_email_chave = (query.value(4), query.value(5))
            emailQuery = AppFunctions.decodificar_dados(tuple_email_chave)
            emailValue, *chaveValue = emailQuery
            if emailValue[-1] == 'z':
                emailValueN = emailValue.replace(emailValue[-1], '')
                self.ui.tableWidget.setItem(rows, 4, QTableWidgetItem(emailValueN))
            else:
                self.ui.tableWidget.setItem(rows, 4, QTableWidgetItem(emailValue))
        self.ui.tableWidget.setRowCount(rows + 5)

    ################################################################
    # Salário Líquido
    ################################################################

    def calcSalaryL(self, id, bonus):
        query = QSqlQuery(f"SELECT id, name, setor, salary, email FROM sistemarh WHERE id = {id}")
        query.next()
        queryName = query.value(1)
        querySetor = query.value(2)
        querySalary = query.value(3)
        queryEmail = query.value(4)
        self.ui.nameLabelS.setText("Nome: " + str(queryName))
        self.ui.cargoLabelS.setText("Cargo: " + str(querySetor))
        self.ui.emailLabelS.setText("Email: " + str(queryEmail))
        self.ui.salaryLabelS.setText("Salário: R$ " + str(querySalary))
        self.ui.bonusLabelS.setText("Bônus: R$ " + str(bonus))

        salINSS = [] # Lista de divisão de salários - INSS
        aliINSS = [] # Lista de divisão de aliquotas em relação aos salários - INSS
        parINSS = []
        query = QSqlQuery(f"SELECT salINSS, aliINSS, parINSS FROM impostoinss")
        while query.next():
            resultOne = query.value(0)
            salINSS.append(resultOne)
            resultTwo = query.value(1)
            aliINSS.append(resultTwo)
            resultThree = query.value(2)
            parINSS.append(resultThree)

        salIRRF = [] # Lista de divisão de salários - IRRF
        aliIRRF = [] # Lista de divisão de aliquotas em relação aos salários - IRRF
        parIRRF = [] # Lista de divisão de dedução do IRRF referente aos salários
        query = QSqlQuery(f"SELECT salIRRF, aliIRRF, parIRRF FROM impostoirrf")
        while query.next():
            resultOne = query.value(0)
            salIRRF.append(resultOne)
            resultTwo = query.value(1)
            aliIRRF.append(resultTwo)
            resultThree = query.value(2)
            parIRRF.append(resultThree)

        bruteValue = float(querySalary) + float(bonus)
        bruteValueB = bruteValue

        if (bruteValue <= 1100):  # Salário igual ou menor a 1100
            taxaINSS = bruteValue * (aliINSS[0] / 100)
        elif (bruteValue <= 2203.48):  # Salário igual ou menor a 2203,48
            bruteValueB = bruteValue - salINSS[0]
            taxaINSS = bruteValueB * (aliINSS[1] / 100) + parINSS[0]
        elif (bruteValue <= 3305.22):  # Salário igual ou menor a 3305,22
            bruteValueB = bruteValue - salINSS[1]
            taxaINSS = bruteValueB * (aliINSS[2] / 100) + (parINSS[0] + parINSS[1])
        elif (bruteValue <= 6433.57):  # Salário igual ou menor a 6433,57
            bruteValueB = bruteValue - salINSS[2]
            taxaINSS = bruteValueB * (aliINSS[3] / 100) + (parINSS[0] + parINSS[1] + parINSS[2])
        else:  # Salário acima do teto do INSS
            taxaINSS = (salINSS[0] * (aliINSS[0] / 100)) + ((salINSS[1] - salINSS[0]) * (aliINSS[1] / 100)) + (
                        (salINSS[2] - salINSS[1]) * (aliINSS[2] / 100)) + (
                                (salINSS[3] - salINSS[2]) * (aliINSS[3] / 100))
        
        self.ui.inssLabelS.setText(f"Taxa INSS: R$ {taxaINSS:.2f}")
        
        # IRRF
        if (bruteValue <= salIRRF[0]):  # Salário igual ou menor a 1903,98.
            taxaIRRF = (bruteValue * 0)
        elif (bruteValue <= salIRRF[1]):  # Salário igual ou menor a 2826,65.
            taxaIRRF = (bruteValue * (aliIRRF[1] / 100)) - parIRRF[1]
        elif (bruteValue <= salIRRF[2]):  # Salário igual ou menor a 3751,05.
            taxaIRRF = (bruteValue * (aliIRRF[2] / 100)) - parIRRF[2]
        elif (bruteValue <= salIRRF[3]):  # Salário igual ou menor a 4664,68.
            taxaIRRF = (bruteValue * (aliIRRF[3] / 100)) - parIRRF[3]
        else:  # Salário maior que 4664,68.
            taxaIRRF = (bruteValue * (aliIRRF[4] / 100)) - parIRRF[4]
        
        self.ui.irrfLabelS.setText(f"Taxa IRRF: R$ {taxaIRRF:.2f}")
        self.ui.discTotalLabelS.setText(f"Desconto Total: R$ {(taxaINSS + taxaIRRF):.2f}")

        finalSalary = bruteValue - (taxaINSS + taxaIRRF)
        self.ui.finalLabelS.setText(f"<b><big>Salário Líquido: R$ {finalSalary:.2f}</big></b>")

    ################################################################
    # Férias Líquida
    ################################################################

    def calcFeriasL(self, id, bonus, diasFerias):
        query = QSqlQuery(f"SELECT id, name, setor, salary, email FROM sistemarh WHERE id = {id}")
        query.next()
        queryName = query.value(1)
        querySetor = query.value(2)
        querySalary = query.value(3)
        queryEmail = query.value(4)
        self.ui.nameLabelF.setText("Nome: " + str(queryName))
        self.ui.cargoLabelF.setText("Cargo: " + str(querySetor))
        self.ui.emailLabelF.setText("Email: " + str(queryEmail))
        self.ui.salaryLabelF.setText("Salário: R$ " + str(querySalary))
        self.ui.bonusLabelF.setText("Bônus: R$ " + str(bonus))

        salINSS = [] # Lista de divisão de salários - INSS
        aliINSS = [] # Lista de divisão de aliquotas em relação aos salários - INSS
        parINSS = []
        query = QSqlQuery(f"SELECT salINSS, aliINSS, parINSS FROM impostoinss")
        while query.next():
            resultOne = query.value(0)
            salINSS.append(resultOne)
            resultTwo = query.value(1)
            aliINSS.append(resultTwo)
            resultThree = query.value(2)
            parINSS.append(resultThree)

        salIRRF = [] # Lista de divisão de salários - IRRF
        aliIRRF = [] # Lista de divisão de aliquotas em relação aos salários - IRRF
        parIRRF = [] # Lista de divisão de dedução do IRRF referente aos salários
        query = QSqlQuery(f"SELECT salIRRF, aliIRRF, parIRRF FROM impostoirrf")
        while query.next():
            resultOne = query.value(0)
            salIRRF.append(resultOne)
            resultTwo = query.value(1)
            aliIRRF.append(resultTwo)
            resultThree = query.value(2)
            parIRRF.append(resultThree)

        bruteValue = float(querySalary) + float(bonus)
        bruteValueB = bruteValue
        valueFerias = (bruteValue * 0.33) / 30 * int(diasFerias)
        totalBrute = valueFerias + bruteValue

        if (bruteValue <= salINSS[0]):  # Salário igual ou menor a 1100
            taxaINSS = bruteValue * (aliINSS[0] / 100)
        elif (bruteValue <= salINSS[1]):  # Salário igual ou menor a 2203,48
            bruteValueB = bruteValue - salINSS[0]
            taxaINSS = bruteValueB * (aliINSS[1] / 100) + parINSS[0]
        elif (bruteValue <= salINSS[2]):  # Salário igual ou menor a 3305,22
            bruteValueB = bruteValue - salINSS[1]
            taxaINSS = bruteValueB * (aliINSS[2] / 100) + (parINSS[0] + parINSS[1])
        elif (bruteValue <= salINSS[3]):  # Salário igual ou menor a 6433,57
            bruteValueB = bruteValue - salINSS[2]
            taxaINSS = bruteValueB * (aliINSS[3] / 100) + (parINSS[0] + parINSS[1] + parINSS[2])
        else:  # Salário acima do teto do INSS
            taxaINSS = (salINSS[0] * (aliINSS[0] / 100)) + ((salINSS[1] - salINSS[0]) * (aliINSS[1] / 100)) + (
                        (salINSS[2] - salINSS[1]) * (aliINSS[2] / 100)) + (
                                   (salINSS[3] - salINSS[2]) * (aliINSS[3] / 100))

        baseValue = totalBrute - taxaINSS
        self.ui.inssLabelF.setText(f"Taxa INSS: R$ {taxaINSS:.2f}")
        self.ui.valBaseLabelF.setText(f"Valor Base: R$ {baseValue:.2f}")

        if ((bruteValue - taxaINSS) <= salIRRF[0]):  # Salário igual ou menor a 1903,98.
            taxaIRRF = (baseValue * 0)
        elif ((bruteValue - taxaINSS) <= salIRRF[1]):  # Salário igual ou menor a 2826,65.
            taxaIRRF = (baseValue * (aliIRRF[1] / 100)) - parIRRF[1]
        elif ((bruteValue - taxaINSS) <= salIRRF[2]):  # Salário igual ou menor a 3751,05.
            taxaIRRF = (baseValue * (aliIRRF[2] / 100)) - parIRRF[2]
        elif ((bruteValue - taxaINSS) <= salIRRF[3]):  # Salário igual ou menor a 4664,68.
            taxaIRRF = (baseValue * (aliIRRF[3] / 100)) - parIRRF[3]
        else:  # Salário maior que 4664,68.
            taxaIRRF = (baseValue * (aliIRRF[4] / 100)) - parIRRF[4]
        
        self.ui.irrfLabelF.setText(f"Taxa IRRF: R$ {taxaIRRF:.2f}")
        self.ui.discTotalLabelF.setText(f"Desconto Total: R$ {(taxaINSS + taxaIRRF):.2f}")

        finalSalary = baseValue - taxaIRRF
        self.ui.finalLabelF.setText(f"<b><big>Férias Líquida: R$ {finalSalary:.2f}</big></b>")

    ################################################################
    # Décimo Terceiro
    ################################################################

    def calcDecimoT(self, id, bonus, meses):
        query = QSqlQuery(f"SELECT id, name, setor, salary, email FROM sistemarh WHERE id = {id}")
        query.next()
        queryName = query.value(1)
        querySetor = query.value(2)
        querySalary = query.value(3)
        queryEmail = query.value(4)
        self.ui.nameLabelD.setText("Nome: " + str(queryName))
        self.ui.cargoLabelD.setText("Cargo: " + str(querySetor))
        self.ui.emailLabelD.setText("Email: " + str(queryEmail))
        self.ui.salaryLabelD.setText("Salário: R$ " + str(querySalary))
        self.ui.bonusLabelD.setText("Bônus: R$ " + str(bonus))

        salINSS = [] # Lista de divisão de salários - INSS
        aliINSS = [] # Lista de divisão de aliquotas em relação aos salários - INSS
        parINSS = []
        query = QSqlQuery(f"SELECT salINSS, aliINSS, parINSS FROM impostoinss")
        while query.next():
            resultOne = query.value(0)
            salINSS.append(resultOne)
            resultTwo = query.value(1)
            aliINSS.append(resultTwo)
            resultThree = query.value(2)
            parINSS.append(resultThree)

        salIRRF = [] # Lista de divisão de salários - IRRF
        aliIRRF = [] # Lista de divisão de aliquotas em relação aos salários - IRRF
        parIRRF = [] # Lista de divisão de dedução do IRRF referente aos salários
        query = QSqlQuery(f"SELECT salIRRF, aliIRRF, parIRRF FROM impostoirrf")
        while query.next():
            resultOne = query.value(0)
            salIRRF.append(resultOne)
            resultTwo = query.value(1)
            aliIRRF.append(resultTwo)
            resultThree = query.value(2)
            parIRRF.append(resultThree)

        bruteValue = float(querySalary) + float(bonus)
        bruteValueB = bruteValue
        
        if (bruteValue <= salINSS[0]):  # Salário igual ou menor a 1100
            taxaINSS = bruteValue * (aliINSS[0] / 100)
        elif (bruteValue <= salINSS[1]):  # Salário igual ou menor a 2203,48
            bruteValueB = bruteValue - salINSS[0]
            taxaINSS = bruteValueB * (aliINSS[1] / 100) + parINSS[0]
        elif (bruteValue <= salINSS[2]):  # Salário igual ou menor a 3305,22
            bruteValueB = bruteValue - salINSS[1]
            taxaINSS = bruteValueB * (aliINSS[2] / 100) + (parINSS[0] + parINSS[1])
        elif (bruteValue <= salINSS[3]):  # Salário igual ou menor a 6433,57
            bruteValueB = bruteValue - salINSS[2]
            taxaINSS = bruteValueB * (aliINSS[3] / 100) + (parINSS[0] + parINSS[1] + parINSS[2])
        else:  # Salário acima do teto do INSS
            taxaINSS = (salINSS[0] * (aliINSS[0] / 100)) + ((salINSS[1] - salINSS[0]) * (aliINSS[1] / 100)) + (
                        (salINSS[2] - salINSS[1]) * (aliINSS[2] / 100)) + (
                                   (salINSS[3] - salINSS[2]) * (aliINSS[3] / 100))
        
        baseValue = bruteValue - taxaINSS
        self.ui.inssLabelD.setText(f"Taxa INSS: R$ {taxaINSS:.2f}")

        if ((bruteValue - taxaINSS) <= salIRRF[0]):  # Salário igual ou menor a 1903,98.
            taxaIRRF = (baseValue * 0)
        elif ((bruteValue - taxaINSS) <= salIRRF[1]):  # Salário igual ou menor a 2826,65.
            taxaIRRF = (baseValue * (aliIRRF[1] / 100)) - parIRRF[1]
        elif ((bruteValue - taxaINSS) <= salIRRF[2]):  # Salário igual ou menor a 3751,05.
            taxaIRRF = (baseValue * (aliIRRF[2] / 100)) - parIRRF[2]
        elif ((bruteValue - taxaINSS) <= salIRRF[3]):  # Salário igual ou menor a 4664,68.
            taxaIRRF = (baseValue * (aliIRRF[3] / 100)) - parIRRF[3]
        else:  # Salário maior que 4664,68.
            taxaIRRF = (baseValue * (aliIRRF[4] / 100)) - parIRRF[4]
        
        self.ui.irrfLabelD.setText(f"Taxa IRRF: R$ {taxaIRRF:.2f}")
        self.ui.discTotalLabelD.setText(f"Desconto Total: R$ {(taxaINSS + taxaIRRF):.2f}")

        # Primeira Parcela
        firstValue = (bruteValue / 12) * int(meses)
        priParc = firstValue / 2
        self.ui.pparcLabelD.setText(f"<b>1° Parcela: R$ {priParc:.2f}</b>")

        # Segunda Parcela
        secondValue = (bruteValue - (taxaINSS + taxaIRRF)) / 12 * int(meses)
        segParc = secondValue - priParc
        self.ui.sparcLabelD.setText(f"<b>2° Parcela: R$ {segParc:.2f}</b>")

        finalSalary = priParc + segParc
        self.ui.finalLabelD.setText(f"<b><big>Férias Líquida: R$ {finalSalary:.2f}</big></b>")

    ################################################################
    # Encriptação
    ################################################################

    alfabeto = {'z':0,'a':1,'b':2,'c':3,'d':4,'e':5,'f':6,'g':7,'h':8,'i':9,'j':10,'k':11,'l':12,'m':13,'n':14,'o':15,'p':16,'q':17,'r':18,'s':19,'t':20,'u':21,'v':22,'w':23,'x':24,'y':25,'0':26,'1':27,'2':28,'3':29,'4':30,'5':31,'6':32,'7':33,'8':34,'9':35,'@':36,'.':37}
    inversos_modulares = {}
    for n in range(len(alfabeto)):
        for m in range(len(alfabeto)):
            if (n*m)%len(alfabeto) == 1: inversos_modulares[n] = m

    # Recupera a chave de um valor dentro do dicionario acima
    def get_key(val):
        for key, value in AppFunctions.alfabeto.items():
            if val == value:
                return key
    
    def determinante_matriz(chave = [[1, 0], [0, 1]]):
        return (chave[0][0] * chave[1][1] - chave[0][1] * chave[1][0])%len(AppFunctions.alfabeto)

    def gerar_chave():
        chave = [[],[]]

        # Gera uma chave aleatória com elementos inteiros de 1 a 1000 invertível mod36
        while True:                               #gera uma chave aleatória com elementos inteiros de
            for i in range(2):                    #1 a 1000 invertível mod36
                chave[0].append(random.randint(1, 1000))
            for i in range(2):
                chave[1].append(random.randint(1, 1000))

            determinante_chave = AppFunctions.determinante_matriz(chave)
            if determinante_chave < 0:
                determinante_chave = determinante_chave*(-1)
            if determinante_chave%len(AppFunctions.alfabeto) not in AppFunctions.inversos_modulares:
                chave.clear()
                chave = [[],[]]
            else:break
        return chave
    
    # faz a encriptação da mensagem segundo a cifra de hill, guardando num banco de dados a email codificada e a chave
    def encriptação(email, chave):
        # matrizes
        matriz_email = []
        matriz_linha = []
        coluna = []
        email_linha = ''
        x = 0

        for char in email:
            coluna.append(AppFunctions.alfabeto[char])
            if len(coluna) == 2:
                matriz_email.append(coluna.copy())
                coluna.clear()
        # correção da matriz
        if len(coluna)>0:
            matriz_email.append([AppFunctions.alfabeto[email[-1]],0])
            coluna.clear()
    
        while len(matriz_linha) < len(matriz_email): #multiplicação das matrizes
            for n_coluna in matriz_email:
                coluna.append(chave[0][0]*n_coluna[0]+chave[0][1]*n_coluna[1])
                coluna.append(chave[1][0]*n_coluna[0]+chave[1][1]*n_coluna[1])
                matriz_linha.append(coluna.copy())
                coluna.clear()

        #matriz codificada mod36
        for j in matriz_linha:
            for i in range(len(j)):
                j[i] = j[i]%len(AppFunctions.alfabeto)


        #email_linha
        for colunas in matriz_linha:
            email_linha += AppFunctions.get_key(colunas[0])
            email_linha += AppFunctions.get_key(colunas[1])
        chaveString = str(chave[0][0]) + '/' + str(chave[0][1]) + '/' + str(chave[1][0]) + '/' + str(chave[1][1])
        return (email_linha,chaveString)

    def decodificar_dados(tupla_email_chave): # tupla = (email, chave)
        chave = tupla_email_chave[1]
        chave_inversa = []
        c = []
        bar = 0
        while chave.find('/',bar) != -1:
            c.append(int(chave[bar:chave.find('/',bar)]))
            bar = chave.find('/', bar) + 1
            if len(c) == 2:
                chave_inversa.append(c.copy())
                c.clear()
        # aqui se obtem a matriz inversa da chave(modlen(alfabeto))
        c.append(int(chave[bar:]))
        chave_inversa.append(c.copy())
        determinante_chave = AppFunctions.inversos_modulares[AppFunctions.determinante_matriz(chave_inversa)]
        temp = chave_inversa[0][0]
        chave_inversa[0][0] = chave_inversa[1][1] * determinante_chave
        chave_inversa[0][1] = -chave_inversa[0][1] * determinante_chave
        chave_inversa[1][0] = -chave_inversa[1][0] * determinante_chave
        chave_inversa[1][1] = temp * determinante_chave
        dados_obtidos = AppFunctions.encriptação(tupla_email_chave[0], chave_inversa)
        return dados_obtidos 

    ################################################################
    # Validações
    ################################################################

    def idTest(id):
        if id.isalnum():
            query = QSqlQuery(f"SELECT id FROM sistemarh WHERE id = {id}")
            querycheck = query.first()
            if (querycheck):
                return True
            else:
                return False
        else:
            return False

    def emailTest(email):
        emailTest = email
        if len(emailTest) >= 3:
            return True
        else:
            return False

    def stringTest(string):
        if string != " ":
            if string != "":
                stringTest = string.replace(" ","").isalpha()
                if (stringTest):
                    return True
                else:
                    return False
            else:
                return False
        else:
            return False

    def valueTest(num):
        try:
            value = int(num)
            return True
        except ValueError:
            try:
                value = float(num)
                return True
            except ValueError: 
                return False
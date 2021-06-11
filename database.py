from modules import *
from main import *

def createConnection(databaseName):
    connection = QSqlDatabase.addDatabase("QSQLITE")
    connection.setDatabaseName(databaseName)

    if not connection.open():
        QMessageBox.warning(
            None,
            "Database",
            f"Database Error: {connection.lastError().text()}",
        )
        return False
    _validateRHTable()
    _validateINSSTable()
    _validateIRRFTable()
    return True

def _validateRHTable():

    query = QSqlQuery("SELECT name FROM sqlite_master WHERE type='table' AND name='sistemarh';")
    validate = query.first()
    if validate == True:
        print("Tabela 'SistemaRH' existente. Não inserindo dados default.")
    else:
        print("Tabela 'SistemaRH' não existe. Criando tabela e inserindo dados default.")
        _createRHTable()
        insertData = QSqlQuery()
        insertData.exec_("""INSERT INTO sistemarh (name, setor, salary, email, chave) VALUES ('admin', 'Gerente', 10000, '7y8ovvy5vm400a67g1', '819/915/499/138')""")


def _createRHTable():

    createTableQuery = QSqlQuery()
    return createTableQuery.exec_(
        """
        CREATE TABLE IF NOT EXISTS sistemarh (
            id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
            name VARCHAR(40) NOT NULL,
            setor VARCHAR(50) NOT NULL,
            salary INTEGER NOT NULL,
            email VARCHAR(40) NOT NULL,
            chave VARCHAR(40)
        )
        """
    )

def _validateINSSTable():

    query = QSqlQuery("SELECT name FROM sqlite_master WHERE type='table' AND name='impostoinss';")
    validate = query.first()
    if validate == True:
        print("Tabela de INSS existente. Não inserindo dados default.")
    else:
        print("Tabela de INSS não existe. Criando tabela e inserindo dados default.")
        _createINSSTable()
        insertData = QSqlQuery()
        insertData.prepare(
        """
        INSERT INTO impostoinss (
            salINSS,
            aliINSS,
            parINSS
        )
        VALUES (?, ?, ?)
        """
        )
        data = [
            (1100, 7.5, 82.5),
            (2203.48, 9, 99.31),
            (3305.22, 12, 132.2),
            (6433.57, 14, 437.97)
        ]
        for salINSS, aliINSS, parINSS in data:
            insertData.addBindValue(salINSS)
            insertData.addBindValue(aliINSS)
            insertData.addBindValue(parINSS)
            insertData.exec_()

def _createINSSTable():

    createTableQuery = QSqlQuery()
    return createTableQuery.exec_(
        """
        CREATE TABLE IF NOT EXISTS impostoinss (
            salINSS REAL NOT NULL,
            aliINSS REAL NOT NULL,
            parINSS REAL NOT NULL
        )
        """
    )

def _validateIRRFTable():

    query = QSqlQuery("SELECT name FROM sqlite_master WHERE type='table' AND name='impostoirrf';")
    validate = query.first()
    if validate == True:
        print("Tabela de IRRF existente. Não inserindo dados default.")
    else:
        print("Tabela de IRRF não existe. Criando tabela e inserindo dados default.")
        _createIRRFTable()
        insertData = QSqlQuery()
        insertData.prepare(
        """
        INSERT INTO impostoirrf (
            salIRRF,
            aliIRRF,
            parIRRF
        )
        VALUES (?, ?, ?)
        """
        )
        data = [
            (1903.98, 0, 0),
            (2826.64, 7.5, 142.8),
            (3751.05, 15, 354.8),
            (4664.68, 22.5, 636.13),
            (4664.68, 27.5, 869.36)
        ]
        for salIRRF, aliIRRF, parIRRF in data:
            insertData.addBindValue(salIRRF)
            insertData.addBindValue(aliIRRF)
            insertData.addBindValue(parIRRF)
            insertData.exec_()

def _createIRRFTable():

    createTableQuery = QSqlQuery()
    return createTableQuery.exec_(
        """
        CREATE TABLE IF NOT EXISTS impostoirrf (
            salIRRF REAL NOT NULL,
            aliIRRF REAL NOT NULL,
            parIRRF REAL NOT NULL
        )
        """
    )
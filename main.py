# Instalar e importar o Yahoo Finance (yfinance) e bibliotecas
import sys
import subprocess
import yfinance as yf
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import matplotlib.pyplot as plt


class MyWindow(QMainWindow):
    def __init__(self):
        super(MyWindow, self).__init__()
        self.setup_main_window()
        self.initUI()

    def setup_main_window(self):
        self.x = 900
        self.y = 650
        self.setMinimumSize(QSize(self.x, self.y))
        self.setWindowTitle("Interface Gráfica com Python")
        self.wid = QWidget(self)
        self.setCentralWidget(self.wid)
        self.layout = QGridLayout()
        self.wid.setLayout(self.layout)

    def initUI(self):
        # Criando botões
        self.b1 = QtWidgets.QPushButton(self)
        self.b1.setText("CONFIRMAR")
        self.b1.clicked.connect(self.confirmar)

        # Criando Qline para receber informações
        self.line_edit = QLineEdit(self)
        self.line_edit.adjustSize()
        self.line_edit.setFixedSize(QSize(200, 20))
        self.receive = str(self.line_edit)

        # Texto
        self.texto = QLabel("Pesquise uma ação para saber sobre suas informações básicas", self)
        self.texto.adjustSize()
        self.largura = self.texto.frameGeometry().width()
        self.altura = self.texto.frameGeometry().height()
        self.texto.setAlignment(QtCore.Qt.AlignCenter)

        self.acaoLine1 = QLabel("Digite a ação: ", self)
        self.acaoLine1.adjustSize()

        self.exibeAcao = QLabel("Ação", self)
        self.exibeAcao.adjustSize()

        self.inicioLabel = QLabel("Data inicial", self)
        self.inicioLabel.adjustSize()

        self.fimLabel = QLabel("Data final", self)
        self.fimLabel.adjustSize()

        # Criando calendarios
        self.calendario1 = QCalendarWidget(self)
        self.calendario1.setGeometry(50, 50, 130, 100)
    
        self.calendario2 = QCalendarWidget(self)
        self.calendario2.setGeometry(50, 50, 130, 100)

        # Organizando os widgets dentro do gridlayout
        self.layout.addWidget(self.texto, 0, 0, 1, 4)
        self.layout.addWidget(self.acaoLine1, 1, 0)
        self.layout.addWidget(self.inicioLabel, 2, 0)
        self.layout.addWidget(self.fimLabel, 2, 2)
        self.layout.addWidget(self.calendario1, 3, 0)
        self.layout.addWidget(self.calendario2, 3, 2)
        self.layout.addWidget(self.exibeAcao, 1, 3)
        self.layout.addWidget(self.line_edit, 1, 1, 1, 0)
        self.layout.addWidget(self.b1, 4, 0, 1, 3)

        for i in range(4):
            self.layout.setRowStretch(i, 1)
            self.layout.setColumnStretch(i, 1)

        
    def confirmar(self):
        ca1 = self.calendario1.selectedDate().toString('yyyy-MM-dd')
        ca2 = self.calendario2.selectedDate().toString('yyyy-MM-dd')
        self.recebe1 = self.line_edit.text()
        self.acao = yf.Ticker(self.recebe1)
        self.dados = self.acao.info["longName"]
        self.dados += "\n"
        self.dados += self.acao.info["sector"]
        self.dados += "\n"
        self.dados += self.acao.info["country"]
        self.exibeAcao.setText(self.dados)
        self.exibeAcao.adjustSize()
        self.exibeAcao.setWordWrap(True)
        # Exibir informações das ações da Petrobras


        # Coletar dados da Petrobras
        data = yf.download(self.recebe1, start=ca1, end=ca2) #Hoje é 18 Nov 2020

        #Coletar somente o fechamento diário
        data = data.Close
        tData = data.size
        print(tData)
        treinamento = round(data.size*.8)
        print(treinamento)
        teste = data.size - round(data.size*.8)
        print(teste)
        # Plotar o gráfico todo
        plt.figure(figsize=(18, 6))
        plt.plot(data, '-')
        plt.xlabel(ca2)
        plt.ylabel('VALOR R$')
        plt.title(self.recebe1)
        plt.show()

        # Plotar treinamento e teste
        plt.figure(figsize=(18, 6))
        plt.plot(data, '-')
        plt.xlabel('DIAS')
        plt.ylabel('VALOR R$')
        plt.title(self.recebe1)
        plt.show()

        # Plotar treinamento e teste
        plt.figure(figsize=(18, 6))
        plt.plot(data[:tData], 'r-')
        plt.plot(data[tData:], 'g-')
        plt.xlabel('DIAS')
        plt.ylabel('VALOR R$')
        plt.title(self.recebe1)
        plt.axvline(data.index[treinamento], 0, 30, color='k', linestyle='dashed', label='Teste')
        plt.text(data.index[treinamento], 25, 'Treinamento', fontsize='x-large')
        plt.text(data.index[teste], 15, 'Testes', fontsize='x-large')
        plt.show()

        # Plotar apenas teste
        plt.figure(figsize=(10, 6))
        plt.plot(data[treinamento:], 'g-')
        plt.xlabel('DIAS')
        plt.ylabel('VALOR R$')
        plt.title(self.recebe1)
        plt.show()

    def busca_acao(self):
        self.script = '.\scripts\calendarios.py'
        self.program = 'python ' + self.script
        print(self.program)
        subprocess.run(self.program, shell=True)


def window():
    app = QApplication(sys.argv)
    win = MyWindow()
    win.show()
    sys.exit(app.exec_())

window()

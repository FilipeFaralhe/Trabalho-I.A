
# Instalar e importar o Yahoo Finance (yfinance) e bibliotecas
import sys
import numpy as np
import yfinance as yf
import torch
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
        self.setWindowTitle("Trabalho Final Redes Neurais")
        self.wid = QWidget(self)
        self.setCentralWidget(self.wid)
        self.layout = QGridLayout()
        self.wid.setLayout(self.layout)

    def initUI(self):
        # Criando botões
        self.b1 = QtWidgets.QPushButton(self)
        self.b1.setText("CONFIRMAR DADOS")
        self.b1.clicked.connect(self.confirmar)

        self.b2 = QtWidgets.QPushButton(self)
        self.b2.setText("INICIAR ANALISE")
        self.b2.clicked.connect(self.analise)

        # Criando Qline para receber informações
        self.line_edit = QLineEdit(self)
        self.line_edit.adjustSize()
        self.line_edit.setFixedSize(QSize(100, 20))


        self.epocas_edit = QLineEdit(self)
        self.epocas_edit.adjustSize()
        self.epocas_edit.setFixedSize(QSize(100, 20))

        self.neuronios_edit = QLineEdit(self)
        self.neuronios_edit.adjustSize()
        self.neuronios_edit.setFixedSize(QSize(100, 20))

        self.learning_edit = QLineEdit(self)
        self.learning_edit.adjustSize()
        self.learning_edit.setFixedSize(QSize(100, 20))

        self.momentum_edit = QLineEdit(self)
        self.momentum_edit.adjustSize()
        self.momentum_edit.setFixedSize(QSize(100, 20))

        # Texto
        self.texto = QLabel("Digite as informações e confirme para iniciar análise", self)
        self.texto.adjustSize()
        self.largura = self.texto.frameGeometry().width()
        self.altura = self.texto.frameGeometry().height()
        self.texto.setAlignment(QtCore.Qt.AlignCenter)

        self.acaoLine1 = QLabel("Digite a ação: ", self)
        self.acaoLine1.adjustSize()

        self.epocas = QLabel("Digite o número de épocas: ", self)
        self.epocas.adjustSize()

        self.neuronios = QLabel("Digite o número de neurônios: ", self)
        self.neuronios.adjustSize()

        self.learning = QLabel("Digite os valores de learning rate: ", self)
        self.learning.adjustSize()

        self.momentum = QLabel("Digite o momentum: ", self)
        self.momentum.adjustSize()

        self.infoAcao = QLabel("Informações básicas da ação: ", self)
        self.infoAcao.adjustSize()

        self.exibeAcao = QLabel("", self)
        self.exibeAcao.adjustSize()

        self.inicioLabel = QLabel("Data inicial", self)
        self.inicioLabel.setAlignment(Qt.AlignCenter)
        self.inicioLabel.adjustSize()

        self.fimLabel = QLabel("Data final", self)
        self.fimLabel.setAlignment(Qt.AlignCenter)
        self.fimLabel.adjustSize()

        # Criando calendarios
        self.calendario1 = QCalendarWidget(self)
        self.calendario1.setGeometry(50, 50, 130, 100)

        self.calendario2 = QCalendarWidget(self)
        self.calendario2.setGeometry(50, 50, 130, 100)

        # Organizando os widgets dentro do gridlayout
        self.layout.addWidget(self.texto, 0, 0, 1, 4)
        self.layout.addWidget(self.acaoLine1, 1, 0)
        self.layout.addWidget(self.epocas, 2, 0)
        self.layout.addWidget(self.epocas_edit, 2, 1)
        self.layout.addWidget(self.learning, 2, 2)
        self.layout.addWidget(self.learning_edit, 2, 3)
        self.layout.addWidget(self.neuronios, 3, 0)
        self.layout.addWidget(self.neuronios_edit, 3, 1)
        self.layout.addWidget(self.momentum, 3, 2)
        self.layout.addWidget(self.momentum_edit, 3, 3)
        self.layout.addWidget(self.infoAcao, 4, 0)
        self.layout.addWidget(self.exibeAcao, 4, 1)
        self.layout.addWidget(self.inicioLabel, 5, 0)
        self.layout.addWidget(self.fimLabel, 5, 2)
        self.layout.addWidget(self.calendario1, 6, 0)
        self.layout.addWidget(self.calendario2, 6, 2)
        self.layout.addWidget(self.line_edit, 1, 1, 1, 0)
        self.layout.addWidget(self.b1, 7, 0, 1, 7)
        self.layout.addWidget(self.b2, 8, 0, 1, 7)

        for i in range(8):
            self.layout.setRowStretch(i, 1)
            self.layout.setColumnStretch(i, 1)

    def confirmar(self):
        try:
            ca1 = self.calendario1.selectedDate().toString('yyyy-MM-dd')
            ca2 = self.calendario2.selectedDate().toString('yyyy-MM-dd')
            self.recebe1 = self.line_edit.text().upper()

            # Convertendo numero recebido
            self.recebe2 = self.epocas_edit.text()
            self.num1 = int(self.recebe2)

            self.recebe3 = self.neuronios_edit.text()
            self.num2 = int(self.recebe3)

            self.recebe4 = self.learning_edit.text()
            self.num3 = float(self.recebe4)

            self.recebe5 = self.momentum_edit.text()
            self.num4 = float(self.recebe5)

            self.acao = yf.Ticker(self.recebe1)

            self.dados = self.acao.info["longName"]
            self.dados += "\n"
            self.dados += self.acao.info["sector"]
            self.dados += "\n"
            self.dados += self.acao.info["country"]
            self.exibeAcao.setText(self.dados)
            self.exibeAcao.adjustSize()
            self.exibeAcao.setWordWrap(True)

            # Coletar dados
            self.data = yf.download(self.recebe1, start=ca1, end=ca2)  # Hoje é 18 Nov 2020

            # Coletar somente o fechamento diário
            self.data = self.data.Close
            self.tData = self.data.size

            self.treinamento = round(self.data.size * .8)

            teste = self.data.size - round(self.data.size * .8)

            # Plotar o gráfico todo
            plt.figure(figsize=(18, 6))
            plt.plot(self.data, '-')
            plt.xlabel(ca2)
            plt.ylabel('VALOR R$')
            plt.title(self.recebe1)
            plt.show()

            # Plotar treinamento e teste
            plt.figure(figsize=(18, 6))
            plt.plot(self.data, '-')
            plt.xlabel('DIAS')
            plt.ylabel('VALOR R$')
            plt.title(self.recebe1)
            plt.show()

            # Plotar treinamento e teste
            plt.figure(figsize=(18, 6))
            plt.plot(self.data[:self.tData], 'r-')
            plt.plot(self.data[self.tData:], 'g-')
            plt.xlabel('DIAS')
            plt.ylabel('VALOR R$')
            plt.title(self.recebe1)
            plt.axvline(self.data.index[self.treinamento], 0, 30, color='k', linestyle='dashed', label='Teste')
            plt.text(self.data.index[self.treinamento], 25, 'Testes', fontsize='x-large')
            plt.text(self.data.index[teste], 15, 'Treinamento', fontsize='x-large')
            plt.show()

            # Plotar apenas teste
            plt.figure(figsize=(10, 6))
            plt.plot(self.data[self.treinamento:], 'g-')
            plt.xlabel('DIAS')
            plt.ylabel('VALOR R$')
            plt.title(self.recebe1)
            plt.show()

        except:
            self.error = QMessageBox()
            self.error.setIcon(QMessageBox.Critical)
            self.error.setWindowTitle("ERRO")
            self.error.setText("Ação não existe")
            self.error.setStandardButtons(QMessageBox.Ok)
            self.error.exec_()

    def analise(self):
            # Criar janela deslizante
            janelas = 50

            data_final = np.zeros([self.data.size - janelas, janelas + 1])

            for i in range(len(data_final)):
                for j in range(janelas + 1):
                    data_final[i][j] = self.data.iloc[i + j]

            # Normalizar entre 0 e 1
            max = data_final.max()
            min = data_final.min()
            dif = data_final.max() - data_final.min()
            data_final = (data_final - data_final.min()) / dif

            x = data_final[:, :-1]
            y = data_final[:, -1]
            # Converter para tensor
            # Entrada do treinamento
            # Saída do treinamento
            training_input = torch.FloatTensor(x[:self.treinamento, :])
            training_output = torch.FloatTensor(y[:self.treinamento])

            # Entrada do teste
            # Saída do teste
            test_input = torch.FloatTensor(x[self.treinamento: , :])
            test_output = torch.FloatTensor(y[self.treinamento:])

            # Classe do modelo da Rede Neural
            class Net(torch.nn.Module):
                def __init__(self, input_size, hidden_size):
                    super(Net, self).__init__()
                    self.input_size = input_size
                    self.hidden_size = hidden_size
                    self.fc1 = torch.nn.Linear(self.input_size, self.hidden_size)
                    self.relu = torch.nn.ReLU()
                    self.fc2 = torch.nn.Linear(self.hidden_size, 1)

                def forward(self, x):
                    hidden = self.fc1(x)
                    relu = self.relu(hidden)
                    output = self.fc2(relu)
                    output = self.relu(output)
                    return output

            # Criar a instância do modelo
            input_size = training_input.size()[1]
            hidden_size = self.num2
            model = Net(input_size, hidden_size)
            print(f'Entrada: {input_size}')
            print(f'Escondida: {hidden_size}')
            print(model)

            # Critério de erro
            criterion = torch.nn.MSELoss()

            # Criando os paramêtros (learning rate[obrigatória] e momentum[opcional])
            lr = self.num3
            momentum = self.num4
            optimizer = torch.optim.SGD(model.parameters(), lr, momentum)

            # Para visualizar os pesos
            for param in model.parameters():
                # print(param)
                pass

            # Treinamento
            model.train()
            epochs = self.num1
            errors = []

            for epoch in range(epochs):
                optimizer.zero_grad()
                # Fazer o forward
                y_pred = model(training_input)
                # Cálculo do erro
                loss = criterion(y_pred.squeeze(), training_output)
                errors.append(loss.item())
                if epoch % 1000 == 0:
                    print(f'Epoch: {epoch}. Train loss: {loss.item()}.')
                # Backpropagation
                loss.backward()
                optimizer.step()

            # Testar o modelo já treinado
            model.eval()
            y_pred = model(test_input)
            after_train = criterion(y_pred.squeeze(), test_output)
            print('Test loss after Training', after_train.item())

            # Gráficos de erro e de previsão
            def plotcharts(errors):
                errors = np.array(errors)
                lasterrors = np.array(errors[-25000:])
                plt.figure(figsize=(18, 5))
                graf01 = plt.subplot(1, 3, 1)  # nrows, ncols, index
                graf01.set_title('Errors')
                plt.plot(errors, '-')
                plt.xlabel('Epochs')
                graf02 = plt.subplot(1, 3, 2)  # nrows, ncols, index
                graf02.set_title('Last 25k Errors')
                plt.plot(lasterrors, '-')
                plt.xlabel('Epochs')
                graf03 = plt.subplot(1, 3, 3)
                graf03.set_title('Tests')
                a = plt.plot(test_output.numpy(), 'y-', label='Real')
                a = plt.plot(y_pred.detach().numpy(), 'b-', label='Predicted')
                plt.legend(loc=7)
                plt.show()
            plotcharts(errors)
        
def window():
    app = QApplication(sys.argv)
    win = MyWindow()
    win.show()
    sys.exit(app.exec_())
window()

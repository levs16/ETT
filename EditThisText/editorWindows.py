import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit, QFileDialog, QAction, QFontDialog, QLabel
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import Qt
from PyQt5 import QtGui


class TextEditor(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowIcon(QtGui.QIcon('icons\\icon.png'))
        self.initUI()

    def initUI(self):
        self.textEdit = QTextEdit()
        self.setCentralWidget(self.textEdit)
        self.statusBar()

        newFile = QAction(QIcon('icons\\new.png'), 'New', self)
        newFile.setShortcut('Ctrl+N')
        newFile.setStatusTip('Create a new file')
        newFile.triggered.connect(self.newFile)

        openFile = QAction(QIcon('icons\\open.png'), 'Open', self)
        openFile.setShortcut('Ctrl+O')
        openFile.setStatusTip('Open a file')
        openFile.triggered.connect(self.openFile)

        saveFile = QAction(QIcon('icons\\save.png'), 'Save', self)
        saveFile.setShortcut('Ctrl+S')
        saveFile.setStatusTip('Save the file')
        saveFile.triggered.connect(self.saveFile)

        saveAsFile = QAction(QIcon('icons\\saveas.png'), 'Save As', self)
        saveAsFile.setShortcut('Ctrl+Shift+S')
        saveAsFile.setStatusTip('Save the file as')
        saveAsFile.triggered.connect(self.saveAsFile)

        exitApp = QAction(QIcon('icons\\exit.png'), 'Exit', self)
        exitApp.setShortcut('Ctrl+Q')
        exitApp.setStatusTip('Exit the application')
        exitApp.triggered.connect(self.close)

        copyText = QAction(QIcon('icons\\copy.png'), 'Copy', self)
        copyText.setShortcut('Ctrl+C')
        copyText.setStatusTip('Copy the selected text')
        copyText.triggered.connect(self.textEdit.copy)

        pasteText = QAction(QIcon('icons\\paste.png'), 'Paste', self)
        pasteText.setShortcut('Ctrl+V')
        pasteText.setStatusTip('Paste the copied text')
        pasteText.triggered.connect(self.textEdit.paste)

        cutText = QAction(QIcon('icons\\cut.png'), 'Cut', self)
        cutText.setShortcut('Ctrl+X')
        cutText.setStatusTip('Cut the selected text')
        cutText.triggered.connect(self.textEdit.cut)

        selectAllText = QAction(QIcon('icons\\selectall.png'), 'Select All', self)
        selectAllText.setShortcut('Ctrl+A')
        selectAllText.setStatusTip('Select all the text')
        selectAllText.triggered.connect(self.textEdit.selectAll)

        fontChange = QAction(QIcon('icons\\font.png'), 'Font', self)
        fontChange.setShortcut('Ctrl+F')
        fontChange.setStatusTip('Change the font of the text')
        fontChange.triggered.connect(self.fontChange)

        aboutWin = QAction(QIcon('icons\\about.png'), 'About', self)
        aboutWin.setShortcut('Ctrl+Shift+I')
        aboutWin.setStatusTip('Display the About window')
        aboutWin.triggered.connect(self.aboutWinOpen)

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(newFile)
        fileMenu.addAction(openFile)
        fileMenu.addAction(saveFile)
        fileMenu.addAction(saveAsFile)
        fileMenu.addAction(exitApp)

        editMenu = menubar.addMenu('&Edit')
        editMenu.addAction(copyText)
        editMenu.addAction(pasteText)
        editMenu.addAction(cutText)
        editMenu.addAction(selectAllText)
        editMenu.addAction(fontChange)

        helpMenu = menubar.addMenu('&Help')
        helpMenu.addAction('About', self.aboutWinOpen)

        toolbar = self.addToolBar('Tools')
        toolbar.setMovable(True)
        toolbar.addAction(newFile)
        toolbar.addAction(openFile)
        toolbar.addAction(saveFile)
        toolbar.addAction(saveAsFile)
        toolbar.addAction(exitApp)
        toolbar.addSeparator()
        toolbar.addAction(copyText)
        toolbar.addAction(pasteText)
        toolbar.addAction(cutText)
        toolbar.addAction(selectAllText)
        toolbar.addSeparator()
        toolbar.addAction(fontChange)

        self.setGeometry(300, 300, 350, 250)
        self.setWindowTitle('EditThisText v0.5')
        self.show()

    def newFile(self):
        self.textEdit.clear()

    def openFile(self):
        try:
            fname = QFileDialog.getOpenFileName(self, 'Open file', '/home')

            if fname[0]:
                f = open(fname[0], 'r')

                with f:
                    data = f.read()
                    self.textEdit.setText(data)
        
        except Exception as e:
            print(f"log> Handled the error: {e}")

    def saveFile(self):
        fname = QFileDialog.getSaveFileName(self, 'Save file', '/home')

        if fname[0]:
            f = open(fname[0], 'w')

            with f:
                data = self.textEdit.toPlainText()
                f.write(data)

    def saveAsFile(self):
        fname = QFileDialog.getSaveFileName(self, 'Save file as', '/home')

        if fname[0]:
            f = open(fname[0], 'w')

            with f:
                data = self.textEdit.toPlainText()
                f.write(data)

    def fontChange(self):
        font, ok = QFontDialog.getFont()

        if ok:
            self.textEdit.setFont(font)

    def aboutWinOpen(self):
        self.about = QMainWindow()
        self.about.setWindowTitle('About Text Editor')
        self.about.setFixedSize(300, 200)

        self.iconLabel = QLabel(self.about)
        self.iconLabel.setPixmap(QPixmap('icons\\icon.png'))
        self.iconLabel.setAlignment(Qt.AlignCenter)
        self.iconLabel.setGeometry(0, 0, 300, 150)

        self.textLabel = QLabel(self.about)
        self.textLabel.setText('Aboba Inc. All Rights Reserved 2023.')
        self.textLabel.setOpenExternalLinks(True)
        self.textLabel.setAlignment(Qt.AlignCenter)
        self.textLabel.setGeometry(0, 150, 300, 50)

        self.about.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = TextEditor()
    sys.exit(app.exec_())
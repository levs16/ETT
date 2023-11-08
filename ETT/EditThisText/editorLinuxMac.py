"""========IMPORTS========"""
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit, QFileDialog, QAction, QFontDialog, QLabel, QPushButton, QListWidget, QListWidgetItem, QTableWidget, QTableWidgetItem
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import Qt, QFileSelector, QFileInfo, QSettings

# Define the file selector for the icons
file_selector = QFileSelector()
file_selector.setExtraSelectors(['light']) # Set the default theme to light

"""========GUI========"""


class TextEditor(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowIcon(QIcon('icons/NewLook/editor.png')) # Init an icon for the app
        self.initUI()

    def initUI(self):
        self.textEdit = QTextEdit()
        self.setCentralWidget(self.textEdit)
        self.statusBar()

        # Load the settings from the previous session
        self.settings = QSettings('Aboba Inc.', 'EditThisText')
        self.restoreGeometry(self.settings.value('geometry'))
        self.restoreState(self.settings.value('windowState'))
        self.recentFiles = self.settings.value('recentFiles', [])
        self.startPageOpen() # Create the start page
        self.updateRecentFiles() # Update the recent files list

        """========BUTTONS========"""
        newFile = QAction(QIcon(file_selector.select('icons/NewLook/new.png')), 'New', self)
        newFile.setShortcut('Ctrl+N')
        newFile.setStatusTip('Create a new file')
        newFile.triggered.connect(self.newFile)

        openFile = QAction(QIcon(file_selector.select('icons/NewLook/open.png')), 'Open', self)
        openFile.setShortcut('Ctrl+O')
        openFile.setStatusTip('Open a file')
        openFile.triggered.connect(self.openFile)

        saveFile = QAction(QIcon(file_selector.select('icons/NewLook/save.png')), 'Save', self)
        saveFile.setShortcut('Ctrl+S')
        saveFile.setStatusTip('Save the file')
        saveFile.triggered.connect(self.saveFile)

        saveAsFile = QAction(QIcon(file_selector.select('icons/NewLook/saveas.png')), 'Save As', self)
        saveAsFile.setShortcut('Ctrl+Shift+S')
        saveAsFile.setStatusTip('Save the file as')
        saveAsFile.triggered.connect(self.saveAsFile)

        exitApp = QAction(QIcon(file_selector.select('icons/NewLook/exit.png')), 'Exit', self)
        exitApp.setShortcut('Ctrl+Q')
        exitApp.setStatusTip('Exit the application')
        exitApp.triggered.connect(self.close)

        copyText = QAction(QIcon(file_selector.select('icons/NewLook/copy.png')), 'Copy', self)
        copyText.setShortcut('Ctrl+C')
        copyText.setStatusTip('Copy the selected text')
        copyText.triggered.connect(self.textEdit.copy)

        pasteText = QAction(QIcon(file_selector.select('icons/NewLook/paste.png')), 'Paste', self)
        pasteText.setShortcut('Ctrl+V')
        pasteText.setStatusTip('Paste the copied text')
        pasteText.triggered.connect(self.textEdit.paste)

        cutText = QAction(QIcon(file_selector.select('icons/NewLook/cut.png')), 'Cut', self)
        cutText.setShortcut('Ctrl+X')
        cutText.setStatusTip('Cut the selected text')
        cutText.triggered.connect(self.textEdit.cut)

        selectAllText = QAction(QIcon(file_selector.select('icons/NewLook/selectall.png')), 'Select All', self)
        selectAllText.setShortcut('Ctrl+A')
        selectAllText.setStatusTip('Select all the text')
        selectAllText.triggered.connect(self.textEdit.selectAll)

        fontChange = QAction(QIcon(file_selector.select('icons/NewLook/font.png')), 'Font', self)
        fontChange.setShortcut('Ctrl+F')
        fontChange.setStatusTip('Change the font of the text')
        fontChange.triggered.connect(self.fontChange)

        aboutWin = QAction(QIcon(file_selector.select('icons/NewLook/about.png')), 'About', self)
        aboutWin.setShortcut('Ctrl+Shift+I')
        aboutWin.setStatusTip('Display the About window')
        aboutWin.triggered.connect(self.aboutWinOpen)

        """========MENUBAR======"""
        # Create the menubar of the program
        menubar = self.menuBar()

        # Add a file menu
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(newFile)
        fileMenu.addAction(openFile)
        fileMenu.addAction(saveFile)
        fileMenu.addAction(saveAsFile)
        fileMenu.addAction(exitApp)

        # Add an edit menu
        editMenu = menubar.addMenu('&Edit')
        editMenu.addAction(copyText)
        editMenu.addAction(pasteText)
        editMenu.addAction(cutText)
        editMenu.addAction(selectAllText)
        editMenu.addAction(fontChange)

        # Add a help menu
        helpMenu = menubar.addMenu('&Help')
        helpMenu.addAction('About', self.aboutWinOpen)

        """========TOOLBAR========"""
        toolbar = self.addToolBar('Tools')
        toolbar.setMovable(True)
        toolbar.setObjectName('Tools') # Set the object name
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
        self.setWindowTitle('EditThisText v0.6')
        self.show()

        # Load settings from the previous session
        self.settings = QSettings('Aboba Inc.', 'EditThisText')
        self.restoreGeometry(self.settings.value('geometry'))
        self.restoreState(self.settings.value('windowState'))
        self.recentFiles = self.settings.value('recentFiles', [])
        self.updateRecentFiles()


    """========METHODS========"""
    # Method to open New File/Create File window
    def newFile(self):
        self.textEdit.clear()


    # Method to open the Open File window
    def openFile(self):
        try:
            fname = QFileDialog.getOpenFileName(self, 'Open file', '/home')

            if fname[0]:
                with open(fname[0], 'r') as f: # Use with statement to simplify file handling
                    data = f.read()
                    self.textEdit.setText(data)
                    self.addRecentFile(fname[0]) # Add the file to the recent files list
        
        except Exception as e:
            print(f"log> Handled the error: {e}")


    # Method to open the Save File window
    def saveFile(self):
        fname = QFileDialog.getSaveFileName(self, 'Save file', '/home')

        if fname[0]:
            with open(fname[0], 'w') as f: # Use with statement to simplify file handling
                data = self.textEdit.toPlainText()
                f.write(data)
                self.addRecentFile(fname[0]) # Add the file to the recent files list


    # Method to open the Save As window
    def saveAsFile(self):
        fname = QFileDialog.getSaveFileName(self, 'Save file as', '/home')

        if fname[0]:
            with open(fname[0], 'w') as f: # Use with statement to simplify file handling
                data = self.textEdit.toPlainText()
                f.write(data)
                self.addRecentFile(fname[0]) # Add the file to the recent files list


    # Method to open the font window
    def fontChange(self):
        font, ok = QFontDialog.getFont()

        if ok:
            self.textEdit.setFont(font)


    # Method to open the About Window(help)
    def aboutWinOpen(self):
        # Create the window
        self.about = QMainWindow()
        self.about.setWindowTitle('About Text Editor')
        self.about.setFixedSize(300, 200)
        
        #Add an icon of the app and stick it to the centre
        self.iconLabel = QLabel(self.about)
        self.iconLabel.setPixmap(QPixmap('icons/NewLook/editor.png').scaled(100, 100, Qt.KeepAspectRatio)) # Use scaled method to resize the icon
        self.iconLabel.setAlignment(Qt.AlignCenter)
        self.iconLabel.setGeometry(100, 0, 100, 100) # Center that image

        # Add the text, wrap it, align and place it
        self.textLabel = QLabel(self.about)
        self.textLabel.setText('EditThisText™ PyQT5 Edition\nAboba Inc.\n©All Rights Reserved. 2020-2023.')
        self.textLabel.setWordWrap(True) # Word wrap to make all that text fit there
        self.textLabel.setOpenExternalLinks(True)
        self.textLabel.setAlignment(Qt.AlignCenter)
        self.textLabel.setGeometry(0, 100, 300, 100) # Some adjustments to the geometry, so that all the text fits
        
        # Show the window
        self.about.show()


    # Add a file to the recent files list
    def addRecentFile(self, file):
        if file not in self.recentFiles:
            self.recentFiles.insert(0, file) # Insert the file at the beginning
        else:
            self.recentFiles.remove(file) # Remove the file if it already exists
            self.recentFiles.insert(0, file) # Insert the file at the beginning
        self.recentFiles = self.recentFiles[:5] # Keep only the last 5 files
        self.updateRecentFiles() # Update the recent files list


    # Update the recent files list method
    def updateRecentFiles(self):
        self.startPage.clear() # Clear the start page
        for file in self.recentFiles:
            item = QListWidgetItem() # Create a list item
            item.setText(QFileInfo(file).fileName()) # Set the item text to the file name
            item.setIcon(QIcon(file_selector.select('icons/NewLook/document.png'))) # Set the item icon to the document icon
            item.setToolTip(file) # Set the item tooltip to the file path
            self.startPage.addItem(item) # Add the item to the start page


    # Open start page method
    def startPageOpen(self):
        self.startPage = QListWidget() # Create a list widget
        self.startPage.setWindowIcon(QIcon('icons/NewLook/editor.png')) # Set the window icon
        self.startPage.setWindowTitle('Start Page') # Set the window title
        self.startPage.setFixedSize(300, 200) # Set the window size
        self.startPage.itemDoubleClicked.connect(self.openRecentFile) # Connect the item double clicked signal to the open recent file slot
        self.startPage.show() # Show the start page


    # Open recent file method
    def openRecentFile(self, item):
        # Open a recent file
        file = item.toolTip() # Get the file path from the item tooltip
        try:
            with open(file, 'r') as f: # Use with statement to simplify file handling
                data = f.read()
                self.textEdit.setText(data)
                self.addRecentFile(file) # Add the file to the recent files list
        except Exception as e:
            print(f"log> Handled the error: {e}")


    # A method save settings from the current session
    def closeEvent(self, event):
        # Save the settings before closing
        self.settings.setValue('geometry', self.saveGeometry())
        self.settings.setValue('windowState', self.saveState())
        self.settings.setValue('recentFiles', self.recentFiles)
        event.accept()


# Launch the program
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = TextEditor()
    sys.exit(app.exec_())
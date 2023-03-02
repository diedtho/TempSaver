import os
import re
import shutil
from datetime import datetime
from PySide6 import QtCore, QtWidgets

class MyWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        # GUI-Elemente erstellen
        self.button = QtWidgets.QPushButton("Temp-Dateien sichern")
        self.label = QtWidgets.QLabel("Noch keine Sicherung durchgeführt")
        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(self.button)
        layout.addWidget(self.label)

        # Verzeichnisse und Startzeitpunkt initialisieren
        self.source_dir = "D:\\Temp"
        self.target_dir = "D:\\Backup-Save"
        self.start_time = datetime.now()

        # Button-Klick-Event hinzufügen
        self.button.clicked.connect(self.backup_temp_files)

    def backup_temp_files(self):
        # Zielordner mit Zeitstempel + Command erstellen
        command = ""
        with open(r'D:\Temp\INSCommand.ini', 'r', encoding='utf-8') as fr:
            for line in fr.readlines():
                if line.startswith('Command='):
                    command = re.sub(r'^Command=(.*)\n$', r'\1', line)
        current_time = datetime.now()
        target_folder_name = current_time.strftime("%H%M%S") + "_" + command
        target_folder_path = os.path.join(self.target_dir, target_folder_name)
        os.makedirs(target_folder_path)

        # Dateien kopieren, die zwischen Startzeit und Klickzeitpunkt geändert wurden
        for filename in os.listdir(self.source_dir):
            if 'TmP' not in filename and '.tmp' not in filename and 'EvaTrace' not in filename:
                file_path = os.path.join(self.source_dir, filename)
                modification_time = datetime.fromtimestamp(os.path.getmtime(file_path))
                if self.start_time <= modification_time < current_time:
                    shutil.copy(file_path, target_folder_path)
                # INSRunExt-Trace und -Log-Datei im Temp-Ordner löschen
                if 'INSTraceFile' in filename or 'INSLogFile' in filename:
                    os.remove(file_path)


        # Startzeitpunkt aktualisieren
        self.start_time = current_time

        # Label aktualisieren
        self.label.setText(f"Sicherung erstellt: {target_folder_name}")

if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    widget = MyWidget()
    widget.show()
    app.exec()

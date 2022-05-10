import sys

from PySide6.QtWidgets import (QApplication, QDialog,
                               QDialogButtonBox, QGroupBox,
                               QLineEdit,
                               QVBoxLayout)


class WhatsUpDialog(QDialog):
    num_grid_rows = 3
    num_buttons = 4

    def __init__(self):
        super().__init__()

        edit_box = QGroupBox("What's updog?")
        edit_box_layout = QVBoxLayout()
        self._editor = QLineEdit()
        edit_box_layout.addWidget(self._editor)
        edit_box.setLayout(edit_box_layout)

        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)

        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)

        main_layout = QVBoxLayout()
        main_layout.addWidget(edit_box)
        main_layout.addWidget(button_box)
        self.setLayout(main_layout)

        self.setWindowTitle("Daagliks")
        self.setMinimumWidth(512)

    def accept(self) -> None:
        print(self._editor.text())
        super().accept()

    def reject(self) -> None:
        print('Rejected')
        super().reject()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    dialog = WhatsUpDialog()

    sys.exit(dialog.exec())

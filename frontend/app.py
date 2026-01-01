import sys
import requests
from PySide6.QtWidgets import (
    QApplication, QWidget, QGridLayout, QLineEdit,
    QPushButton, QMessageBox, QVBoxLayout, QLabel
)
from PySide6.QtCore import Qt

API_URL = "http://localhost:8080/solve"


class SudokuApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sudoku Solver")
        self.setFixedSize(420, 540)

        title = QLabel("Sudoku Solver")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size:26px; font-weight:bold;")

        self.grid_layout = QGridLayout()
        self.grid_layout.setSpacing(0)

        self.cells = [[QLineEdit() for _ in range(9)] for _ in range(9)]

        for r in range(9):
            for c in range(9):
                cell = self.cells[r][c]
                cell.setFixedSize(42, 42)
                cell.setMaxLength(1)
                cell.setAlignment(Qt.AlignCenter)

                # Border logic for clean 3x3 boxes
                top = "2px" if r % 3 == 0 else "1px"
                left = "2px" if c % 3 == 0 else "1px"
                right = "2px" if c == 8 else "1px"
                bottom = "2px" if r == 8 else "1px"

                cell.setStyleSheet(f"""
                    QLineEdit {{
                        font-size: 18px;
                        font-weight: 500;
                        border-top: {top} solid black;
                        border-left: {left} solid black;
                        border-right: {right} solid black;
                        border-bottom: {bottom} solid black;
                        padding: 0px;
                        background-color: white;
                        qproperty-alignment: AlignCenter;
                    }}
                """)

                self.grid_layout.addWidget(cell, r, c)

        self.solve_btn = QPushButton("Solve Sudoku")
        self.solve_btn.setFixedHeight(48)
        self.solve_btn.setStyleSheet("""
            QPushButton {
                background-color: #2c7be5;
                color: white;
                font-size:16px;
                font-weight:600;
                border-radius:10px;
            }
            QPushButton:hover {
                background-color: #1a5fd0;
            }
        """)
        self.solve_btn.clicked.connect(self.solve)

        layout = QVBoxLayout()
        layout.addWidget(title)
        layout.addSpacing(12)
        layout.addLayout(self.grid_layout)
        layout.addSpacing(22)
        layout.addWidget(self.solve_btn)

        self.setLayout(layout)

    def solve(self):
        grid = []

        for r in range(9):
            row = []
            for c in range(9):
                text = self.cells[r][c].text()
                row.append(int(text) if text.isdigit() else 0)
            grid.append(row)

        try:
            response = requests.post(API_URL, json={"grid": grid})
            response.raise_for_status()

            solved = response.json()
            for r in range(9):
                for c in range(9):
                    self.cells[r][c].setText(str(solved[r][c]))

        except Exception:
            QMessageBox.critical(self, "Error", "No valid solution found!")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SudokuApp()
    window.show()
    sys.exit(app.exec())

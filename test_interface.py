import sys

try:
    from PySide6.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QWidgetItem, QPushButton, QLabel, QTextEdit, QProgressBar, QGroupBox)
    from PySide6.QtCore import Qt, QTimer
    from PySide6.QtGui import QPixmap, QFont
    UI_FRAMEWORK = "PySide6"
    print(f"Using {UI_FRAMEWORK}")

except ImportError:
    try:
        from PySide6.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QPushButton, QLabel, QTextEdit, QProgressBar, QGroupBox)
        from PySide6.QtCore import Qt, QTimer
        from PySide6.QtGui import QPixmap, QFont
        UI_FRAMEWORK = "PyQt6"
        print(f"Using {UI_FRAMEWORK}")

    except ImportError:
        sys.exit(1)

class OculusTestWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.setup_timer()

    def initUI(self):
        self.setWindowTitle("Oculus Test")
        self.setGeometry(100, 100, 800, 600)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)

        self.create_control_panel(main_layout)

        self.create_video_panel(main_layout)

    def create_control_panel(self, main_layout):
        control_group = QGroupBox("Control Panel")
        control_layout = QVBoxLayout()
        control_group.setLayout(control_layout)
        control_group.setMaximumWidth(300)

        self.btn_start = QPushButton("Start")
        self.btn_start.setStyleSheet("QPushButton { background-color: rgb(255, 255, 255); }")
        self.btn_start.clicked.connect(self.toggle_detection)

        self.btn_screenshot = QPushButton("Screenshot")
        self.btn_screenshot.setStyleSheet("QPushButton { background-color: rgb(255, 255, 255); }")
        self.btn_screenshot.clicked.connect(self.take_screenshot)

        self.btn_settings = QPushButton("Settings")
        self.btn_settings.clicked.connect(self.show_settings)

        stats_group = QGroupBox("Stats")
        stats_layout = QVBoxLayout()
        stats_group.setLayout(stats_layout)

        self.lbl_fps = QLabel("FPS: 0")
        self.lbl_objects = QLabel("Objects: 0")
        self.lbl_processing = QLabel("Processing: 0ms")

        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)

        log_group = QGroupBox("Log")
        log_layout = QVBoxLayout()
        log_group.setLayout(log_layout)

        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        self.log_text.setMaximumHeight(150)

        control_layout.addWidget(self.btn_start)
        control_layout.addWidget(self.btn_screenshot)
        control_layout.addWidget(self.btn_settings)
        control_layout.addWidget(stats_group)

        stats_layout.addWidget(self.lbl_fps)
        stats_layout.addWidget(self.lbl_objects)
        stats_layout.addWidget(self.lbl_processing)
        stats_layout.addWidget(self.progress_bar)

        control_layout.addWidget(log_group)
        log_layout.addWidget(self.log_text)

        control_layout.addStretch()
        main_layout.addWidget(control_group)

    def create_video_panel(self, main_layout):
        video_group = QGroupBox("Video")
        video_layout = QVBoxLayout()
        video_group.setLayout(video_layout)

        self.video_label = QLabel()
        self.video_label.setStyleSheet("""
                    QLabel {
                        background-color: #1e1e1e;
                        border: 2px solid #555;
                        color: white;
                        font-size: 16px;
                        text-align: center;
                    }
                """)
        self.video_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.video_label.setText("Video flux with detection")
        self.video_label.setMinimumSize(480, 360)

        video_layout.addWidget(self.video_label)
        main_layout.addWidget(video_group)

    def setup_timer(self):
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_simulation)
        self.frame_count = 0
        self.is_detecting = False

    def toggle_detection(self):
        if not self.is_detecting:
            self.is_detecting = True
            self.btn_start.setText("Stop")
            self.btn_start.setStyleSheet(
                "QPushButton { background-color: #f44336; color: white; font-size: 14px; padding: 10px; }")
            self.timer.start(100)
            self.log("Detection started")
        else:
            self.is_detecting = False
            self.btn_start.setText("Start Détection")
            self.btn_start.setStyleSheet(
                "QPushButton { background-color: #4CAF50; color: white; font-size: 14px; padding: 10px; }")
            self.timer.stop()
            self.log("Detection stopped")

    def update_simulation(self):
        self.frame_count += 1

        fps = 15 + (self.frame_count % 10)
        objects = (self.frame_count % 8) + 1
        processing_time = 75 + (self.frame_count % 30)

        self.lbl_fps.setText(f"FPS: {fps}")
        self.lbl_objects.setText(f"Objects detected: {objects}")
        self.lbl_processing.setText(f"Time process: {processing_time}ms")

        progress = (self.frame_count * 3) % 100
        self.progress_bar.setValue(progress)

        status_text = f"DETECTION ACTIV\n\nFrame: {self.frame_count}\nObjets: {objects}\nFPS: {fps}"
        self.video_label.setText(status_text)

    def take_screenshot(self):
        self.log(f"Screenshot_{self.frame_count:04d}.jpg saved")

    def show_settings(self):
        self.log("Settings")

    def log(self, message):
        self.log_text.append(f"[{self.frame_count:04d}] {message}")
        scrollbar = self.log_text.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())


def main():
    print(f"🎯 OCULUS - Test Interface ({UI_FRAMEWORK})")
    print("=" * 50)

    app = QApplication(sys.argv)

    window = OculusTestWindow()
    window.show()

    print("✅ Interface started")

    try:
        result = app.exec()
        print("✅ Interface closed")
        return True
    except Exception as e:
        print(f"❌ Error interface: {e}")
        return False


if __name__ == "__main__":
    success = main()
    if success:
        print("\n🎉 SUCCESS !")
    else:
        print("\n💥 ERROR")
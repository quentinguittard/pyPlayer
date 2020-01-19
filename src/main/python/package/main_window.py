from functools import partial

from PySide2 import QtWidgets, QtMultimedia, QtMultimediaWidgets, QtCore


class MainWindow(QtWidgets.QMainWindow):
    """This is a class to create the main window of the application."""

    def __init__(self):
        """The constructor of the main window."""
        super().__init__()
        self.setWindowTitle("pyPlayer")

        self.open_icon = self.style().standardIcon(QtWidgets.QStyle.SP_DriveDVDIcon)
        self.play_icon = self.style().standardIcon(QtWidgets.QStyle.SP_MediaPlay)
        self.previous_icon = self.style().standardIcon(QtWidgets.QStyle.SP_MediaSkipBackward)
        self.pause_icon = self.style().standardIcon(QtWidgets.QStyle.SP_MediaPause)
        self.stop_icon = self.style().standardIcon(QtWidgets.QStyle.SP_MediaStop)

        self.setup_ui()

    def setup_ui(self):
        """Setup the user interface of the application."""
        self.create_widgets()
        self.modify_widgets()
        self.create_layouts()
        self.add_widgets_to_layouts()
        self.setup_connections()

    def create_widgets(self):
        """Create the widgets of the application."""
        self.video_widget = QtMultimediaWidgets.QVideoWidget()
        self.player = QtMultimedia.QMediaPlayer()
        self.toolbar = QtWidgets.QToolBar()
        self.file_menu = self.menuBar().addMenu("File")

        # ACTIONS

        self.act_open = self.file_menu.addAction(self.open_icon, "Open")
        self.act_open.setShortcut("Ctrl+O")
        self.act_play = self.toolbar.addAction(self.play_icon, "Play")
        self.act_previous = self.toolbar.addAction(self.previous_icon, "Back")
        self.act_pause = self.toolbar.addAction(self.pause_icon, "Pause")
        self.act_stop = self.toolbar.addAction(self.stop_icon, "Stop")

    def add_widgets_to_layouts(self):
        """Add created widgets to the user interface layout."""
        self.addToolBar(self.toolbar)
        self.setCentralWidget(self.video_widget)
        self.player.setVideoOutput(self.video_widget)

    def setup_connections(self):
        """Setup the connections between the widgets and their functions."""
        self.act_open.triggered.connect(self.open)
        self.act_play.triggered.connect(self.player.play)
        self.act_pause.triggered.connect(self.player.pause)
        self.act_stop.triggered.connect(self.player.stop)
        self.act_previous.triggered.connect(partial(self.player.setPosition, 0))
        self.player.stateChanged.connect(self.update_buttons)

    def open(self):
        """Open a dialog to select a video file and play it."""
        file_dialog = QtWidgets.QFileDialog(self)
        file_dialog.setMimeTypeFilters(["video/mp4"])
        movies_dir = QtCore.QStandardPaths.writableLocation(QtCore.QStandardPaths.MoviesLocation)
        file_dialog.setDirectory(movies_dir)
        if file_dialog.exec_() == QtWidgets.QDialog.Accepted:
            movie = file_dialog.selectedUrls()[0]
            self.player.setMedia(movie)
            self.player.play()

    def update_buttons(self, state):
        """Update video player buttons depending of its state.

        :param state: The state of the media player.
        :type state: QtMultimedia.QMediaPlayer.State
        """
        self.act_play.setDisabled(state == QtMultimedia.QMediaPlayer.PlayingState)
        self.act_pause.setDisabled(state == QtMultimedia.QMediaPlayer.PausedState)
        self.act_stop.setDisabled(state == QtMultimedia.QMediaPlayer.StoppedState)

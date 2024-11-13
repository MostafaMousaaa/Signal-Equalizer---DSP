import os
import sys
import numpy as np
import pandas as pd
import soundfile as sf
import scipy
from scipy import signal
import matplotlib.pyplot as plt
import plotly.graph_objs as go
import plotly.offline as pyo
import copy
 
from PyQt5 import QtWidgets, QtCore, uic
from PyQt5.QtWidgets import QMessageBox, QApplication, QVBoxLayout, QWidget
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtCore import QUrl
from PyQt5.QtGui import QIcon

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

from classes import FileBrowser
from UITEAM15 import Ui_MainWindow  # Import the Ui_MainWindow class

class MainApp(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MainApp, self).__init__()
        self.setupUi(self)
        self.setupUI()
        self.connectSignals()

        
        # Initialize QMediaPlayer
        self.player = QMediaPlayer()
       
        # Track if a signal has been uploaded
        self.is_audio_uploaded = False
        self.timer = QtCore.QTimer(self)  # Timer for updating the plot
        self.timer.timeout.connect(self.updatePlot)  # Connect to a method to update the plot
        self.current_position = 0  # Track the current position in the signal

    def setupUI(self):
        """Setup UI elements and initial configurations."""
        # Link input and output view boxes
        self.inputViewBox = self.PlotWidget_inputSignal.getViewBox()
        self.outputViewBox = self.PlotWidget_outputSignal.getViewBox()
        self.inputViewBox.setXLink(self.outputViewBox)
        self.inputViewBox.setYLink(self.outputViewBox)
        self.PlotWidget_fourier.setLabel('left', 'Magnitude')
        self.PlotWidget_fourier.setLabel('bottom', 'Frequency')
        self.pushButton_playPause.setText("Play")
        self.pushButton_stop.setText("Rewind")
        self.pushButton_zoomIn.setText("Zoom In")
        self.pushButton_zoomOut.setText("Zoom Out")
        self.speedSlider.setMinimum(50)
        self.speedSlider.setMaximum(150)
        self.speedSlider.setValue(100)
        
   
    

    def connectSignals(self):
        """Connect UI signals to their respective slots."""
        self.pushButton_uploadButton.clicked.connect(self.uploadAndPlotSignal)
        self.pushButton_playPause.clicked.connect(self.togglePlayPause)
        self.pushButton_zoomIn.clicked.connect(lambda: self.zoom(0.8))
        self.pushButton_zoomOut.clicked.connect(lambda: self.zoom(1.25))
        self.pushButton_stop.clicked.connect(self.stopAndReset)
        self.checkBox_showSpectrogram.stateChanged.connect(self.showAndHideSpectrogram)
        self.comboBox_frequencyScale.activated.connect(self.setFrequencyScale)

        # Connect the speed slider to the setSpeed function
        self.speedSlider.valueChanged.connect(self.setSpeed)




    def setMode(self, mode):
        """Set the mode of the application."""
        pass

    def uploadAndPlotSignal(self):
        """Upload and plot the signal."""
        file_path, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Open Audio File", "", "Audio Files (*.wav *.mp3)")
        
        if file_path:
            try:
                audio_data, sample_rate = sf.read(file_path)
                if audio_data.ndim == 2:
                    audio_data = audio_data.mean(axis=1)
                self.audio_data = audio_data
                self.sample_rate = sample_rate
                self.plotSignal_timeDomain(audio_data, sample_rate, audio_data, self.PlotWidget_inputSignal)
                self.plotFrequencySpectrum()

                url = QUrl.fromLocalFile(file_path)
                self.player.setMedia(QMediaContent(url))

                # Mark audio as uploaded
                self.is_audio_uploaded = True

                QMessageBox.information(self, "Success", "Audio file uploaded and plotted successfully!")
            
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to read audio file: {e}")

    def updatePlot(self):
        """Update the plot based on the current position in the audio."""
        if not self.is_audio_uploaded:
            return

        # Get the current position of the audio in seconds
        current_time = self.player.position() / 1000  # Convert milliseconds to seconds
        
        # Update the plot to show the current segment of the signal
        time_segment = np.linspace(current_time, current_time + 1, num=self.sample_rate)  # 1 second segment
        signal_segment = self.audio_data[int(current_time * self.sample_rate):int((current_time + 1) * self.sample_rate)]
        self.plotSignal_timeDomain(self.audio_data, self.sample_rate, signal_segment, self.PlotWidget_inputSignal)
            


    def plotSignal_timeDomain(self, audio, audioSamplingRate, signal, widget):
        """Plot the signal in the time domain."""
        # Clear the widget
        widget.clear()
        
        # Create a time array based on the sampling rate and signal length
        time = np.linspace(0, len(signal) / audioSamplingRate, num=len(signal))
        
        # Plot the signal
        widget.plot(time, signal, pen="b")  # `pen="b"` sets the line color to blue
        
    def plotSpectrogram(self, fig, canvas, audio, audioSamplingRate, signal):
        """Plot the spectrogram of the signal."""
        pass

    def plotFrequencySpectrum(self):
        """Plot the frequency spectrum of the signal."""
        pass

    def computeFourierTransform(self):
        """Compute the Fourier transform"""
        pass

    def computeFourierTransform(self):
        """Compute the Fourier transform of the signal."""
        pass

    def invFourierTransform(self, magnitude, phase):
        """Compute the inverse Fourier transform."""
        pass

    def setFrequencyScale(self):
        """Set the smoothing window."""
        pass

    def setWindowParameters(self):
        """Set the parameters for the smoothing window."""
        pass

    def getMappedSliderValue(self, slider_value):
        """Get the mapped value of the slider."""
        pass

    def generateWindow(self, sliderNumber, Value):
        """Generate the window for smoothing."""
        pass

    def applySmoothingWindow(self, gainList, targetBand):
        """Apply the smoothing window."""
        pass

    def togglePlayPause(self):
        """Toggle play/pause of the signal and update button text."""
        if not self.is_audio_uploaded:
            self.pushButton_playPause.setText("Play")  # Default to "Play" if no audio is uploaded
            return  # Don't perform any actions if no audio has been uploaded

        # Check if the player is currently playing
        if self.player.state() == QMediaPlayer.PlayingState:
            self.player.pause()  # Pause the player
            self.pushButton_playPause.setText("Play")  # Update button text to "Play"
            self.timer.stop()  # Stop the timer when paused
            print("Player paused")
        else:
            self.player.play()  # Start playing the audio
            self.pushButton_playPause.setText("Pause")  # Update button text to "Pause"
            self.timer.start(50)  # Start the timer to update the plot every 50ms
            print("Player playing")



    def setSpeed(self):
        """Adjust playback speed based on the speed slider's value."""
        if not self.is_audio_uploaded:
            return  # Do nothing if no audio has been uploaded

        # Map the slider value to playback speed: 100 is 1.0x, lower is slower, higher is faster
        slider_value = self.speedSlider.value()
        playback_speed = slider_value / 100.0  # Convert to playback speed factor (0.5 - 1.5)

        # Set the playback rate
        self.player.setPlaybackRate(playback_speed)

        print(f"Playback speed set to {playback_speed}x")



    def stopAndReset(self):
        """Stop, reset, and play the signal from the beginning if currently playing."""
        if not self.is_audio_uploaded:
            return  # No audio uploaded, so nothing to reset

        # Check if the player is currently playing
        is_playing = self.player.state() == QMediaPlayer.PlayingState

        # Stop the audio playback
        self.player.stop()
        self.pushButton_playPause.setText("Play")  # Reset play button text initially

        # Reset the player position to the beginning (rewind)
        self.player.setPosition(0)  # Rewind to the start
        self.current_position = 0  # Reset the position tracker

        # Reset the plot to show the first part of the signal
        self.plotSignal_timeDomain(self.audio_data, self.sample_rate, 
                                self.audio_data[:self.sample_rate], self.PlotWidget_inputSignal)

        # Stop the timer if running
        self.timer.stop()

        # If the audio was playing before pressing rewind, start playing from the beginning
        if is_playing:
            self.player.play()
            self.pushButton_playPause.setText("Pause")  # Update to "Pause" since it's now playing
            self.timer.start(50)  # Restart the timer to update the plot

        print("Audio reset to the beginning", "and started playing" if is_playing else "and is paused")



    def zoom(self, factor):
        """Zoom in or out on the signal by adjusting the x-axis limits."""
        # Ensure audio is uploaded
        if not self.is_audio_uploaded:
            return
        
        # Get the current x-axis range
        x_min, x_max = self.PlotWidget_inputSignal.viewRange()[0]
        current_range = x_max - x_min

        # Calculate the new range based on the zoom factor
        new_range = current_range * factor

        # Calculate the center of the current view to keep the zoom centered
        center = (x_min + x_max) / 2
        x_min_new = max(0, center - new_range / 2)
        x_max_new = min(len(self.audio_data) / self.sample_rate, center + new_range / 2)

        # Set the new x-axis range
        self.PlotWidget_inputSignal.setXRange(x_min_new, x_max_new)
        print(f"Zoom applied: factor={factor}, new range=({x_min_new}, {x_max_new})")


    def showAndHideSpectrogram(self, state):
        """Show or hide the spectrogram."""
        pass

    def get_min_max_for_widget(self, widget, data_type):
        """Get the min and max values for the widget."""
        pass

    def clearAll(self):
        """Clear all data and reset the UI."""
        pass

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainApp()
    window.show()
    sys.exit(app.exec_())

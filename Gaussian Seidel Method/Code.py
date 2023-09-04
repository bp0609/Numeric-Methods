import sys
import os
import random
import matplotlib
# Make sure that we are using QT5
matplotlib.use('Qt5Agg')
from PyQt5 import QtCore, QtWidgets

import numpy as np
import matplotlib
from numpy import arange, sin, pi
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.animation import FuncAnimation
from matplotlib import pyplot
import scipy.signal

progname = os.path.basename(sys.argv[0])

class MyMplCanvas(FigureCanvas):
    """Ultimately, this is a QWidget (as well as a FigureCanvasAgg, etc.)."""

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = self.fig.add_subplot(111, autoscale_on=True)

        FigureCanvas.__init__(self, self.fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self,
                                   QtWidgets.QSizePolicy.Expanding,
                                   QtWidgets.QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

    def compute_initial_figure(self):
        pass


class BaseDynamicMplCanvas(MyMplCanvas):
    """Base class for drawing canvas"""

    def __init__(self, *args, **kwargs):
        self.initialfilter = (np.array([0.0]), np.array([1.0]))
        self.finalfilter = (np.array([1.0]), np.array([1.0]))
        if 'initialfilter' in kwargs:
            self.initialfilter = kwargs.pop('initialfilter')
        if 'finalfilter' in kwargs:
            self.finalfilter = kwargs.pop('finalfilter')
        MyMplCanvas.__init__(self, *args, **kwargs)

    def update_filter(self, newfilter):
        self.initialfilter = self.finalfilter
        self.finalfilter = newfilter

class MyDynamicFreqAnimation(BaseDynamicMplCanvas):

    def __init__(self, *args, **kwargs):
        self.phase_mode = False
        if 'phase_mode' in kwargs:
            self.phase_mode = kwargs.pop('phase_mode')
        BaseDynamicMplCanvas.__init__(self, *args, **kwargs)
        self.ln, = self.axes.plot([], [], animated=True)
        self.phase_correction = 0.0
        self.compute_initial_figure()

    def prettify_plot(self):
        self.axes.grid(True)
        self.axes.set_xlabel(r"$\omega$")
        if self.phase_mode:
            self.axes.set_ylabel(r"$\angle H(e^{j\omega})$ (rad)")
        else:
            self.axes.set_ylabel(r"$|H(e^{j\omega})|^2$ (dB)")
        x = np.arange(0.0, 1.1, 0.2)
        axtext = [("$" + str(i)[:3] + "\pi$") for i in x]
        axtext[0] = "0"
        axtext[-1] = "$\pi$"
        self.axes.set_xticks(x * np.pi)
        self.axes.set_xticklabels(axtext)
        self.axes.set_xlim(0.0, np.pi)
        if self.phase_mode:
            self.axes.set_yticks([-np.pi, 0, np.pi])
            self.axes.set_yticklabels(['$-\pi$', 0, '$\pi$'])
            self.axes.set_ylim(-np.pi, np.pi)
        else:
            self.axes.set_ylim((-50, 20))
        self.axes.grid(True)

    def compute_initial_figure(self):
        w, self.response_initial = scipy.signal.freqz(self.initialfilter[0], self.initialfilter[1])
        self.w, self.response_final = scipy.signal.freqz(self.finalfilter[0], self.finalfilter[1])
        self.prettify_plot()
        if self.phase_mode:
            self.ln.set_data(w, np.unwrap(np.angle(self.response_initial) - self.phase_correction * self.w))
        else:
            resp = 20*np.log10(np.abs(self.response_initial))
            self.ln.set_data(w, resp)
        return self.ln,

    def advance_animation(self, frame):
        ALPHA = frame / 200
        response = (1 - ALPHA) * self.response_initial + ALPHA * self.response_final
        self.ln.set_xdata(self.w)
        if self.phase_mode:
            self.ln.set_ydata(np.unwrap(np.angle(response) - self.phase_correction * self.w))
        else:
            self.ln.set_ydata(20*np.log10(np.abs(response)))
        return self.ln,

    def update_filter(self, newfilter, phase_correction=0.0):
        BaseDynamicMplCanvas.update_filter(self, newfilter)
        self.phase_correction = float(phase_correction)
        self.ani = FuncAnimation(self.fig, self.advance_animation, frames=np.r_[0:201],
                                     init_func=self.compute_initial_figure,
                                blit=True, interval=5,repeat=False)
        self.draw()

class MyDynamicPoleZeroAnimation(BaseDynamicMplCanvas):

    def __init__(self, *args, **kwargs):
        BaseDynamicMplCanvas.__init__(self, *args, **kwargs)
        self.ln_zeros, = self.axes.plot([], [], 'ro', animated=True)
        self.ln_poles, = self.axes.plot([], [], 'bx', animated=True)
        self.compute_initial_figure()

    def prettify_plot(self):
        self.axes.grid(True)
        self.axes.set_xlabel(r"Re($z$)")
        self.axes.set_ylabel(r"Im($z$)")
        self.axes.set_xlim((-2, 2))
        self.axes.set_ylim((-2, 2))
        self.axes.set_aspect(1)
        self.axes.grid(True)
        c = pyplot.Circle((0, 0), 1, fill=False, lw=2)
        self.axes.add_artist(c)

    def clean_polezero_sizes(self):
        if len(self.initial_zeros) < len(self.final_zeros):
            c = np.zeros(len(self.final_zeros), dtype='complex128')
            c[:len(self.initial_zeros)] += self.initial_zeros
            self.initial_zeros = c
        elif len(self.final_zeros) < len(self.initial_zeros):
            c = np.zeros(len(self.initial_zeros), dtype='complex128')
            c[:len(self.final_zeros)] += self.final_zeros
            self.final_zeros = c

        if len(self.initial_poles) < len(self.final_poles):
            c = np.zeros(len(self.final_poles), dtype='complex128')
            c[:len(self.initial_poles)] += self.initial_poles
            self.initial_poles = c
        elif len(self.final_poles) < len(self.initial_poles):
            c = np.zeros(len(self.initial_poles), dtype='complex128')
            c[:len(self.final_poles)] += self.final_poles
            self.final_poles = c

    def compute_initial_figure(self):
        self.initial_zeros = np.array(np.roots(self.initialfilter[0]), dtype='complex128')
        self.final_zeros = np.array(np.roots(self.finalfilter[0]), dtype='complex128')
        self.initial_poles = np.array(np.roots(self.initialfilter[1]), dtype='complex128')
        self.final_poles = np.array(np.roots(self.finalfilter[1]), dtype='complex128')
        self.clean_polezero_sizes()

        self.prettify_plot()
        self.ln_zeros.set_data(np.real(self.initial_zeros), np.imag(self.initial_zeros))
        self.ln_poles.set_data(np.real(self.initial_poles), np.imag(self.initial_poles))
        return self.ln_zeros, self.ln_poles,

    def advance_animation(self, frame):
        ALPHA = frame / 200
        poles = (1 - ALPHA) * self.initial_poles + ALPHA * self.final_poles
        zeros = (1 - ALPHA) * self.initial_zeros + ALPHA * self.final_zeros
        self.ln_zeros.set_data(np.real(zeros), np.imag(zeros))
        self.ln_poles.set_data(np.real(poles), np.imag(poles))
        return self.ln_zeros, self.ln_poles,

    def update_filter(self, newfilter, phase_correction=0.0):
        BaseDynamicMplCanvas.update_filter(self, newfilter)
        self.initial_zeros = np.array(np.roots(self.initialfilter[0]), dtype='complex128')
        self.final_zeros = np.array(np.roots(self.finalfilter[0]), dtype='complex128')
        self.initial_poles = np.array(np.roots(self.initialfilter[1]), dtype='complex128')
        self.final_poles = np.array(np.roots(self.finalfilter[1]), dtype='complex128')
        self.clean_polezero_sizes()
        self.ani = FuncAnimation(self.fig, self.advance_animation, frames=np.r_[0:201],
                                     init_func=self.compute_initial_figure,
                                blit=True, interval=5,repeat=False)
        self.draw()

class MyDynamicMplImpResponse(BaseDynamicMplCanvas):
    """A canvas that updates itself every second with a new plot."""

    def __init__(self, *args, **kwargs):
        BaseDynamicMplCanvas.__init__(self, *args, **kwargs)
        self.compute_initial_figure()
        self.delay = 0

    def prettify_plot(self):
        self.xmax = min([max(len(self.response_final), len(self.response_initial)), 100])
        self.axes.set_xlim(-1 + self.delay, self.xmax + 1 + self.delay)
        self.ymax = max([np.max(self.response_final), np.max(self.response_initial)]) + 0.1
        self.ymin = min([np.min(self.response_final), np.min(self.response_initial)]) - 0.1
        if abs(self.ymax - self.ymin) < 0.3:
            self.ymin = 0

    def compute_initial_figure(self, delay=0):
        self.delay = delay
        x = np.zeros(max(len(self.initialfilter[0]), len(self.finalfilter[0])) + 1)
        if len(self.initialfilter[1]) > 0:
            # IIR filter
            x = np.zeros(50)
        x[0] = 1.0
        self.axes.cla()
        self.response_initial = scipy.signal.lfilter(self.initialfilter[0], self.initialfilter[1], x)
        self.response_final = scipy.signal.lfilter(self.finalfilter[0], self.finalfilter[1], x)
        self.prettify_plot()
        self.axes.stem(np.r_[self.delay:self.delay+len(self.response_final)],self.response_final)

    def update_filter(self, newfilter, delay=0):
        BaseDynamicMplCanvas.update_filter(self, newfilter)
        self.delay = int(delay)
        self.compute_initial_figure(delay=self.delay)
        self.draw()

class ApplicationWindow(QtWidgets.QMainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.setWindowTitle("application main window")

        self.main_widget = QtWidgets.QWidget(self)

        l = QtWidgets.QGridLayout(self.main_widget)
        initialfilter = (np.array([1.0, 0.5]), np.array([1.0]))
        finalfilter = initialfilter
        self.ir = MyDynamicMplImpResponse(self.main_widget, width=5, height=4, dpi=100,
                                              initialfilter=initialfilter,
                                              finalfilter=finalfilter)
        self.mr = MyDynamicFreqAnimation(self.main_widget, width=5, height=4, dpi=100,
                                         initialfilter=initialfilter,
                                         finalfilter=finalfilter)
        self.pr = MyDynamicFreqAnimation(self.main_widget,phase_mode=True, width=5, height=4, dpi=100,
                                         initialfilter=initialfilter,
                                         finalfilter=finalfilter)
        self.pz = MyDynamicPoleZeroAnimation(self.main_widget, width=4, height=4, dpi=100,
                                                 initialfilter=initialfilter,
                                                 finalfilter=finalfilter)
        l.addWidget(self.ir, 0, 0)
        l.addWidget(self.mr, 0, 1)
        l.addWidget(self.pr, 1, 1)
        l.addWidget(self.pz, 1, 0)

        self.lineEdit1 = QtWidgets.QLineEdit()
        self.lineEdit2 = QtWidgets.QLineEdit()
        self.lineEdit1.setText("1,0.5")
        self.lineEdit2.setText("1")
        self.update_button = QtWidgets.QPushButton("Update")
        self.update_button.clicked.connect(self.update_filter_coeffs)
        v = QtWidgets.QVBoxLayout()
        v.addStretch(1)
        self.zeros_label = QtWidgets.QLabel("<b>Zeros:</b>")
        self.poles_label = QtWidgets.QLabel("<b>Poles:</b>")
        v.addWidget(self.zeros_label)
        v.addWidget(self.poles_label)
        v.addWidget(QtWidgets.QLabel("b:"))
        v.addWidget(self.lineEdit1)
        v.addWidget(QtWidgets.QLabel("a:"))
        v.addWidget(self.lineEdit2)
        v.addWidget(self.update_button)
        l.addLayout(v, 2, 0)

        v2 = QtWidgets.QHBoxLayout()
        self.lineEdit3 = QtWidgets.QLineEdit()
        self.lineEdit3.setText("0")
        v2.addWidget(QtWidgets.QLabel("Delay:"))
        v2.addWidget(self.lineEdit3)
        l.addLayout(v2, 2, 1)

        self.main_widget.setFocus()
        self.setCentralWidget(self.main_widget)

    def update_filter_coeffs(self):
        b = np.array([float(i) for i in self.lineEdit1.text().split(',')])
        a = np.array([float(i) for i in self.lineEdit2.text().split(',')])
        self.pr.update_filter((b, a), self.lineEdit3.text())
        self.mr.update_filter((b, a))
        self.ir.update_filter((b, a), self.lineEdit3.text())
        self.pz.update_filter((b, a))
        zeros = np.roots(b)
        poles = np.roots(a)
        format_roots = lambda x : ','.join(["%.2f + %.2f<i>j</i>" % (i.real, i.imag) for i in x])
        zeros_str = format_roots(zeros)
        poles_str = format_roots(poles)
        self.zeros_label.setText("<b>Zeros:</b>" + zeros_str)
        self.poles_label.setText("<b>Poles:</b>" + poles_str)

if __name__ == "__main__":
    matplotlib.rc('text', usetex=True)
    matplotlib.rc('text', usetex=True)
    matplotlib.rc('font', size=20)
    matplotlib.rc('axes', labelsize=20)
    matplotlib.rc('legend', fontsize='large')
    matplotlib.rc('xtick', labelsize=14)
    matplotlib.rc('ytick', labelsize=14)
    qApp = QtWidgets.QApplication(sys.argv)
    aw = ApplicationWindow()
    aw.setWindowTitle("%s" % progname)
    aw.show()
    aw.mr.update_filter(([1.0, 0.5], [1.0]))
    aw.pr.update_filter(([1.0, 0.5], [1.0]))
    aw.pz.update_filter(([1.0, 0.5], [1.0]))
    sys.exit(qApp.exec_())
#!/usr/bin/env python3

import wx
import wx.lib.newevent
import serial
import serial.threaded

import numpy as np
import matplotlib
matplotlib.use('WXAgg')
import matplotlib.pyplot

from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from matplotlib.backends.backend_wx import NavigationToolbar2Wx
from matplotlib.figure import Figure

def _float(x):
    try:
        return float(x)
    except:
        return 0


DataArrivedEvent, EVT_DATA_ARRIVED = wx.lib.newevent.NewEvent()

class PlotCanvas(wx.Panel):
    MAX_VALUES  = 500

    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        self.figure = Figure()
        self.axes = self.figure.add_subplot(111)
        self.canvas = FigureCanvas(self, -1, self.figure)
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.canvas, 1, wx.LEFT | wx.TOP | wx.GROW)
        self.SetSizer(self.sizer)
        self.Fit()
        self.tvals = np.array([])
        self.yvals = np.array([])
        self.plot, = self.axes.plot(self.tvals, self.yvals, color='blue', linewidth=2)
        self.navBar = NavigationToolbar2Wx(self.canvas)
        
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.navBar, 0, wx.EXPAND)
        self.sizer.Add(self.canvas, 1, wx.EXPAND)
        self.SetSizer(self.sizer)

    def push_values(self, tvals, yvals):
        self.tvals = np.concatenate((self.tvals, tvals))
        self.yvals = np.concatenate((self.yvals, yvals))
        sz = self.tvals.size
        if sz >= self.MAX_VALUES:
            self.tvals = self.tvals[(sz - self.MAX_VALUES):]
            self.yvals = self.yvals[(sz - self.MAX_VALUES):]
        self.plot.set_xdata(self.tvals)
        self.plot.set_ydata(self.yvals)
        self.axes.relim()
        self.axes.autoscale_view()
        self.canvas.draw()
        self.Refresh()

    def clear_values(self):
        self.tvals = []
        self.yvals = []
        self.plot.set_xdata(self.tvals)
        self.plot.set_ydata(self.yvals)
        self.axes.relim()
        self.axes.autoscale_view()
        self.canvas.draw()
        self.Refresh()

class MainFrame ( wx.Frame ):
    
    def __init__( self, parent, serial ):
        wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = wx.EmptyString, pos = wx.DefaultPosition, size = wx.Size( 1024,680 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )
        
        self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )
        
        bSizer1 = wx.BoxSizer( wx.VERTICAL )
        
        self.m_panel1 = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
        bSizer2 = wx.BoxSizer( wx.VERTICAL )
        
        self.m_staticText1 = wx.StaticText( self.m_panel1, wx.ID_ANY, u"Kp:", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText1.Wrap( -1 )
        bSizer2.Add( self.m_staticText1, 0, wx.EXPAND|wx.TOP|wx.RIGHT|wx.LEFT, 5 )
        
        self.m_sliderKp = wx.Slider( self.m_panel1, wx.ID_ANY, 0, -1000, 1000, wx.DefaultPosition, wx.DefaultSize, wx.SL_HORIZONTAL )
        bSizer2.Add( self.m_sliderKp, 0, wx.EXPAND|wx.TOP|wx.RIGHT|wx.LEFT, 5 )
        
        bSizer3 = wx.BoxSizer( wx.HORIZONTAL )
        
        self.m_textCtrlKpmin = wx.TextCtrl( self.m_panel1, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer3.Add( self.m_textCtrlKpmin, 0, wx.TOP|wx.RIGHT|wx.LEFT, 5 )
        
        
        bSizer3.AddStretchSpacer( 1 )
        
        self.m_textCtrlKp = wx.TextCtrl( self.m_panel1, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.TE_READONLY )
        bSizer3.Add( self.m_textCtrlKp, 0, wx.TOP|wx.RIGHT|wx.LEFT, 5 )
        
        
        bSizer3.AddStretchSpacer( 1 )
        
        self.m_textCtrlKpmax = wx.TextCtrl( self.m_panel1, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer3.Add( self.m_textCtrlKpmax, 0, wx.TOP|wx.RIGHT|wx.LEFT, 5 )
        
        
        bSizer2.Add( bSizer3, 0, wx.EXPAND, 5 )
        
        self.m_staticText3 = wx.StaticText( self.m_panel1, wx.ID_ANY, u"Ki:", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText3.Wrap( -1 )
        bSizer2.Add( self.m_staticText3, 0, wx.TOP|wx.RIGHT|wx.LEFT|wx.EXPAND, 5 )
        
        self.m_sliderKi = wx.Slider( self.m_panel1, wx.ID_ANY, 0, -1000, 1000, wx.DefaultPosition, wx.DefaultSize, wx.SL_HORIZONTAL )
        bSizer2.Add( self.m_sliderKi, 0, wx.EXPAND|wx.TOP|wx.RIGHT|wx.LEFT, 5 )
        
        bSizer4 = wx.BoxSizer( wx.HORIZONTAL )
        
        self.m_textCtrlKimin = wx.TextCtrl( self.m_panel1, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer4.Add( self.m_textCtrlKimin, 0, wx.TOP|wx.RIGHT|wx.LEFT, 5 )
        
        
        bSizer4.AddStretchSpacer( 1 )
        
        self.m_textCtrlKi = wx.TextCtrl( self.m_panel1, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.TE_READONLY )
        bSizer4.Add( self.m_textCtrlKi, 0, wx.TOP|wx.RIGHT|wx.LEFT, 5 )
        
        
        bSizer4.AddStretchSpacer( 1 )
        
        self.m_textCtrlKimax = wx.TextCtrl( self.m_panel1, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer4.Add( self.m_textCtrlKimax, 0, wx.TOP|wx.RIGHT|wx.LEFT, 5 )
        
        
        bSizer2.Add( bSizer4, 0, wx.EXPAND, 5 )
        
        self.m_staticText4 = wx.StaticText( self.m_panel1, wx.ID_ANY, u"Kd:", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText4.Wrap( -1 )
        bSizer2.Add( self.m_staticText4, 0, wx.EXPAND|wx.TOP|wx.RIGHT|wx.LEFT, 5 )
        
        self.m_sliderKd = wx.Slider( self.m_panel1, wx.ID_ANY, 0, -1000, 1000, wx.DefaultPosition, wx.DefaultSize, wx.SL_HORIZONTAL )
        bSizer2.Add( self.m_sliderKd, 0, wx.EXPAND|wx.TOP|wx.RIGHT|wx.LEFT, 5 )
        
        bSizer5 = wx.BoxSizer( wx.HORIZONTAL )
        
        self.m_textCtrlKdmin = wx.TextCtrl( self.m_panel1, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer5.Add( self.m_textCtrlKdmin, 0, wx.TOP|wx.RIGHT|wx.LEFT, 5 )
        
        
        bSizer5.AddStretchSpacer( 1 )
        
        self.m_textCtrlKd = wx.TextCtrl( self.m_panel1, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.TE_READONLY )
        bSizer5.Add( self.m_textCtrlKd, 0, wx.TOP|wx.RIGHT|wx.LEFT, 5 )
        
        
        bSizer5.AddStretchSpacer( 1 )
        
        self.m_textCtrlKdmax = wx.TextCtrl( self.m_panel1, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer5.Add( self.m_textCtrlKdmax, 0, wx.TOP|wx.RIGHT|wx.LEFT, 5 )
        
        
        bSizer2.Add( bSizer5, 0, wx.EXPAND, 5 )
        
        self.m_staticText5 = wx.StaticText( self.m_panel1, wx.ID_ANY, u"Desired Value", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText5.Wrap( -1 )
        bSizer2.Add( self.m_staticText5, 0, wx.EXPAND|wx.TOP|wx.RIGHT|wx.LEFT, 5 )
        
        self.m_textCtrlDesired = wx.TextCtrl( self.m_panel1, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer2.Add( self.m_textCtrlDesired, 0, wx.EXPAND|wx.TOP|wx.RIGHT|wx.LEFT, 5 )
        
        bSizer6 = wx.BoxSizer( wx.HORIZONTAL )
        
        
        bSizer6.AddStretchSpacer( 1 )
        
        self.m_buttonClear = wx.Button( self.m_panel1, wx.ID_ANY, u"Clear Graph", wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer6.Add( self.m_buttonClear, 0, wx.TOP|wx.LEFT, 5 )
        
        self.m_buttonReset = wx.Button( self.m_panel1, wx.ID_ANY, u"Send Reset", wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer6.Add( self.m_buttonReset, 0, wx.ALIGN_RIGHT|wx.TOP|wx.RIGHT|wx.LEFT, 5 )
        
        
        bSizer2.Add( bSizer6, 0, wx.EXPAND, 5 )
        
        self.m_plotCanvas = PlotCanvas(self.m_panel1)
        bSizer2.Add( self.m_plotCanvas, 1, wx.EXPAND|wx.TOP|wx.BOTTOM|wx.RIGHT|wx.LEFT, 5 )
        
        
        self.m_panel1.SetSizer( bSizer2 )
        self.m_panel1.Layout()
        bSizer2.Fit( self.m_panel1 )
        bSizer1.Add( self.m_panel1, 1, wx.EXPAND, 5 )
        
        
        self.SetSizer( bSizer1 )
        self.Layout()
        # self.m_statusBar = self.CreateStatusBar( 1, wx.ST_SIZEGRIP, wx.ID_ANY )
        
        self.Centre( wx.BOTH )
        
        # Connect Events
        self.m_sliderKp.Bind( wx.EVT_SCROLL, self.OnUpdated )
        self.m_textCtrlKpmin.Bind( wx.EVT_TEXT, self.OnUpdated )
        # self.m_textCtrlKp.Bind( wx.EVT_TEXT, self.OnUpdated )
        self.m_textCtrlKpmax.Bind( wx.EVT_TEXT, self.OnUpdated )
        self.m_sliderKi.Bind( wx.EVT_SCROLL, self.OnUpdated )
        self.m_textCtrlKimin.Bind( wx.EVT_TEXT, self.OnUpdated )
        # self.m_textCtrlKi.Bind( wx.EVT_TEXT, self.OnUpdated )
        self.m_textCtrlKimax.Bind( wx.EVT_TEXT, self.OnUpdated )
        self.m_sliderKd.Bind( wx.EVT_SCROLL, self.OnUpdated )
        self.m_textCtrlKdmin.Bind( wx.EVT_TEXT, self.OnUpdated )
        # self.m_textCtrlKd.Bind( wx.EVT_TEXT, self.OnUpdated )
        self.m_textCtrlKdmax.Bind( wx.EVT_TEXT, self.OnUpdated )
        self.m_textCtrlDesired.Bind( wx.EVT_TEXT, self.OnUpdated )
        self.m_buttonClear.Bind( wx.EVT_BUTTON, self.OnClear )
        self.m_buttonReset.Bind( wx.EVT_BUTTON, self.OnReset )
        self.Bind( EVT_DATA_ARRIVED, self.OnDataArrived )
        
        self.Kp = [
            self.m_textCtrlKp,
            self.m_textCtrlKpmin,
            self.m_textCtrlKpmax,
            self.m_sliderKp ]
        
        self.Ki = [
            self.m_textCtrlKi,
            self.m_textCtrlKimin,
            self.m_textCtrlKimax,
            self.m_sliderKi ]
        
        self.Kd = [
            self.m_textCtrlKd,
            self.m_textCtrlKdmin,
            self.m_textCtrlKdmax,
            self.m_sliderKd ]

        defaults = [
                0, 10, # P
                0, 1,  # I
                0, 50  # D
            ]

        i = 0
        for kx in [ self.Kp, self.Ki, self.Kd ]:
            kx[1].SetValue(str(defaults[i]))
            i = i + 1
            kx[2].SetValue(str(defaults[i]))
            i = i + 1
        self.m_textCtrlDesired.SetValue("300.0")
        self.serial = serial

    def OnDataArrived(self, event):
        self.m_plotCanvas.push_values(event.data[0], event.data[1])

    def MapSlider(self, slider, kxmin, kxmax):
        smin = slider.GetMin()
        smax = slider.GetMax()
        s = slider.GetValue()
        return kxmin + (s-smin) * (kxmax-kxmin) / (smax-smin)

    def OnUpdated( self, event ):
        result = []
        for kx in [ self.Kp, self.Ki, self.Kd ]:
            try:
                kxmin = float(kx[1].GetValue())
                kxmax = float(kx[2].GetValue())
                kxval = self.MapSlider(kx[3], kxmin, kxmax)
                result.append(str(kxval))
                kx[0].SetValue(str(kxval))
            except Exception as ex:
                print("invalid values?", ex)
                return
        try:
            desired = float(self.m_textCtrlDesired.GetValue())
            result.append(str(desired))
        except Exception as ex:
            print("invalid values?", ex)
            return
        to_send = b"X" + ",".join(result).encode() + b"\n"
        # print(to_send)
        self.serial.write(to_send)

    def OnReset( self, event ):
        self.serial.write(b"R\n")

    def OnClear( self, event ):
        self.m_plotCanvas.clear_values()
    


class ProcessLine(serial.threaded.LineReader):
    TERMINATOR=b"\n"
    ENCODING = 'ascii'
    BUFFER_LIMIT = 5

    def __init__(self, frame):
        super(self.__class__, self).__init__()
        self.frame = frame
        self.n = 0
        self.tvals = []
        self.yvals = []

    def connect_made(self, transport):
        pass

    def handle_line(self, line):
        print(line)
        try:
            t, y, *_ = line.strip().split(",")
            t = _float(t)
            y = _float(y)
            self.tvals.append(t)
            self.yvals.append(y)
            self.n = self.n + 1
            if self.n >= self.BUFFER_LIMIT:
                evt = DataArrivedEvent(data=[self.tvals[:], self.yvals[:]])
                wx.PostEvent(self.frame, evt)
                self.data = []
                self.n = 0
                self.tvals = []
                self.yvals = []
        except Exception as ex:
            print(ex)

    def connection_lost(self, exc):
        print(exc)
        try:
            evt = DataArrivedEvent(data=None)
            wx.PostEvent(self.frame, evt)
        except Exception as e:
            print(e)


def main():
    ser = serial.Serial("/dev/ttyUSB1", 9600)
    app = wx.App()
    frame = MainFrame(None, ser)
    frame.Show()
    with serial.threaded.ReaderThread(ser, lambda: ProcessLine(frame)) as protocol:
        app.MainLoop()


if __name__ == "__main__":
    main()



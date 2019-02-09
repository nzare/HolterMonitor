"""
Demonstrates some customized mouse interaction by drawing a crosshair that follows 
the mouse.


"""

#import initExample ## Add path to library (just for examples; you do not need this)
import numpy as np
import pyqtgraph as pg
from pyqtgraph.Qt import QtGui, QtCore
from pyqtgraph.Point import Point


#reading from a file and storing in an array
putinto =  open ('Desktop/100.txt','r').read()
arr = putinto.split('\n')
a = []
b = []
c = []
for line in arr:
	if (len(line) > 2):
		x = line.split(',')
		a.append(int(x[0])-960)
		b.append(int(x[1])-960)
		c.append(int(x[2])-960)	




#generate layout
app = QtGui.QApplication([])
win = pg.GraphicsWindow()
win.resize(1420,820)
win.setWindowTitle('ECG Waves')
label = pg.LabelItem(justify='right')
win.addItem(label)
p1 = win.addPlot(row=1, col=0)
#p2 = win.addPlot(row=2, col=0)

region = pg.LinearRegionItem()
region.setZValue(10)
# Add the LinearRegionItem to the ViewBox, but tell the ViewBox to exclude this 
# item when doing auto-range calculations.
#p2.addItem(region, ignoreBounds=True)

#pg.dbg()
p1.setAutoVisible(y=True)
p1.showGrid(x=True, y=True)

#create numpy arrays
#make the numbers large to show that the xrange shows data from 10000 to all the way 0
data1 =  5 * pg.gaussianFilter(np.random.random(size=10000), 10) + 3 * np.random.random(size=10000)
data2 =  5 * pg.gaussianFilter(np.random.random(size=10000), 10) + 3 * np.random.random(size=10000)

p1.plot(b, pen="r")
#p1.plot(data2, pen="g")

#p2.plot(data1, pen="w")

def update():
    #global data1, curve1
    region.setZValue(1000)
    minX, maxX = region.getRegion()
    p1.setXRange(maxX, minX, padding=0)   
    #data1[:-1] = data1[1:]  # shift data in the array one sample left
                            # (see also: np.roll)
   # data1[-1] = np.random.normal()
   # curve1.setData(data1)
    
   
   # curve2.setData(data1)
    #curve1.setPos(0, 0)

# update all plots


region.sigRegionChanged.connect(update)

def updateRegion(window, viewRange):
    rgn = viewRange[0]
    region.setRegion(rgn)

p1.sigRangeChanged.connect(updateRegion)

region.setRegion([2000, 1700])

#cross hair
vLine = pg.InfiniteLine(angle=90, movable=False)
hLine = pg.InfiniteLine(angle=0, movable=False)
#bLine = pg.InfiniteLine(angle=0, movable=False)
p1.addItem(vLine, ignoreBounds=True)
p1.addItem(hLine, ignoreBounds=True)
#p1.addItem(bLine, ignoreBounds=True)

vb = p1.vb
z = 10
def mouseMoved(evt):
    pos = evt[0]  ## using signal proxy turns original arguments into a tuple
    if p1.sceneBoundingRect().contains(pos):
        mousePoint = vb.mapSceneToView(pos)
        index = int(mousePoint.x())
        if (b[index] <=200): 
        	label.setText("<span style='color: red; font-size: 12pt'>x=%0.1f,   <span style='color: red'>y1=%0.1f</span>, <span style='color: red'>z=%0.1f</span>" % (mousePoint.x(), float(b[index]),float(c[index])))
	else:
		label.setText("<span style='color: red; font-size: 12pt'>x=%0.1f,   <span style='color: blue'>y1=%0.1f</span>, <span style='color: red'>z=%0.1f</span>" % (mousePoint.x(), float(b[index]),float(c[index])))
        vLine.setPos(mousePoint.x())
        hLine.setPos(mousePoint.y())
#	bLine.setPos(975)


proxy = pg.SignalProxy(p1.scene().sigMouseMoved, rateLimit=60, slot=mouseMoved)
#p1.scene().sigMouseMoved.connect(mouseMoved)


## Start Qt event loop unless running in interactive mode or using pyside.
if __name__ == '__main__':
    import sys
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()


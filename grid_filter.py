# Import the necessary ImageJ classes
from ij import IJ
from ij.gui import Roi, OvalRoi, Overlay, GenericDialog
from ij.plugin import FFT
from ij import WindowManager as WM 
from ij.process import ImageProcessor
from math import sin, cos, radians
from java.awt import Color
from java.awt.event import AdjustmentListener, ItemListener  
from ij.plugin.frame import RoiManager



imp = IJ.getImage()
imp = FFT.forward(imp)
cx=imp.width/2
cy=imp.height/2

def generate_Roi(imp, rm, nx,ny,lx,ly, r, ratio=1, angle =0, shiftx=0, shifty=0):
	cx=imp.width/2+shiftx
	cy=imp.height/2+shifty
	rm.runCommand(imp, "reset")
	for i in range(2*nx+1):
		for j in range(2*ny+1):
			x=(cx-nx*lx+i*lx)*ratio
			y=(cy-ny*ly+j*ly)*ratio
			rad=radians(angle)
			x = cx + (x - cx)*cos(rad) - (y - cy)*sin(rad)
			y = cy + (x - cx)*sin(rad) + (y - cy)*cos(rad)
			rm.addRoi(OvalRoi(x, y, r, r))

class DiracFilterPreviewer(AdjustmentListener):  
  def __init__(self, imp, rm, sliders):
    """ 
       imp: an ImagePlus 
       slider: a java.awt.Scrollbar UI element 
       preview_checkbox: a java.awt.Checkbox controlling whether to 
                         dynamically update the ImagePlus as the 
                         scrollbar is updated, or not. 
    """  
    self.imp = imp  
    self.rm=rm
    self.original_ip = imp.getProcessor().duplicate() # store a copy  
    self.n_slider = sliders[0]
    self.l_slider = sliders[1]
    self.r_slider = sliders[2]
    self.angle_slider = sliders[3]
    self.shiftx = sliders[4]
    self.shifty = sliders[5]
    
    
  def adjustmentValueChanged(self, event): 
  	#if event.getValueIsAdjusting():
  		#return
  	self.set_roi()  

  def reset(self):  
    """ Restore the original ImageProcessor """  
    self.imp.setProcessor(self.original_ip)  
    
  def set_roi(self):  
    """ Execute the in-place scaling of the ImagePlus. """
    n=self.n_slider.getValue()
    l=self.l_slider.getValue()
    r=self.r_slider.getValue()
    angle=self.angle_slider.getValue()
    shiftx=self.shiftx.getValue()
    shifty=self.shifty.getValue()
    generate_Roi(self.imp, self.rm, n, n, l, l, r, angle=angle, shiftx=shiftx, shifty=shifty)
    

gd = GenericDialog("Dirac Filter")
gd.addSlider("n", 1, 10, 2)
gd.addSlider("l", 0, 70, 50)
gd.addSlider("r", 1, 30, 5)
gd.addSlider("angle", 0, 90, 0)
gd.addSlider("Shift x", -20, 20, 0)
gd.addSlider("Shift y", -20, 20, 0)
sliders=gd.getSliders()
imp = WM.getCurrentImage()
rm=RoiManager()
rm.runCommand(imp,"Show All");
previewer=DiracFilterPreviewer(imp, rm, sliders)
for i in range(6):
	sliders[i].addAdjustmentListener(previewer)

gd.showDialog()

rm.runCommand(imp,"Combine");
#rm.runCommand(imp, "reset")









IJ.setBackgroundColor(0, 0, 0);
IJ.run(imp, "Clear Outside", "slice");



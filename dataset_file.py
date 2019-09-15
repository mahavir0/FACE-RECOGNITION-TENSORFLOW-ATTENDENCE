import cv2
import numpy as np
import matplotlib.pyplot as plt
output_datadir = './train_img'

#def collect_data(self):
#output_dir = os.path.expanduser(self.output_datadir)
#if not os.path.exists(output_dir):
    #os.makedirs(output_dir)

images = 'my-image.png'    
img = cv2.imread(images)
write_name = 'corners_found'+'.jpg'
cv2.imwrite(write_name, img)
#cv2.imshow('write_name',write_name)

cv2.destroyAllWindows()
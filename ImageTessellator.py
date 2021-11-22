#Author: Written by Brendon Madison, grad student of KU PHSX and ASTR on 21st of November, 2021
#First Macro: Take an image and tessellate it. This means to divide into continuous tiles.
#Second Macro: Take a bunch of tessellated images/tiles and then rearrange them into an image.
#Purpose: Why may we want to do this? What if we can only telemeter so much data? Then we can't telementer
#           a MegaPixel image. So we can divide it into smaller images and then telemeter.
#           Then, at the ground, the untessellator can be run to reconstruct the image.
#           There is also the added function of being able to change the file extension.
#           This effectively allows the user to compress the images or keep them uncompressed.
#           Using .png keeps it compressed but using .jpg will compress it.
#           In fact, .png usually increases total (after untessellator) file size by ~2
#           .jpg usually decreases total (after untessellator) file size by ~2 if it started as .png

#           To do:
#                   Do more testing. Create a file&directory hierarchy. Migrate parser to optional .ini file method.
#Example command line:
#python ImageTessellator.py EarthTest.jpg .jpg 3 4
#This tessellates EarthTest.jpg with .jpg extension into 3 rows and 4 columns

import cv2
import numpy as np
import argparse

parser = argparse.ArgumentParser(description='Find image and then tessellate it. Also untesselate it.')
parser.add_argument('Im',metavar='Im',type=str,help='String for name of image')
parser.add_argument('Ex',metavar='Ex',type=str,help='Extension of images.')
parser.add_argument('Nr',metavar='Nr',type=int,help='Number of rows')
parser.add_argument('Nc',metavar='Nc',type=int,help='Number of columns')

args = parser.parse_args()

def TessellateImage(numrow,numcol,imname,ext):
    #Take an image and tessellate it. Essentially, divide into continuous tiles.
    #Grab the image!
    image = cv2.imread(imname)
    #R and C ... integer divide by the number of rows and columns.
    #It divides into RxC tessellations
    #You have to add 1 or else imperfect divisions result in more than R or C rows or columns
    #In turn, this also means that some tessellations have different dimensions
    #But this is not that big of an issue compared to the alternative of having a variable number of columns and rows
    R = image.shape[0]//numrow + 1
    C = image.shape[1]//numcol + 1

    tess = [image[j:j+R,k:k+C] for j in range(0,image.shape[0],R) for k in range(0,image.shape[1],C)]

    #Loop over the tesselations
    for i in range(len(tess)):
    # show the output image (Optional)
        #cv2.imshow("TessellateTest_"+str(i)+".jpg",tess[i])
        #cv2.waitKey(0)
        #Save the output image
        #have to use imname[0:len(args.Im)-4] to remove the file extension
        cv2.imwrite(str(imname[0:len(imname)-4])+"_tile_"+str(i)+str(ext),tess[i])
    
    return

def UntessellateImage(numrow,numcol,imname,ext):
    #Take a group of images that follow the naming convention of:
    #name_number.jpg example: Tessellation_5.jpg would be the 6th tessellation tile.
    
    #Its imnam because its like imname but we removed the e. e stands for file extension...
    #haha!
    imnam = str(imname[0:len(imname)-4])
    #Counter for keeping track of tile number and number of rows assembled
    c = 0
    rowc = 0
    for i in range(numrow):
        #Read the first tile of the row
        imrow = cv2.imread(str(imnam)+"_tile_"+str(c)+str(ext))        
        #Loop for stacking all the remaining tiles in the row
        c += 1
        for j in range(numcol-1):
            imrow = np.hstack((imrow,cv2.imread(str(imnam)+"_tile_"+str(c)+str(ext))))
            c += 1
        #Stack the rows on top of eachother
        #Though we have to check the first one because we need img to have the correct data format
        #And so it has the same dimensions as all the future rows
        if rowc == 0:
            img = imrow
        else:
            img = np.vstack((img,imrow))
        rowc += 1
    #Optional -- display the image
    #cv2.imshow(str(imnam)+"_Untessellated.jpg",img)
    #cv2.waitKey(0)
    cv2.imwrite(str(imnam)+"_Untessellated"+str(ext),img)

#You have to pass all but the extension for the filename
#Which is why we pass args.Im[0:len(args.Im)-4] as it removes the extension
TessellateImage(args.Nr,args.Nc,args.Im,args.Ex)

UntessellateImage(args.Nr,args.Nc,args.Im,args.Ex)
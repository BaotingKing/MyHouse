# -*- coding: utf-8 -*-

# import cpuid,pika
import sys
import numpy as np
import cv2, os, time, sqlite3, collections, hashlib, ConfigParser
# from matplotlib import pyplot as plt
from random import shuffle
import xml.etree.ElementTree as ET
from Crypto.Cipher import AES
# from Crypto import Random
from hashlib import md5


#
# def CheckLicence():
#     licencefile = open('/home/westwell/Documents/NBPort/code/licence','r')
#     licence = licencefile.read()
#     c = cpuid.cpuid_t()
#     var=0
#     varkey=map(ord,"welloacen")
#     varkey_sub2=map(ord,"rongqi")
#     # Dump the raw cpuid data
#     for i in range(0, 10):
#        cpuid.cpuid(i, c)
#     #   print "0x%08x %s" % (i, map(hex, [c.eax, c.ebx, c.ecx, c.edx]))
#
#     for i in range(0, 10):
#        cpuid.cpuid(0x80000000 + i, c)
#        var+=c.eax
#        if i%3==0:
#           for i in range(len(varkey)):
#              var+=varkey[i]
#        if i%2==0:
#           for i in range(len(varkey_sub2)):
#              var+=varkey_sub2[i]
#     #   print var
#
#     #   print "0x%08x %s" % (0x80000000 + i, map(hex, [c.eax, c.ebx, c.ecx, c.edx]))
#     md5 = hashlib.md5()
#     md5.update(str(var))
#
#     if not licence == md5.hexdigest():
#         sys.exit('licence not matched')

def NonMaximumSuppressionMap(labelmap, scoremap, suppresssize):
    finallabel = np.zeros((0, 4))
    mapshape = np.array([scoremap.shape[0:2]])
    while (scoremap > 0).any():
        index = scoremap.argmax()
        index = np.array([index / mapshape[0, 1], index % mapshape[0, 1]])
        singlelabel = np.array([[labelmap[index[0], index[1]], scoremap[index[0], index[1]], index[0], index[1]]])
        finallabel = np.concatenate((finallabel, singlelabel), 0)
        suppressedLoc = np.array([0, 0, mapshape[0, 0], mapshape[0, 1]])
        if index[0] - suppresssize[0] > 0:
            suppressedLoc[0] = index[0] - suppresssize[0]
        if index[0] + suppresssize[0] < suppressedLoc[2]:
            suppressedLoc[2] = index[0] + suppresssize[0]
        if index[1] - suppresssize[1] > 0:
            suppressedLoc[1] = index[1] - suppresssize[1]
        if index[1] + suppresssize[1] < suppressedLoc[3]:
            suppressedLoc[3] = index[1] + suppresssize[1]
        scoremap[suppressedLoc[0]:suppressedLoc[2], suppressedLoc[1]:suppressedLoc[3]] = 0

    return finallabel


def NonMaximaSuppression(AllLocation):
    Score = AllLocation[:, 4]
    Score = Score.tolist()
    ProcessLocation = AllLocation.tolist()
    KeptLocation = []  # location kept after NonMaximaSuppression
    localKept = []  # location kept in every run
    localScore = []
    while len(ProcessLocation) > 0:
        MaxIndex = Score.index(max(Score))
        MaxLocation = ProcessLocation[MaxIndex]
        KeptLocation.append(MaxLocation)
        print 'Score:', Score[MaxIndex]
        del Score[MaxIndex]
        del ProcessLocation[MaxIndex]
        for i in range(len(ProcessLocation)):
            IOU = BoxOverlap(MaxLocation, ProcessLocation[i])  # Intersection over uion
            if IOU < (Score[i] / 6):
                localKept.append(ProcessLocation[i])
                localScore.append(Score[i])
        ProcessLocation = localKept
        Score = localScore
        localKept = []
        localScore = []

    KeptLocation = np.asarray(KeptLocation)
    return KeptLocation


# def ExtendBox(Location,LargestX,LargestY):
#    Location[:,0:2] -= 10
#    Location[:,0:2] += 10
#    index = Location<0
#    Location[index]=0
#    index = Location[:,2]>LargestX
#    Location[index,2]=LargestX
#    index = Location[:,3]>LargestY
#    Location[index,3]=LargestY

def ExtendBox(Boxes, dim):  # dim = 0 for width, dim = 1 for height
    for i in range(Boxes.shape[0]):
        singleBox = Boxes[i, :]
        edgesize = singleBox[dim + 2] - singleBox[dim]
        if edgesize < 36:
            diff = (36 - edgesize) / 2.0
            singleBox[dim] = int(singleBox[dim] - diff)
            singleBox[dim + 2] = int(singleBox[dim + 2] + diff)


# elif edgesize>36:
#            diff = (edgesize-36)/2.0
#            singleBox[dim] = int(singleBox[dim] + diff)
#            singleBox[dim+2] = int(singleBox[dim+2] - diff)




def MergeBoxes(Boxes, threshold=0):
    FinalBoxes = np.zeros((0, 5))
    MergedBoxes = Boxes[0:1, :].copy()
    LeftBoxes = Boxes[1:, :].copy()
    while LeftBoxes.size > 0:
        IOU = np.zeros((LeftBoxes.shape[0], 1))
        for i in range(len(LeftBoxes)):
            IOU[i, 0] = BoxOverlap(MergedBoxes[0, :], LeftBoxes[i, :])
        index = IOU[:, 0] > threshold
        if not index.any():
            FinalBoxes = np.concatenate((FinalBoxes, MergedBoxes), 0)
            MergedBoxes = LeftBoxes[0:1, :].copy()
            LeftBoxes = LeftBoxes[1:, :].copy()
        else:
            CrossedBoxes = np.concatenate((MergedBoxes, LeftBoxes[index, :]), 0)
            MergedBoxes = np.array(
                [CrossedBoxes[:, 0].min(), CrossedBoxes[:, 1].min(), CrossedBoxes[:, 2].max(), CrossedBoxes[:, 3].max(),
                 CrossedBoxes[:, 4].max()])
            MergedBoxes = MergedBoxes.reshape((1, 5))
            LeftBoxes = LeftBoxes[IOU[:, 0] <= 0, :]
    FinalBoxes = np.concatenate((FinalBoxes, MergedBoxes), 0)
    return FinalBoxes


def BoxOverlap(Region1, Region2):  # Region1 and Region2 is 1d ndarray
    if Region1[0] > Region2[2]:
        return 0
    if Region1[1] > Region2[3]:
        return 0
    if Region1[2] < Region2[0]:
        return 0
    if Region1[3] < Region2[1]:
        return 0
    Width = min(Region1[2], Region2[2]) - max(Region1[0], Region2[0])
    Height = min(Region1[3], Region2[3]) - max(Region1[1], Region2[1])
    IntersectionArea = Width * Height
    Area1 = (Region1[3] - Region1[1]) * (Region1[2] - Region1[0])
    Area2 = (Region2[3] - Region2[1]) * (Region2[2] - Region2[0])
    #    print Area1+Area2-IntersectionArea
    if Area1 + Area2 - IntersectionArea == 0:
        return 1000
    return IntersectionArea * 1.0 / (Area1 + Area2 - IntersectionArea)


def DrawLines(image, corner, color=(255, 0, 0)):
    for i in range(4):
        cv2.line(image, (int(corner[0, i]), int(corner[1, i])), (int(corner[0, i + 1]), int(corner[1, i + 1])), color,
                 2)


def DrawLocation(image, AllLocation, color=(255, 0, 0)):
    if AllLocation.size > 0:
        if AllLocation.ndim == 1:
            cv2.rectangle(image, (int(AllLocation[0]), int(AllLocation[1])), (int(AllLocation[2]), int(AllLocation[3])),
                          color, 2)
        else:
            for SingleLocation in AllLocation:
                cv2.rectangle(image, (int(SingleLocation[0]), int(SingleLocation[1])),
                              (int(SingleLocation[2]), int(SingleLocation[3])), color, 2)


def GenerateImageList(ImageListFile):
    imagefile = open(ImageListFile, 'r')
    ImageList = imagefile.readlines()
    return ImageList


def ReadFeatureFromFile(FeatureFile, Label, LabelDim):  # label 0 means pedestuirain, 1 means background
    Feature = []
    Label = []
    for FeatureName in FeatureFile:
        feature = np.load(FeatureName.split()[0])
        label = GenerateLabelForFeature(feature.shape[0], LabelDim, Label)
        Feature.extend(feature)
        Label.extend(label)
    Feature = np.asarray(Feature)
    Label = np.asarray(Label)
    return Feature, Label


def GenerateLabelForFeature(LabelNum, LabelDim, TrueDim):
    _label = np.zeros((LabelNum, LabelDim))
    _label[:, TrueDim] = 1
    return _label


# def showImage(image):
#    plt.figure(1)
#    plt.imshow(image)
#    plt.show()

def ShuffleFeature(trainfeature, trainlabel):
    RandomFeature = np.zeros(trainfeature.shape)
    RandomLabel = np.zeros(trainlabel.shape)
    RandomOrder = np.arange(0, trainfeature.shape[0])
    shuffle(RandomOrder)
    order = 0;
    for i in RandomOrder:
        RandomFeature[order, :] = np.copy(trainfeature[i, :])
        RandomLabel[order, :] = trainlabel[i, :]
        order += 1
    return RandomFeature, RandomLabel


def MakeTrainSample(digitsLocation, NumRegion, orientationFlag):
    locationDiff = np.array([NumRegion[0:2], NumRegion[0:2]])
    locationDiff = locationDiff.reshape(4)
    label = np.zeros((0, 5))
    sublabel = np.zeros((1, 5))
    for i in range(1, len(digitsLocation)):
        singleLocation = digitsLocation[i]
        if len(singleLocation) == 0:
            continue
        singleLocation = np.array(singleLocation)
        for j in range(singleLocation.shape[0]):
            singleLocation[j, 0:4] += locationDiff
            sublabel[0, 0] = i
            sublabel[0, 1:5] = singleLocation[j, 0:4]
            label = np.concatenate((label, sublabel), 0)
    return label


# def GetResultFromLocation(digitsLocation,NumRegion,orientationFlag): #orientationFlag = 2 for horizontal region, 5 for vertical region
#    eliminateRegion = np.array([NumRegion[0],(NumRegion[1]+NumRegion[3])/2,NumRegion[2],(NumRegion[1]+NumRegion[3])/2])#Label in this region will be eliminated
#    locationDiff = np.array([NumRegion[0:2],NumRegion[0:2]])
#    locationDiff = locationDiff.reshape(4)
#    label = np.zeros((0,5))
#    sublabel = np.zeros((1,5))
#    score = 0
#    for i in range(1,len(digitsLocation)):
#        singleLocation = digitsLocation[i]
#        if len(singleLocation) == 0:
#            continue
#        singleLocation = np.array(singleLocation)
#        for j in range(singleLocation.shape[0]):
#            singleLocation[j,0:4] += locationDiff
#            if InElininateRegion(singleLocation[j,0:2],eliminateRegion) and orientationFlag==2:
#                continue
#            sublabel[0,0] = i
#            sublabel[0,1:5] = singleLocation[j,0:4]
#            label = np.concatenate((label,sublabel),0)
#            score += singleLocation[j,4]
#    return label, score # label = label + location

# def InElininateRegion(location,eliminateRegion):
#    para_A,para_B = ComputeLine(eliminateRegion)
#    if para_A*location[0]+location[1]+para_B>=0:
#        return True
#    else:
#        return False

# compute ax+y+b=0 from two points
def ComputeLine(location):
    tempa = location[0] - location[2]  # x1-x2
    tempb = location[3] - location[1]  # y2-y1
    tempc = location[1] * location[2] - location[0] * location[3]  # x2y1-x1y2
    return tempb / tempa, tempc / tempa


def isEqulatToGT(predicted, groundtruth):
    predicted_string = ''
    for i in predicted:
        predicted_string += str(int(i))
    if predicted_string == groundtruth:
        return True
    else:
        return False


def GenerateFileName(imageorder):
    filename = ''
    for i in range(5 - len(str(imageorder))):
        filename += '0'
    filename += str(imageorder)
    return filename


def CheckFolderExists(folder):
    if not os.path.exists(folder):
        os.makedirs(folder)


def CreateObjInXML(root, num):
    #    root = tree.getroot()
    example = ['word', 'Unspecified', '1', '0', '\n\t\t\t']
    for i in range(num):
        example_obj = root.findall('object')[-1]
        example_obj.tail = '\n\t'
        obj = ET.SubElement(root, example_obj.tag)
        obj.text = '\n\t\t'
        for i in range(len(example_obj)):
            sub_obj = ET.SubElement(obj, example_obj[i].tag)
            sub_obj.text = example[i]
            if i == (len(example_obj) - 1):
                sub_obj.tail = '\n\t'
            else:
                sub_obj.tail = '\n\t\t'
        example_obj = example_obj.find('bndbox')
        bndbox = obj.find('bndbox')
        for i in range(len(example_obj)):
            sub_obj = ET.SubElement(bndbox, example_obj[i].tag)
            sub_obj.text = 'xxxx'
            if i == (len(example_obj) - 1):
                sub_obj.tail = '\n\t\t'
            else:
                sub_obj.tail = '\n\t\t\t'
    last_obj = root.findall('object')[-1]
    last_obj.tail = '\n'


def AssignValueToObj_lorry_roi(root, allBoxes, label):
    objs = root.findall('object')
    for i in range(len(objs)):
        name = objs[i].find('name')
        name.text = label[0]
        bndbox = objs[i].find('bndbox')
        for j in range(len(bndbox)):
            bndbox[j].text = str(int(allBoxes[i, j]) + 1)


def AssignValueToObj(root, allBoxes, label):
    objs = root.findall('object')
    for i in range(len(objs)):
        name = objs[i].find('name')
        name.text = label[i]
        bndbox = objs[i].find('bndbox')
        for j in range(len(bndbox)):
            bndbox[j].text = str(int(allBoxes[i, j]) + 1)


def openTrainFile(filepath, categories):
    categorytrainlist = []
    for i in range(1, len(categories)):
        categorytrainlist.append(open(filepath + categories[i] + '_train.txt', 'w'))
        categorytrainlist.append(open(filepath + categories[i] + '_test.txt', 'w'))
    return categorytrainlist


def writeTrainFile(categorytrainlist, labels, categories, imname):
    for i in range(len(categorytrainlist)):
        singlelabel = i / 2 + 1
        if (labels == singlelabel).any():
            categorytrainlist[i].write(imname + ' ' + '1' + '\n')
        else:
            categorytrainlist[i].write(imname + ' ' + '-1' + '\n')


# label1 = np.array([1,2,3],dtype='int')
#    label2 = np.array([4,5,6],dtype='int')
#    if (labels != label1).any() and (labels != label2).any():
#        print '*****error*****'

def closeTrainFile(categorytrainlist):
    for singlefile in categorytrainlist:
        singlefile.close()


def AffineTransformation(image, affinetype):
    if not np.any(image):
        return image
    affinefile = 'affine_' + affinetype + '.npy'
    affine_matrix = np.load('/home/westwell/Documents/NBPort/code/util/' + affinefile)
    zeropadding = np.zeros(image.shape, dtype='uint8')
    image = np.concatenate((zeropadding, image), 0)  # 上下拼接
    zeropadding = np.zeros((image.shape[0], 200, 3), dtype='uint8')
    image = np.concatenate((zeropadding, image), 1)  # 左右拼接
    affine_image = cv2.warpAffine(image, affine_matrix, (image.shape[1] + 350, image.shape[0]))
    for rows in range(affine_image.shape[0]):
        if np.any(affine_image[rows, :, :]):
            break
    affine_image = affine_image[rows:, :, :]
    ##    start =time.time()
    for cols in range(affine_image.shape[1]):
        if np.any(affine_image[:, cols, :]):
            break
    affine_image = affine_image[:, cols:, :]
    cols = affine_image.shape[1] - 1
    while True:
        if np.any(affine_image[:, cols, :]):
            break
        cols -= 1
    affine_image = affine_image[:, 0:cols, :]
    return affine_image


#
def ReverseAffine(image, boxes_list, affinetype):
    affinefile = 'affine_' + affinetype + '.npy'
    affine_matrix = np.load('/home/westwell/Documents/NBPort/code/util/' + affinefile)
    affine_matrix = cv2.invertAffineTransform(affine_matrix)
    corners = []
    for boxes in boxes_list:
        #        corners = np.zeros
        #        for i in range(boxes.shape[0]):
        corner = np.ones((3, 5))
        corner[0:2, 0] = np.array([boxes[0, 0], boxes[0, 1]])
        corner[0:2, 1] = np.array([boxes[0, 2], boxes[0, 1]])
        corner[0:2, 2] = np.array([boxes[0, 2], boxes[0, 3]])
        corner[0:2, 3] = np.array([boxes[0, 0], boxes[0, 3]])
        corner[0:2, 4] = np.array([boxes[0, 0], boxes[0, 1]])
        corner = np.dot(affine_matrix, corner)
        corners.append(corner)  # corner is the 2x5 matrix, the first row is x coordinate, the second row i y coordinate
    affine_image = cv2.warpAffine(image, affine_matrix, (image.shape[1], image.shape[0]))
    for rows in range(affine_image.shape[0]):
        if np.any(affine_image[rows, :, :]):
            break
    affine_image = affine_image[rows:, :, :]
    for i in range(len(corners)):
        corner = corners[i]
        corner[1, :] -= rows
    #    rows = affine_image.shape[0]-1
    #    while True:
    #        if np.any(affine_image[rows,:,:]):
    #            break
    #        rows -= 1
    #    affine_image = affine_image[0:rows,:,:]
    for cols in range(affine_image.shape[1]):
        if np.any(affine_image[:, cols, :]):
            break
    affine_image = affine_image[:, cols:, :]
    for i in range(len(corners)):
        corner = corners[i]
        corner[0, :] -= cols
    #    cols = affine_image.shape[1]-1
    #    while True:
    #        if np.any(affine_image[:,cols,:]):
    #            break
    #        cols -= 1
    #    affine_image = affine_image[:,0:cols,:]
    return affine_image, corners


def AffineTransformation_annotation(image, boxes):
    affine_matrix = np.load('util/affine2.npy')
    zeropadding = np.zeros(image.shape, dtype='uint8')
    boxes[:, 1] += image.shape[0]
    boxes[:, 3] += image.shape[0]
    image = np.concatenate((zeropadding, image), 0)
    corners = []
    for i in range(boxes.shape[0]):
        corner = np.ones((3, 5))
        corner[0:2, 0] = np.array([boxes[i, 0], boxes[i, 1]])
        corner[0:2, 1] = np.array([boxes[i, 2], boxes[i, 1]])
        corner[0:2, 2] = np.array([boxes[i, 2], boxes[i, 3]])
        corner[0:2, 3] = np.array([boxes[i, 0], boxes[i, 3]])
        corner[0:2, 4] = np.array([boxes[i, 0], boxes[i, 1]])
        corner = np.dot(affine_matrix, corner)
        corners.append(corner)
    affine_image = cv2.warpAffine(image, affine_matrix, (image.shape[1], image.shape[0]))
    for rows in range(affine_image.shape[0]):
        if (affine_image[rows, :, :] != 0).any():
            break
    for i in range(len(corners)):
        corner = corners[i]
        corner[1, :] -= rows
        if i == 1:
            boxes[i, 0] = corner[0, 0]
            boxes[i, 1] = (corner[1, 0] + corner[1, 1]) / 2
            boxes[i, 2] = corner[0, 2]
            #            boxes[i,3] = (5*corner[1,2]+corner[1,3])/6
            boxes[i, 3] = corner[1, 2]
        else:
            boxes[i, 0] = corner[0, 0]
            boxes[i, 1] = (3 * corner[1, 0] + corner[1, 1]) / 4
            boxes[i, 2] = corner[0, 2]
            boxes[i, 3] = (4 * corner[1, 2] + corner[1, 3]) / 5

    affine_image = affine_image[rows:, :, :]
    return affine_image, corners, boxes


def CLAHE(image):
    image = image[:, :, ::-1]
    image = cv2.cvtColor(image, cv2.cv.CV_BGR2Lab)
    L_channel = image[:, :, 0]
    clahe = cv2.createCLAHE(clipLimit=3, tileGridSize=(8, 8))
    L_channel = clahe.apply(L_channel)
    image[:, :, 0] = L_channel
    image = cv2.cvtColor(image, cv2.cv.CV_Lab2RGB)
    #    image = image[:,:,::-1]
    return image


def ArrayToString(inputarray):
    outputstring = ''
    for i in inputarray:
        outputstring += str(int(i))
    return outputstring


def ListToString(inputlist):
    inputlist = labelToletters(inputlist)
    outputstring = ''
    for i in inputlist:
        outputstring += i
    return outputstring


def BoolToString(inputbool):
    if inputbool == True:
        return '1'
    elif inputbool == False:
        return '0'


def StringToArray(inputString):
    outputarray = np.zeros((7), dtype=int)
    if len(inputString) == 7:
        for i in range(len(inputString)):
            outputarray[i] = int(inputString[i])
        return outputarray
    else:
        for i in range(len(inputString) / 2):
            outputarray[i] = int(inputString[2 * i:2 * i + 2])
        return outputarray


def SplitGroundTruth(inputString):
    groundTruth = []
    groundTruth.append(inputString[0:4])
    #    groundTruth.append(StringToArray(inputString[4:11]))
    groundTruth.append(inputString[4:11])
    groundTruth.append(inputString[11:15])
    return groundTruth


def labelToletters(label, labeltype):
    if labeltype == 'letters':
        groundtruth = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S',
                       'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    elif labeltype == 'types':
        groundtruth = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I',
                       'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    letters_label = []
    for i in label:
        if int(i) == -1:
            letters_label.append('-')
        else:
            letters_label.append(groundtruth[int(i)])
    return letters_label


def CheckRules(digits, letters, realtime, Crane_No):
    #    if isWorklistConnected():
    #        letters = labelToletters(letters,'letters')
    #        Container_No=''
    #        for letter in letters:
    #            Container_No += letter
    #        for digit in digits:
    #            if digit==-1:
    #                Container_No += '-'
    #            else:
    #                Container_No += str(int(digit))
    #        if realtime:
    #            dbname = 'HarborInfo'+Crane_No+'.db'
    #            conn = sqlite3.connect('/home/westwell/Documents/NBPort/code/LocationInfo/'+dbname)
    #            cursor = conn.cursor()
    #            if len(Crane_No) <2:
    #                Crane_No = ('QC0'+Crane_No)
    #            else:
    #                Crane_No = ('QC'+Crane_No)
    #            Container_No = (Container_No,)
    #            selectResult = cursor.execute('SELECT containerNo ,CraneNo FROM ContainerList WHERE ( containerNo = ?)',Container_No)
    #            countResult = collections.Counter(selectResult).most_common(10)
    #            if (len(countResult) <= 0):
    #                return False
    #            else:
    #                return True
    #            cursor.close()
    #            conn.close()
    #        else:
    if not realtime:
        letters = labelToletters(letters, 'letters')
        Container_No = ''
        for letter in letters:
            Container_No += letter
        for digit in digits:
            if digit == -1:
                Container_No += '-'
            else:
                Container_No += str(int(digit))
        conn = sqlite3.connect('/cv/Rongqi/digits/testvideo/varify_DB')
        cursor = conn.cursor()
        Container_No = (Container_No,)
        selectResult = cursor.execute('SELECT containerNo ,CraneNo FROM ContainerList WHERE ( containerNo = ?)',
                                      Container_No)
        countResult = collections.Counter(selectResult).most_common(10)
        cursor.close()
        conn.close()
        if (len(countResult) <= 0):
            return False
        else:
            return True
        #    else:
    if np.any(letters == -1) or np.any(digits == -1):
        return False
    if np.all(letters == 0) or np.all(digits == 0):
        return False
    letters_label = letters.copy()
    letter_cor = [10, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 34, 35, 36, 37,
                  38]
    label_sum = 0
    for i in range(letters_label.shape[0]):
        letters_label[i] = letter_cor[int(letters_label[i])]
    entire_label = np.concatenate((letters_label, digits[0:6]), 0)
    for i in range(entire_label.shape[0]):
        label_sum += entire_label[i] * 2 ** i
    checkNum = label_sum % 11
    if checkNum == 10:
        checkNum = 0
    if checkNum == int(digits[6]):
        return True
    else:
        return False


def isWorklistConnected():
    chipconnection_data = sqlite3.connect('/home/westwell/Documents/NBPort/code/ChipConnection.db')
    cu = chipconnection_data.cursor()
    command = 'select isConnected from WorkListConnection'
    cu.execute(command)
    content = cu.fetchone()[0]
    cu.close()
    chipconnection_data.close()
    if content == 1:
        return True
    else:
        return False


def combineResult(predicted, rule):
    types = predicted[2]
    digits = predicted[1]
    letters = predicted[0]
    digits = labelToletters(digits, 'types')
    letters = labelToletters(letters, 'letters')
    types = labelToletters(types, 'types')
    finalresult = ''
    for letter in letters:
        finalresult += letter
    #    if len(finalresult)<4:
    #        for i in range(4-len(finalresult)):
    #            finalresult += '-'
    finalresult += ' '
    for digit in digits:
        finalresult += str(digit)
    #    if len(finalresult)<12:
    #        for i in range(12-len(finalresult)):
    #            finalresult += '-'
    finalresult += ' '
    for singletype in types:
        finalresult += singletype
    #    if len(finalresult)<17:
    #        for i in range(17-len(finalresult)):
    #            finalresult += '-'
    finalresult += ' '
    finalresult += str(rule)
    return finalresult


# def check_correct(predicted1,predicted2,rule_check1,rule_check2):
#    if rule_check1 and rule_check2:
#        if np.all(predicted1[0] == predicted2[0]) and np.all(predicted1[1] == predicted2[1]):
#            finalresult = [combineResult(predicted1,rule_check1),combineResult(predicted1,rule_check1)]
#            return True,finalresult
#        else:
#            finalresult = [combineResult(predicted1,rule_check1),combineResult(predicted2,rule_check2)]
#            return False,finalresult
#    elif rule_check1:
#        finalresult = [combineResult(predicted1,rule_check1),combineResult(predicted1,rule_check1)]
#        return True,finalresult
#    elif rule_check2:
#        finalresult = [combineResult(predicted2,rule_check2),combineResult(predicted2,rule_check2)]
#        return True,finalresult
#    else:
#        return False,None
#
# def compareResult(predicted1,score1,rule_check1, predicted2,score2,rule_check2,realtime,craneNO):#result cotain the info:[predicted,score,rule_check,region],predicted is [letters,digits,types]
#    predicted1,predicted2 = getBetterType(predicted1,predicted2,score1,score2)  
#    isCorrect,finalresult = check_correct(predicted1,predicted2,rule_check1,rule_check2)
#    if isCorrect:
#        return finalresult,False
#    elif not finalresult is None:
#        return finalresult,True
#    else:
#        combinedpredicted1 = [predicted1[0],predicted2[1],predicted1[2]]
#        combinedpredicted2 = [predicted2[0],predicted1[1],predicted2[2]]
#        isCorrect,finalresult = check_correct(combinedpredicted1,combinedpredicted2,CheckRules(predicted2[1],predicted1[0],realtime,craneNO),CheckRules(predicted1[1],predicted2[0],realtime,craneNO))
#        if isCorrect:
#            return finalresult,False #the results returned are finalresult, isWarning
#        elif not finalresult is None:
#            return finalresult,True
#        else:
#            kept = score1>score2
#            keptresult = []
#            disCard = []
#            for i in range(3):
#                if kept[i]:
#                    keptresult.append(predicted1[i])
#                    disCard.append(predicted2[i])
#                else:
#                    keptresult.append(predicted2[i])
#                    disCard.append(predicted1[i])
#            return [combineResult(keptresult,False),combineResult(disCard,False)],True
#
# def getBetterType(predicted1,predicted2,score1,score2): #to get the better container type recognition result
#    if np.all(score1==0) or np.all(score2==0): #debug to deal with the situation when type is not recognized  if score1[2]==0 or score2[2]==0:
#        return predicted1,predicted2
#    elif score1[2]>score2[2]:
#        predicted2[2]=predicted1[2]
#    elif score1[2]<=score2[2]:
#        predicted1[2]=predicted2[2]
##    print predicted1[2],predicted2[2]
#    return predicted1,predicted2
#
def getCameraID(cameraSetting):
    temp = cameraSetting.split('/')[-1]
    temp = temp.split('.')[0]
    cameraID = temp.split('_')[-1]
    return int(cameraID)


def isSingle(predicted1, predicted2, rule_check1, rule_check2):
    #    print predicted1[2][0:2]
    doubleside = np.array([2, 2])
    if np.all(predicted1[2][0:2] == doubleside) or np.all(predicted2[2][0:2] == doubleside):
        return False
    elif rule_check1 and rule_check2 and (not np.all(predicted1[1] == predicted2[1])):
        return False
    else:
        return True


# def processDoubleResult(predicted1,rule_check1,predicted2,rule_check2):
#    finalresult = [combineResult(predicted1,rule_check1),combineResult(predicted2,rule_check2)]
#    if rule_check1 and rule_check2:
#        isWarning = False
#    else:
#        isWarning = True
#    return finalresult,isWarning

def UpdateSqlData(sqldata, refinedResult, isWarning, isSingle, isStable, carChannel):
    if isWarning:
        warning_tag = 1
    else:
        warning_tag = 0
    if isSingle:
        single_tag = 1
    else:
        single_tag = 2
    if isStable:
        stable_tag = 1
    else:
        stable_tag = 0
    sqldata_cu = sqldata.cursor()
    sqldata_cu.execute(
        "update ContainerInfo set Cam1Result='%s',Cam2Result='%s', CarLineNO = '%d',isWarning='%d',ReserveInt1='%d',ReserveInt2='%d' where rowid = 1" % (
        refinedResult[0], refinedResult[1], carChannel, warning_tag, single_tag, stable_tag))
    sqldata.commit()
    sqldata_cu.close()


#    print refinedResult
#    print isStable

def UpdateImgPath(sqldata, imname1, imname2):
    sqldata_cu = sqldata.cursor()
    sqldata_cu.execute("update ContainerInfo set ImgPath='%s'" % (imname1 + ' ' + imname2))
    sqldata.commit()
    sqldata_cu.close()


def loadUIImage():
    imagepath = '/home/westwell/Documents/NBPort/code/UI/image/'
    UIimage = []
    for i in range(1, 5):
        imname = imagepath + str(i) + '.jpg'
        image = cv2.imread(imname)
        #        print image.shape
        UIimage.append(image)
    return UIimage


# def drawUI(image,UIimages,results,isSingle,isStable,carChannel,craneNo):
##    if isStable:
##        result1_check = results[0].split(' ')[-1]
##        result2_check = results[1].split(' ')[-1]
##        if isSingle:
##            if result1_check == 'False' and isResultExist(results[0]):
##                UIimage = UIimages[2]
##            else:
##                UIimage = UIimages[0]
##        else:
##            if result1_check == 'False' and result2_check == 'True' and isResultExist(results[0]):
##                UIimage = UIimages[3]
##            elif result1_check == 'True' and result2_check == 'False' and isResultExist(results[1]):
##                UIimage = UIimages[4]
##            elif result1_check == 'False' and result2_check == 'False':
##                if isResultExist(results[0]) and isResultExist(results[1]):
##                    UIimage = UIimages[5]
##                elif isResultExist(results[0]):
##                    UIimage = UIimages[3]
##                elif isResultExist(results[1]):
##                    UIimage = UIimages[4]
##                else:
##                    UIimage = UIimages[1]
##            else:
##                UIimage = UIimages[1]
##    else:
#    if isSingle:
#        UIimage = UIimages[0]
#    else:
#        UIimage = UIimages[1]
#
#    image= np.concatenate((UIimage,image),0)
#    
#    if isSingle:
#        image = drawLetters(image,results[0],20,220)
#    else:
#        image = drawLetters(image,results[0],20,153)
#        image = drawLetters(image,results[1],20,286)
#    cv2.putText(image,str(carChannel),(1850,32),cv2.cv.CV_FONT_HERSHEY_DUPLEX, 1.2, (0,0,0),2)
#    if int(craneNo) <10: #when the craneNO is larger than 10, there are are two digits. the location is different
#        cv2.putText(image,craneNo,(1707,32),cv2.cv.CV_FONT_HERSHEY_DUPLEX, 1.2, (0,0,0),2)
#    else:
#        cv2.putText(image,craneNo,(1690,32),cv2.cv.CV_FONT_HERSHEY_DUPLEX, 1.2, (0,0,0),2)
#    return image

def drawUI(images, UIimages, results, isSingle, carChannel, craneNo, lorryNum):
    if isSingle:
        UIimage = UIimages[0]
    else:
        UIimage = UIimages[1]

    for i in range(len(images)):
        image = images[i]
        if i == 0:
            resizedimage = cv2.resize(image, (560, 316))
            UIimage[376:692, 1349:1909, :] = resizedimage
        elif i == 1:
            resizedimage = cv2.resize(image, (560, 316))
            UIimage[701:1017, 1349:1909, :] = resizedimage
        elif i == 2:
            resizedimage = cv2.resize(image, (1329, 641))
            UIimage[376:1017, 10:1339, :] = resizedimage
        elif i == 4:
            resizedimage = cv2.resize(image, (560, 316))
            UIimage[50:366, 1349:1909, :] = resizedimage

    finalimage = UIimage.copy()
    if isSingle:
        finalimage = drawLetters(finalimage, results[0], 10, 242)
    else:
        finalimage = drawLetters(finalimage, results[0], 10, 173)
        finalimage = drawLetters(finalimage, results[1], 10, 301)
    cv2.putText(finalimage, str(carChannel), (1860, 32), cv2.cv.CV_FONT_HERSHEY_DUPLEX, 1.2, (0, 0, 0), 2)
    if len(craneNo) < 2:  # when the craneNO is larger than 10, there are are two digits. the location is different
        cv2.putText(finalimage, craneNo, (1717, 32), cv2.cv.CV_FONT_HERSHEY_DUPLEX, 1.2, (0, 0, 0), 2)
    else:
        cv2.putText(finalimage, craneNo, (1700, 32), cv2.cv.CV_FONT_HERSHEY_DUPLEX, 1.2, (0, 0, 0), 2)

    #    ##draw truck NUM
    if len(lorryNum) < 2:
        cv2.putText(finalimage, lorryNum, (1364, 32), cv2.cv.CV_FONT_HERSHEY_DUPLEX, 1.2, (0, 0, 0), 2)
    elif len(lorryNum) < 3:
        cv2.putText(finalimage, lorryNum, (1354, 32), cv2.cv.CV_FONT_HERSHEY_DUPLEX, 1.2, (0, 0, 0), 2)
    else:
        cv2.putText(finalimage, lorryNum, (1342, 32), cv2.cv.CV_FONT_HERSHEY_DUPLEX, 1.2, (0, 0, 0), 2)

    return finalimage


def drawLetters(image, result, coordinate_x, coordinate_y):
    if not isResultExist(result):
        return image
    #    if result == 'AAAA 0000000 0000 False' or result == 'AAAA 0000000 0000 True':
    #        return image
    for i, letter in enumerate(result):
        if i == 17:
            break
        if letter == ' ':
            coordinate_x += 5
            continue
        cv2.putText(image, letter, (coordinate_x, coordinate_y), cv2.cv.CV_FONT_HERSHEY_DUPLEX, 3.5, (0, 0, 0), 5)
        coordinate_x += 89
    return image


def isChipConnected(sqldata):
    cu = sqldata.cursor()
    command = 'select isConnected from ChipConnection'
    cu.execute(command)
    content = cu.fetchone()[0]
    cu.close()
    if content == 0:
        sys.exit('Chip Connection Lost')


def isResultExist(result):
    results = result.split(' ')
    if results[0] == 'AAAA' or results[1] == '0000000' or results[2] == '0000':
        return False
    else:
        return True


# def finalRecognition(predictions,singleScores,rule_checks,digitLocations,isSingle,finalresults):
##    print digitLocations[0][0]
#    if isSingle:
#        rule_check,finalResult,warningLocation = AdjustResult(predictions[0],singleScores[0])
#        if rule_check:
#            return False,[finalResult,finalResult],[np.zeros((0)),np.zeros((0))]
#        rule_check,finalResult,warningLocation = AdjustResult(predictions[0],singleScores[0])
#        if rule_check:
#            return False,[finalResult,finalResult],[np.zeros((0)),np.zeros((0))]
#        else:
#            return True,finalresults,[warningLocation,warningLocation]
#    else:
#        if (not rule_checks[0]) and (not rule_checks[1]):
#            rule_check1,finalResult1,warningLocation1 = AdjustResult(predictions[0],singleScores[0])
#            rule_check2,finalResult2,warningLocation2 = AdjustResult(predictions[1],singleScores[1])
#            if rule_check1 and rule_check2:
#                return False,[finalResult1,finalResult2],[np.zeros((0)),np.zeros((0))] #the first parameter is isWarning
#            elif rule_check1:
#                return True, [finalResult1,finalresults[1]],[np.zeros((0)),warningLocation2]
#            elif rule_check2:
#                return True, [finalresults[0],finalResult2],[warningLocation1,np.zeros((0))]
#            else:
#                return True,finalresults,[warningLocation1,warningLocation2]
#        elif (not rule_checks[0]):
#            rule_check,finalResult,warningLocation = AdjustResult(predictions[0],singleScores[0])
#            if rule_check:
#                return False,[finalResult,finalresults[1]],[np.zeros((0)),np.zeros((0))]
#            else:
#                return True,finalresults,[warningLocation,np.zeros((0))]
#        elif (not rule_checks[1]):
#            rule_check,finalResult,warningLocation = AdjustResult(predictions[1],singleScores[1])
#            if rule_check:
#                return False,[finalresults[0],finalResult],[np.zeros((0)),np.zeros((0))]
#            else:
#                return True,finalresults,[np.zeros((0)),warningLocation]
#
# def AdjustResult(prediction,singleScore): #only useful when there is only one digits or letter is wrong
#    elevenScore = np.concatenate((singleScore[0],singleScore[1]))
#    print elevenScore
#    if np.sum(elevenScore<0.96)>=2: #parameter 0.9 TBD
#        warningLocation = []
#        for i,singleScore in enumerate(elevenScore):
#            if singleScore<0.955:
#                warningLocation.append(i+1)
#        print warningLocation
#        return False,None,np.asarray(warningLocation)
#    minLoc = elevenScore.argmin()
#    if minLoc >=4 and elevenScore[minLoc] < 0.955:  #parameter 0.9 TBD
#        for i in range(10):
#            prediction[1][minLoc-4]=i
#            rule_check = CheckRules(prediction[1],prediction[0])
#            if rule_check:
#                finalReuslt = combineResult(prediction,True)
#                return True,finalReuslt,np.zeros((0))
#    else:
#        warningLocation = [minLoc+1]
#        print warningLocation
#    return False,None,np.asarray(warningLocation)

def scoreToString(Scores):
    score_string = ''
    for score in Scores:
        for singlescore in score:
            score_string += str(singlescore)
            score_string += '$'
    return score_string


def writeCorrectFile(Correct_file_single, Correct_file_double, finalResults, isWarning, isSingle):
    if isSingle:
        for singleresult in finalResults:
            Correct_file_single.write(singleresult + '$')
        if isWarning:
            Correct_file_single.write('0')
        else:
            Correct_file_single.write('1')
        Correct_file_single.write('\n')
        Correct_file_single.flush()
    else:
        for i in range(2):
            if finalResults[i].split(' ')[3] == 'True':
                Correct_file_double.write(finalResults[i] + '$' + '1' + '\n')
            else:
                Correct_file_double.write(finalResults[i] + '$' + '0' + '\n')
        Correct_file_double.flush()


def ModifyDeviceINI(craneNo):
    cameraConfig = ConfigParser.ConfigParser()
    cameraConfig.read('/home/westwell/Documents/NBPort/code/config/camera.ini')
    #    dbname = '/home/westwell/Documents/NBPort/code/LocationInfo/HarborInfo'+craneNo+'.db'
    #    conn = sqlite3.connect(dbname)
    #    cursor = conn.cursor()
    crane_str = 'Crane_' + craneNo
    deviceconfig = ConfigParser.ConfigParser()
    for i in range(4):
        deviceName = 'Device' + str(i + 1) + '.ini'
        #        cursor.execute("select cam_ip from CameraIPList where cam_no ='%s'" %(str(i+1)))
        #        ipvalue = cursor.fetchone()[0]
        cameraip_str = 'cam' + str(i + 1) + '_IP'
        username_str = 'cam' + str(i + 1) + '_username'
        pswd_str = 'cam' + str(i + 1) + '_password'
        ipvalue = cameraConfig.get(crane_str, cameraip_str)
        ipvalue += '		//'
        username = cameraConfig.get(crane_str, username_str)
        username += ' 	//'
        password = cameraConfig.get(crane_str, pswd_str)
        password += ' 	//'
        #        if i==0:
        #            ipvalue = '10.5.14.'+craneNo+'1		//'
        #        elif i==1:
        #            ipvalue = '10.5.14.'+craneNo+'4		//'
        #        elif i==2:
        #            ipvalue = '10.5.14.'+craneNo+'3		//'
        #        elif i==3:
        #            ipvalue = '10.5.14.'+craneNo+'2		//'
        deviceconfig.read(deviceName)
        deviceconfig.set("DEVICE", "ip", ipvalue)
        deviceconfig.set("DEVICE", "username", username)
        deviceconfig.set("DEVICE", "password", password)
        deviceconfig.write(open(deviceName, "wb"))


# cursor.close()
#    conn.close()


def writeLog(path, logname, message):
    CheckFolderExists(path)
    logfile = open(path + logname, 'a')
    logfile.write(str(time.localtime()) + '\n' + message + '\n')
    logfile.close()


# def sendSignal(inputstring): #for varify use only
#     connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
#     channel = connection.channel()
#     rpc_key = 'runme'
#     channel.queue_declare(queue=rpc_key)
#     channel.basic_publish(exchange='',
#                           routing_key=rpc_key,
#                           body=inputstring)
#     connection.close()


def derive_key_and_iv(password, salt, key_length, iv_length):
    d = d_i = ''
    while len(d) < key_length + iv_length:
        d_i = md5(d_i + password + salt).digest()
        d += d_i
    return d[:key_length], d[key_length:key_length + iv_length]


def decrypt(in_file, out_file, password, key_length=32):
    bs = AES.block_size
    salt = in_file.read(bs)[len('Salted__'):]
    key, iv = derive_key_and_iv(password, salt, key_length, bs)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    next_chunk = ''
    finished = False
    while not finished:
        chunk, next_chunk = next_chunk, cipher.decrypt(in_file.read(1024 * bs))
        if len(next_chunk) == 0:
            padding_length = ord(chunk[-1])
            chunk = chunk[:-padding_length]
            finished = True
        out_file.write(chunk)


def filedecrypy(path):
    files = [(a, s) for a, b, c in os.walk(path) for s in c if os.path.isfile(a + '/' + s)]
    prename = ""
    for decryptfile in files:
        Folders = decryptfile[0].split('/')
        Folders = decryptfile[0].split('/')
        SaveFolder = '/home/westwell/Documents/NBPort/Model/' + Folders[-1]
        CheckFolderExists(SaveFolder)
        #        print "Decrypting file: ", decryptfile[1]
        startdecrypt = time.time()
        if decryptfile[1] == 'test':

            with open(decryptfile[0] + '/' + decryptfile[1], 'rb') as in_file, open(
                                    SaveFolder + '/' + 'faster_rcnn_test.pt', 'wb') as out_file:

                decrypt(in_file, out_file, 'caffemodel')
        else:
            with open(decryptfile[0] + '/' + decryptfile[1], 'rb') as in_file, open(
                                                    SaveFolder + '/' + prename + decryptfile[1] + '.caffemodel',
                                                    'wb') as out_file:
                decrypt(in_file, out_file, 'caffemodel')


# print "***********"
#        print "*********"
#        print "decrypt time: ", time.time()-startdecrypt

def getDistanceMatrix(points):
    distance = np.zeros((points.shape[0], points.shape[0]))
    for i, singlepoint in enumerate(points):
        distance[i, :] = np.sqrt(np.sum((points - singlepoint) ** 2, 1))
    return distance


def removeOverlappedRegion(regions):
    numofregions = regions.shape[0]
    kepted = np.ones((numofregions), dtype=np.bool)
    for i, singleregion in enumerate(regions):
        if not kepted[i]:
            continue
        count = i + 1
        while count < numofregions:
            if not kepted[count]:
                count += 1
                continue
            IOU = BoxOverlap(singleregion, regions[count, :])
            # print 'IOU: ',IOU
            if IOU > 0.2:
                if singleregion[4] >= regions[count, 4]:
                    kepted[count] = False
                else:
                    kepted[i] = False
                    break
            count += 1
    # print kepted
    keptregion = regions[kepted, :]
    return keptregion

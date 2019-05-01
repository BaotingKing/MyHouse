#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author: Zhang.Baoting
# Time: 2018/7/30
import cv2


# ====================================================
# ===============Show result in UI====================
# ===============Show result in UI====================
def loadUIImage(imgnum, path='/home/UI/image/'):
    UI_image = []
    for i in range(1, imgnum):
        im_name = path + str(i) + '.jpg'
        image_temp = cv2.imread(im_name)
        UI_image.append(image_temp)
    return UI_image


def isResultExist(result):
    result = result.split(' ')     # appoint: space to distinguish
    if result[0] == 'AAAA' or result[1] == '0000000' or result[2] == '0000':
        # Initialize result: AAAA 0000000 0000 False/True
        return False
    else:
        return True


def drawLetters(image, result, coordinate_x, coordinate_y):
    if not isResultExist(result):
        return image
    for i, letter in enumerate(result):        # format: result = 'AAAA 0000000 0000 True'
        if i == 17:
            break
        if letter == '':
            coordinate_x += 5
            continue
        cv2.putText(image, letter, (coordinate_x, coordinate_y),\
                    cv2.CV_FEATURE_PARAMS_HOG, 3.5, (0,0,0), 5)
        coordinate_x += 89
    return image


def drawUI(images, UI_face_imgs, results, isSingle, carChannel, craneNo, lorryNum):
    """
    be careful the param   -->：2018-07
    """
    if isSingle:
        UIimage = UI_face_imgs[0]
    else:
        UIimage = UI_face_imgs[1]

    for i in range(len(images)):     # be careful---2018
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
        finalimage = drawLetters(finalimage, results[0], 560, 316)
    else:
        finalimage = drawLetters(finalimage, results[0], 10, 173)
        finalimage = drawLetters(finalimage, results[1], 10, 301)

    cv2.putText(finalimage, str(carChannel), (1860, 32), cv2.CV_FEATURE_PARAMS_HOG, 1.2, (0, 0, 0), 2)
    if len(craneNo) < 2:  # when the craneNO is larger than 10, there are are two digits. the location is different
        cv2.putText(finalimage, str(craneNo), (1717, 32), cv2.CV_FEATURE_PARAMS_HOG, 1.2, (0, 0, 0), 2)
    else:
        cv2.putText(finalimage, str(craneNo), (1700, 32), cv2.CV_FEATURE_PARAMS_HOG, 1.2, (0, 0, 0), 2)

    #    ##draw truck NUM
    if len(lorryNum) < 2:
        cv2.putText(finalimage, str(lorryNum), (1364, 32), cv2.CV_FEATURE_PARAMS_HOG, 1.2, (0, 0, 0), 2)
    elif len(lorryNum) < 3:
        cv2.putText(finalimage, str(lorryNum), (1354, 32), cv2.CV_FEATURE_PARAMS_HOG, 1.2, (0, 0, 0), 2)
    else:
        cv2.putText(finalimage, str(lorryNum), (1342, 32), cv2.CV_FEATURE_PARAMS_HOG, 1.2, (0, 0, 0), 2)

    return finalimage
"""
def drawUI_other(image,UIimages,results,isSingle,isStable,carChannel,craneNo):
    if isStable:
        result1_check = results[0].split(' ')[-1]
        result2_check = results[1].split(' ')[-1]
        if isSingle:
            if result1_check == 'False' and isResultExist(results[0]):
                UIimage = UIimages[2]
            else:
                UIimage = UIimages[0]
        else:
            if result1_check == 'False' and result2_check == 'True' and isResultExist(results[0]):
                UIimage = UIimages[3]
            elif result1_check == 'True' and result2_check == 'False' and isResultExist(results[1]):
                UIimage = UIimages[4]
            elif result1_check == 'False' and result2_check == 'False':
                if isResultExist(results[0]) and isResultExist(results[1]):
                    UIimage = UIimages[5]
                elif isResultExist(results[0]):
                    UIimage = UIimages[3]
                elif isResultExist(results[1]):
                    UIimage = UIimages[4]
                else:
                    UIimage = UIimages[1]
            else:
                UIimage = UIimages[1]
    else:
        if isSingle:
            UIimage = UIimages[0]
        else:
            UIimage = UIimages[1]
            image= np.concatenate((UIimage,image),0)

    if isSingle:
        image = drawLetters(image,results[0],20,220)
    else:
        image = drawLetters(image,results[0],20,153)
        image = drawLetters(image,results[1],20,286)

    cv2.putText(image,str(carChannel),(1850,32),cv2.cv.CV_FONT_HERSHEY_DUPLEX, 1.2, (0,0,0),2)
    if int(craneNo) <10: #when the craneNO is larger than 10, there are are two digits. the location is different
        cv2.putText(image,craneNo,(1707,32),cv2.cv.CV_FONT_HERSHEY_DUPLEX, 1.2, (0,0,0),2)
    else:
        cv2.putText(image,craneNo,(1690,32),cv2.cv.CV_FONT_HERSHEY_DUPLEX, 1.2, (0,0,0),2)

    return image
"""
#!/usr/bin/python
# -*- coding: utf-8 -*-
# @author: ZK
# Time: 2019/06/06
# Func: continuously captures images for camera calibration
import cv2
import os
import numpy as np
import time


def save_load_param(pattern, img_size=None, result_cm=None, result_dc=None):
    if pattern == 'load':
        if os.path.isfile('cameraMatrix.npy'):
            cm = np.load('cameraMatrix.npy')
        else:
            cm = None
        if os.path.isfile('distCoeffs.npy'):
            dc = np.load('distCoeffs.npy')
        else:
            dc = None
        return cm, dc
    elif pattern == 'save':
        np.save('cameraMatrix.npy', result_cm)
        np.save('distCoeffs.npy', result_dc)
        with open('result_parm.txt', 'a+') as f_handle:
            print('================================================', file=f_handle)
            print('The Camera images size is:', img_size, file=f_handle)
            print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), file=f_handle)
            print('Camera parameter information:\ncameraMatrix:\n{0} \n distCoeffs:\n{1}'.format(result_cm, result_dc), file=f_handle)



def calibrate_proc(board, flag=False):
    """The camera continuously captures images for camera calibration"""
    capture_num = 10  # Number of capture needed
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
    x_cor = board[0]
    y_cor = board[1]

    objp = np.zeros((x_cor * y_cor, 3), np.float32)
    objp[:, :2] = np.mgrid[0:x_cor, 0:y_cor].T.reshape(-1, 2)
    # objp[:, 0] = objp[:, 0] * square_size[0]
    # objp[:, 1] = objp[:, 1] * square_size[1]
    obj_points = []  # 3d points in real world space
    img_points = []  # 2d points in image plane.

    cap = cv2.VideoCapture(0)
    count = 0  # Record the number of successful checkerboard images detected
    while True:
        ret, frame = cap.read()
        if cv2.waitKey(1) & 0xFF == ord(' '):
            img_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            # Step1: Extract corner information
            ret, corners = cv2.findChessboardCorners(img_gray, (x_cor, y_cor), None)  # Find the corners

            if ret:
                print('This is cnt:{0}/{1}'.format(count, capture_num))
                # Step2: Further extract sub-pixel corner information
                corners = cv2.cornerSubPix(img_gray, corners, (5, 5), (-1, -1), criteria)
                obj_points.append(objp)
                img_points.append(corners)
                # Step3: Draw the interior corner points found on the checkerboard calibration map(optional)
                cv2.drawChessboardCorners(frame, (x_cor, y_cor), corners, ret)

                count += 1
                if count >= capture_num:
                    print('Finished capture images and Camera calibrate....')
                    break
            else:
                print('Continue.....')

        cv2.imshow('Camera calibrate', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Step4: Camera calibrate
    global cameraMatrix, distCoeffs
    ret, cameraMatrix, distCoeffs, rvecs, tvecs = cv2.calibrateCamera(objectPoints=obj_points,
                                                                      imagePoints=img_points,
                                                                      imageSize=img_gray.shape[::-1],
                                                                      cameraMatrix=None,
                                                                      distCoeffs=None)
    print('================================================')
    print('The Camera images size is:', img_gray.shape[::-1])
    print('Camera parameter information:\ncameraMatrix:\n{0} \n distCoeffs:\n{1}'.format(cameraMatrix, distCoeffs))
    save_load_param(pattern='save', img_size=img_gray.shape, result_cm=cameraMatrix, result_dc=distCoeffs)

    mean_error = 0
    for i in range(len(obj_points)):
        imgpoints2, _ = cv2.projectPoints(obj_points[i], rvecs[i], tvecs[i], cameraMatrix, distCoeffs)
        error = cv2.norm(img_points[i], imgpoints2, cv2.NORM_L2) / len(imgpoints2)
        mean_error += error

    print("total error: ", mean_error / len(obj_points))


if __name__ == '__main__':
    print('*********************:Start camera calibration')
    board_shape = (6, 9)  # 棋盘格内角规格
    calibrate_proc(board_shape)
    print('*********************: End')

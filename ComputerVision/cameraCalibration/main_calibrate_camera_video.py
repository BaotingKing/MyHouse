#!/usr/bin/python
# -*- coding: utf-8 -*-
# @author: ZK
# Time: 2019/06/06
# Func: continuously captures images for camera calibration
import cv2
import numpy as np


def calibrate_proc(board):
    """The camera continuously captures images for camera calibration"""
    capture_num = 3  # Number of capture needed
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
    x_cor = board[0]
    y_cor = board[1]

    objp = np.zeros((x_cor * y_cor, 3), np.float32)
    objp[:, :2] = np.mgrid[0:x_cor, 0:y_cor].T.reshape(-1, 2)
    # objp[:, 0] = objp[:, 0] * 10
    # objp[:, 1] = objp[:, 1] * 10
    obj_points = []  # 3d points in real world space
    img_points = []  # 2d points in image plane.

    cap = cv2.VideoCapture(1)
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
                if count > capture_num:
                    print('Finished capture images and Camera calibrate....')
                    break
            else:
                print('Continue.....')

        cv2.imshow('Here', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Step4: Camera calibrate
    global cameraMatrix, distCoeffs
    ret, cameraMatrix, distCoeffs, rvecs, tvecs = cv2.calibrateCamera(objectPoints=obj_points,
                                                                      imagePoints=img_points,
                                                                      imageSize=img_gray.shape[::-1],
                                                                      cameraMatrix=None,
                                                                      distCoeffs=None)
    print('Camera parameter information:\ncameraMatrix:\n{0} \n distCoeffs:\n{1}'.format(cameraMatrix, distCoeffs))

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

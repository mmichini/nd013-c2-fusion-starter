# ---------------------------------------------------------------------
# Project "Track 3D-Objects Over Time"
# Copyright (C) 2020, Dr. Antje Muntzinger / Dr. Andreas Haja.
#
# Purpose of this file : Kalman filter class
#
# You should have received a copy of the Udacity license together with this program.
#
# https://www.udacity.com/course/self-driving-car-engineer-nanodegree--nd013
# ----------------------------------------------------------------------
#

# imports
import numpy as np

# add project directory to python path to enable relative imports
import os
import sys
PACKAGE_PARENT = '..'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))
import misc.params as params 

class Filter:
    '''Kalman filter class'''
    def __init__(self):
        pass

    def F(self):
        ############
        # TODO Step 1: implement and return system matrix F
        ############

        # Retrieve the dt value from the params
        dt = params.dt

        # Create the F matrix
        F = np.matrix([
            [1,  0,  0, dt,  0,  0],
            [0,  1,  0,  0, dt,  0],
            [0,  0,  1,  0,  0, dt],
            [0,  0,  0,  1,  0,  0],
            [0,  0,  0,  0,  1,  0],
            [0,  0,  0,  0,  0,  1]])

        return F
        
        ############
        # END student code
        ############ 

    def Q(self):
        ############
        # TODO Step 1: implement and return process noise covariance Q
        ############

        q = params.q

        Q = np.matrix([
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, q, 0, 0],
            [0, 0, 0, 0, q, 0],
            [0, 0, 0, 0, 0, q]])

        return Q
        
        ############
        # END student code
        ############ 

    def predict(self, track):
        ############
        # TODO Step 1: predict state x and estimation error covariance P to next timestep, save x and P in track
        ############

        x = track.x
        P = track.P

        F = self.F()
        Q = self.Q()

        x = F * x # state prediction
        P = F * P * F.transpose() + Q # covariance prediction

        track.set_x(x)
        track.set_P(P)

        return x, P
        
        ############
        # END student code
        ############ 

    def update(self, track, meas):
        ############
        # TODO Step 1: update state x and covariance P with associated measurement, save x and P in track
        ############

        x = track.x
        P = track.P

        H = meas.sensor.get_H(x)
        gamma = self.gamma(track, meas)
        S = self.S(track, meas, H)

        # Compute Kalman gain
        K = P * H.transpose() * np.linalg.inv(S)

        # Update state
        x = x + K * gamma

        # Update state covariance
        I = np.eye(P.shape[0])
        P = (I - K * H) * P

        track.set_x(x)
        track.set_P(P)

        ############
        # END student code
        ############ 
        track.update_attributes(meas)
    
    def gamma(self, track, meas):
        ############
        # TODO Step 1: calculate and return residual gamma
        ############

        hx = meas.sensor.get_hx(track.x)
        gamma = meas.z - hx

        return gamma
        
        ############
        # END student code
        ############ 

    def S(self, track, meas, H):
        ############
        # TODO Step 1: calculate and return covariance of residual S
        ############
        
        R = meas.R
        P = track.P

        S = H*P*H.transpose() + R

        return S
        
        ############
        # END student code
        ############ 
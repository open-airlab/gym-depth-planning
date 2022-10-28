import gym
import gym_depth_planning
import numpy as np
import matplotlib.pyplot as plt
import os
from matplotlib import rc
import pickle

rc('font', **{'family': 'serif', 'size': '12'})
rc('text', usetex=True)


class ApfAgent():
    def __init__(self):
        pass

    def compute_action(self, observation):
        target = observation['moving_target']
        print(target)
        distances = observation['depth_cam'][32, :]/255*15.
        alpha = 0.1
        repel_x = 0
        repel_y = 0
        for i in range(64):
            distance = distances[i]
            if distance > 10:
                continue
            angle = np.arctan2(31.5 - i, 31.5)
            repel_pixel = 1 / (distance * distance + 0.1)
            repel_x -= np.cos(angle) * repel_pixel
            repel_y -= np.sin(angle) * repel_pixel
            # print(repel_x, repel_y, angle*180/np.pi)
        atract_x = alpha * target[0]
        atract_y = alpha * target[1]
        force_x = atract_x + repel_x
        force_y = atract_y + repel_y
        print(force_x, force_y)
        force_angle = np.arctan2(force_y, force_x) * 180 / np.pi
        print(force_angle)
        if np.abs(force_angle) < 22.5:
            return np.clip([force_angle/22.5, 0], -1, 1)
        else:
            return np.clip([np.sign(force_angle), np.sign(force_angle)*(np.abs(force_angle)-22.5)/22.5], -1, 1)

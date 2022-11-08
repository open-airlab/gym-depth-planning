import os
from pathlib import Path

import gym, gym_depth_planning
import numpy as np

from stable_baselines3 import PPO
from stable_baselines3.common.monitor import Monitor
from stable_baselines3.common.vec_env import DummyVecEnv
from stable_baselines3.common.results_plotter import load_results, ts2xy
from stable_baselines3.common.callbacks import CheckpointCallback

from gym_depth_planning.utils import sys_utils


if __name__ == '__main__':
    env = gym.make("depth_planner-v0", no_dynamics=True, discrete_actions=False)  ## switch discrete_actions=True for DDP
    env.env.forward_direction = True
    env.env.start_x = -10
    env.env.enable_safety_reward = True  # True for SCDP, False for CDP and DDP
    logdir = sys_utils.get_or_create_dir(os.getcwd(), "log")
    env = Monitor(env, filename=logdir, allow_early_resets=True)
    env = DummyVecEnv([lambda: env])

    model = PPO("MultiInputPolicy", env, n_steps=1024, verbose=1)
    checkpoint_callback = CheckpointCallback(save_freq=1000, save_path='./log/', name_prefix='rl_model')
    model.learn(total_timesteps=int(1e5), callback=checkpoint_callback)

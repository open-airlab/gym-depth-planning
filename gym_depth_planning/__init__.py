from gym.envs.registration import register

register(
    id='depth_planner-v0',
    entry_point='gym_depth_planning.envs:UAVDepthPlanningEnv_v0',
)

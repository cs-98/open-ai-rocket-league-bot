import rlgym
from rlgym.utils.obs_builders import ObsBuilder
from rlgym.utils import common_values
from rlgym.utils.gamestates import PlayerData, GameState
import numpy as np
from rlgym.utils.terminal_conditions import TerminalCondition
from rlgym.utils.terminal_conditions.common_conditions import TimeoutCondition
from rlgym.utils.state_setters import StateSetter
from rlgym.utils.state_setters import StateWrapper
from rlgym.utils.common_values import BLUE_TEAM, ORANGE_TEAM, CEILING_Z
from stable_baselines3 import PPO

# importing one of the built-in reward functions
from rlgym.utils.reward_functions.common_rewards import LiuDistancePlayerToBallReward

# custom observation builder provided by the tutorial
# observation builders serve to inform the model about the changing environment.
class CustomObsBuilderBluePerspective(ObsBuilder):
  def reset(self, initial_state: GameState):
    pass

  def build_obs(self, player: PlayerData, state: GameState, previous_action: np.ndarray):
    obs = []
    
    #If this observation is being built for a player on the orange team, we need to invert all the physics data we use.
    inverted = player.team_num == common_values.ORANGE_TEAM
    
    if inverted:
      obs += state.inverted_ball.serialize()
    else:
      obs += state.ball.serialize()
      
    for player in state.players:
      if inverted:
        obs += player.inverted_car_data.serialize()
      else:
        obs += player.car_data.serialize()
    
    return np.asarray(obs, dtype=np.float32)

# custom terminal condition provided by the tutorial
# terminal condition defines the condition that an agent must meet to end their current iteration/episode and reset to the initial state.
class CustomTerminalCondition(TerminalCondition):
  def reset(self, initial_state: GameState):
    pass

  def is_terminal(self, current_state: GameState) -> bool:
    return current_state.last_touch != -1

# another terminal condition but this time based on whether an agent fails to hit the ball in a certain amount of time
default_tick_skip = 8
physics_ticks_per_second = 120
ep_len_seconds = 20

max_steps = int(round(ep_len_seconds * physics_ticks_per_second / default_tick_skip))

condition1 = TimeoutCondition(max_steps)
condition2 = CustomTerminalCondition()

# custom state setter which allows you to manipulate the state of the game to your liking. In this instance, the ball is placed near the center with the player.
class CustomStateSetter(StateSetter):
    def reset(self, state_wrapper: StateWrapper):
    
        # Set up our desired spawn location and orientation. Here, we will only change the yaw, leaving the remaining orientation values unchanged.
        desired_car_pos = [100,100,17] #x, y, z
        desired_yaw = np.pi/2
        
        # Loop over every car in the game.
        for car in state_wrapper.cars:
            if car.team_num == BLUE_TEAM:
                pos = desired_car_pos
                yaw = desired_yaw
                
            elif car.team_num == ORANGE_TEAM:
                # We will invert values for the orange team so our state setter treats both teams in the same way.
                pos = [-1*coord for coord in desired_car_pos]
                yaw = -1*desired_yaw
                
            # Now we just use the provided setters in the CarWrapper we are manipulating to set its state. Note that here we are unpacking the pos array to set the position of 
            # the car. This is merely for convenience, and we will set the x,y,z coordinates directly when we set the state of the ball in a moment.
            car.set_pos(*pos)
            car.set_rot(yaw=yaw)
            car.boost = 0.33
            
        # Now we will spawn the ball in the center of the field, floating in the air.
        state_wrapper.ball.set_pos(x=0, y=0, z=CEILING_Z/2)

# pass everything we created to the rlgym function to make a model
env = rlgym.make(game_speed=10, reward_fn = LiuDistancePlayerToBallReward(), obs_builder=CustomObsBuilderBluePerspective(), terminal_conditions=[condition1, condition2], state_setter=CustomStateSetter())

#Initialize PPO from stable_baselines3
model = PPO("MlpPolicy", env=env, verbose=1)

#Train our agent!
model.learn(total_timesteps=int(1e6))

while True:
    obs = env.reset()
    done = False

    while not done:
      #Here we sample a random action. If you have an agent, you would get an action from it here.
      action1 = env.action_space.sample() 
      #action2 = env.action_space.sample()
      #actions = [action1, action2]
      next_obs, reward, done, gameinfo = env.step(action1)
      
      obs = next_obs
######################################################
#       Main file of Project  -  Used to call all agents
######################################################


from AgentOneSimulator import *
from AgentTwoSimulator import *
from AgentThreeSimulator import *
from AgentFourSimulator import *
from UStarAgent import *


if __name__=="__main__":

    simulate_agent_one(1,44,45)
    simulate_agent_two(1,44,45)
    simulate_u_star_agent(1,44,45)

         
import time

from discoverySimulator.obstacles import RectangularObstacle
from discoverySimulator.obstacles.CircularObstacle import CircularObstacle
from discoverySimulator.ressources.RL import RL
from discoverySimulator.robots import CircularTwoWheelsRobot
from discoverySimulator.sensors import Telemeter
from discoverySimulator.simulation import Environment, Simulation

def reinforcementLearningTest():

    env=Environment(900,900)
    robot=CircularTwoWheelsRobot()
    telemeter1 = Telemeter(maximumMeasurableDistance=50)
    telemeter2 = Telemeter(maximumMeasurableDistance=50)
    robot.addComponent(telemeter1,0,20,20)
    robot.addComponent(telemeter2,0,20,-20)
    env.addObject(robot,500,400,-90)
    env.addObject(CircularObstacle(40, "#ff8fff"), 600, 250)
    env.addObject(CircularObstacle(30, "#ff8fff"), 700, 200)
    env.addObject(CircularObstacle(50, "#ff8fff"), 650, 500)
    env.addObject(CircularObstacle(20, "#ff8fff"), 300, 600)
    env.addObject(CircularObstacle(55, "#ff8fff"), 400, 800)
    env.addObject(CircularObstacle(55, "#ff8fff"), 150, 150)
    env.addObject(RectangularObstacle(40, 200, "#ff8fff"), 650, 400, 10)
    env.addObject(RectangularObstacle(50, 100, "#ff8fff"), 550, 600, 45)
    env.addObject(RectangularObstacle(50, 100, "#ff8fff"), 450, 300, 0)
    env.addObject(RectangularObstacle(100, 150, "#ff8fff"), 380, 450, -90)

    actionBuilders = [
        {
            "id":robot.getLeftWheel().getID(),
            "getter": robot.getLeftWheel().getSpeed,
            "setter": robot.getLeftWheel().setSpeed,
            "min": 0,
            "max": 300,
            "intervals":2
        },
        {
            "id":robot.getRightWheel().getID(),
            "getter": robot.getRightWheel().getSpeed,
            "setter": robot.getRightWheel().setSpeed,
            "min": 0,
            "max": 300,
            "intervals":2
        }
    ]

    spaceBuilders = [
        {"id":robot.getLeftWheel().getID()},
        {"id":robot.getRightWheel().getID()},
        {
            "id":telemeter1.getID(),
            "getter": telemeter1.getValue,
            "min":0,
            "max":telemeter1.getMaximumMesurableDistance(),
            "intervals":1
        },
        {
            "id": telemeter2.getID(),
            "getter": telemeter2.getValue,
            "min": 0,
            "max": telemeter2.getMaximumMesurableDistance(),
            "intervals": 1
        }
    ]

    rl = RL(actionBuilders,spaceBuilders,{
        "explorationRateDecrease":0.999,
        "discount":0.7,
        "learning":0.2
    })

    sim = Simulation(env)
    sim.run()
    sim.showInterface()

    initialPose = robot.getPose().copy()

    while True:
        if not robot.getCollidedState():
            startPosition = (robot.getPose().getX(), robot.getPose().getY())
            startOrientation = robot.getPose().getOrientation()
            startOrientation %= 360

            before_closest_obstacle = min(telemeter1.getValue(), telemeter2.getValue())

            # action during 0.1 second to see the result of the action
            rl.execute()

            time.sleep(0.1)

            endPosition = (robot.getPose().getX(), robot.getPose().getY())
            endOrientation = robot.getPose().getOrientation()

            distance = ((endPosition[0] - startPosition[0]) ** 2 + (endPosition[1] - startPosition[1]) ** 2)**0.5
            # distance*=(robot.getLeftWheel().getSpeed()+robot.getRightWheel().getSpeed())/abs(robot.getLeftWheel().getSpeed()+robot.getRightWheel().getSpeed()+1)

            after_closest_obstacle = min(telemeter1.getValue(),telemeter2.getValue())
            # reward+=(robot.getLeftLinearSpeed()+robot.getRightLinearSpeed())/2 * 0.1
            # reward+= (endOrientation-startOrientation)**2 *-0.3
            #
            # if robot.getCollidedState():
            #     reward=-1000
            if after_closest_obstacle==telemeter1.getMaximumMesurableDistance() and before_closest_obstacle<telemeter1.getMaximumMesurableDistance():
                reward=1
            elif after_closest_obstacle<telemeter1.getMaximumMesurableDistance() and before_closest_obstacle==telemeter1.getMaximumMesurableDistance():
                reward=-1
            elif after_closest_obstacle<telemeter1.getMaximumMesurableDistance() and before_closest_obstacle<telemeter1.getMaximumMesurableDistance() and after_closest_obstacle<before_closest_obstacle:
                reward=-1
            elif after_closest_obstacle <telemeter1.getMaximumMesurableDistance() and before_closest_obstacle<telemeter1.getMaximumMesurableDistance() and after_closest_obstacle >= before_closest_obstacle:
                reward=0
            else:
                reward=distance/(1+(endOrientation-startOrientation)**2)

            # reward += (robot.getLeftLinearSpeed() + robot.getRightLinearSpeed()) / abs(robot.getLeftLinearSpeed() + robot.getRightLinearSpeed()+1) * distance/(1+(endOrientation-startOrientation)**2) * 0.6
            # print(reward)
            rl.learn(reward)
        else:
            robot.setPose(initialPose.copy())
            robot.setLeftWheelSpeed(0)
            robot.setRightWheelSpeed(0)
            robot.setCollidedState(False)
            rl.reset()

        time.sleep(.01)

    # # pretrained table
    # while True:
    #     rl.execute()
    #     time.sleep(.01)








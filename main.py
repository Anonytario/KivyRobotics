import kivy
import socket
from kivy.app import App
from kivy.uix.widget import Widget

try:
    import sim
except:
    print ('--------------------------------------------------------------')
    print ('"sim.py" could not be imported. This means very probably that')
    print ('either "sim.py" or the remoteApi library could not be found.')
    print ('Make sure both are in the same folder as this file,')
    print ('or appropriately adjust the file "sim.py"')
    print ('--------------------------------------------------------------')
    print ('')

import time

print ('Program started')
clientID = sim.simxStart('192.168.0.109',19999,True,True,5000,5)
sim.simxAddStatusbarMessage(clientID,'Funcionando...',sim.simx_opmode_oneshot_wait)
sim.simxFinish(-1) # just in case, close all opened connections
clientID=sim.simxStart('192.168.0.109',19999,True,True,5000,5) # Connect to CoppeliaSim
robotname = 'LineTracer'
res,objs=sim.simxGetObjects(clientID,sim.sim_handle_all,sim.simx_opmode_blocking)
if res==sim.simx_return_ok:
    print ('Number of objects in the scene: ',len(objs))
else:
    print ('Remote API function call returned with error code: ',res)

time.sleep(0.02)

erro, robot = sim.simxGetObjectHandle(clientID, robotname, sim.simx_opmode_oneshot_wait)
[erro, robotLeftMotor] = sim.simxGetObjectHandle(clientID, 'DynamicLeftJoint',sim.simx_opmode_oneshot_wait)
[erro, robotRightMotor] = sim.simxGetObjectHandle(clientID, 'DynamicRightJoint', sim.simx_opmode_oneshot_wait)

class PongGame(Widget):

    def quit(self):
        sim.simxPauseSimulation(clientID,sim.simx_opmode_oneshot_wait)

    def pressR(self):
        vref = 1.0
        sim.simxPauseCommunication(clientID, True)
        sim.simxSetJointTargetVelocity(clientID, robotRightMotor, vref, sim.simx_opmode_oneshot)
        sim.simxPauseCommunication(clientID, False)

    def releaseR(self):
        vref = 0.0
        sim.simxPauseCommunication(clientID, True)
        sim.simxSetJointTargetVelocity(clientID, robotRightMotor, vref, sim.simx_opmode_oneshot)
        sim.simxPauseCommunication(clientID, False)

    def pressL(self):
        vref = 1.0
        sim.simxPauseCommunication(clientID, True)
        sim.simxSetJointTargetVelocity(clientID, robotLeftMotor, vref, sim.simx_opmode_oneshot)
        sim.simxPauseCommunication(clientID, False)

    def releaseL(self):
        vref = 0.0
        sim.simxPauseCommunication(clientID, True)
        sim.simxSetJointTargetVelocity(clientID, robotLeftMotor, vref, sim.simx_opmode_oneshot)
        sim.simxPauseCommunication(clientID, False)


class PongApp(App):
    def build(self):
        return PongGame()


if __name__ == '__main__':
    PongApp().run()
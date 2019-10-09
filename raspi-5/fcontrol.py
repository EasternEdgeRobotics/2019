import control
import sys
sys.path.append('libraries')
import maestro

servo = maestro.Controller()

th = control.Thruster(servo, int(sys.argv[1]))

th.Fly(float(sys.argv[2]))

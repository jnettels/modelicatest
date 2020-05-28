"""Example script for testing the latest OMPython with AixLib 0.9.1.

While the simulation of the CHP works just fine, the HeatPump example
fails without any error message.
After the simulate() command is called, the script simply never
finishes and an omc.exe task keeps running seemingly indefinitely.

python -m pip install -U https://github.com/OpenModelica/OMPython/archive/master.zip
"""

import os
import sys
from OMPython import OMCSessionZMQ


def run_OpenModelica_CLI():
    """Run simulations with calls to the OpenModelica command line."""
    # Create a subdirectory for the simulation
    sim_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                           'sim_'+sys.platform  # separate windows and linux
                           )

    if os.path.exists(sim_dir) is False:
        os.mkdir(sim_dir)

    omc = OMCSessionZMQ()
    base_path = omc.sendExpression('getInstallationDirectoryPath()')
    file = os.path.join(base_path, r'lib/omlibrary/AixLib 0.9.1/package.mo')

    cmds = [
        'loadFile("{}")'.format(file),
        'cd("{}")'.format(sim_dir),
        # CHP example
        'checkModel(AixLib.FastHVAC.Examples.HeatGenerators.CHP.CHP)',
        'simulate(AixLib.FastHVAC.Examples.HeatGenerators.CHP.CHP)',
        'plot(temperatureSensor_after.T)',
        # heatpump example
        'checkModel(AixLib.FastHVAC.Examples.HeatGenerators.HeatPump.HeatPump)',
        'simulate(AixLib.FastHVAC.Examples.HeatGenerators.HeatPump.HeatPump)',
        'plot(innerCycle.QCon)',
      ]
    for cmd in cmds:
        print('\n{}:'.format(cmd))
        answer = omc.sendExpression(cmd)
        print('{}\n'.format(answer))


if __name__ == '__main__':
    run_OpenModelica_CLI()

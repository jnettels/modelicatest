"""Example script for testing the latest OMPython with AixLib 0.9.1.

While the simulation of the CHP works just fine, the HeatPump example
fails without any error message.
After the simulate() command is called, the script simply never
finishes and an omc.exe task keeps running seemingly indefinitely.

python -m pip install -U https://github.com/OpenModelica/OMPython/archive/master.zip
"""

import os
import sys
import pprint
from OMPython import OMCSessionZMQ


def main():
    """Run argument parser."""
    args = run_ArgParser()
    model = args.model

    if model == 'all':
        run_series()
    else:
        run_OpenModelica_CLI(model)


def run_OpenModelica_CLI(model=None):
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

    model = "AixLib.FastHVAC.Examples.{}".format(model)
    cmds = [
        'setCommandLineOptions("-d=newInst")',
        'loadFile("{}")'.format(file),
        'cd("{}")'.format(sim_dir),
        'isPackage({})'.format(model),
        'isModel({})'.format(model),
        'checkModel({})'.format(model),
        'simulate({})'.format(model),
        # 'plot(temperatureSensor_after.T)',
        # 'plot(innerCycle.QCon)',
      ]

    for cmd in cmds:
        print(cmd)
        answer = omc.sendExpression(cmd)
        pprint.pprint(answer)
        print()


def run_series():
    """Run a series of models."""
    models = [
        'Chiller.Chiller',  # needs "New Frontend"
        'HeatExchangers.DHWHeatExchanger',
        'HeatExchangers.MultiRadiator',
        'HeatExchangers.RadiatorMultiLayer',
        'HeatGenerators.Boiler.Boiler',
        'HeatGenerators.CHP.CHP',
        'HeatGenerators.HeatPump.HeatPump',  # needs "New Frontend"
        'Examples.Pipes.Pipes',
        'Pumps.FluidSource',
        'Pumps.Pump',
        'Sensors.SensorVerification',
        'Sinks.SinkSourceVesselTest',
        'Storage.BufferStorageVariablePorts',
        'Valves.ThermostaticValve',
        'Valves.ThermostaticValveRadiator',
        'Valves.ThreeWayValve',
        ]
    for model in models:
        run_OpenModelica_CLI(model)

    print('All models simulated.')


def run_ArgParser():
    """Define and run the argument parser. Return the chosen file path."""
    import argparse

    description = 'Run Modelica with AixLib example models'
    parser = argparse.ArgumentParser(description=description,
                                     formatter_class=argparse.
                                     ArgumentDefaultsHelpFormatter)

    parser.add_argument('-m', '--model', dest='model', help='name of model.',
                        type=str, default='HeatGenerators.CHP.CHP')

    return parser.parse_args()


if __name__ == '__main__':
    main()
    # run_OpenModelica_CLI('HeatGenerators.HeatPump.HeatPump')
    # run_series()

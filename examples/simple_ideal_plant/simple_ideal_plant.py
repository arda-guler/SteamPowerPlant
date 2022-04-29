# 3rd party imports
from iapws import IAPWS95 as Water # for water properties
import warnings
warnings.filterwarnings("ignore") # stop scipy from freaking out (optional)

# local imports
from machinery import *

# initialize thermodynamic devices
d_pump = pump() # isentropic pump
d_boiler = boiler() # constant pressure boiler
d_turbine = turbine() # isentropic turbine
d_condenser = condenser() # constant pressure condenser
devices = [d_pump, d_boiler, d_turbine, d_condenser]

# set mass flow rate in kg/s
# all devices use the same flow
mdot = 150
for d in devices:
    d.set_property("mdot", mdot)

# if you wanted to have an arbitrary mdot and use
# specific (per mass) values in your calculations,
# you could just set mdot = 1 and enter specific
# values for all Q and W values

# first device to use is the pump
# set pump work input in kW
d_pump.set_property("W in", 250)

# set pump inlet state, 0.01 MPa, 0 quality 
d_pump.set_inlet_state(Water(P=0.01, x=0))

# calculate pump outlet state
d_pump.solve_for_outlet()

print("Insentropic pump:")
print("Pump h out:", d_pump.outlet_state.h)
print("Pump P out:", d_pump.outlet_state.P)
print("Pump T out:", d_pump.outlet_state.T)
print("")

# let's move on to the boiler
# set the heat input first
d_boiler.set_property("Q in", 450000)

# connect pump outlet to boiler inlet
d_boiler.set_inlet_state(d_pump.outlet_state)

# calculate boiler outlet state
d_boiler.solve_for_outlet()

print("Constant pressure boiler:")
print("Boiler h out:", d_boiler.outlet_state.h)
print("Boiler P out:", d_boiler.outlet_state.P)
print("Boiler T out:", d_boiler.outlet_state.T)
print("")

# time to move onto the turbine
# first connect the boiler outlet
# to turbine inlet
d_turbine.set_inlet_state(d_boiler.outlet_state)

# let's do something different and go the other way
# around this time; we will specify the outlet state
# and get the work output

# since condenser is constant pressure, turbine outlet
# pressure has to be the same as condenser outlet, which
# is already fixed.
# also, since the turbine is isentropic, the turbine
# inlet and outlet entropies should be the same
d_turbine.set_outlet_state(Water(P=d_pump.inlet_state.P, s=d_turbine.inlet_state.s))
turbine_work = d_turbine.solve_for_W_out()
print("Turbine work output (kW): %.2f kW" % turbine_work)

# finally, moving onto the condenser
# outlet and inlet states are fixed
d_condenser.set_inlet_state(d_turbine.outlet_state)
d_condenser.set_outlet_state(d_pump.inlet_state)

# let's get the heat rejection
Q_out = d_condenser.solve_for_Q_out()
print("Condenser heat rejection (kW): %.2f kW" % Q_out)

# before we end the program, let's also calculate
# power plant efficiency
plant_efficiency = (d_turbine.data["W out"] - d_pump.data["W in"])/d_boiler.data["Q in"]
print("\nPower plant efficiency: " + str(plant_efficiency*100) + "%")

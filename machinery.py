from iapws import IAPWS95 as Water # for water properties

class device:
    def set_property(self, prop, val):
        self.data[prop] = val

    def set_inlet_state(self, state):
        self.inlet_state = state

    def set_outlet_state(self, state):
        self.outlet_state = state

class turbine(device):
    def __init__(self):
        self.data = {
            "W out": None,
            "mdot": None}

    def solve_for_W_out(self):
        self.data["W out"] = (self.inlet_state.h - self.outlet_state.h) * self.data["mdot"]
        return self.data["W out"]

class pump(device):
    def __init__(self):
        self.data = {
            "W in": None,
            "mdot": None}

    def solve_for_outlet(self):
        h_out = self.inlet_state.h + self.data["W in"]/self.data["mdot"]
        self.outlet_state = Water(h=h_out, s=self.inlet_state.s)
        return self.outlet_state

class boiler(device):
    def __init__(self):
        self.data = {
            "Q in": None,
            "mdot": None}

    def solve_for_outlet(self):
        h_out = self.inlet_state.h + self.data["Q in"]/self.data["mdot"]
        self.outlet_state = Water(h=h_out, P=self.inlet_state.P)
        return self.outlet_state

class condenser(device):
    def __init__(self):
        self.data = {
            "Q out": None,
            "mdot": None}

    def solve_for_Q_out(self):
        self.data["Q out"] = (self.inlet_state.h - self.outlet_state.h) * self.data["mdot"]
        return self.data["Q out"]

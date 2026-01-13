
class loadCellParams:
    def __init__(self, cell_name):
        # Takes the cell properties and stores it as a dictionary

    def get_manu


class calculate_pack_parameters:
    '''
    For a given cell,
    * nominal voltage target is created and the tolerance on it is defined - defining the potential series configurations
    * energy target is created and the tolerance on it is defined - defining the potential parallel configurations (when also accounting for the series voltage)
    * returns
    * Once a series and parallel number have been determined - the division into cell modules is then calculated
    '''
    def __init__(self, V_target, V_tol, E_target, E_tol, cell_name):
        self.V_target = V_target
        self.V_range = [V_target-V_tol, V_target+V_tol]
        self.V_tol = V_tol # Vpack = Vtarget +- Vtol
        self.E_target = E_target
        self.E_range = [E_target-E_tol, E_target+E_tol]
        self.E_tol = E_tol



class pack_layout_config:
    '''
    '''
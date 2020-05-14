from mesa.visualization.modules import CanvasGrid, ChartModule
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.UserParam import UserSettableParameter
from .model import SIR_Model


def portrayCell(cell):
    '''
        This function is registered with the visualization server to be called
        each tick to indicate how to draw the cell in its current state.
        :param cell:  the cell in the simulation
        :return: the portrayal dictionary.
        '''
    if cell is None:
        return
    portrayal = {"Shape": "rect", "w": 1, "h": 1, "Filled": "true", "Layer": 0, "x": cell.x, "y": cell.y}
    
    if cell.isSusceptible:
        portrayal["Color"] = "white"        
    elif cell.isInfected:
        portrayal["Color"] = "red"
    elif cell.isRecovered:
        portrayal["Color"] = "green"
    elif cell.isQuarantined:
        portrayal["Color"] = "yellow"

   # portrayal["Color"] = 
    
    return portrayal


# Make a world that is 50x50, on a 500x500 display.
canvas_element = CanvasGrid(portrayCell, 50, 50, 500, 500)
cell_chart = ChartModule([{"Label": "Fraction Infected", "Color": 'Red'}],
                         canvas_height=500, canvas_width=1000)
cell_chart2 = ChartModule([{"Label": "Fraction Recovered", "Color": 'Green'}],
                         canvas_height=500, canvas_width=1000)

model_params = {
    "height": 50,
    "width": 50,
    "dummy": UserSettableParameter("static_text", value = "NB. Use 'Reset'-button to activate new model settings"),
    "density": UserSettableParameter("slider", "Initial density", 0.2, 0.01, 1.0, 0.01),
    "p_inf": UserSettableParameter("slider", "Probability of infection = R0 / 9: ", 0.1, 0.01, 1.0, 0.01),
    "p_rec": UserSettableParameter("slider", "Probability of recovery", 0.2, 0.01, 1.0, 0.01),
    "p_reinf": UserSettableParameter("slider", "Probability of reinfection", 0.05, 0.0, 1.0, 0.01),
    "p_test": UserSettableParameter("slider", "Testing rate of population", 0.1, 0.0, 1.0, 0.01),
    "spatial": UserSettableParameter("checkbox", "Spatial", value=False),}

server = ModularServer(SIR_Model, [canvas_element, cell_chart, cell_chart2], "SIR basic model",  model_params)
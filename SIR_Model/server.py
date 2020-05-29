from mesa.visualization.modules import CanvasGrid, ChartModule
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.UserParam import UserSettableParameter


from .model import infection_model


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
    elif cell.isDead:
        portrayal["Color"] = "black"


    
    return portrayal


# Make a world that is 50x50, on a 500x500 display.
canvas_element = CanvasGrid(portrayCell, 50, 50, 500, 500)

# The two graphs that are displayed in the web socket
cell_chart = ChartModule([{"Label": "Fraction Infected", "Color": 'Red'},
                          {"Label": "Fraction Quarantined", "Color": 'Yellow'}],
                         canvas_height=500, canvas_width=1000)
cell_chart2 = ChartModule([{"Label": "Fraction Recovered", "Color": 'Green'},
                           {"Label": "Fraction Dead", "Color": 'Black'}],
                         canvas_height=500, canvas_width=1000)

# The parameters that can be set a priori by the user in the web socket
model_params = {
    "height": 50,
    "width": 50,
    "dummy": UserSettableParameter("static_text", value = '''Use 'Reset'-button to activate new model settings 
                                   \n White cells are Susceptible individuals
                                   \n Red cells are Infected individuals
                                   \n Green cells are Recovered individuals
                                   \n Yellow cells are Infected but Quarantined individuals'''),
    "density": UserSettableParameter("slider", "Initial density", 0.1, 0.01, 1.0, 0.01),
    "p_inf": UserSettableParameter("slider", "Probability of infection", 0.1, 0.01, 1.0, 0.01),
    "p_rec": UserSettableParameter("slider", "Probability of recovery", 0.1, 0.01, 1.0, 0.01),
    "p_reinf": UserSettableParameter("slider", "Probability of reinfection", 0.01, 0.0, 1.0, 0.01),
    "p_death": UserSettableParameter("slider", "Probability of death", 0.02, 0.0, 1.0, 0.01),
    "p_test": UserSettableParameter("slider", "Testing rate of population", 0.05, 0.0, 1.0, 0.01),
    "test_n": UserSettableParameter("checkbox", "Test Neighbors", value = True),
    "hood" : UserSettableParameter("choice", "Neighborhood", value= "Moore", 
                                   choices= ["Moore", "Von Neumann"])}

# Command that runs the server
server = ModularServer(infection_model, [canvas_element, cell_chart, cell_chart2], "SIR basic model",  model_params)

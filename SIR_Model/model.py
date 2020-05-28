from mesa import Model
from mesa.datacollection import DataCollector
from mesa.time import SimultaneousActivation
from mesa.space import Grid
from mesa.batchrunner import BatchRunner

from .cell import Cell

class SIR_Model(Model):
   

    def __init__(self, height=100, width=100, dummy="", density=0.5, 
                 p_inf = 0.1, p_rec = 0.3, p_reinf = 0.05, p_test = 0.1,
                 p_death = 0.2,test_n = 0, hood = "Moore"):
                
        '''
        Create a new playing area of (height, width) cells.
        '''
        
        # Use SimultaneousActivation which simulates all the cells
        # computing their next state simultaneously.  This needs to
        # be done because each cell's next state depends on the current
        # state of all its neighbors -- before they've changed.
        self.schedule = SimultaneousActivation(self)

        # Use a simple grid, where edges wrap around.
        self.grid = Grid(height, width, torus=True)
        self.datacollector = DataCollector(
            {"Fraction Infected": lambda m: self.count_infected(m,width*height),
             "Fraction Quarantined": lambda m: self.count_quarantined(m,width*height),
             "Fraction Recovered": lambda m: self.count_recovered(m,width*height),
             "Fraction Dead": lambda m: self.count_dead(m,width*height)})

        # Place a cell at each location, with some initialized to
        # ALIVE and some to DEAD.
        for (contents, x, y) in self.grid.coord_iter():
            cell = Cell((x, y), self, p_inf, p_rec, p_reinf, p_test, p_death, test_n, hood)
            if self.random.random() < density:
                cell.state = cell.INFECTED
            self.grid.place_agent(cell, (x, y))
            self.schedule.add(cell)
      
        self.measure_CA = []
        self.running = True
        self.datacollector.collect(self)
        
        
        var_params = {"hood": ["Moore", "Von Neumann"] }
        fixed_params = {"density": 0.4,
                    "p_inf": 0.1,
                    "p_rec": 0.1,
                    "p_reinf": 0.01,
                    "p_death": 0.02,
                    "p_test": 0.05,
                    "test_n": True}
        
        mod_rep = self.datacollector
        b_runn = BatchRunner(SIR_Model, var_params, fixed_params, model_reporters = mod_rep) 
        b_runn.run_all
        coll = b_runn.get_model_vars_dataframe
        print(coll)
        
    def step(self):
        '''
        Have the scheduler advance each cell by one step
        '''
        self.measure_CA = [a for a in self.schedule.agents]
        self.schedule.step()
        # collect data
        self.datacollector.collect(self)
        #      step_data = self.datacollector.get_model_vars_dataframe()
        #      step_data.to_csv("numdata.csv")
    
    @staticmethod
    def count_infected(model,grid_size):
        """
            Helper method to count INFECTED cells in the model.
        """
        list_state = [a for a in model.schedule.agents if (a.state == a.INFECTED or a.state == a.QUARANTINED)]
        return len(list_state)/grid_size
    
    @staticmethod
    def count_recovered(model,grid_size):
        """
            Helper method to count RECOVERED cells in the model.
        """
        list_state = [a for a in model.schedule.agents if (a.state == a.RECOVERED or a.state == a.DEAD)]
        return len(list_state)/grid_size
    
    @staticmethod
    def count_quarantined(model,grid_size):
        """
            Helper method to count QUARANTINED cells in the model.
        """
        list_state = [a for a in model.schedule.agents if a.state == a.QUARANTINED]
        return len(list_state)/grid_size

    @staticmethod
    def count_dead(model, grid_size):
        '''
            Helper method to count DEAD cells in the model.

        '''
        list_state = [a for a in model.schedule.agents if a.state == a.DEAD]
        return len(list_state)/grid_size

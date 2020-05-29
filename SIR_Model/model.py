from mesa import Model
from mesa.datacollection import DataCollector
from mesa.time import SimultaneousActivation
from mesa.space import Grid

from .cell import Cell

class infection_model(Model):
   

    def __init__(self, height=100, width=100, dummy="", density=0.5, 
                 p_inf = 0.1, p_rec = 0.3, p_reinf = 0.05, p_test = 0.1,
                 p_death = 0.2,test_n = 0, hood = "Moore", datacollector = {}):
                
        '''
        Create a new playing area of (height, width) cells.
        '''
        
        # Use SimultaneousActivation which simulates all the cells
        # computing their next state simultaneously.  This needs to
        # be done because each cell's next state depends on the current
        # state of all its neighbors -- before they've changed.
        self.height = height
        self.width = width
        self.schedule = SimultaneousActivation(self)

        # Use a simple grid, where edges wrap around.
        self.grid = Grid(height, width, torus=True)

        # Use the DataCollector method to store the relevant information of our
        # model. This helps with plotting in the web socke, but also with running 
        #more models at the same time using BatchRunner (in batch.py)
        self.datacollector = DataCollector(
            model_reporters = self.compute_reporters())

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
        
        


        
    def step(self):
        '''
        Have the scheduler advance each cell by one step
        '''
        self.measure_CA = [a for a in self.schedule.agents]
        self.schedule.step()

        # collect data
        self.datacollector.collect(self)


    def compute_reporters(self):
        '''
        
        Returns
        A dictionary of the fractions of the population that are Infected, Quarantined,
        Recovered or Dead
        '''
        mod_rep = {"Fraction Infected": lambda m: self.count_infected(m, self.height * self.width),
                   "Fraction Quarantined": lambda m: self.count_quarantined(m, self.height * self.width),
                   "Fraction Recovered": lambda m: self.count_recovered(m, self.height * self.width),
                   "Fraction Dead": lambda m: self.count_dead(m, self.height * self.width),}
        return mod_rep

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

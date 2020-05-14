from mesa import Agent

class Cell(Agent):
    '''Represents a single ALIVE or DEAD cell in the simulation.'''

    SUSCEPTIBLE = 0
    INFECTED = 1
    RECOVERED = 2
    QUARANTINED = 3

    def __init__(self, pos, model,prob_inf, prob_rec, prob_reinf, prob_test, spatial, init_state= SUSCEPTIBLE):
        '''
        Create a cell, in the given state, at the given x, y position.
        '''
        super().__init__(pos, model)
        self.x, self.y = pos
        self.spatial = spatial
        self.state = init_state
        self._nextState = None
        self.prob_inf = prob_inf
        self.prob_rec = prob_rec
        self.prob_reinf = prob_reinf
        self.prob_test = prob_test

    @property
    def isInfected(self):
        return self.state == self.INFECTED
    @property
    def isSusceptible(self):
        return self.state == self.SUSCEPTIBLE
    @property
    def isRecovered(self):
        return self.state == self.RECOVERED
    @property
    def isQuarantined(self):
        return self.state == self.QUARANTINED

    @property
    def neighbors(self):
        return self.model.grid.neighbor_iter((self.x, self.y), True)

    def step(self):
        '''
        Compute if the cell will be in S, I, R or Q in the next state.  This is
        based on the current state of the cell and the number of infected individuals
        in the neighborhood.  The state is not changed here, but is just computed
        and stored in self._nextState, because our current state may still be
        necessary for our neighbors to calculate their next state.
        '''

        
        if self.spatial:
            infected_neighbors = sum(neighbor.isInfected for neighbor in self.neighbors)

        # The next function is using random cells instead of neigboring cells;
        # in this way "mean field" is simulated
        else:
            self.neighbourhood = self.random.sample(self.model.measure_CA, 9)
            infected_neighbors = sum(neighbor.isInfected for neighbor in self.neighbourhood)


        # Assume nextState is unchanged, unless changed below.

        # If current state is SUSCEPTIBLE, change next state to infected, based on number of infected neighbors
        if self.isSusceptible and self.random.random() < infected_neighbors * self.prob_inf:
            self._nextState = self.INFECTED
        # If current state is INFECTED or QUARANTINED, recover based on some probability
        elif (self.isInfected or self.isQuarantined) and self.random.random() < self.prob_rec:
            self._nextState = self.RECOVERED        
        elif self.isRecovered and self.random.random() < infected_neighbors * self.prob_reinf:
            self._nextState = self.INFECTED
        else:
            self._nextState = self.state
        
        #random testing of prob_test rate of the population
        if self.random.random() < self.prob_test :
            if self.isInfected:
                self._nextState = self.QUARANTINED
                
            

        
                    
    def advance(self):
        '''
        Set the state to the new computed state -- computed in step().
        '''

        self.state = self._nextState

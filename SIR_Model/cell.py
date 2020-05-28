from mesa import Agent

class Cell(Agent):
    '''Represents a single ALIVE or DEAD cell in the simulation.'''

    SUSCEPTIBLE = 0
    INFECTED = 1
    RECOVERED = 2
    QUARANTINED = 3
    DEAD = 4
    

    def __init__(self, pos, model,prob_inf, prob_rec, prob_reinf, prob_test,
                 prob_death, test_n, hood, init_state= SUSCEPTIBLE, init_qme = False):
        '''
        Create a cell, in the given state, at the given x, y position.
        '''
        super().__init__(pos, model)
        self.x, self.y = pos
        self.state = init_state
        self._nextState = None
        self.prob_inf = prob_inf
        self.prob_rec = prob_rec
        self.prob_reinf = prob_reinf
        self.prob_test = prob_test
        self.prob_death = prob_death
        self.days_infected = 0
        self.quarantineMe = init_qme
        self.test_n = test_n
        self.hood = hood
        
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
    def isDead(self):
        return self.state == self.DEAD
    
    @property
    def neighbors(self):
        return self.model.grid.iter_neighbors((self.x, self.y), True)  #PROBLEM MIGHT BE HERE
  
    @property
    def VN_neighbors(self):
        return self.model.grid.iter_neighbors((self.x, self.y), False)  

        
    def step(self):
        '''
        Compute if the cell will be in S, I, R or Q in the next state.  This is
        based on the current state of the cell and the number of infected individuals
        in the neighborhood.  The state is not changed here, but is just computed
        and stored in self._nextState, because our current state may still be
        necessary for our neighbors to calculate their next state.
        '''

        

        infected_neighbors = sum(neighbor.isInfected for neighbor in self.neighbors)
        
        if self.hood == "Moore":
            self.neighbourhood = self.neighbors
        else:
            self.neighbourhood = self.VN_neighbors



        if self.quarantineMe == True:
            self._nextState = self.QUARANTINED
            self.quarantineMe = False
        # If current state is SUSCEPTIBLE, change next state to infected, based on number of infected neighbors
        elif self.isSusceptible and self.random.random() < (infected_neighbors * self.prob_inf):
            self._nextState = self.INFECTED
        # If current state is INFECTED or QUARANTINED, recover based on some probability
        elif (self.isInfected or self.isQuarantined) and self.random.random() < self.prob_rec:
            self._nextState = self.RECOVERED
        # If cell is infected or quarantined, die based on some probability
        elif (self.isInfected or self.isQuarantined) and self.random.random() < self.prob_death:
            self._nextState = self.DEAD
        # If cell is recovered, get reinfected based on prob_reinf
        elif self.isRecovered and self.random.random() < (infected_neighbors * self.prob_reinf):
            self._nextState = self.INFECTED
        else:
            self._nextState = self.state
        

        #random testing of prob_test rate of the population that is not dead or tested positive
        if self.test_n == True:
            if not(self.isQuarantined or self.isDead) and self.random.random() < self.prob_test :
                if self.isInfected:
                    self._nextState = self.QUARANTINED
                    for n in self.neighbourhood:
                        if n.isInfected:
                            n.quarantineMe = True
        else:
            if not(self.isQuarantined or self.isDead) and self.random.random() < self.prob_test :
                if self.isInfected:
                    self._nextState = self.QUARANTINED


            
        
                    
    def advance(self):
        '''
        Set the state to the new computed state -- computed in step().
        '''

        self.state = self._nextState

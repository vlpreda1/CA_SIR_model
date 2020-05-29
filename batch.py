from SIR_Model.model import infection_model

from mesa.batchrunner import BatchRunner
#import matplotlib.pyplot as plt
#import pandas


fixed_params = {"hood": "Moore",
                "density": 0.1,
                "p_reinf": 0.01,
                "p_death": 0.02,
                "p_inf": 0.1,
                "p_rec": 0.1}
var_params = {
                "p_test": [0.5, 0.1, 0.15],
                "test_n": [True, False]}


mod = infection_model()

batch_runn = BatchRunner(infection_model, var_params, fixed_params, iterations = 1, 
                           max_steps = 250,model_reporters = mod.datacollector.model_reporters)

batch_runn.run_all()

coll = batch_runn.get_model_vars_dataframe()
coll.to_csv("data.csv")
#plt.scatter(coll."Fraction Infected", coll.
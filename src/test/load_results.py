import pickle
import statistics
import numpy as np


data = ['phase_10_825_int16.pkl', 'phase_10_1_int16.pkl']

for i in range(len(data)):

    with open(data[i], 'rb') as f:  # Python 3: open(..., 'rb')
        my_time, error, char_of_error = pickle.load(f)
        avg_time = np.mean(my_time)
        # error = list(filter(lambda a: a != 0, error))
        char_of_error = list(filter(lambda a: a.any() != 0, char_of_error))
        # suma błednych znakow
        num_of_char = sum(char_of_error)
        # srednia na 1 blad znakow
        avg_char_of_error = np.mean(char_of_error)


    xdd = "fefef"

    dedefe = "fefe"





# # Getting back the objects:
# with open('objs.pkl') as f:  # Python 3: open(..., 'rb')
#     obj0, obj1, obj2 = pickle.load(f)




# remove()  - remove 0 from errors
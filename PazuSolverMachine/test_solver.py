import numpy as np
from pazusolver import Map

if __name__ == "__main__":
    #BEAM_DEPTH = 120
    #ROUTE_MAXLENGTH = 20
    N = 10

    color = np.array([[0,0,255], [0, 255, 255], [0,255,0],
                      [255,0,0], [147,20,255], [68,18,62],
                      [0,0,0]])
    
    sum = 0
    min = 20
    max = 0
    for i in range(N):
        while(True):
            m = np.random.randint(6, size = (5,6))
            map = Map(m)
            map.count_combos()
            if map.num_combos == 0:
                map.solve_map()
                answer = map.ans()
                sum += answer
                if answer < min:
                    min = answer
                if answer > max:
                    max = answer
                break
    
    print 'Average: '+str(sum/N)+', Min: '+str(min)+', Max: '+str(max)

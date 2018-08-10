import cv2
import numpy as np
import time
from combo import Combo
from route import Route
import random

def in_map(i,j):
    return (i >= 0) and (i < 5) and (j >= 0) and (j < 6)

def goal(i, j, direct):
    if direct == 0: #Right
        return [i, j+1]
    elif direct == 1: #Down
        return [i+1, j]
    elif direct == 2: #Up
        return [i-1, j]
    elif direct == 3: #Left
        return [i, j-1]

def moveable(i, j, direct):
    go = goal(i, j, direct)
    return in_map(go[0], go[1])

def moveable_route(i, j, route):
    go = [i,j]
    possible = True
    for direct in route:
        if not moveable(go[0], go[1], direct):
            possible = False
            break
        go = goal(go[0], go[1], direct)
    return possible

def create_routes(prev, dep):
    routes = []
    for i in range(4**dep):
        # Remove back routes
        if (i%4 == 3 - prev):
            continue
        j = i/4
        k = 1
        route = [0] * (dep)
        route[0] = i%4 
        flag = False

        while j > 0:
            flag = True
            # Remove back routes
            if (j%4 == 3 - route[k-1]):
                flag = False
                break
            route[k] = j%4
            k += 1
            j /= 4
        if flag or (dep == 1):
            routes.append(route)
    return routes

class Map:
    def __init__(self,m):
        self.map = np.array(m, copy = True)
        self.combos = []
        self.num_combos = 0
        self.num_cbnodes = 0
        self.dropcom = 0
        self.check = np.zeros((5,6), dtype = np.int)
        self.save_route = []
        self.save_map = []

    def reset_cb(self):
        self.combos = []
        self.num_combos = 0
        self.num_cbnodes = 0
        self.check = np.zeros((5,6), dtype = np.int)

    def reset_save(self):
        self.save_route = []
        self.save_map = []

    def draw_state(self):
        img = np.zeros((300,360,3), np.uint8)
        for i in range(5):
            for j in range(6):
                cv2.circle(img, (30+60*j, 30+60*i), 20, color[self.map[i,j]], -1)
                
        return img

    def draw_state_with_cursor(self, cursor):
        img = np.zeros((300,360,3), np.uint8)
        for i in range(5):
            for j in range(6):
                cv2.circle(img, (30+60*j, 30+60*i), 20, color[self.map[i,j]], -1)
        cv2.circle(img, (30+60*cursor[1], 30+60*cursor[0]), 20, (255, 255, 255), 5)
        return img

    def search_around(self, i, j):
        right = 1
        down = 1
        #Find combos in right direction
        for id in range(i+1, 5):
            if self.map[id,j] == self.map[i,j]:
                right += 1
            else:
                break
                
        #Find combos in down direction
        for jd in range(j+1, 6):
            if self.map[i,jd] == self.map[i,j]:
                down += 1
            else:
                break

        #Create combo found
        cb = Combo([i,j])
        cb.add_node([i,j])
        has_combo = False
        if right >= 3:
            has_combo = True
            for id in range(i+1, i+right):
                self.check[id,j] = 1
                cb.add_node([id,j])

        if down >= 3:
            has_combo = True
            for jd in range(j+1, j+down):
                self.check[i,jd] = 1
                cb.add_node([i,jd])
                
        if has_combo:
            self.num_combos += 1
            self.num_cbnodes += cb.len()
            self.combos.append(cb)

    def count_combos(self):
        self.reset_cb()
        for i in range(5):
            for j in range(6):
                if self.check[i,j] == 1 :
                    continue
                if self.map[i,j] == 6:
                    continue
                self.search_around(i,j)

    def kill_combos(self):
        for combo in self.combos:
            for node in combo.combo_node:
                self.map[node[0],node[1]] = 6
    
    def update_map(self):
        for j in range(6):
            d = np.where(self.map[:,j]==6)[0]
            _map = np.delete(self.map[:,j], d)
            self.map[:,j] = np.concatenate((6*np.ones(d.shape[0], dtype=np.int),_map))

    def calc_combos(self):
        self.count_combos()
        _ori_map = np.array(self.map, copy = True)
        _ncombos = self.num_combos
        _ncbnodes = self.num_cbnodes
        self.kill_combos()
        self.update_map()
        self.count_combos()
        # Evaluate function = n_combos + 0.1 * dropcoms
        self.dropcom = self.num_combos + 0.01 * self.num_cbnodes
        self.num_combos = _ncombos 
        self.num_cbnodes = _ncbnodes
        self.map = np.array(_ori_map, copy = True)
                
    def move_node(self, i, j, direct):
        # Swap [i,j] and goal(i,j,direct)
        _goal = goal(i, j, direct)
        tmp = self.map[i,j]
        self.map[i,j] = self.map[_goal[0], _goal[1]]
        self.map[_goal[0], _goal[1]] = tmp
        return _goal

    def move_route(self, i, j, rou):
        _goal = [i,j]
        for di in rou:
            _goal = self.move_node(_goal[0], _goal[1], di)
        return _goal    

    def search_route_dep1(self):
        ori_map = np.array(self.map, copy = True)
        for i in range(5):
            for j in range(6):
                for di in range(4):
                    if not moveable(i, j, di):
                        continue
                    pos = self.move_node(i, j, di)
                    self.calc_combos()
                    rou = Route([i,j])
                    rou.update(di, pos)
                    rou.set_ncombos(self.num_combos + 0.01 * self.num_cbnodes, self.dropcom)
                    if len(self.save_route) < BEAM_DEPTH:
                        self.save_route.append(rou)
                        self.save_map.append(self.map)
                        #if rou.ncombos > 0:
                        #    rou.print_route()

                    elif rou.sumcoms > min(self.save_route, key=lambda x: x.ncombos).sumcoms:
                        ind = self.save_route.index(min(self.save_route, key=lambda x: x.ncombos))
                        # Replace min
                        self.save_route.pop(ind)
                        self.save_map.pop(ind)
                        
                        self.save_route.append(rou)
                        self.save_map.append(self.map)
                           
                    # Back to start map
                    self.map = np.array(ori_map, copy = True)
    
    # search_route for depth >= 2
    def search_route(self, depth):
        route_save = np.array(self.save_route, copy = True)
        map_save = np.array(self.save_map, copy = True)
        #self.reset_save()
        for (i, (_route, _map)) in enumerate(zip(route_save, map_save)):
            remain_depth = depth - len(_route.direction)
            routes = create_routes(_route.direction[-1], remain_depth)

            if (remain_depth > MAX_DEPTHSEARCH):
                # Remove father map
                self.save_route.pop(i)
                self.save_map.pop(i)
                
                # Replace by random child map
                self.map = np.array(_map, copy = True)
                new_rou = Route([_route.start[0], _route.start[1]])
                new_rou.copy_route(_route)
                while (True):
                    ran = random.randint(0, len(routes)-1)
                    rou = routes[ran]
                    if moveable_route(new_rou.end[0], new_rou.end[1], rou):
                        new_end = self.move_route(new_rou.end[0], new_rou.end[1], rou)
                        self.calc_combos()
                        new_rou.update_rou(rou, new_end)
                        new_rou.set_ncombos(self.num_combos + 0.01 * self.num_cbnodes, self.dropcom)
                        self.save_route.append(new_rou)
                        self.save_map.append(self.map)
                        break
            else:    
                for rou in routes:
                    self.map = np.array(_map, copy = True)
                    new_rou = Route([_route.start[0], _route.start[1]])
                    new_rou.copy_route(_route)
                    # Check if we can move node of not    
                    if not moveable_route(new_rou.end[0], new_rou.end[1], rou):
                        continue
                    new_end = self.move_route(new_rou.end[0], new_rou.end[1], rou)
                    self.calc_combos()
                    new_rou.update_rou(rou, new_end)
                    new_rou.set_ncombos(self.num_combos + 0.01 * self.num_cbnodes, self.dropcom)
                    
                    if len(self.save_route) < BEAM_DEPTH:
                        self.save_route.append(new_rou)
                        self.save_map.append(self.map)
                        
                    elif (new_rou.sumcoms > _route.sumcoms) and (new_rou.sumcoms > min(self.save_route, key=lambda x: x.sumcoms).sumcoms):    
                        ind = self.save_route.index(min(self.save_route, key=lambda x: x.sumcoms))
                        # Replace min
                        self.save_route.pop(ind)
                        self.save_map.pop(ind)
                        
                        self.save_route.append(new_rou)
                        self.save_map.append(self.map)

    def solve_map(self):
        self.search_route_dep1()
        for dep in range(2, ROUTE_MAXLENGTH+1):
            self.search_route(dep)
            
    def best_route(self):
        rou = max(self.save_route, key=lambda x: x.ncombos)
        return rou.start, rou.direction, rou.end 
        
    def ans(self):
        #print len(self.save_route)
        rou = max(self.save_route, key=lambda x: x.ncombos)
        rou.print_route()
        #rou = max(self.save_route, key=lambda x: len(x.direction))
        #rou.print_route()
        #return rou.ncombos + rou.dropcoms

BEAM_DEPTH = 5
ROUTE_MAXLENGTH = 30
MAX_DEPTHSEARCH = 8
        
if __name__ == "__main__":
    
    m = np.array([[4, 4, 0, 3, 3, 1],
                  [2, 5, 2, 2, 1, 4],
                  [3, 3, 4, 2, 4, 1],
                  [3, 4, 1, 5, 5, 1],
                  [4, 4, 3, 2, 3, 0]])

    color = np.array([[0,0,255], [0, 255, 255], [0,255,0],
                      [255,0,0], [147,20,255], [68,18,62],
                      [0,0,0], [0,0,0]])
    
    start_time=time.time()
    map = Map(m)
    map.solve_map()
    map.ans()
    elapsed_time=time.time() - start_time
    print 'Elapsed time: ' + str(elapsed_time)

    #map.kill_combos()
    #img2 = map.draw_state()
    cursor, route, _end = map.best_route()
    sleep_time = 1

    map = Map(m)
    img = map.draw_state()
    #while(1):
    cv2.imshow('Map', img)
    cv2.imwrite('./out/Map1.jpg', img)
    cv2.waitKey(20)
    
    #while(1):
    #    if cv2.waitKey(20) == 27: 
    #        break
    time.sleep(sleep_time)
    img = map.draw_state_with_cursor(cursor)
    cv2.imshow('Map', img)
    cv2.imwrite('./out/Map2.jpg', img)
    cv2.waitKey(20)
    #while(1):
    #    if cv2.waitKey(20) == 27: 
    #        break
    time.sleep(sleep_time)

    for (i,di) in enumerate(route):
        cursor = map.move_node(cursor[0], cursor[1], di)
        img = map.draw_state_with_cursor(cursor)
        cv2.imshow('Map', img)
        cv2.imwrite('./out/Map'+str(3+i)+'.jpg', img)
        cv2.waitKey(20)
        #while(1):
        #    if cv2.waitKey(20) == 27: 
        #        break
        time.sleep(sleep_time)
            
    map.count_combos()
    print map.num_combos, map.num_cbnodes
    map.kill_combos()
    img = map.draw_state()
    cv2.imshow('Map', img)
    cv2.imwrite('./out/Map'+str(3+len(route))+ '.jpg', img)
    time.sleep(sleep_time)
    
    map.update_map()
    img = map.draw_state()
    cv2.imshow('Map', img)
    cv2.imwrite('./out/Map'+str(4+len(route))+ '.jpg', img)
    time.sleep(sleep_time)
    
    map.count_combos()
    print map.num_combos, map.num_cbnodes
    map.kill_combos()
    img = map.draw_state()
    cv2.imshow('Map', img)
    cv2.imwrite('./out/Map'+str(5+len(route))+ '.jpg', img)
    time.sleep(sleep_time)

    map.update_map()
    img = map.draw_state()
    cv2.imshow('Map', img)
    cv2.imwrite('./out/Map'+str(6+len(route))+ '.jpg', img)
    time.sleep(sleep_time)
    #cv2.waitKey(20)
    while(1):
        if cv2.waitKey(20) == 27: 
            break
    cv2.destroyAllWindows()

    '''
    map = Map(m)
    map.count_combos()
    print map.num_combos, map.num_cbnodes
    img = map.draw_state()
    map.kill_combos()
    print map.num_combos, map.num_cbnodes
    img2 = map.draw_state()
    map.update_map()
    img3 = map.draw_state()
    while(1):
        cv2.imshow('Map', img)
        cv2.imshow('Map2', img2)
        cv2.imshow('Map3', img3)
        if cv2.waitKey(20) == 27: 
            break
    cv2.destroyAllWindows()
    '''

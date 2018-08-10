def test(dep,n):
    a = []
    for i in range(4**dep):
        if (i%4 == 3-n):
            continue
        j = i/4
        k = 1
        array = [0] * (dep)
        array[0] = i%4 
        flag = False

        while j > 0:
            flag = True
            if (j%4 == 3 - array[k-1]):
                flag = False
                break
            array[k] = j%4
            k += 1
            j /= 4
        if flag or (dep == 1):
            a.append(array)
    #for _a in a:
    #    print _a
    print len(a)

test(9, 1)

from time import sleep
from pymunk import Vec2d, vec2d

listA = []

for i in range(6):
    listA.append([i,i])


listB = [[i,i] for i in range(6)]   # triks
listC = [[i,i] for i in range(6) if i > 3]   # triks2

print(listA)
print(listB)
print(listC)



vec1 = (listA[0][0], listA[0][1])
vec2 = (listA[1][0], listA[1][1])

print(vec1)
print(vec2)

vec = [Vec2d(x,y) for x,y in listB]
print(vec[1])
print(vec)
print(len(vec))

vec1 = Vec2d(1,1)
print(vec1/2)




import datetime
from time import sleep

t_a = datetime.datetime.now()
sleep(3)
t_b = datetime.datetime.now()
delta_t = t_b - t_a
print(delta_t)
print(delta_t.microseconds)
print((delta_t.total_seconds()))

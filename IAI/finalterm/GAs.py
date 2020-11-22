import random

# import from data.py
from data import Course, Instructor, Room, Time, Data, Class

SIZE = 15

class Schedule:
    def __init__(self):
        self.data = data
        self.classes = []
        self.conflicts = 0
        self.fit = -1
        self.num = 0
        self.fitchange = True
    
    def get_classes(self):
        self.fitchange = True
        return self.classes
    
    def get_fit(self):
        if self.fitchange:
            self.fit = self.calculate_fit()
            self.fitchange = False
        return self.fit
    
    def initialize(self):
        depts = self.data.departments
        for dept in depts:
            courses = dept.courses
            for course in courses:
                temp = Class(self.num, dept, course)
                temp.time = data.times[random.randrange(0, len(data.times))]
                temp.room = data.rooms[random.randrange(0, len(data.rooms))]
                temp.instructor = course.instructors[random.randrange(0, len(course.instructors))]
                self.classes.append(temp)
                self.num += 1
        return self
    
    def calculate_fit(self):
        self.conflicts = 0
        classes = self.get_classes()
        for i in range(len(classes)):
            if classes[i].room.capacity < classes[i].course.numStudent:
                self.conflicts += 1
            for j in range(i, len(classes)):
                if ( classes[i].time == classes[j].time and classes[i].ID != classes[i].ID ):
                    if classes[i].room == classes[j].room:
                        self.conflicts += 1
                    if classes[i].instructor == classes[j].instructor:
                        self.conflicts += 1
        return 1 / (self.conflicts + 1)
    
class Population:
    def __init__(self, size):
        self.size = size
        self.data = data
        self.schedules = list()
        for i in range(size):
            self.schedules.append(Schedule().initialize())

class GAs:
    def __init__(self, numGoodSchedule, mutationRate, selectionSize):
        self.numGoodSchedule = numGoodSchedule
        self.mutationRate = mutationRate
        self.selectionSize = selectionSize

    def crossoverPop(self, pop):
        crossover_pop = Population(0)
        for i in range(SIZE):
            if ( i  < self.numGoodSchedule ):
                crossover_pop.schedules.append(pop.schedules[i])
            else:
                temp1 = self.selectTourPop(pop).schedules[0] # parent 1
                temp2 = self.selectTourPop(pop).schedules[0] # parent 2
                crossover_pop.schedules.append(self.crossoverSchedule(temp1, temp2))
        return crossover_pop
    
    # select tournament population
    def selectTourPop(self, pop):
        tournament_pop = Population(0)
        for i in range(self.selectionSize):
            tournament_pop.schedules.append(pop.schedules[random.randrange(0, SIZE)])
        tournament_pop.schedules.sort(key = lambda value : value.get_fit(), reverse=True)
        return tournament_pop
    
    def crossoverSchedule(self, temp1, temp2):
        crossoverSche = Schedule().initialize()
        for i in range(len(crossoverSche.classes)):
            if ( random.random() > 0.5 ):
                crossoverSche.classes[i] = temp1.classes[i]
            else:
                crossoverSche.classes[i] = temp2.classes[i]
        return crossoverSche
    
    def mutatePop(self, pop):
        for i in range(self.numGoodSchedule, SIZE):
            self.mutateSchedules(pop.schedules[i])
        return pop
    
    def mutateSchedules(self, temp):
        schedule = Schedule().initialize()
        for i in range(len(temp.classes)):
            if ( self.mutationRate > random.random() ):
                temp.classes[i] = schedule.classes[i]
        return temp
    
    def evolve(self, pop):
        return self.mutatePop(self.crossoverPop(pop))


data = Data()
iter = 0
pop = Population(SIZE)
pop.schedules.sort(key = lambda value : value.get_fit(), reverse=True)
gas = GAs(numGoodSchedule=3, mutationRate=0.2, selectionSize=5)
while ( pop.schedules[0].get_fit() < 1.0 ):
    iter += 1
    print(f'Iter : {iter}')
    pop = gas.evolve(pop)
    pop.schedules.sort(key = lambda value : value.get_fit(), reverse=True)

# print Best Schedules
print('Time\t\tInstructor\tDepartment\tRoom\tCourse')
days = ['T2','T3','T4','T5','T6','T7']
count = 0
res = pop.schedules[0]
for count in range(len(days)):
    for i in range(len(res.classes)):
        c = res.classes[i]
        if days[count] in c.time.time:
            print(f'{c.time.time}', end='\t')
            print(f'{c.instructor.name}', end='\t')
            print(f'{c.department.name}', end='\t\t')
            print(f'{c.room.ID}({c.course.numStudent})', end='\t')
            print(f'{c.course.name}')
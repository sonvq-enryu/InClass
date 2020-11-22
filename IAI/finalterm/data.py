ListRoom = [['R1', 35], ['R2', 35], ['R3', 80], ['R4', 35], ['R5', 35], ['R6', 35]]
ListTime = ['T2 06:50-09:15', 'T2 09:25-11:50', 'T2 12:30-14:55', 'T2 15:05-17:30',
            'T3 06:50-09:15', 'T3 09:25-11:50',
            'T4 06:50-09:15','T4 15:05-17:30',
            'T5 06:50-09:15', 'T5 09:25-11:50', 'T5 12:30-14:55',
            'T6 06:50-09:15', 'T6 09:25-11:50', 'T6 15:05-17:30',
            'T7 06:50-09:15', 'T7 09:25-11:50']
ListInstructor = [['GV1', 'Nguyen Van A'], ['GV2', 'Nguyen Van B'], ['GV3', 'Nguyen Van C'],
                  ['GV4', 'Huynh Van D'], ['GV5', 'Tran Quoc E'], ['GV6', 'Nguyen Van F'],
                  ['GV7', 'Tran Thanh G'], ['GV8', 'Huynh Gia H'], ['GV9', 'Tran Ngoc J']]

class Course:
    def __init__(self, name, instructors, numStudent):
        self.name = name
        self.instructors = instructors
        self.numStudent = numStudent

class Instructor:
    def __init__(self, ID, name):
        self.ID = ID
        self.name = name

class Room:
    def __init__(self, ID, capacity):
        self.ID = ID
        self.capacity = capacity

class Time:
    def __init__(self, time):
        self.time = time

class Department:
    def __init__(self, name, courses):
        self.name = name
        self.courses = courses

class Class:
    def __init__(self, ID, department, course):
        self.ID = ID
        self.department = department
        self.course = course
        self.instructor = None
        self.time = None
        self.room = None

class Data:
    def __init__(self):
        self.rooms = list()
        self.times = list()
        self.instructors = list()

        for room in ListRoom:
            self.rooms.append(Room(room[0], room[1]))
        for time in ListTime:
            self.times.append(Time(time))
        for instuctor in ListInstructor:
            self.instructors.append(Instructor(instuctor[0], instuctor[1]))
        
        # CNTT Department(Name-Group, Instructors for this Course)
        C1 = Course('DSTT-G1', [self.instructors[0], self.instructors[1], self.instructors[2]], 30)
        C2 = Course('DSST-G2', [self.instructors[0], self.instructors[1], self.instructors[2]], 30)
        C3 = Course('GT-G1', [self.instructors[0], self.instructors[1], self.instructors[2]], 70)
        C4 = Course('GT-G2', [self.instructors[0], self.instructors[1], self.instructors[2]], 30)
        C5 = Course('CTDLGT1-G1', [self.instructors[0], self.instructors[3], self.instructors[5]], 30)
        C6 = Course('CTDLGT1-G2', [self.instructors[0], self.instructors[3], self.instructors[5]], 70)
        C7 = Course('CTDLGT2', [self.instructors[3], self.instructors[4], self.instructors[6]], 70)
        C8 = Course('HDH', [self.instructors[2], self.instructors[5]], 30)
        C9 = Course('PPT', [self.instructors[0], self.instructors[1], self.instructors[2]], 30)
        C10 = Course('CTRR', [self.instructors[4], self.instructors[5], self.instructors[6]], 30)
        C11 = Course('TTH', [self.instructors[3], self.instructors[6], self.instructors[4]], 70)
        C12 = Course('MMT', [self.instructors[4], self.instructors[5], self.instructors[3]], 30)
        # KHXH Department
        C13 = Course('MAC-G1', [self.instructors[7], self.instructors[8]], 70)
        C14 = Course('MAC-G2', [self.instructors[7], self.instructors[8]], 30)
        C15 = Course('TTHCM', [self.instructors[7], self.instructors[8]], 30)
        C16 = Course('DLCNXH', [self.instructors[7], self.instructors[8]], 30)
        # get all course to courses
        self.courses = [C1, C2, C3, C4, C5, C6, C7, C8, C9, C10, C11, C12, C13, C14, C15, C16]

        # Get department for this course
        CNTT = Department('CNTT', [C1, C2, C3, C4, C5, C6, C7, C8, C9, C10, C11, C12])
        KHXH = Department('KHXH', [C13, C14, C15, C16])
        self.departments = [CNTT, KHXH]

        self.numClasses = 0
        for dept in self.departments:
            self.numClasses += len(dept.courses)

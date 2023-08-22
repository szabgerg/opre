import sys
class Keret:
    def __init__(self, name, num, freeze, age, volt):#name: a keret neve, num: a keretben lévő lap száma, freeze: a fagyasztás ideje, age: a keret korát jelöli, volt: a referáló bit
        self.name = str(name)
        self.num = num
        self.freeze = freeze
        self.age = age
        self.volt = volt


    def older(self):
        self.age += 1

    def less_freeze(self):
        self.freeze -= 1

def find_oldest(kerettar):
    keret_oldest = None
    for keret in kerettar:
        if keret_oldest is None or keret.age > keret_oldest:
            keret_oldest = keret
    return keret_oldest

def time_moving(kerettar):
    for keret in kerettar:
        if (keret.num != 0):
            keret.older()
        if (keret.freeze != 0):
            keret.less_freeze()


def oldest_and_freeze_end(kerettar):

    for keret in kerettar:
        if keret.freeze == 0 and keret.volt == False:
            return keret
        elif keret.freeze == 0 and keret.volt == True:
            keret.volt = False
            keret.age = 0

    kerettar.sort(key=lambda x: x.age, reverse=True)  # koruk szerint rendezi 

    for keret in kerettar:
        if keret.freeze == 0 and keret.volt == False:
            return keret


input_str = sys.stdin.read()
input_list = input_str.strip().split(',')
lap_h =[int(n) if int(n) > 0 else -int(n) for n in input_list]

#print(lap_h)


ki = ""
laphiba = 0

A = Keret('A', 0, 0, 0, False)
B = Keret('B', 0, 0, 0, False)
C = Keret('C', 0, 0, 0, False)

kerettar = []

kerettar.append(A)
kerettar.append(B)
kerettar.append(C)

kerettar.sort(key= lambda x: x.age, reverse= True) #koruk szerint rendezi

for lap in lap_h:
    van = False
    for keret in kerettar:
        if(lap == keret.num):    #ha benne van az adott lap már
            ki += '-'
            time_moving(kerettar)
            keret.volt = True
            keret.freeze = 0
            van = True
            kerettar.sort(key=lambda x: x.age, reverse=True)  # koruk szerint rendezi
            break

    if van is False:
        laphiba += 1
        good = 0
        for keret in kerettar:
            if(keret.freeze <= 0): #ha a "fagyasztás" véget ért akkor lesz hely az újnak
                good += 1

        if (good == 0): #nem ért véget a fagyasztás, nincs hely, ezért ki '*', a fagyasztás csökken, a kor nő
            ki += '*'
            time_moving(kerettar)
            kerettar.sort(key=lambda x: x.age, reverse=True)  # koruk szerint rendezi

        else:#van olyan ahol a freeze = 0
            result = oldest_and_freeze_end(kerettar) # freeze 0 és a volt(referáló)bit is 0 (hamis) és a legöregebb

            result.num = lap
            result.age = -1
            result.freeze = 4
            result.volt = False
            ki += result.name
            time_moving(kerettar)
            kerettar.sort(key=lambda x: x.age, reverse=True)  # koruk szerint rendezi

print(ki)
print(laphiba)
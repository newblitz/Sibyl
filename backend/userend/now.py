from datetime import datetime
a=datetime.now().time().hour
print(a)
time_slot_av = [("09:00","09:00"),("10:00","10:00"),("11:00","11:00"),("14:00","14:00"),("15:00","15:00"),("16:00","16:00")]
for index,el in enumerate(time_slot_av):
    if int(el[0].split(":")[0])==a:
        answer= index
        break
    else:
        answer=0
final_list=[]
for el in range(answer+1,len(time_slot_av)):
    final_list.append(time_slot_av[el])
print(final_list)
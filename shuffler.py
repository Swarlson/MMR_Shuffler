import tkinter.messagebox
from tkinter import *
import csv
import re
def gen_teams():
    teamA = []
    teamB = []
    id = results_sb.get(results_sb.curselection())
    if isinstance(id,str):
        id1 = int(id.split('(')[0])
        id2 = int(re.findall(r"\(\s*\+?(-?\d+)\s*\)", id)[0])
        teamA = results[id1][id2][0]
        teamB = results[id1][id2][1]
    else:
        teamA = results[id][0][0]
        teamB = results[id][0][1]
    #width so endloss fucky aber prevents wrapping i guess. Alt: Fixed length und max length names
    player11.config(text = teamA[0], width = len(teamA[0])*8, anchor = "e")
    player12.config(text = teamA[1], width = len(teamA[1])*8, anchor = "e")
    player13.config(text = teamA[2], width = len(teamA[2])*8, anchor = "e")
    player14.config(text = teamA[3], width = len(teamA[3])*8, anchor = "e")
    player15.config(text = teamA[4], width = len(teamA[4])*8, anchor = "e")
    player21.config(text = teamB[0], width = len(teamB[0])*8, anchor = "e")
    player22.config(text = teamB[1], width = len(teamB[1])*8, anchor = "e")
    player23.config(text = teamB[2], width = len(teamB[2])*8, anchor = "e")
    player24.config(text = teamB[3], width = len(teamB[3])*8, anchor = "e")
    player25.config(text = teamB[4], width = len(teamB[4])*8, anchor = "e")
    scoreA= 0
    scoreB= 0
    for member in teamA:
        scoreA += int(players_dict[member])
    for member in teamB:
        scoreB += int(players_dict[member])
    teamA_mmr.config(text=str(scoreA), width = 40)
    teamB_mmr.config(text=str(scoreB), width = 40)
    diff = scoreA - scoreB
    mmr_diff.config(text=str(abs(diff)))
    mmr_diff.config(bg="red") if diff>0 else mmr_diff.config(bg="green")



def fill_box(value):
    set_shuffled_off()
    p_value = value
    if not player0.get():
        player0mmr.delete(0,END)
        player0.insert(0,p_value)
        player0mmr.insert(0, players_dict[p_value])
        return
    if not player1.get():
        player1mmr.delete(0,END)
        player1.insert(0,p_value)
        player1mmr.insert(0, players_dict[p_value])
        return
    if not player2.get():
        player2mmr.delete(0,END)
        player2.insert(0,p_value)
        player2mmr.insert(0, players_dict[p_value])
        return
    if not player3.get():
        player3mmr.delete(0,END)
        player3.insert(0,p_value)
        player3mmr.insert(0, players_dict[p_value])
        return
    if not player4.get():
        player4mmr.delete(0,END)
        player4.insert(0,p_value)
        player4mmr.insert(0, players_dict[p_value])
        return
    if not player5.get():
        player5mmr.delete(0,END)
        player5.insert(0,p_value)
        player5mmr.insert(0, players_dict[p_value])
        return
    if not player6.get():
        player6mmr.delete(0,END)
        player6.insert(0,p_value)
        player6mmr.insert(0, players_dict[p_value])
        return
    if not player7.get():
        player7mmr.delete(0,END)
        player7.insert(0,p_value)
        player7mmr.insert(0, players_dict[p_value])
        return
    if not player8.get():
        player8mmr.delete(0,END)
        player8.insert(0,p_value)
        player8mmr.insert(0, players_dict[p_value])
        return
    if not player9.get():
        player9mmr.delete(0,END)
        player9.insert(0,p_value)
        player9mmr.insert(0, players_dict[p_value])
        return
    tkinter.messagebox.showinfo('Error', 'There are already 10 active players selected')

def average_shuffle():
    active_players = [player0.get(), player1.get(), player2.get(), player3.get(), player4.get(), player5.get(), player6.get(), player7.get(), player8.get(), player9.get()]
    global results
    results = {}
    teamA = []
    teamB_roster = []
    teamA.append(active_players[0])
    active_players.pop(0)
    teamB = active_players[:]

    for i in range(9):
        for j in range(8):
            for k in range(7):
                for l in range(6):
                    scoreA = 0
                    scoreB = 0
                    teamA.append(teamB[i])
                    teamB.pop(i)
                    teamA.append(teamB[j])
                    teamB.pop(j)
                    teamA.append(teamB[k])
                    teamB.pop(k)
                    teamA.append(teamB[l])
                    teamB.pop(l)
                    if (teamB in teamB_roster):
                        teamB = active_players[:]
                        teamA = teamA[:1]
                        continue
                    else:
                        teamB_roster.append(teamB)
                    for member in teamA:
                        scoreA += int(players_dict[member])
                    for member in teamB:
                        scoreB += int(players_dict[member])
                    scoredif = abs(scoreA - scoreB)
                    try:
                        results[scoredif].append([teamA,teamB])
                    except:
                        results[scoredif] = [[teamA,teamB]]
                    teamB = active_players[:]
                    teamA = teamA[:1]

    results_sb.delete(0,END)
    idx = 1
    for x in sorted(results.keys()):
        if len(results[x]) < 2:
            results_sb.insert(idx,x)
            idx += 1
        else:
            idx2 = 0
            for y in results[x]:
                results_sb.insert(idx, "%d (%d)" % (x, idx2)) 
                idx += 1
                idx2 += 1
        #max 10 results
        if idx > 10:
            break

    set_shuffled_on()

def set_shuffled_off():
    status.config(bg="red", fg="white", text="Not Shuffled")
def set_shuffled_on():
    status.config(bg="green", fg="white", text="Shuffled")
#load csv
filename = 'players.csv'
players_dict = {}
with open(filename, mode ='r')as file:
  csvFile = csv.DictReader(file)

  for lines in csvFile:
        players_dict[lines['Alias']] = lines['MMR']

PLAYERS = list(players_dict.keys())

#create window
win = tkinter.Tk()
Rwidth = 800
Rheight = 640
win.geometry(str(Rwidth) + "x" + str(Rheight))
win.title("MMR Shuffler")
win.columnconfigure(0,minsize=250)

frame1 = Frame(win) #Players
frame3 = Frame(win) #Dropdown
frame4 = Frame(win) #Buttons
frame5 = Frame(win) #Proposed Teams
frame6 = Frame(win) #StatusFrame


frame5.columnconfigure(1,minsize=150)
frame5.columnconfigure(3,minsize=150)
frame5.config(bd=1,relief = RIDGE)

frame3.grid(row=0, column=0)
frame1.grid(row=0, column=1)
frame4.grid(row=1, column=0)
frame5.grid(row=3, column=1)
frame6.grid(row=3, column = 0, pady=20)



p0 = StringVar(frame3)
p0.set("Choose Player")
w0 = OptionMenu(frame3, p0, *PLAYERS, command=fill_box)
w0.grid(row=0, column=3)

status = Message(frame6, text = "Not Shuffled")
status.config(bg="red", fg="white", width="300")
status.pack()

mmr_msg = Message(frame5, text ="Total MMR: ")
mmr_msg.config(bd=1, relief=RAISED)
mmr_msg.grid(row=6, column=0)

teamAname = Message(frame5,text="Team A")
teamAname.config(bg="red", fg="white", width="300")
teamAname.grid(row=0, column=1)

teamA_mmr = Message(frame5,text="Team A MMR")
teamA_mmr.config(bg="red", fg="white", width="300")
teamA_mmr.grid(row=6, column=1)

teamBname = Message(frame5,text="Team B")
teamBname.config(bg="green", fg="white", width="300")
teamBname.grid(row=0, column=3)

teamB_mmr = Message(frame5,text="Team B MMR")
teamB_mmr.config(bg="green", fg="white", width="300")
teamB_mmr.grid(row=6, column=3)

mmr_diff = Message(frame5,text="Diff")
#mmr_diff.config(bg="green", fg="white", width="300")
mmr_diff.grid(row=6, column=2)

player11 = Message(frame5)
player12 = Message(frame5)
player13 = Message(frame5)
player14 = Message(frame5)
player15 = Message(frame5)
player21 = Message(frame5)
player22 = Message(frame5)
player23 = Message(frame5)
player24 = Message(frame5)
player25 = Message(frame5)

player11.grid(row=1, column=1)
player12.grid(row=2, column=1)
player13.grid(row=3, column=1)
player14.grid(row=4, column=1)
player15.grid(row=5, column=1)
player21.grid(row=1, column=3)
player22.grid(row=2, column=3)
player23.grid(row=3, column=3)
player24.grid(row=4, column=3)
player25.grid(row=5, column=3)


Label(frame3,text="Add player: ").grid(row=0, column=1, columnspan=2)


player0 = Entry(frame1)
player1 = Entry(frame1)
player2 = Entry(frame1)
player3 = Entry(frame1)
player4 = Entry(frame1)
player5 = Entry(frame1)
player6 = Entry(frame1)
player7 = Entry(frame1)
player8 = Entry(frame1)
player9 = Entry(frame1)

player0mmr = Entry(frame1)
player1mmr = Entry(frame1)
player2mmr = Entry(frame1)
player3mmr = Entry(frame1)
player4mmr = Entry(frame1)
player5mmr = Entry(frame1)
player6mmr = Entry(frame1)
player7mmr = Entry(frame1)
player8mmr = Entry(frame1)
player9mmr = Entry(frame1)

Label(frame1,text='Player1  ').grid(row=0)
Label(frame1,text='Player2  ').grid(row=1)
Label(frame1,text='Player3  ').grid(row=2)
Label(frame1,text='Player4  ').grid(row=3)
Label(frame1,text='Player5  ').grid(row=4)
Label(frame1,text='Player6  ').grid(row=5)
Label(frame1,text='Player7  ').grid(row=6)
Label(frame1,text='Player8  ').grid(row=7)
Label(frame1,text='Player9  ').grid(row=8)
Label(frame1,text='Player10').grid(row=9)


player0.grid(row=0, column=1)
player1.grid(row=1, column=1)
player2.grid(row=2, column=1)
player3.grid(row=3, column=1)
player4.grid(row=4, column=1)
player5.grid(row=5, column=1)
player6.grid(row=6, column=1)
player7.grid(row=7, column=1)
player8.grid(row=8, column=1)
player9.grid(row=9, column=1)

player0mmr.grid(row=0, column=2)
player1mmr.grid(row=1, column=2)
player2mmr.grid(row=2, column=2)
player3mmr.grid(row=3, column=2)
player4mmr.grid(row=4, column=2)
player5mmr.grid(row=5, column=2)
player6mmr.grid(row=6, column=2)
player7mmr.grid(row=7, column=2)
player8mmr.grid(row=8, column=2)
player9mmr.grid(row=9, column=2)

shuffle_btn = Button(frame4, text = 'Average MMR Shuffle', command=average_shuffle)
shuffle_btn.pack(side = BOTTOM)

results_sb = Listbox(frame6)
#results_sb.grid(row=2, column=0, pady = 50)
results_sb.pack()

show_results = Button(frame6, text="Generate Teams", command = gen_teams)
#show_results.grid(row=3, column=0)
show_results.pack()
btn2 = Button(frame4, text = 'Dummy Button')
btn2.pack(side = BOTTOM)
win.mainloop()
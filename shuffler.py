import tkinter.messagebox
from tkinter import *
import csv
import re

#globals

global results
global players_dict
global PLAYERS

def update_team(player_msg, team):
    i = 0
    for p in player_msg:
        p.config(text = team[i], width = len(team[i])*8)
        i+=1

def reset_all():
    pass
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
    update_team(teamA_players, teamA)
    update_team(teamB_players, teamB)
    scoreA= 0
    scoreB= 0
    for member in teamA:
        scoreA += int(players_dict[member])
    for member in teamB:
        scoreB += int(players_dict[member])
    scoreA = int(scoreA/5)
    scoreB = int(scoreB/5)
    teamA_mmr.config(text=str(scoreA), width = 40)
    teamB_mmr.config(text=str(scoreB), width = 40)
    diff = scoreA - scoreB
    mmr_diff.config(text=str(abs(diff)))
    mmr_diff.config(bg="red") if diff>0 else mmr_diff.config(bg="green")


#würde auch in schleifen gehen aber brauchst halt 2 neue arrays dunno if worth im moment vll für reset später
def fill_box(value):
    set_shuffled_off()
    p_value = value
    if not player0.get():
        player0.insert(0,p_value)
        player0mmr.config(text = players_dict[p_value])
        return
    if not player1.get():
        player1.insert(0,p_value)
        player1mmr.config(text = players_dict[p_value])
        return
    if not player2.get():
        player2.insert(0,p_value)
        player2mmr.config(text = players_dict[p_value])
        return
    if not player3.get():
        player3.insert(0,p_value)
        player3mmr.config(text = players_dict[p_value])
        return
    if not player4.get():
        player4.insert(0,p_value)
        player4mmr.config(text = players_dict[p_value])
        return
    if not player5.get():
        player5.insert(0,p_value)
        player5mmr.config(text = players_dict[p_value])
        return
    if not player6.get():
        player6.insert(0,p_value)
        player6mmr.config(text = players_dict[p_value])
        return
    if not player7.get():
        player7.insert(0,p_value)
        player7mmr.config(text = players_dict[p_value])
        return
    if not player8.get():
        player8.insert(0,p_value)
        player8mmr.config(text = players_dict[p_value])
        return
    if not player9.get():
        player9.insert(0,p_value)
        player9mmr.config(text = players_dict[p_value])
        return
    tkinter.messagebox.showinfo('Error', 'There are already 10 active players selected')

def average_shuffle():
    active_players = [player0.get(), player1.get(), player2.get(), player3.get(), player4.get(), player5.get(), player6.get(), player7.get(), player8.get(), player9.get()]
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

def A_Won():
    for p in teamA_players:
        p.config(bg="orange")

def B_Won():
    for p in teamB_players:
        p.config(bg="orange")
#load csv
def load_db():
    filename = 'players.csv'
    players_dict = {}
    with open(filename, mode ='r')as file:
        csvFile = csv.DictReader(file)
    for lines in csvFile:
            players_dict[lines['Alias']] = lines['MMR']
    PLAYERS = list(players_dict.keys())

load_db()
#create window
win = tkinter.Tk()
Rwidth = 800
Rheight = 640
win.geometry(str(Rwidth) + "x" + str(Rheight))
win.title("MMR Shuffler")
win.columnconfigure(0,minsize=250)

frame1 = Frame(win) #Players
frame2 = Frame(win) #Results
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
frame2.grid(row=4, column=1)



p0 = StringVar(frame3)
p0.set("Choose Player")
w0 = OptionMenu(frame3, p0, *PLAYERS, command=fill_box)
w0.grid(row=0, column=3)

status = Message(frame6, text = "Not Shuffled")
status.config(bg="red", fg="white", width="300")
status.pack()

mmr_msg = Message(frame5, text ="Average MMR: ")
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

teamA_players = [player11, player12, player13, player14, player15]
i = 0
for p in teamA_players:
    i += 1
    p.grid(row = i, column = 1)

player21 = Message(frame5)
player22 = Message(frame5)
player23 = Message(frame5)
player24 = Message(frame5)
player25 = Message(frame5)

teamB_players = [player21, player22, player23, player24, player25]
i = 0
for p in teamB_players:
    i += 1
    p.grid(row = i, column = 3)


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

player0mmr = Message(frame1)
player1mmr = Message(frame1)
player2mmr = Message(frame1)
player3mmr = Message(frame1)
player4mmr = Message(frame1)
player5mmr = Message(frame1)
player6mmr = Message(frame1)
player7mmr = Message(frame1)
player8mmr = Message(frame1)
player9mmr = Message(frame1)

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
results_sb.pack()

show_results = Button(frame6, text="Generate Teams", command = gen_teams)
show_results.pack()

btn2 = Button(frame4, text = 'Dummy Button')
btn2.pack(side = BOTTOM)

A_winner_btn = Button(frame2, text="Team A won!", command=A_Won)
A_winner_btn.pack(side = LEFT)

B_winner_btn = Button(frame2, text="Team B won!", command=B_Won)
B_winner_btn.pack(side = RIGHT)

next_round_btn = Button(win, text="Next Round!", command=reset_all)
next_round_btn.config(height=5)
next_round_btn.grid(row=4, column=3)
win.mainloop()

#TODO: 1. Reset funktionen machen (Clear: TeamA/TeamB, Unshuffle, Avr MMR/dif, Shuffle liste links, reload DB)
#      2. Wenn player felder geupdated werden: => Unshuffle, UpdateMMR(wie validation), Remove player aus liste links
#      3. Win Buttons sollten DB updaten (und evtl visuell oben darstellen)

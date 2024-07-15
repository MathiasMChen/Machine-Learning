import numpy as np
from random import random as r
import random

def run(m,n):
    swiss_round = int(np.log2(m)) - 1
    teams = {}
    for i in range(m):
        teams[i+1] = r()
    tot = sum(teams.values())
    for i in teams:
        teams[i] = teams[i] / tot * m
    swiss_result = {i+1:0 for i in range(m)}
    for k in range(n):
        results = {(i,j):[] for i in range(swiss_round) for j in range(swiss_round)}
        results[(0,0)] = [i+1 for i in range(m)]
        advance = []
        eliminate = []
        round = 1
        while round <= swiss_round * 2 - 1:
            for win in range(max(round-swiss_round,0), min(round,swiss_round)):
                loss = round - 1 - win
                record = (win,loss)
                lst = results[record]
                while lst:
                    team_1 = random.choice(lst)
                    lst.remove(team_1)
                    team_2 = random.choice(lst)
                    lst.remove(team_2)
                    odd_1 = teams[team_1] / (teams[team_1] + teams[team_2])
                    if r() < odd_1:
                        if win == swiss_round - 1:
                            advance.append(team_1)
                        else:
                            results[(win+1,loss)].append(team_1)
                        if loss == swiss_round - 1:
                            eliminate.append(team_2)
                        else:
                            results[(win,loss+1)].append(team_2)
                    else:
                        if win == swiss_round - 1:
                            advance.append(team_2)
                        else:
                            results[(win+1,loss)].append(team_2)
                        if loss == swiss_round - 1:
                            eliminate.append(team_1)
                        else:
                            results[(win,loss+1)].append(team_1)
            round += 1

        for i in advance:
            swiss_result[i] += 1

    swiss_output = {i: swiss_result[i]/n * 100 for i in swiss_result}

    group_result = {i+1:0 for i in range(m)}
    for _ in range(n):
        lst = sorted(teams.items(), key=lambda x:x[1], reverse=True)
        advance = []
        seeds = [lst[0:m//4], lst[m//4:2*m//4],lst[2*m//4:3*m//4],lst[3*m//4:m]]
        groups = [[] for _ in range(m//4)]
        for i in range(len(groups)):
            for j in range(len(seeds)):
                team = random.choice(seeds[j])
                seeds[j].remove(team)
                groups[i].append(team)
        
        for group in groups:
            record = {team[0]:[0,0] for team in group}
            for team_1, val_1 in group:
                for team_2, val_2 in group:
                    if team_1 == team_2:
                        continue
                    odd_1 = val_1 / (val_1 + val_2)
                    if r() < odd_1:
                        record[team_1][0] += 1
                        record[team_2][1] += 1
                    else:
                        record[team_2][0] += 1
                        record[team_1][1] += 1
            
            lst = sorted(record.items(), key=lambda x:x[1][0], reverse=True)
            qualify = lst[1][1][0]
            fourth = False
            if lst[2][1][0] < qualify:
                advance.append(lst[0][0])
                advance.append(lst[1][0])
            else:
                tie_breaker = [lst[1][0],lst[2][0]]
                if lst[0][1][0] > qualify:
                    advance.append(lst[0][0])
                else:
                    tie_breaker.append(lst[0][0])
                if lst[3][1][0] == qualify:
                    tie_breaker.append(lst[3][0])
                    fourth = True
                if len(tie_breaker) == 2:
                    team_1 = tie_breaker[0]
                    team_2 = tie_breaker[1]
                    odd_1 = teams[team_1] / (teams[team_1] + teams[team_2])
                    if r() < odd_1:
                        advance.append(team_1)
                    else:
                        advance.append(team_2)
                elif len(tie_breaker) == 4:
                    team_1 = random.choice(tie_breaker)
                    tie_breaker.remove(team_1)
                    team_2 = random.choice(tie_breaker)
                    tie_breaker.remove(team_2)
                    odd_1 = teams[team_1] / (teams[team_1] + teams[team_2])
                    if r() < odd_1:
                        advance.append(team_1)
                    else:
                        advance.append(team_2)
                    team_1 = tie_breaker[0]
                    team_2 = tie_breaker[1]
                    odd_1 = teams[team_1] / (teams[team_1] + teams[team_2])
                    if r() < odd_1:
                        advance.append(team_1)
                    else:
                        advance.append(team_2)
                elif len(tie_breaker) == 3:
                    team_3 = random.choice(tie_breaker)
                    tie_breaker.remove(team_3)
                    team_1 = tie_breaker[0]
                    team_2 = tie_breaker[1]
                    if fourth:
                        odd_1 = teams[team_1] / (teams[team_1] + teams[team_2])
                        if r() < odd_1:
                            odd_2 = teams[team_1] / (teams[team_1] + teams[team_3])
                            if r() < odd_2:
                                advance.append(team_1)
                            else:
                                advance.append(team_3)
                        else:
                            odd_2 = teams[team_2] / (teams[team_2] + teams[team_3])
                            if r() < odd_2:
                                advance.append(team_2)
                            else:
                                advance.append(team_3)
                    else:
                        odd_1 = teams[team_1] / (teams[team_1] + teams[team_2])
                        if r() > odd_1:
                            advance.append(team_2)
                            odd_2 = teams[team_1] / (teams[team_1] + teams[team_3])
                            if r() < odd_2:
                                advance.append(team_1)
                            else:
                                advance.append(team_3)
                        else:
                            advance.append(team_1)
                            odd_2 = teams[team_2] / (teams[team_2] + teams[team_3])
                            if r() < odd_2:
                                advance.append(team_2)
                            else:
                                advance.append(team_3)

        for i in advance:
            group_result[i] += 1

    group_output = {i: group_result[i]/n * 100 for i in group_result}
    swiss = sorted(swiss_output.items(), key=lambda x:x[1], reverse=True)
    swiss = [i for i,_ in swiss]
    group = sorted(group_output.items(), key=lambda x:x[1], reverse=True)
    group = [i for i,_ in group]
    team = sorted(teams.items(), key=lambda x:x[1], reverse=True)
    team = [i for i,_ in team]
    return swiss, group, team 
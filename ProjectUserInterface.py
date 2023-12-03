# Veeti Rajaniemi - 050323 - Basics of Database Systems Project - User Interface

import sqlite3
db = sqlite3.connect("Project_database.db")
cur = db.cursor()


def main():
    print("PREMIER LEAGUE 22/23 DATABASE - USER INTERFACE")

    while(True):
        print("\nMenu options:\n")
        print("1) Print players from a team")
        print("2) Print team stats")
        print("3) Print player stats")
        print("4) Print teams and matches")
        print("5) Print top goalscorers")
        print("6) Modify player data")
        print("0) Quit")

        userInput = input("\nWhat do you want to do? ")
        print()

        if userInput == "1":
            printPlayersFromTeam()
        elif userInput == "2":
            printTeamStats() 
        elif userInput == "3":
            printPlayerStats()
        elif userInput == "4":
            printTeamsAndMatches()
        elif userInput == "5":
            printTopScorers()
        elif userInput == "6":
            modifyPlayerData()
        elif userInput == "0":
            print("Thanks for using the program!")
            break
        else:
            print("Invalid choise, please try again!")

    db.close()        
    return


def printPlayersFromTeam():
    team = input("Which team's players you want to search for? ")
    
    print("\nID | Player | Team | Age | Nationality | Position\n")
    cur.execute("SELECT * FROM Player WHERE team_name=?", (team,))
    playerdata = cur.fetchall()

    for row in playerdata:
        print(row)

    return

def printTeamStats():
    print("Team | Matches played | Avg age | Avg poss | Num of players | Contract players | Wage rank | Weekly wages (€)\n")
    query = """SELECT team_name, matches_played, avg_age, avg_possession, num_of_players, contract_players,
    rank AS 'wage_rank', weekly_wages_eur
    FROM (SELECT * FROM Team INNER JOIN Wage ON Team.team_name = Wage.team_name) T"""
    cur.execute(query)
    teamdata = cur.fetchall()
    for row in teamdata:
        print(row)
    return

def printPlayerStats():
    player = input("Which player's stats you want to search for? ")
    team = input("In which team does he play? ")
    cur.execute("SELECT playerID, position FROM Player WHERE player_name=? AND team_name=?",(player,team))
    info = cur.fetchone()
    
    playerID = info[0]
    position = info[1]
    
    if position == "GK":
        print("\nID | Player | Team | Age | Nationality | Matches | CS | GA")
        cur.execute("SELECT * FROM GK_stats WHERE playerID=?", (playerID,))
    
    else:
        print("\nID | Player | Team | Age | Nationality | Goals | Shots | SOT")
        cur.execute("SELECT * FROM Shooting_stats WHERE playerID=?",(playerID,))
    playerdata = cur.fetchall()

    for row in playerdata:
        print(row)
        
    return

def printTeamsAndMatches():

    query = """SELECT Team.team_name, Team.num_of_players, Team.matches_played, Team.avg_age, Team.avg_possession, Match_results.matchID,
    Match_results.day, Match_results.date, Match_results.home_team, Match_results.score, Match_results.away_team FROM Team
    INNER JOIN Team_Match ON Team.team_name = Team_Match.team_name
    INNER JOIN Match_results ON Team_Match.matchID = Match_results.matchID
    ORDER BY Team.team_name;"""
    cur.execute(query)
    
    matchdata = cur.fetchall()
    print("\nTeam | NOP | MP | AvgAge | AvgPoss | MatchID | Day | Date | Home | Score | Away\n")

    for row in matchdata:
        print(row)
    
    return

def printTopScorers():
    num = input("How many top scorers you want to search for? ")
    cur.execute("SELECT player_name AS player, team_name AS team, goals_scored FROM Shooting_stats ORDER BY goals_scored DESC LIMIT ?",(num,))
    topscorers = cur.fetchall()
    print("\nPlayer | Team | Goals\n")
    for row in topscorers:
        print(row)
    return

def modifyPlayerData():
    print("1) Add new player")
    print("2) Delete a player")
    print("3) Edit player's team")

    choice = input("\nSelect an option: ")
    if choice == "1":
        cur.execute("SELECT MAX(playerid) FROM Player")
        data = cur.fetchone()
        newid = data[0] + 1
        name = input("Give player's name: ")
        team = input("Give player's team: ")
        age = input("Give player's age: ")
        nat = input("Give player's nationality (3 letters): ")
        pos = input("Give player's preferred position: (2 letters): ")
        cur.execute("INSERT INTO Player VALUES (?,?,?,?,?,?)",(newid,name,team,age,nat,pos))

    elif choice == "2":
        id = input("Give the playerID of a player you want to delete: ")
        cur.execute("DELETE FROM Player WHERE playerid=?", (id,))

    elif choice == "3":
        id = input("Give the playerID of a player whose team you want to change: ")
        newteam = input("Give the name of the new team: ")
        cur.execute("UPDATE Player SET team_name=? WHERE playerID=?",(newteam,id))

    db.commit()



    return        


main()


class Players():
    def __init__(self):
        self.games = []
        # self.host = host
        # self.players = []

    def addGame(self, roomID, host, players):
        game = {
            'roomID': roomID,
            'host': host,
            'players': [],
        }
        self.games.append(game)
        print(self.games)
        return game

    def grabHost(self,roomID):
        game = [game for game in self.games if game["roomID"] == roomID]
        host = game[0]["host"]
        return host

    def addPlayer(self, roomID, username):
        print(self.games)
        game = [game for game in self.games if game["roomID"] == roomID]
        print(game[0])
        game[0]["players"].append(username)
        print(game[0]["players"])
        return game

    def grabPlayers(self,roomID):
        game = [game for game in self.games if game["roomID"] == roomID]
        players = game[0]["players"]
        return players

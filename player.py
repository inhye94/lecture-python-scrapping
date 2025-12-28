class Player:
  def __init__(self, name, team):
    self.name = name
    self.xp = 1500
    self.team = team
  
  def introduce(self):
    print(f"Hello, I'm {self.name} from team {self.team}.")

class Team:
  def __init__(self, team_name):
    self.team_name = team_name
    self.players = []

  def add_player(self, name):
    new_player = Player(name, self.team_name)
    self.players.append(new_player)
  
  # 삭제 기능
  def remove_player(self, name):
    for player in self.players:
      if player.name == name:
        self.players.remove(player)
        print(f"Player {name} has been removed from team {self.team_name}.")
        break

  # 전체 XP 출력 기능
  def show_total_xp(self):
    total_xp = 0
    for player in self.players:
      total_xp += player.xp

    print(f"Total XP for team {self.team_name}: {total_xp}")

  def show_players(self):
    for player in self.players:
      player.introduce()

team_red = Team("Red Dragons")
team_red.add_player("Nico")

team_blue = Team("Blue Warriors")
team_blue.add_player("Kiki")
team_blue.add_player("Fifi")
team_blue.show_players()
team_blue.show_total_xp()

team_blue.remove_player("Kiki")
team_blue.show_players()
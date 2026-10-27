import random
import streamlit as st
import os

st.set_page_config(page_title="FOOTBALL DIRECTOR", page_icon="⚽", layout="wide")

# 1. 리그 및 팀 구성 (EPL 10팀, 라리가 10팀)
CLUBS = {
    "Manchester City": {"budget": 170, "rating": 88, "league": "Premier League"},
    "Arsenal": {"budget": 115, "rating": 84, "league": "Premier League"},
    "Liverpool": {"budget": 120, "rating": 85, "league": "Premier League"},
    "Chelsea": {"budget": 140, "rating": 83, "league": "Premier League"},
    "Manchester United": {"budget": 150, "rating": 82, "league": "Premier League"},
    "Tottenham": {"budget": 100, "rating": 81, "league": "Premier League"},
    "Newcastle": {"budget": 110, "rating": 80, "league": "Premier League"},
    "Aston Villa": {"budget": 80, "rating": 79, "league": "Premier League"},
    "West Ham": {"budget": 75, "rating": 78, "league": "Premier League"},
    "Everton": {"budget": 60, "rating": 76, "league": "Premier League"},
    
    "Real Madrid": {"budget": 180, "rating": 88, "league": "La Liga"},
    "Barcelona": {"budget": 145, "rating": 86, "league": "La Liga"},
    "Atletico Madrid": {"budget": 110, "rating": 84, "league": "La Liga"},
    "Real Sociedad": {"budget": 70, "rating": 81, "league": "La Liga"},
    "Athletic Bilbao": {"budget": 65, "rating": 80, "league": "La Liga"},
    "Villarreal": {"budget": 60, "rating": 79, "league": "La Liga"},
    "Real Betis": {"budget": 55, "rating": 78, "league": "La Liga"},
    "Valencia": {"budget": 50, "rating": 77, "league": "La Liga"},
    "Sevilla": {"budget": 55, "rating": 77, "league": "La Liga"},
    "Celta Vigo": {"budget": 45, "rating": 75, "league": "La Liga"}
}

# 2. 선수 데이터 및 레전드 추가
PLAYER_DATA = [
    ("Kylian Mbappe", "ST", 27, 92, 170, "Real Madrid"),
    ("Vinicius Junior", "LW", 26, 91, 150, "Real Madrid"),
    ("Zinedine Zidane", "AM", 29, 95, 200, "Real Madrid"), # 레전드
    ("Cristiano Ronaldo", "LW", 28, 95, 120, "Real Madrid"), # 레전드
    ("Lamine Yamal", "RW", 19, 90, 150, "Barcelona"),
    ("Ronaldinho", "LW", 26, 94, 180, "Barcelona"), # 레전드
    ("Lionel Messi", "RW", 25, 96, 250, "Barcelona"), # 레전드
    ("Erling Haaland", "ST", 26, 92, 175, "Manchester City"),
    ("Kevin De Bruyne", "AM", 35, 86, 20, "Manchester City"),
    ("Sergio Aguero", "ST", 27, 91, 130, "Manchester City"), # 레전드
    ("Bukayo Saka", "RW", 25, 89, 120, "Arsenal"),
    ("Thierry Henry", "ST", 26, 94, 190, "Arsenal"), # 레전드
    ("Dennis Bergkamp", "AM", 28, 92, 140, "Arsenal"), # 레전드
    ("Mohamed Salah", "RW", 34, 88, 25, "Liverpool"),
    ("Steven Gerrard", "CM", 27, 92, 150, "Liverpool"), # 레전드
    ("Son Heung-min", "LW", 34, 84, 15, "Tottenham"),
    ("Wayne Rooney", "ST", 27, 93, 160, "Manchester United"), # 레전드
    ("Cole Palmer", "AM", 24, 89, 125, "Chelsea"),
    ("Frank Lampard", "CM", 28, 91, 140, "Chelsea"), # 레전드
]

POSITIONS = ["GK", "CB", "LB", "RB", "DM", "CM", "AM", "LW", "RW", "ST"]

def money(value):
    return f"€{value:.1f}m"

def get_player_image_path(player_name):
    # images 폴더 내 선수 이름과 일치하는 이미지 찾기
    extensions = ['.png', '.jpg', '.jpeg']
    for ext in extensions:
        path = f"images/{player_name}{ext}"
        if os.path.exists(path):
            return path
    return None # 이미지가 없으면 None 반환

def player_from_data(row, pid):
    name, pos, age, rating, value, club = row
    return {
        "id": pid, "name": name, "pos": pos, "age": age,
        "rating": rating, "value": float(value),
        "club": club, "youth": False,
        "stats": {"games": 0, "goals": 0, "assists": 0} # 스탯 초기화
    }

def new_season_table():
    return {club: {"P": 0, "W": 0, "D": 0, "L": 0, "GF": 0, "GA": 0, "Pts": 0} for club in CLUBS}

def init_game(club):
    roster, market = [], []
    pid = 1

    for row in PLAYER_DATA:
        if row[5] == club:
            roster.append(player_from_data(row, pid))
        else:
            market.append(player_from_data(row, pid))
        pid += 1

    while len(roster) < 18:
        pos = random.choice(POSITIONS)
        rating = random.randint(72, 82)
        roster.append({
            "id": pid, "name": f"Player {pid}", "pos": pos,
            "age": random.randint(20, 32), "rating": rating,
            "value": round(max(1, (rating - 60) ** 2 / 8), 1),
            "club": club, "youth": False,
            "stats": {"games": 0, "goals": 0, "assists": 0}
        })
        pid += 1

    return roster, market, pid

def init_state(club):
    roster, market, pid = init_game(club)
    st.session_state.club = club
    st.session_state.budget = float(CLUBS[club]["budget"])
    st.session_state.roster = roster
    st.session_state.starters = [p["id"] for p in sorted(roster, key=lambda x: x['rating'], reverse=True)[:11]]
    st.session_state.market = market
    st.session_state.next_pid = pid
    st.session_state.youth = []
    st.session_state.season = 2026
    st.session_state.week = 1
    st.session_state.table = new_season_table()
    st.session_state.log = [f"{club} 구단의 감독이 되었습니다!"]
    st.session_state.ucl_status = "아직 출전하지 않음"
    st.session_state.ucl_played = False
    st.session_state.trophies = 0
    st.session_state.last_match = None
    st.session_state.formation = "4-3-3"
    st.session_state.training = "Balanced"
    st.session_state.ballon_dor = None

def add_log(message):
    st.session_state.log.insert(0, message)
    st.session_state.log = st.session_state.log[:15]

def squad_strength(roster, starters):
    if not starters: return 50
    starter_players = [p for p in roster if p["id"] in starters]
    if not starter_players: return 50
    ratings = [p["rating"] for p in starter_players]
    return round(sum(ratings) / len(ratings), 1)

def play_match():
    if st.session_state.week > 38:
        st.warning("시즌이 끝났습니다. 다음 시즌을 시작하세요.")
        return
    if len(st.session_state.starters) != 11:
        st.error("선발 라인업을 11명으로 설정해주세요.")
        return

    club = st.session_state.club
    strength = squad_strength(st.session_state.roster, st.session_state.starters)
    
    # 같은 리그 팀과 경기
    my_league = CLUBS[club]["league"]
    league_opponents = [c for c, data in CLUBS.items() if data["league"] == my_league and c != club]
    opponent = random.choice(league_opponents)
    opp_strength = CLUBS[opponent]["rating"] + random.uniform(-2, 2)

    expected = max(0.25, min(3.2, 1.25 + (strength - opp_strength) / 12))
    opp_expected = max(0.2, min(3.0, 1.15 + (opp_strength - strength) / 13))

    goals = min(6, max(0, round(random.gauss(expected, 0.9))))
    conceded = min(6, max(0, round(random.gauss(opp_expected, 0.9))))

    # 내 팀 스탯 기록 (선발 선수들)
    starter_players = [p for p in st.session_state.roster if p["id"] in st.session_state.starters]
    for p in starter_players: p["stats"]["games"] += 1
    
    attackers = [p for p in starter_players if p["pos"] in ["ST", "LW", "RW", "AM"]]
    if not attackers: attackers = starter_players
    
    for _ in range(goals):
        scorer = random.choice(attackers)
        scorer["stats"]["goals"] += 1
        if random.random() > 0.3

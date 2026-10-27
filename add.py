import random
import requests
import streamlit as st

st.set_page_config(
    page_title="FOOTBALL DIRECTOR",
    page_icon="⚽",
    layout="wide"
)

# =========================
# 구단 데이터
# 예산 단위: €m
# =========================

CLUBS = {
    "Manchester United": {"budget": 125, "rating": 83, "league": "Premier League"},
    "Manchester City": {"budget": 170, "rating": 88, "league": "Premier League"},
    "Arsenal": {"budget": 115, "rating": 84, "league": "Premier League"},
    "Liverpool": {"budget": 120, "rating": 85, "league": "Premier League"},
    "Chelsea": {"budget": 105, "rating": 82, "league": "Premier League"},
    "Tottenham": {"budget": 90, "rating": 81, "league": "Premier League"},
    "Newcastle United": {"budget": 95, "rating": 81, "league": "Premier League"},
    "Aston Villa": {"budget": 75, "rating": 80, "league": "Premier League"},
    "West Ham": {"budget": 65, "rating": 78, "league": "Premier League"},
    "Everton": {"budget": 45, "rating": 74, "league": "Premier League"},

    "Real Madrid": {"budget": 180, "rating": 88, "league": "La Liga"},
    "Barcelona": {"budget": 145, "rating": 86, "league": "La Liga"},
    "Atletico Madrid": {"budget": 95, "rating": 84, "league": "La Liga"},
    "Athletic Bilbao": {"budget": 55, "rating": 79, "league": "La Liga"},
    "Real Sociedad": {"budget": 55, "rating": 79, "league": "La Liga"},
    "Sevilla": {"budget": 50, "rating": 77, "league": "La Liga"},
    "Valencia": {"budget": 45, "rating": 76, "league": "La Liga"},
    "Villarreal": {"budget": 60, "rating": 79, "league": "La Liga"},
    "Real Betis": {"budget": 50, "rating": 77, "league": "La Liga"},
    "Girona": {"budget": 40, "rating": 75, "league": "La Liga"},
}

# =========================
# 선수 데이터
# 형식: 이름, 포지션, 나이, 능력치, 가치, 소속 구단
# 능력치와 가치는 게임용 예시
# =========================

PLAYER_DATA = []

def add_players(club, players):
    for name, pos, age, rating, value in players:
        PLAYER_DATA.append(
            (name, pos, age, rating, value, club)
        )


# 맨체스터 유나이티드
add_players("Manchester United", [
    ("Peter Schmeichel", "GK", 62, 92, 1),
    ("Gary Neville", "RB", 51, 88, 1),
    ("Rio Ferdinand", "CB", 47, 92, 1),
    ("Nemanja Vidic", "CB", 44, 91, 1),
    ("Denis Irwin", "LB", 60, 88, 1),
    ("Roy Keane", "DM", 55, 93, 1),
    ("Paul Scholes", "CM", 51, 94, 1),
    ("David Beckham", "RW", 51, 93, 1),
    ("Ryan Giggs", "LW", 52, 92, 1),
    ("Wayne Rooney", "ST", 41, 94, 1),
    ("Cristiano Ronaldo", "ST", 41, 97, 1),
    ("Bruno Fernandes", "AM", 32, 87, 55),
])

# 맨체스터 시티
add_players("Manchester City", [
    ("Ederson", "GK", 33, 87, 25),
    ("Kyle Walker", "RB", 36, 83, 10),
    ("Vincent Kompany", "CB", 40, 91, 1),
    ("Ruben Dias", "CB", 29, 88, 65),
    ("Rodri", "DM", 30, 92, 100),
    ("David Silva", "AM", 40, 92, 1),
    ("Kevin De Bruyne", "AM", 35, 90, 20),
    ("Yaya Toure", "CM", 43, 91, 1),
    ("Phil Foden", "LW", 26, 89, 105),
    ("Sergio Aguero", "ST", 38, 94, 1),
    ("Erling Haaland", "ST", 26, 93, 175),
])

# 아스널
add_players("Arsenal", [
    ("David Seaman", "GK", 63, 91, 1),
    ("Lauren", "RB", 49, 86, 1),
    ("Tony Adams", "CB", 59, 93, 1),
    ("Sol Campbell", "CB", 52, 91, 1),
    ("Ashley Cole", "LB", 45, 91, 1),
    ("Patrick Vieira", "DM", 50, 94, 1),
    ("Cesc Fabregas", "CM", 39, 91, 1),
    ("Robert Pires", "LW", 52, 92, 1),
    ("Freddie Ljungberg", "RW", 49, 88, 1),
    ("Dennis Bergkamp", "AM", 57, 95, 1),
    ("Thierry Henry", "ST", 49, 97, 1),
    ("Bukayo Saka", "RW", 25, 89, 120),
    ("Declan Rice", "DM", 27, 88, 105),
    ("William Saliba", "CB", 25, 87, 80),
])

# 리버풀
add_players("Liverpool", [
    ("Alisson Becker", "GK", 33, 89, 30),
    ("Trent Alexander-Arnold", "RB", 28, 88, 70),
    ("Virgil van Dijk", "CB", 35, 89, 18),
    ("Alan Hansen", "CB", 71, 91, 1),
    ("Andy Robertson", "LB", 32, 85, 15),
    ("Steven Gerrard", "CM", 46, 96, 1),
    ("Xabi Alonso", "DM", 44, 92, 1),
    ("John Barnes", "LW", 63, 91, 1),
    ("Mohamed Salah", "RW", 34, 91, 25),
    ("Kenny Dalglish", "ST", 75, 96, 1),
    ("Ian Rush", "ST", 65, 93, 1),
    ("Florian Wirtz", "AM", 23, 89, 120),
    ("Alexis Mac Allister", "CM", 27, 86, 75),
])

# 첼시
add_players("Chelsea", [
    ("Petr Cech", "GK", 44, 93, 1),
    ("Cesar Azpilicueta", "RB", 37, 86, 1),
    ("John Terry", "CB", 46, 95, 1),
    ("Ricardo Carvalho", "CB", 48, 90, 1),
    ("Ashley Cole", "LB", 45, 91, 1),
    ("Claude Makelele", "DM", 53, 92, 1),
    ("Frank Lampard", "CM", 48, 95, 1),
    ("Eden Hazard", "LW", 35, 94, 1),
    ("Arjen Robben", "RW", 42, 92, 1),
    ("Didier Drogba", "ST", 48, 94, 1),
    ("Gianfranco Zola", "AM", 60, 92, 1),
    ("Cole Palmer", "AM", 24, 89, 125),
    ("Enzo Fernandez", "CM", 25, 86, 80),
])

# 토트넘
add_players("Tottenham", [
    ("Hugo Lloris", "GK", 39, 86, 1),
    ("Kyle Walker", "RB", 36, 83, 10),
    ("Ledley King", "CB", 46, 90, 1),
    ("Jan Vertonghen", "CB", 39, 87, 1),
    ("Danny Rose", "LB", 36, 84, 1),
    ("Luka Modric", "CM", 41, 94, 1),
    ("Glenn Hoddle", "AM", 68, 93, 1),
    ("David Ginola", "LW", 59, 90, 1),
    ("Gareth Bale", "RW", 37, 94, 1),
    ("Harry Kane", "ST", 33, 95, 1),
    ("Son Heung-min", "LW", 34, 89, 15),
    ("James Maddison", "AM", 29, 85, 45),
])

# 뉴캐슬
add_players("Newcastle United", [
    ("Shay Given", "GK", 50, 87, 1),
    ("Kieran Trippier", "RB", 36, 84, 8),
    ("Jonathan Woodgate", "CB", 46, 87, 1),
    ("Fabian Schar", "CB", 34, 83, 8),
    ("Stuart Pearce", "LB", 64, 88, 1),
    ("David Batty", "DM", 57, 86, 1),
    ("Gary Speed", "CM", 56, 90, 1),
    ("Peter Beardsley", "AM", 65, 92, 1),
    ("Alan Shearer", "ST", 56, 96, 1),
    ("Les Ferdinand", "ST", 59, 90, 1),
    ("Bruno Guimaraes", "CM", 29, 87, 80),
])

# 아스톤 빌라
add_players("Aston Villa", [
    ("Emiliano Martinez", "GK", 34, 87, 25),
    ("Matty Cash", "RB", 29, 81, 20),
    ("Olof Mellberg", "CB", 49, 87, 1),
    ("Paul McGrath", "CB", 67, 92, 1),
    ("Lucas Digne", "LB", 33, 82, 12),
    ("Gareth Barry", "DM", 45, 89, 1),
    ("James Milner", "CM", 40, 86, 1),
    ("Jack Grealish", "LW", 31, 89, 1),
    ("Dwight Yorke", "ST", 55, 91, 1),
    ("Peter Withe", "ST", 76, 90, 1),
    ("Ollie Watkins", "ST", 30, 85, 45),
])

# 웨스트햄
add_players("West Ham", [
    ("Ludek Miklosko", "GK", 64, 86, 1),
    ("Vladimir Coufal", "RB", 34, 80, 8),
    ("Bobby Moore", "CB", 85, 97, 1),
    ("Rio Ferdinand", "CB", 47, 92, 1),
    ("Julian Dicks", "LB", 57, 86, 1),
    ("Declan Rice", "DM", 27, 89, 1),
    ("Mark Noble", "CM", 39, 87, 1),
    ("Paolo Di Canio", "AM", 58, 91, 1),
    ("Trevor Brooking", "AM", 78, 92, 1),
    ("Geoff Hurst", "ST", 84, 94, 1),
    ("Michail Antonio", "ST", 36, 80, 5),
])

# 에버턴
add_players("Everton", [
    ("Neville Southall", "GK", 67, 93, 1),
    ("Phil Neville", "RB", 49, 85, 1),
    ("Brian Labone", "CB", 84, 91, 1),
    ("John Stones", "CB", 32, 87, 1),
    ("Leighton Baines", "LB", 42, 89, 1),
    ("Alan Ball", "CM", 81, 94, 1),
    ("Tim Cahill", "AM", 47, 89, 1),
    ("Steven Pienaar", "LW", 44, 85, 1),
    ("Kevin Sheedy", "LW", 66, 88, 1),
    ("Dixie Dean", "ST", 123, 97, 1),
    ("Wayne Rooney", "ST", 41, 94, 1),
])

# 레알 마드리드
add_players("Real Madrid", [
    ("Iker Casillas", "GK", 45, 95, 1),
    ("Dani Carvajal", "RB", 34, 86, 12),
    ("Sergio Ramos", "CB", 40, 95, 1),
    ("Fernando Hierro", "CB", 58, 93, 1),
    ("Roberto Carlos", "LB", 53, 94, 1),
    ("Luka Modric", "CM", 41, 94, 1),
    ("Zinedine Zidane", "AM", 54, 98, 1),
    ("Cristiano Ronaldo", "LW", 41, 97, 1),
    ("Luis Figo", "RW", 54, 94, 1),
    ("Karim Benzema", "ST", 39, 94, 1),
    ("Ronaldo Nazario", "ST", 50, 97, 1),
    ("Kylian Mbappe", "ST", 27, 94, 170),
    ("Vinicius Junior", "LW", 26, 92, 150),
    ("Jude Bellingham", "CM", 23, 91, 145),
    ("Federico Valverde", "CM", 28, 89, 95),
    ("Thibaut Courtois", "GK", 34, 90, 35),
])

# 바르셀로나 — 메시를 바르셀로나 소속으로 설정
add_players("Barcelona", [
    ("Victor Valdes", "GK", 44, 89, 1),
    ("Dani Alves", "RB", 43, 93, 1),
    ("Carles Puyol", "CB", 48, 94, 1),
    ("Gerard Pique", "CB", 39, 92, 1),
    ("Eric Abidal", "LB", 47, 88, 1),
    ("Sergio Busquets", "DM", 38, 94, 1),
    ("Xavi", "CM", 46, 97, 1),
    ("Andres Iniesta", "CM", 42, 97, 1),
    ("Ronaldinho", "LW", 46, 97, 1),
    ("Lionel Messi", "RW", 39, 100, 1),
    ("Luis Suarez", "ST", 39, 95, 1),
    ("Lamine Yamal", "RW", 19, 91, 150),
    ("Pedri", "CM", 23, 89, 110),
    ("Gavi", "CM", 22, 86, 75),
    ("Raphinha", "LW", 29, 88, 75),
    ("Robert Lewandowski", "ST", 38, 86, 18),
    ("Frenkie de Jong", "CM", 29, 87, 55),
])

# 아틀레티코 마드리드
add_players("Atletico Madrid", [
    ("Jan Oblak", "GK", 33, 91, 35),
    ("Juanfran", "RB", 41, 88, 1),
    ("Diego Godin", "CB", 40, 93, 1),
    ("Miranda", "CB", 42, 89, 1),
    ("Filipe Luis", "LB", 41, 90, 1),
    ("Gabi", "DM", 43, 89, 1),
    ("Koke", "CM", 34, 88, 20),
    ("Diego Simeone", "CM", 56, 90, 1),
    ("Antoine Griezmann", "AM", 35, 90, 12),
    ("Fernando Torres", "ST", 42, 93, 1),
    ("Radamel Falcao", "ST", 40, 93, 1),
    ("Julian Alvarez", "ST", 26, 88, 90),
])

# 아틀레틱 빌바오
add_players("Athletic Bilbao", [
    ("Unai Simon", "GK", 29, 86, 35),
    ("Andoni Iraola", "RB", 44, 87, 1),
    ("Aymeric Laporte", "CB", 32, 86, 25),
    ("Fernando Amorebieta", "CB", 41, 84, 1),
    ("Aitor Larrazabal", "LB", 54, 86, 1),
    ("Javi Martinez", "DM", 38, 88, 1),
    ("Ander Herrera", "CM", 37, 83, 1),
    ("Julen Guerrero", "AM", 52, 89, 1),
    ("Iker Muniain", "LW", 34, 88, 1),
    ("Aritz Aduriz", "ST", 45, 91, 1),
    ("Inaki Williams", "ST", 32, 85, 35),
    ("Nico Williams", "LW", 24, 88, 70),
])

# 레알 소시에다드
add_players("Real Sociedad", [
    ("Alex Remiro", "GK", 31, 85, 20),
    ("Alvaro Odriozola", "RB", 30, 80, 8),
    ("Inigo Martinez", "CB", 35, 86, 1),
    ("Robin Le Normand", "CB", 29, 86, 30),
    ("Aihen Munoz", "LB", 29, 79, 8),
    ("Xabi Alonso", "DM", 44, 92, 1),
    ("Mikel Merino", "CM", 30, 86, 1),
    ("David Silva", "AM", 40, 92, 1),
    ("Antoine Griezmann", "LW", 35, 90, 1),
    ("Nihat Kahveci", "ST", 47, 89, 1),
    ("Alexander Isak", "ST", 27, 88, 1),
    ("Mikel Oyarzabal", "LW", 29, 86, 45),
])

# 세비야
add_players("Sevilla", [
    ("Andres Palop", "GK", 53, 88, 1),
    ("Jesus Navas", "RB", 41, 88, 1),
    ("Jules Kounde", "CB", 28, 87, 1),
    ("Sergio Ramos", "CB", 40, 94, 1),
    ("Adriano", "LB", 41, 87, 1),
    ("Ivan Rakitic", "CM", 38, 89, 1),
    ("Ever Banega", "CM", 38, 89, 1),
    ("Dani Alves", "RW", 43, 92, 1),
    ("Jose Antonio Reyes", "LW", 43, 89, 1),
    ("Frederic Kanoute", "ST", 49, 91, 1),
    ("Carlos Bacca", "ST", 40, 88, 1),
])

# 발렌시아
add_players("Valencia", [
    ("Santiago Canizares", "GK", 57, 91, 1),
    ("Miguel", "RB", 46, 87, 1),
    ("Roberto Ayala", "CB", 53, 92, 1),
    ("Carlos Marchena", "CB", 47, 89, 1),
    ("Amedeo Carboni", "LB", 61, 88, 1),
    ("David Albelda", "DM", 49, 89, 1),
    ("Gaizka Mendieta", "CM", 52, 92, 1),
    ("Pablo Aimar", "AM", 47, 92, 1),
    ("Vicente", "LW", 45, 90, 1),
    ("David Villa", "ST", 45, 94, 1),
    ("Mario Kempes", "ST", 72, 95, 1),
])

# 비야레알
add_players("Villarreal", [
    ("Pepe Reina", "GK", 44, 87, 1),
    ("Mario Gaspar", "RB", 35, 82, 1),
    ("Gonzalo Rodriguez", "CB", 42, 87, 1),
    ("Mateo Musacchio", "CB", 36, 84, 1),
    ("Joan Capdevila", "LB", 48, 88, 1),
    ("Marcos Senna", "DM", 50, 90, 1),
    ("Santi Cazorla", "CM", 41, 91, 1),
    ("Juan Roman Riquelme", "AM", 48, 94, 1),
    ("Robert Pires", "LW", 52, 91, 1),
    ("Diego Forlan", "ST", 47, 93, 1),
    ("Giuseppe Rossi", "ST", 39, 88, 1),
])

# 레알 베티스
add_players("Real Betis", [
    ("Claudio Bravo", "GK", 43, 86, 1),
    ("Hector Bellerin", "RB", 31, 81, 8),
    ("Aissa Mandi", "CB", 34, 82, 1),
    ("Marc Bartra", "CB", 35, 83, 1),
    ("Juan Miranda", "LB", 26, 80, 10),
    ("Guido Rodriguez", "DM", 32, 85, 1),
    ("Joaquin", "RW", 45, 91, 1),
    ("Isco", "AM", 34, 88, 1),
    ("Nabil Fekir", "AM", 33, 87, 1),
    ("Ruben Castro", "ST", 45, 89, 1),
    ("Alfonso Perez", "ST", 54, 87, 1),
])

# 지로나
add_players("Girona", [
    ("Paulo Gazzaniga", "GK", 34, 82, 8),
    ("Arnau Martinez", "RB", 23, 80, 18),
    ("David Lopez", "CB", 36, 80, 1),
    ("Daley Blind", "CB", 36, 83, 1),
    ("Miguel Gutierrez", "LB", 25, 83, 25),
    ("Aleix Garcia", "CM", 29, 85, 1),
    ("Ivan Martin", "CM", 27, 82, 15),
    ("Portu", "RW", 34, 80, 1),
    ("Savio", "LW", 22, 84, 1),
    ("Cristhian Stuani", "ST", 39, 84, 1),
    ("Artem Dovbyk", "ST", 29, 86, 1),
])

# 포지션 목록
POSITIONS = ["GK", "CB", "LB", "RB", "DM", "CM", "AM", "LW", "RW", "ST"]


# =========================
# 선수 사진
# Wikipedia의 공개 요약 API에서 사진을 조회
# 인터넷이 연결되어 있어야 표시됨
# =========================

@st.cache_data(ttl=86400, show_spinner=False)
def get_player_image(name):
    clean_name = name.replace("(Legend)", "").strip()
    url = (
        "https://en.wikipedia.org/api/rest_v1/page/summary/"
        + requests.utils.quote(clean_name.replace(" ", "_"))
    )
    try:
        response = requests.get(
            url,
            timeout=3,
            headers={"User-Agent": "FootballDirectorGame/1.0"}
        )
        if response.status_code == 200:
            data = response.json()
            return data.get("thumbnail", {}).get("source")
    except requests.RequestException:
        pass
    return None


def show_player_card(player):
    image_url = get_player_image(player["name"])
    with st.container(border=True):
        if image_url:
            st.image(image_url, use_container_width=True)
        else:
            st.markdown("### ⚽")
        st.markdown(f"**{player['name']}**")
        st.write(
            f"{player['pos']} · OVR {player['rating']} · "
            f"{player['age']}세"
        )
        st.caption(f"소속: {player['club']}")
        st.caption(f"시장 가치: €{player['value']:.1f}m")


# =========================
# 공통 함수
# =========================

def money(amount):
    return f"€{amount:.1f}m"


def new_table():
    return {
        club: {
            "P": 0, "W": 0, "D": 0, "L": 0,
            "GF": 0, "GA": 0, "Pts": 0
        }
        for club in CLUBS
    }


def add_log(message):
    st.session_state.log.insert(0, message)
    st.session_state.log = st.session_state.log[:20]


def create_player(row, pid):
    name, pos, age, rating, value, club = row
    return {
        "id": pid,
        "name": name,
        "pos": pos,
        "age": age,
        "rating": rating,
        "value": float(value),
        "club": club,
        "youth": False,
        "apps": 0,
        "goals": 0,
        "assists": 0,
        "rating_sum": 0.0,
        "clean_sheets": 0,
        "motm": 0,
    }


def init_game(club):
    roster = []
    pid = 1

    for row in PLAYER_DATA:
        if row[5] == club:
            roster.append(create_player(row, pid))
            pid += 1

    # 선수단을 최소 18명으로 채움
    while len(roster) < 18:
        pos = random.choice(POSITIONS)
        age = random.randint(18, 32)
        rating = random.randint(65, 80)
        player = {
            "id": pid,
            "name": random.choice([
                "Alex Morgan", "Leo Silva", "Daniel Costa",
                "Noah Martin", "Sam Taylor", "Marco Rossi",
                "Min-jae Park", "Ethan Cole", "Lucas Meyer",
                "Kai Tanaka"
            ]) + f" {pid}",
            "pos": pos,
            "age": age,
            "rating": rating,
            "value": round(max(1, (rating - 60) ** 2 / 8), 1),
            "club": club,
            "youth": False,
            "apps": 0,
            "goals": 0,
            "assists": 0,
            "rating_sum": 0.0,
            "clean_sheets": 0,
            "motm": 0,
        }
        roster.append(player)
        pid += 1

    market = []
    for row in PLAYER_DATA:
        if row[5] != club:
            market.append(create_player(row, pid))
            pid += 1

    for n in range(25):
        rating = random.randint(65, 82)
        market.append({
            "id": pid,
            "name": random.choice([
                "A. Kim", "J. Silva", "M. Novak", "T. Ito",
                "D. Park", "L. Santos"
            ]) + f" {n + 1}",
            "pos": random.choice(POSITIONS),
            "age": random.randint(18, 31),
            "rating": rating,
            "value": round(max(1, (rating - 58) ** 2 / 9), 1),
            "club": "Free Agent",
            "youth": False,
            "apps": 0,
            "goals": 0,
            "assists": 0,
            "rating_sum": 0.0,
            "clean_sheets": 0,
            "motm": 0,
        })
        pid += 1

    return roster, market, pid


def init_state(club):
    roster, market, pid = init_game(club)

    st.session_state.club = club
    st.session_state.budget = float(CLUBS[club]["budget"])
    st.session_state.roster = roster
    st.session_state.market = market
    st.session_state.next_pid = pid
    st.session_state.youth = []
    st.session_state.season = 2026
    st.session_state.week = 1
    st.session_state.table = new_table()
    st.session_state.log = [f"{club} 감독 커리어가 시작됐습니다."]
    st.session_state.trophies = 0
    st.session_state.last_match = None
    st.session_state.formation = "4-3-3"
    st.session_state.training = "균형"
    st.session_state.starting_xi = []
    st.session_state.ballondor = "아직 시즌 종료 전"
    st.session_state.ucl_status = "아직 진출하지 못했습니다."
    st.session_state.ucl_played = False


def team_strength(roster):
    if not roster:
        return 50
    top = sorted(
        roster,
        key=lambda p: p["rating"],
        reverse=True
    )[:11]
    return round(
        sum(p["rating"] for p in top) / len(top),
        1
    )


def simulate_match():
    club = st.session_state.club
    league = CLUBS[club]["league"]

    if st.session_state.week > 38:
        st.warning("시즌이 끝났습니다. 다음 시즌을 시작하세요.")
        return

    opponent_pool = [
        c for c in CLUBS
        if c != club and CLUBS[c]["league"] == league
    ]
    opponent = random.choice(opponent_pool)

    roster = st.session_state.roster
    if not roster:
        st.error("선수단이 비어 있습니다.")
        return

    xi_ids = st.session_state.starting_xi
    if len(xi_ids) != 11:
        xi = sorted(
            roster,
            key=lambda p: p["rating"],
            reverse=True
        )[:11]
    else:
        xi = [p for p in roster if p["id"] in xi_ids]

    strength = sum(p["rating"] for p in xi) / max(1, len(xi))
    opponent_strength = CLUBS[opponent]["rating"] + random.uniform(-2, 2)

    formation_bonus = {
        "4-3-3": 1.0,
        "4-4-2": 0.4,
        "5-3-2": 0.2
    }
    tactic_bonus = {
        "공격": 1.2,
        "균형": 0.0,
        "수비": -0.3
    }

    difference = strength - opponent_strength
    expected_goals = max(
        0.3,
        min(3.2, 1.4 + difference / 12)
    )
    expected_goals += formation_bonus.get(
        st.session_state.formation, 0
    )
    expected_goals += tactic_bonus.get(
        st.session_state.training, 0
    )

    gf = max(0, min(6, round(random.gauss(expected_goals, 0.9))))
    ga = max(
        0,
        min(6, round(random.gauss(1.25 - difference / 14, 0.9)))
    )

    table = st.session_state.table
    t = table[club]
    t["P"] += 1
    t["GF"] += gf
    t["GA"] += ga

    if gf > ga:
        t["W"] += 1
        t["Pts"] += 3
        result = "승리"
    elif gf == ga:
        t["D"] += 1
        t["Pts"] += 1
        result = "무승부"
    else:
        t["L"] += 1
        result = "패배"

    # 다른 구단 경기 결과 시뮬레이션
    others = [c for c in opponent_pool if c != opponent]
    random.shuffle(others)

    for i in range(0, len(others) - 1, 2):
        a, b = others[i], others[i + 1]
        x, y = random.randint(0, 3), random.randint(0, 3)

        for team, scored, conceded in [(a, x, y), (b, y, x)]:
            tt = table[team]
            tt["P"] += 1
            tt["GF"] += scored
            tt["GA"] += conceded

            if scored > conceded:
                tt["W"] += 1
                tt["Pts"] += 3
            elif scored == conceded:
                tt["D"] += 1
                tt["Pts"] += 1
            else:
                tt["L"] += 1

    goal_scorers = []

    for p in xi:
        p["apps"] += 1
        performance = max(
            4.5,
            min(
                10,
                random.gauss(
                    6.5 + (p["rating"] - 80) / 12,
                    0.7
                )
            )
        )
        p["rating_sum"] += performance

        if p["pos"] == "GK" and ga == 0:
            p["clean_sheets"] += 1

        if random.random() < max(0.04, (p["rating"] - 55) / 120):
            if p["pos"] in ["ST", "LW", "RW", "AM"]:
                p["goals"] += 1
                goal_scorers.append(p)
            elif p["pos"] not in ["GK", "CB"]:
                p["assists"] += 1

    if goal_scorers:
        random.choice(goal_scorers)["motm"] += 1
    elif xi:
        max(xi, key=lambda p: p["rating"])["motm"] += 1

    st.session_state.last_match = (
        club, gf, ga, opponent, result
    )
    st.session_state.week += 1
    st.session_state.budget += 2.5

    add_log(
        f"{st.session_state.week - 1}라운드: "
        f"{club} {gf}-{ga} {opponent} — {result}"
    )


def sign_youth():
    if st.session_state.budget < 1:
        st.error("유스 발굴 비용이 부족합니다.")
        return

    pid = st.session_state.next_pid
    pos = random.choice(POSITIONS)
    rating = random.randint(55, 72)

    player = {
        "id": pid,
        "name": random.choice([
            "민준 이", "지호 박", "Alex Kim", "Leo Santos"
        ]) + f" {pid}",
        "pos": pos,
        "age": random.randint(15, 18),
        "rating": rating,
        "value": round(random.uniform(0.1, 2.5), 1),
        "club": st.session_state.club,
        "youth": True,
        "apps": 0,
        "goals": 0,
        "assists": 0,
        "rating_sum": 0.0,
        "clean_sheets": 0,
        "motm": 0,
    }

    st.session_state.next_pid += 1
    st.session_state.youth.append(player)
    st.session_state.budget -= 1
    add_log(f"유스 발굴: {player['name']} ({pos}, OVR {rating})")


def buy_player(pid):
    player = next(
        (p for p in st.session_state.market if p["id"] == pid),
        None
    )
    if not player:
        return

    fee = player["value"] * 1.15

    if st.session_state.budget < fee:
        st.error("이적 자금이 부족합니다.")
        return

    if len(st.session_state.roster) >= 30:
        st.error("1군 선수단은 최대 30명입니다.")
        return

    st.session_state.budget -= fee
    player["club"] = st.session_state.club
    st.session_state.roster.append(player)
    st.session_state.market = [
        p for p in st.session_state.market if p["id"] != pid
    ]
    add_log(f"{player['name']} 영입 완료: {money(fee)}")


def sell_player(pid):
    player = next(
        (p for p in st.session_state.roster if p["id"] == pid),
        None
    )
    if not player:
        return

    fee = player["value"] * 0.85
    st.session_state.budget += fee
    st.session_state.roster = [
        p for p in st.session_state.roster if p["id"] != pid
    ]

    player["club"] = "Free Agent"
    st.session_state.market.append(player)
    add_log(f"{player['name']} 판매: {money(fee)}")


def end_season():
    club = st.session_state.club
    played = st.session_state.table[club]["P"]

    if played == 0:
        st.warning("시즌 종료 전에 리그 경기를 한 번 이상 진행하세요.")
        return

    standings = sorted(
        [
            (name, data)
            for name, data in st.session_state.table.items()
            if CLUBS[name]["league"] == CLUBS[club]["league"]
        ],
        key=lambda item: (
            item[1]["Pts"],
            item[1]["GF"] - item[1]["GA"],
            item[1]["GF"]
        ),
        reverse=True
    )

    place = [name for name, _ in standings].index(club) + 1
    prize = {1: 60, 2: 40, 3: 28, 4: 20}.get(place, 8)
    st.session_state.budget += prize

    players = st.session_state.roster
    if players:
        winner = max(
            players,
            key=lambda p: (
                p["goals"] * 4
                + p["assists"] * 3
                + p["motm"] * 2
                + p["rating_sum"] / max(1, p["apps"])
            )
        )

        st.session_state.ballondor = (
            f"{winner['name']} — {winner['goals']}골, "
            f"{winner['assists']}도움, 평균 평점 "
            f"{winner['rating_sum'] / max(1, winner['apps']):.2f}"
        )

    if place <= 2:
        st.session_state.ucl_status = "챔피언스리그 진출 확정"
    else:
        st.session_state.ucl_status = "리그 상위 2팀 진출 조건 미달"

    if place == 1:
        st.session_state.trophies += 1
        add_log(
            f"{st.session_state.season} 시즌 리그 우승! "
            f"상금 {money(prize)}"
        )
    else:
        add_log(f"시즌 종료: 리그 {place}위, 상금 {money(prize)}")

    st.session_state.season += 1
    st.session_state.week = 1
    st.session_state.table = new_table()
    st.session_state.ucl_played = False
    st.session_state.starting_xi = []

    for p in st.session_state.roster:
        p["age"] += 1

        if p["age"] <= 23 and random.random() < 0.6:
            p["rating"] = min(95, p["rating"] + 1)
        elif p["age"] >= 32 and random.random() < 0.45:
            p["rating"] = max(55, p["rating"] - 1)

        p.update({
            "apps": 0,
            "goals": 0,
            "assists": 0,
            "rating_sum": 0.0,
            "clean_sheets": 0,
            "motm": 0
        })

    add_log(f"{st.session_state.season} 시즌이 시작됐습니다.")


def play_ucl():
    if st.session_state.ucl_played:
        st.warning("이번 시즌 유럽 대회를 이미 진행했습니다.")
        return

    club = st.session_state.club
    league = CLUBS[club]["league"]

    standings = sorted(
        [
            (name, data)
            for name, data in st.session_state.table.items()
            if CLUBS[name]["league"] == league
        ],
        key=lambda item: (
            item[1]["Pts"],
            item[1]["GF"] - item[1]["GA"],
            item[1]["GF"]
        ),
        reverse=True
    )

    place = [name for name, _ in standings].index(club) + 1

    if place > 2:
        st.warning("챔피언스리그는 해당 리그 상위 2팀만 참가할 수 있습니다.")
        return

    strength = team_strength(st.session_state.roster)
    opponents = [
        name for name in CLUBS
        if CLUBS[name]["league"] != league
    ]

    results = []

    for round_name in ["8강", "4강", "결승"]:
        opponent = random.choice(opponents)
        opp_rating = CLUBS[opponent]["rating"]

        gf = max(
            0,
            round(random.gauss(1.5 + (strength - opp_rating) / 13, 1))
        )
        ga = max(
            0,
            round(random.gauss(1.2 + (opp_rating - strength) / 14, 1))
        )

        if gf == ga:
            gf += random.choice([0, 1])

        results.append(
            f"{round_name}: {club} {gf}-{ga} {opponent}"
        )

        if gf < ga:
            st.session_state.ucl_status = f"{round_name} 탈락"
            break
    else:
        st.session_state.ucl_status = "챔피언스리그 우승 🏆"
        st.session_state.trophies += 1
        st.session_state.budget += 45

    st.session_state.ucl_played = True
    add_log("유럽 대회 결과: " + " / ".join(results))


# =========================
# 화면 디자인
# =========================

st.markdown("""
<style>
.stApp {
    background: linear-gradient(145deg, #08131f, #102b32);
    color: #eef8f4;
}
h1, h2, h3 {
    color: #eafff6;
}
div[data-testid="stMetric"] {
    background: #102c32;
    padding: 14px;
    border-radius: 12px;
    border: 1px solid #24635b;
}
.stButton > button {
    border-radius: 10px;
    font-weight: 700;
}
</style>
""", unsafe_allow_html=True)

st.title("⚽ FOOTBALL DIRECTOR")
st.caption(
    "구단 운영 · 레전드 선수 · 이적시장 · 유스 아카데미 · 리그 · 챔피언스리그"
)
st.info(
    "팬 제작 게임용 예시 데이터입니다. "
    "선수 능력치와 시장 가치는 실제 공식 기록과 다를 수 있습니다."
)


# =========================
# 커리어 시작
# =========================

if "club" not in st.session_state:
    st.subheader("새 감독 커리어 시작")
    chosen = st.selectbox("운영할 구단", list(CLUBS.keys()))

    st.write(
        f"리그: {CLUBS[chosen]['league']} · "
        f"초기 예산: {money(CLUBS[chosen]['budget'])}"
    )

    if st.button("커리어 시작 ⚽", type="primary"):
        init_state(chosen)
        st.rerun()

    st.stop()


# =========================
# 메인 화면
# =========================

club = st.session_state.club

st.header(f"🏟️ {club}")
st.caption(
    f"{st.session_state.season} 시즌 · "
    f"{CLUBS[club]['league']} · "
    f"{st.session_state.week - 1}/38 경기"
)

m1, m2, m3, m4 = st.columns(4)
m1.metric("이적 자금", money(st.session_state.budget))
m2.metric("선수단", f"{len(st.session_state.roster)}명")
m3.metric("팀 전력", f"{team_strength(st.session_state.roster)} OVR")
m4.metric("우승 트로피", f"{st.session_state.trophies}개")

tabs = st.tabs([
    "📋 대시보드",
    "👥 선수단",
    "🔁 이적시장",
    "🌱 유스",
    "🏆 리그 & 유럽",
    "📊 시즌 기록",
    "📜 구단 소식"
])


# =========================
# 대시보드
# =========================

with tabs[0]:
    left, right = st.columns(2)

    with left:
        st.subheader("전술 설정")

        st.selectbox(
            "포메이션",
            ["4-3-3", "4-4-2", "5-3-2"],
            key="formation"
        )

        st.selectbox(
            "팀 지침",
            ["균형", "공격", "수비"],
            key="training"
        )

        player_options = {
            f"{p['name']} · {p['pos']} · OVR {p['rating']}": p["id"]
            for p in st.session_state.roster
        }

        chosen_xi = st.multiselect(
            "선발 11명 선택",
            list(player_options.keys()),
            key="xi_picker",
            help="11명을 선택하지 않으면 능력치 상위 11명이 자동 출전합니다."
        )

        st.session_state.starting_xi = [
            player_options[x] for x in chosen_xi
        ]

        if st.button(
            "⚽ 리그 경기 진행",
            type="primary",
            use_container_width=True
        ):
            simulate_match()
            st.rerun()

        if st.button("📅 시즌 종료 및 다음 시즌"):
            end_season()
            st.rerun()

    with right:
        st.subheader("최근 경기")

        if st.session_state.last_match:
            c, gf, ga, opponent, result = st.session_state.last_match
            st.markdown(f"### {c} **{gf} : {ga}** {opponent}")
            st.write(result)
        else:
            st.write("아직 진행한 경기가 없습니다.")

        st.subheader("🏅 구단 발롱도르")
        st.write(st.session_state.ballondor)
        st.caption("시즌 종료 시 선수 기록을 기준으로 선정합니다.")

        st.subheader("⭐ 우리 구단 주요 선수")
        top_players = sorted(
            st.session_state.roster,
            key=lambda p: p["rating"],
            reverse=True
        )[:3]

        cols = st.columns(3)
        for col, player in zip(cols, top_players):
            with col:
                show_player_card(player)


# =========================
# 선수단
# =========================

with tabs[1]:
    st.subheader("1군 선수단")

    roster = sorted(
        st.session_state.roster,
        key=lambda p: (-p["rating"], p["age"])
    )

    show_images = st.checkbox("선수 사진 카드 표시", value=True)

    if show_images:
        for start in range(0, len(roster), 4):
            cols = st.columns(4)
            for col, player in zip(cols, roster[start:start + 4]):
                with col:
                    show_player_card(player)

    st.dataframe(
        [
            {
                "선수": p["name"],
                "포지션": p["pos"],
                "나이": p["age"],
                "능력치": p["rating"],
                "가치": money(p["value"]),
                "출전": p["apps"],
                "골": p["goals"],
                "도움": p["assists"],
                "평균 평점": round(
                    p["rating_sum"] / max(1, p["apps"]), 2
                ),
                "클린시트": p["clean_sheets"],
                "MOTM": p["motm"],
            }
            for p in roster
        ],
        hide_index=True,
        use_container_width=True
    )

    options = {
        f"{p['name']} · {p['pos']} · OVR {p['rating']}": p["id"]
        for p in st.session_state.roster
    }

    if options:
        selected = st.selectbox("판매할 선수", list(options.keys()))

        if st.button("선수 판매"):
            sell_player(options[selected])
            st.rerun()


# =========================
# 이적시장
# =========================

with tabs[2]:
    st.subheader("🔁 이적시장")

    search = st.text_input("선수 이름 검색")
    position = st.selectbox("포지션 필터", ["전체"] + POSITIONS)

    available = [
        p for p in st.session_state.market
        if search.lower() in p["name"].lower()
        and (position == "전체" or p["pos"] == position)
    ]

    available.sort(key=lambda p: p["rating"], reverse=True)
    st.caption(f"검색 결과: {len(available)}명")

    for p in available[:50]:
        c1, c2, c3, c4, c5 = st.columns([3, 1, 1, 1.4, 1.2])

        c1.write(f"**{p['name']}**")
        c2.write(p["pos"])
        c3.write(f"OVR {p['rating']}")

        fee = p["value"] * 1.15
        c4.write(money(fee))

        if c5.button("영입", key=f"buy_{p['id']}"):
            buy_player(p["id"])
            st.rerun()

        with st.expander(f"📷 {p['name']} 선수 정보"):
            show_player_card(p)


# =========================
# 유스 아카데미
# =========================

with tabs[3]:
    st.subheader("🌱 유스 아카데미")
    st.write("유스 발굴 비용: €1.0m")

    if st.button("유스 선수 발굴", type="primary"):
        sign_youth()
        st.rerun()

    if st.session_state.youth:
        st.dataframe(
            [
                {
                    "선수": p["name"],
                    "포지션": p["pos"],
                    "나이": p["age"],
                    "능력치": p["rating"],
                    "가치": money(p["value"]),
                }
                for p in st.session_state.youth
            ],
            hide_index=True,
            use_container_width=True
        )

        youth_options = {
            f"{p['name']} · OVR {p['rating']}": p["id"]
            for p in st.session_state.youth
        }

        selected_youth = st.selectbox(
            "1군으로 승격할 선수",
            list(youth_options.keys())
        )

        if st.button("1군 승격"):
            pid = youth_options[selected_youth]
            player = next(
                p for p in st.session_state.youth if p["id"] == pid
            )
            player["youth"] = True
            st.session_state.roster.append(player)
            st.session_state.youth = [
                p for p in st.session_state.youth if p["id"] != pid
            ]
            add_log(f"{player['name']} 1군 승격")
            st.rerun()
    else:
        st.info("아직 발굴한 유스 선수가 없습니다.")


# =========================
# 리그 및 챔피언스리그
# =========================

with tabs[4]:
    st.subheader("🏆 리그 순위")

    league = CLUBS[club]["league"]
    standings = [
        (name, data)
        for name, data in st.session_state.table.items()
        if CLUBS[name]["league"] == league
    ]

    standings.sort(
        key=lambda item: (
            item[1]["Pts"],
            item[1]["GF"] - item[1]["GA"],
            item[1]["GF"]
        ),
        reverse=True
    )

    st.dataframe(
        [
            {
                "순위": i + 1,
                "구단": name,
                "경기": t["P"],
                "승": t["W"],
                "무": t["D"],
                "패": t["L"],
                "득점": t["GF"],
                "실점": t["GA"],
                "득실차": t["GF"] - t["GA"],
                "승점": t["Pts"],
            }
            for i, (name, t) in enumerate(standings)
        ],
        hide_index=True,
        use_container_width=True
    )

    st.caption("게임 규칙: 각 리그 상위 2팀이 챔피언스리그에 진출합니다.")
    st.subheader("🌍 챔피언스리그")
    st.write(f"현재 상태: **{st.session_state.ucl_status}**")

    if st.button("유럽 대회 진행", type="primary"):
        play_ucl()
        st.rerun()


# =========================
# 시즌 기록
# =========================

with tabs[5]:
    st.subheader("📊 시즌 선수 기록")

    stats = sorted(
        st.session_state.roster,
        key=lambda p: (
            p["goals"] * 4 + p["assists"] * 3 + p["motm"] * 2
        ),
        reverse=True
    )

    st.dataframe(
        [
            {
                "선수": p["name"],
                "출전": p["apps"],
                "골": p["goals"],
                "도움": p["assists"],
                "평균 평점": round(
                    p["rating_sum"] / max(1, p["apps"]), 2
                ),
                "클린시트": p["clean_sheets"],
                "MOTM": p["motm"],
            }
            for p in stats
        ],
        hide_index=True,
        use_container_width=True
    )


# =========================
# 구단 소식 및 새 커리어
# =========================

with tabs[6]:
    st.subheader("📜 구단 소식")

    for message in st.session_state.log:
        st.write("• " + message)

    if st.button("🔄 새 커리어 시작"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()


st.divider()
st.caption(
    "Football Director · 팬 제작 축구 경영 게임 · 게임용 예시 데이터"
)

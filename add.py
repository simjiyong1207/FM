
import random
import streamlit as st

st.set_page_config(
    page_title="FOOTBALL DIRECTOR",
    page_icon="⚽",
    layout="wide"
)

CLUBS = {
    "Real Madrid": {"budget": 180, "rating": 88, "league": "La Liga"},
    "Barcelona": {"budget": 145, "rating": 86, "league": "La Liga"},
    "Manchester City": {"budget": 170, "rating": 88, "league": "Premier League"},
    "Arsenal": {"budget": 115, "rating": 84, "league": "Premier League"},
    "Liverpool": {"budget": 120, "rating": 85, "league": "Premier League"},
    "Bayern Munich": {"budget": 130, "rating": 86, "league": "Bundesliga"},
    "Paris Saint-Germain": {"budget": 150, "rating": 85, "league": "Ligue 1"},
    "Inter": {"budget": 90, "rating": 84, "league": "Serie A"},
}

# 선수 이름은 실제 선수에서 가져왔으며 능력치와 이적료는 게임용 예시입니다.
PLAYER_DATA = [
    ("Kylian Mbappe","ST",27,92,170,"Real Madrid"),
    ("Vinicius Junior","LW",26,91,150,"Real Madrid"),
    ("Jude Bellingham","CM",23,90,145,"Real Madrid"),
    ("Federico Valverde","CM",28,88,95,"Real Madrid"),
    ("Thibaut Courtois","GK",34,89,35,"Real Madrid"),
    ("Rodrygo","RW",25,86,80,"Real Madrid"),
    ("Lamine Yamal","RW",19,90,150,"Barcelona"),
    ("Pedri","CM",23,88,110,"Barcelona"),
    ("Gavi","CM",22,85,75,"Barcelona"),
    ("Raphinha","LW",29,87,75,"Barcelona"),
    ("Robert Lewandowski","ST",38,84,18,"Barcelona"),
    ("Frenkie de Jong","CM",29,86,55,"Barcelona"),
    ("Erling Haaland","ST",26,92,175,"Manchester City"),
    ("Phil Foden","AM",26,88,105,"Manchester City"),
    ("Rodri","DM",30,91,100,"Manchester City"),
    ("Ruben Dias","CB",29,87,65,"Manchester City"),
    ("Kevin De Bruyne","AM",35,86,20,"Manchester City"),
    ("Bukayo Saka","RW",25,89,120,"Arsenal"),
    ("Declan Rice","DM",27,88,105,"Arsenal"),
    ("Martin Odegaard","AM",27,87,85,"Arsenal"),
    ("William Saliba","CB",25,87,80,"Arsenal"),
    ("Gabriel Martinelli","LW",25,85,65,"Arsenal"),
    ("Mohamed Salah","RW",34,88,25,"Liverpool"),
    ("Virgil van Dijk","CB",35,86,18,"Liverpool"),
    ("Alexis Mac Allister","CM",27,86,75,"Liverpool"),
    ("Florian Wirtz","AM",23,89,120,"Liverpool"),
    ("Alisson Becker","GK",33,88,30,"Liverpool"),
    ("Harry Kane","ST",33,90,55,"Bayern Munich"),
    ("Jamal Musiala","AM",23,90,130,"Bayern Munich"),
    ("Michael Olise","RW",24,88,95,"Bayern Munich"),
    ("Joshua Kimmich","DM",31,87,40,"Bayern Munich"),
    ("Manuel Neuer","GK",40,82,3,"Bayern Munich"),
    ("Ousmane Dembele","RW",29,87,65,"Paris Saint-Germain"),
    ("Achraf Hakimi","RB",27,87,75,"Paris Saint-Germain"),
    ("Vitinha","CM",26,88,95,"Paris Saint-Germain"),
    ("Gianluigi Donnarumma","GK",27,88,55,"Paris Saint-Germain"),
    ("Lautaro Martinez","ST",29,88,100,"Inter"),
    ("Nicolo Barella","CM",29,87,85,"Inter"),
    ("Alessandro Bastoni","CB",27,87,80,"Inter"),
    ("Marcus Thuram","ST",29,85,55,"Inter"),
    ("Cole Palmer","AM",24,89,125,"Chelsea"),
    ("Enzo Fernandez","CM",25,86,80,"Chelsea"),
    ("Son Heung-min","LW",34,84,15,"Tottenham"),
    ("Bruno Fernandes","AM",32,87,55,"Manchester United"),
    ("Julián Álvarez","ST",26,87,90,"Atletico Madrid"),
    ("Antoine Griezmann","AM",35,84,12,"Atletico Madrid"),
    ("Victor Osimhen","ST",27,88,100,"Galatasaray"),
    ("Khvicha Kvaratskhelia","LW",25,88,100,"Paris Saint-Germain"),
    ("Cristiano Ronaldo", "LW", 28, 95, 120, "Manchester United Legends"),
    ("Wayne Rooney", "ST", 27, 93, 45, "Manchester United Legends"),
    ("David Beckham", "RM", 27, 92, 35, "Manchester United Legends"),
    ("Paul Scholes", "CM", 29, 92, 30, "Manchester United Legends"),
    ("Ryan Giggs", "LW", 27, 91, 25, "Manchester United Legends"),
    ("Eric Cantona", "ST", 28, 91, 25, "Manchester United Legends"),
    ("Roy Keane", "CM", 30, 91, 28, "Manchester United Legends"),
    ("Rio Ferdinand", "CB", 28, 90, 30, "Manchester United Legends"),
    ("Nemanja Vidic", "CB", 28, 90, 25, "Manchester United Legends"),
    ("Peter Schmeichel", "GK", 29, 91, 18, "Manchester United Legends"),
    ("Ruud van Nistelrooy", "ST", 27, 92, 35, "Manchester United Legends"),
    ("Robin van Persie", "ST", 29, 91, 30, "Manchester United Legends"),
    ("Patrice Evra", "LB", 28, 88, 18, "Manchester United Legends"),
    ("Gary Neville", "RB", 29, 87, 15, "Manchester United Legends"),
    ("Ole Gunnar Solskjaer", "ST", 28, 88, 18, "Manchester United Legends"),
    ("Edwin van der Sar", "GK", 35, 89, 12, "Manchester United Legends"),
    ("Michael Carrick", "CM", 29, 87, 18, "Manchester United Legends"),
    ("Andy Cole", "ST", 27, 89, 20, "Manchester United Legends"),
    ("Dwight Yorke", "ST", 27, 89, 20, "Manchester United Legends"),
    ("Jaap Stam", "CB", 27, 90, 22, "Manchester United Legends"),
]

POSITIONS = ["GK", "CB", "LB", "RB", "DM", "CM", "AM", "LW", "RW", "ST"]


def money(value):
    return f"€{value:.1f}m"


def player_from_data(row, pid):
    name, pos, age, rating, value, club = row
    return {
        "id": pid, "name": name, "pos": pos, "age": age,
        "rating": rating, "value": float(value),
        "club": club, "youth": False
    }


def new_season_table():
    return {
        club: {"P": 0, "W": 0, "D": 0, "L": 0,
               "GF": 0, "GA": 0, "Pts": 0}
        for club in CLUBS
    }


def init_game(club):
    roster = []
    pid = 1

    for row in PLAYER_DATA:
        if row[5] == club:
            roster.append(player_from_data(row, pid))
            pid += 1

    while len(roster) < 18:
        pos = random.choice(POSITIONS)
        age = random.randint(20, 32)
        rating = random.randint(72, 82)
        name = random.choice([
            "Alex Morgan", "Leo Silva", "Daniel Costa",
            "Noah Martin", "Sam Taylor", "Marco Rossi",
            "Min-jae Park", "Ethan Cole", "Lucas Meyer",
            "Kai Tanaka"
        ])
        roster.append({
            "id": pid, "name": f"{name} {pid}", "pos": pos,
            "age": age, "rating": rating,
            "value": round(max(1, (rating - 60) ** 2 / 8), 1),
            "club": club, "youth": False
        })
        pid += 1

    market = []
    for row in PLAYER_DATA:
        if row[5] != club:
            market.append(player_from_data(row, pid))
            pid += 1

    for n in range(18):
        pos = random.choice(POSITIONS)
        age = random.randint(19, 31)
        rating = random.randint(68, 83)
        value = round(max(1, (rating - 58) ** 2 / 9), 1)
        name = random.choice([
            "A. Kim", "J. Silva", "M. Novak",
            "T. Ito", "D. Brown", "L. Costa"
        ])
        market.append({
            "id": pid, "name": f"{name} {n + 1}", "pos": pos,
            "age": age, "rating": rating, "value": value,
            "club": "Free Agent", "youth": False
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
    st.session_state.table = new_season_table()
    st.session_state.log = [f"{club} 구단의 감독이 되었습니다!"]
    st.session_state.ucl_status = "아직 출전하지 않음"
    st.session_state.ucl_played = False
    st.session_state.trophies = 0
    st.session_state.last_match = None
    st.session_state.formation = "4-3-3"
    st.session_state.training = "Balanced"


def add_log(message):
    st.session_state.log.insert(0, message)
    st.session_state.log = st.session_state.log[:15]


def squad_strength(roster):
    if not roster:
        return 50
    ratings = sorted(
        [p["rating"] for p in roster],
        reverse=True
    )[:11]
    return round(sum(ratings) / len(ratings), 1)


def play_match():
    if st.session_state.week > 38:
        st.warning("시즌이 끝났습니다. 다음 시즌을 시작하세요.")
        return

    club = st.session_state.club
    strength = squad_strength(st.session_state.roster)
    opponent = random.choice([c for c in CLUBS if c != club])
    opp_strength = CLUBS[opponent]["rating"] + random.uniform(-2, 2)

    tactic_bonus = {
        "Attacking": 1.5,
        "Balanced": 0,
        "Defensive": -0.5
    }.get(st.session_state.training, 0)

    formation_bonus = {
        "4-3-3": 0.7,
        "4-4-2": 0.2,
        "5-3-2": -0.2
    }.get(st.session_state.formation, 0)

    expected = max(
        0.25,
        min(3.2, 1.25 + (strength - opp_strength
                          + tactic_bonus + formation_bonus) / 12)
    )
    opp_expected = max(
        0.2,
        min(3.0, 1.15 + (opp_strength - strength
                         - tactic_bonus - formation_bonus) / 13)
    )

    goals = min(6, max(0, round(random.gauss(expected, 0.9))))
    conceded = min(6, max(0, round(random.gauss(opp_expected, 0.9))))

    table = st.session_state.table[club]
    table["P"] += 1
    table["GF"] += goals
    table["GA"] += conceded

    if goals > conceded:
        table["W"] += 1
        table["Pts"] += 3
        outcome = "승리 🎉"
    elif goals == conceded:
        table["D"] += 1
        table["Pts"] += 1
        outcome = "무승부"
    else:
        table["L"] += 1
        outcome = "패배"

    add_log(
        f"{st.session_state.week}라운드: "
        f"{club} {goals}-{conceded} {opponent} ({outcome})"
    )

    others = [c for c in CLUBS if c != club]
    random.shuffle(others)

    for i in range(0, len(others) - 1, 2):
        team_a, team_b = others[i], others[i + 1]
        score_a, score_b = random.randint(0, 3), random.randint(0, 3)

        for team, scored, allowed in [
            (team_a, score_a, score_b),
            (team_b, score_b, score_a)
        ]:
            row = st.session_state.table[team]
            row["P"] += 1
            row["GF"] += scored
            row["GA"] += allowed

            if scored > allowed:
                row["W"] += 1
                row["Pts"] += 3
            elif scored == allowed:
                row["D"] += 1
                row["Pts"] += 1
            else:
                row["L"] += 1

    st.session_state.last_match = (
        club, goals, conceded, opponent, outcome
    )
    st.session_state.week += 1
    st.session_state.budget += 2.5

    if random.random() < 0.12 and st.session_state.roster:
        player = random.choice(st.session_state.roster)
        add_log(f"{player['name']} 선수가 피로 누적 상태입니다.")


def end_season():
    club = st.session_state.club
    if st.session_state.table[club]["P"] == 0:
        st.warning("먼저 리그 경기를 진행하세요.")
        return

    ranking = sorted(
        st.session_state.table.items(),
        key=lambda item: (
            item[1]["Pts"],
            item[1]["GF"] - item[1]["GA"],
            item[1]["GF"]
        ),
        reverse=True
    )
    place = [team for team, _ in ranking].index(club) + 1
    prize = {1: 60, 2: 40, 3: 28, 4: 20}.get(place, 8)
    st.session_state.budget += prize

    if place == 1:
        st.session_state.trophies += 1
        add_log(f"🏆 리그 우승! 상금 {money(prize)}")
    else:
        add_log(f"시즌 종료: 리그 {place}위, 상금 {money(prize)}")

    st.session_state.season += 1
    st.session_state.week = 1
    st.session_state.table = new_season_table()
    st.session_state.ucl_played = False
    st.session_state.ucl_status = "아직 출전하지 않음"

    for player in st.session_state.roster:
        player["age"] += 1
        if player["age"] <= 23 and random.random() < 0.6:
            player["rating"] = min(95, player["rating"] + 1)
        elif player["age"] >= 32 and random.random() < 0.45:
            player["rating"] = max(55, player["rating"] - 1)

    add_log(f"{st.session_state.season} 시즌이 시작되었습니다.")


def sign_youth():
    pid = st.session_state.next_pid
    pos = random.choice(POSITIONS)
    age = random.randint(15, 18)
    rating = random.randint(55, 72)

    player = {
        "id": pid,
        "name": random.choice([
            "Min-jun Lee", "Ji-ho Park", "Alex Kim",
            "Leo Santos", "Noah Chen", "Daniel Ito"
        ]) + f" {pid}",
        "pos": pos,
        "age": age,
        "rating": rating,
        "value": round(random.uniform(0.1, 2.5), 1),
        "club": st.session_state.club,
        "youth": True
    }

    st.session_state.next_pid += 1
    st.session_state.youth.append(player)
    st.session_state.budget -= 1
    add_log(
        f"🌱 유스 영입: {player['name']} "
        f"({pos}, {age}세, OVR {rating})"
    )


def buy_player(pid):
    player = next(
        (p for p in st.session_state.market if p["id"] == pid),
        None
    )
    if player is None:
        return

    fee = player["value"] * 1.15

    if st.session_state.budget < fee:
        st.error("이적 자금이 부족합니다.")
        return

    if len(st.session_state.roster) >= 30:
        st.error("선수단은 최대 30명까지 보유할 수 있습니다.")
        return

    st.session_state.budget -= fee
    player["club"] = st.session_state.club
    st.session_state.roster.append(player)
    st.session_state.market = [
        p for p in st.session_state.market if p["id"] != pid
    ]
    add_log(f"✍️ {player['name']} 영입 완료: {money(fee)}")


def sell_player(pid):
    player = next(
        (p for p in st.session_state.roster if p["id"] == pid),
        None
    )
    if player is None:
        return

    fee = player["value"] * 0.85
    st.session_state.budget += fee
    st.session_state.roster = [
        p for p in st.session_state.roster if p["id"] != pid
    ]
    player["club"] = "Free Agent"
    st.session_state.market.append(player)
    add_log(f"↗️ {player['name']} 판매 완료: {money(fee)}")


def play_ucl():
    if st.session_state.ucl_played:
        st.warning("이번 시즌 유럽 대회를 이미 진행했습니다.")
        return

    club = st.session_state.club
    ranking = sorted(
        st.session_state.table.items(),
        key=lambda item: (
            item[1]["Pts"],
            item[1]["GF"] - item[1]["GA"]
        ),
        reverse=True
    )
    place = [team for team, _ in ranking].index(club) + 1

    if st.session_state.week > 1 and place > 4:
        st.warning("유럽 대회에는 리그 상위 4팀만 참가할 수 있습니다.")
        return

    strength = squad_strength(st.session_state.roster)
    opponents = [c for c in CLUBS if c != club]
    results = []

    for round_name in ["8강", "4강", "결승"]:
        opponent = random.choice(opponents)
        opponent_rating = CLUBS[opponent]["rating"]

        goals = max(
            0, round(random.gauss(
                1.4 + (strength - opponent_rating) / 13, 1
            ))
        )
        conceded = max(
            0, round(random.gauss(
                1.2 + (opponent_rating - strength) / 14, 1
            ))
        )

        if goals == conceded:
            goals += random.choice([0, 1])

        results.append(
            f"{round_name}: {club} {goals}-{conceded} {opponent}"
        )

        if goals < conceded:
            st.session_state.ucl_status = f"{round_name} 탈락"
            break
    else:
        st.session_state.ucl_status = "우승 🏆"
        st.session_state.trophies += 1
        st.session_state.budget += 45

    st.session_state.ucl_played = True
    add_log("🌍 유럽 대회: " + " / ".join(results))

    if st.session_state.ucl_status == "우승 🏆":
        add_log("🏆 유럽 대회 우승! €45m 상금 획득")


# 화면 디자인
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
st.caption("구단 운영 · 이적시장 · 유스 · 리그 · 유럽 챔피언스 컵")
st.info(
    "팬 제작 구단 운영 게임입니다. "
    "선수의 능력치와 이적료는 게임용 예시이며 실시간 데이터가 아닙니다."
)

if "club" not in st.session_state:
    st.subheader("새 감독 커리어 시작")
    chosen = st.selectbox("운영할 구단 선택", list(CLUBS.keys()))
    st.write(
        f"초기 이적 자금: {money(CLUBS[chosen]['budget'])} "
        f"· 리그: {CLUBS[chosen]['league']}"
    )

    if st.button("커리어 시작 ⚽", type="primary"):
        init_state(chosen)
        st.rerun()

    st.stop()

club = st.session_state.club

st.markdown(f"## 🏟️ {club}")
st.caption(
    f"{st.session_state.season} 시즌 · "
    f"{CLUBS[club]['league']} · "
    f"{st.session_state.week - 1}/38 경기 진행"
)

m1, m2, m3, m4 = st.columns(4)
m1.metric("이적 자금", money(st.session_state.budget))
m2.metric("선수단", f"{len(st.session_state.roster)}명")
m3.metric("팀 전력", f"{squad_strength(st.session_state.roster)} OVR")
m4.metric("우승 트로피", f"{st.session_state.trophies}개")

tabs = st.tabs([
    "📋 대시보드", "👥 선수단", "🔁 이적시장",
    "🌱 유스", "🏆 리그 & 유럽 대회", "📜 구단 소식"
])

with tabs[0]:
    left, right = st.columns(2)

    with left:
        st.subheader("다음 경기")

        st.selectbox(
            "전술", ["4-3-3", "4-4-2", "5-3-2"],
            key="formation"
        )
        st.selectbox(
            "팀 지침",
            ["Balanced", "Attacking", "Defensive"],
            format_func=lambda x: {
                "Balanced": "균형",
                "Attacking": "공격",
                "Defensive": "수비"
            }[x],
            key="training"
        )

        if st.button("⚽ 리그 경기 진행", type="primary",
                     use_container_width=True):
            play_match()
            st.rerun()

        if st.button("📅 시즌 종료 및 다음 시즌",
                     use_container_width=True):
            end_season()
            st.rerun()

    with right:
        st.subheader("최근 경기")

        if st.session_state.last_match:
            c, gf, ga, opponent, outcome = st.session_state.last_match
            st.markdown(f"### {c}  **{gf} : {ga}**  {opponent}")
            st.write(outcome)
        else:
            st.write("아직 진행한 경기가 없습니다.")

        st.subheader("운영 팁")
        st.write("- 유망주를 발굴하고 성장시키세요.")
        st.write("- 선수를 영입하거나 판매해 팀을 강화하세요.")
        st.write("- 리그에서 좋은 성적을 거두어 유럽 대회에 도전하세요.")

with tabs[1]:
    st.subheader("1군 선수단")

    if st.session_state.roster:
        roster_sorted = sorted(
            st.session_state.roster,
            key=lambda p: (-p["rating"], p["age"])
        )

        st.dataframe(
            [{
                "선수": p["name"],
                "포지션": p["pos"],
                "나이": p["age"],
                "능력치": p["rating"],
                "게임 가치": money(p["value"]),
                "유형": "유스 승격" if p["youth"] else "일반"
            } for p in roster_sorted],
            use_container_width=True,
            hide_index=True
        )

        options = {
            f"{p['name']} · {p['pos']} · OVR {p['rating']}": p["id"]
            for p in st.session_state.roster
        }
        selected = st.selectbox(
            "판매할 선수 선택", list(options.keys()),
            key="sell_select"
        )

        if st.button("선수 판매", key="sell_button"):
            sell_player(options[selected])
            st.rerun()
    else:
        st.warning("선수단이 비어 있습니다.")

with tabs[2]:
    st.subheader("이적시장")
    st.write("선수의 능력치와 게임 가치에 따라 이적료가 계산됩니다.")

    search = st.text_input("선수 이름 검색")
    position = st.selectbox("포지션 필터", ["전체"] + POSITIONS)

    available = [
        p for p in st.session_state.market
        if search.lower() in p["name"].lower()
        and (position == "전체" or p["pos"] == position)
    ]
    available.sort(key=lambda p: p["rating"], reverse=True)

    st.caption(f"검색 결과: {len(available)}명")

    if not available:
        st.info("조건에 맞는 선수가 없습니다.")
    else:
        for p in available[:35]:
            c1, c2, c3, c4, c5 = st.columns([3, 1, 1, 1.4, 1.2])
            c1.write(f"**{p['name']}**")
            c2.write(p["pos"])
            c3.write(f"OVR {p['rating']}")
            fee = p["value"] * 1.15
            c4.write(money(fee))

            if c5.button("영입", key=f"buy_{p['id']}"):
                buy_player(p["id"])
                st.rerun()

with tabs[3]:
    st.subheader("🌱 유스 아카데미")
    st.write("유스 선수를 발굴해 젊은 선수를 확보하세요.")
    st.write("유스 발굴 비용: €1.0m")

    if st.button("유스 선수 발굴", type="primary"):
        if st.session_state.budget >= 1:
            sign_youth()
            st.rerun()
        else:
            st.error("유스 발굴 비용이 부족합니다.")

    if st.session_state.youth:
        st.dataframe(
            [{
                "선수": p["name"],
                "포지션": p["pos"],
                "나이": p["age"],
                "능력치": p["rating"],
                "가치": money(p["value"])
            } for p in st.session_state.youth],
            hide_index=True,
            use_container_width=True
        )

        youth_options = {
            f"{p['name']} · OVR {p['rating']}": p["id"]
            for p in st.session_state.youth
        }
        selected_youth = st.selectbox(
            "1군으로 승격할 선수", list(youth_options.keys())
        )

        if st.button("1군 승격"):
            pid = youth_options[selected_youth]
            player = next(
                p for p in st.session_state.youth if p["id"] == pid
            )
            player["youth"] = True
            st.session_state.roster.append(player)
            st.session_state.youth = [
                y for y in st.session_state.youth if y["id"] != pid
            ]
            add_log(f"⬆️ {player['name']} 선수가 1군으로 승격했습니다.")
            st.rerun()
    else:
        st.info("아직 발굴한 유스 선수가 없습니다.")

with tabs[4]:
    st.subheader("🏆 리그 순위")

    table_rows = []
    for name, row in st.session_state.table.items():
        table_rows.append({
            "구단": name,
            "경기": row["P"],
            "승": row["W"],
            "무": row["D"],
            "패": row["L"],
            "득점": row["GF"],
            "실점": row["GA"],
            "득실차": row["GF"] - row["GA"],
            "승점": row["Pts"]
        })

    table_rows.sort(
        key=lambda x: (x["승점"], x["득실차"], x["득점"]),
        reverse=True
    )
    table_rows = [
        {"순위": i + 1, **row}
        for i, row in enumerate(table_rows)
    ]

    st.dataframe(table_rows, hide_index=True, use_container_width=True)
    st.caption("리그 상위 4팀은 유럽 챔피언스 컵 출전 자격을 얻습니다.")

    st.divider()
    st.subheader("🌍 European Champions Cup")
    st.write("8강 → 4강 → 결승으로 진행되는 간단한 토너먼트입니다.")
    st.write(f"현재 상태: **{st.session_state.ucl_status}**")

    if st.button("유럽 대회 진행", type="primary"):
        play_ucl()
        st.rerun()

with tabs[5]:
    st.subheader("📜 구단 소식")

    for item in st.session_state.log:
        st.write("• " + item)

    if st.button("🔄 새 커리어 시작"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()

st.divider()
st.caption(
    "Football Director · 팬 제작 구단 운영 게임 · "
    "게임용 예시 데이터"
)

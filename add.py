
import random
import requests
import streamlit as st
from streamlit_sortables import sort_items

st.set_page_config(
    page_title="FOOTBALL DIRECTOR",
    page_icon="⚽",
    layout="wide"
)

# -------------------------
# 디자인
# -------------------------
st.markdown("""
<style>
.stApp {
    background: #08130f;
    color: #f2f7f4;
}
.block-container {
    max-width: 1450px;
    padding-top: 1.5rem;
}
div[data-testid="stMetric"] {
    background: #12251c;
    border: 1px solid #28523b;
    padding: 16px;
    border-radius: 15px;
}
div[data-testid="stTabs"] button {
    font-weight: 700;
}
.player-card {
    background: #14251d;
    border: 1px solid #294a37;
    border-radius: 14px;
    padding: 12px;
    text-align: center;
}
.pitch {
    background: linear-gradient(90deg, #17613c, #20764a);
    border: 3px solid #b8e5c6;
    border-radius: 15px;
    padding: 15px;
    color: white;
    text-align: center;
}
.small-note {
    color: #a8c4b2;
    font-size: 13px;
}
</style>
""", unsafe_allow_html=True)

st.title("⚽ FOOTBALL DIRECTOR")
st.caption("BUILD YOUR CLUB · SELECT YOUR XI · WIN TROPHIES")

# -------------------------
# 구단 데이터
# -------------------------
CLUBS = {
    "Manchester United": ("Premier League", 125, 83),
    "Manchester City": ("Premier League", 170, 88),
    "Arsenal": ("Premier League", 115, 84),
    "Liverpool": ("Premier League", 120, 85),
    "Chelsea": ("Premier League", 105, 82),
    "Tottenham": ("Premier League", 90, 81),
    "Newcastle United": ("Premier League", 95, 81),
    "Aston Villa": ("Premier League", 75, 80),
    "West Ham": ("Premier League", 65, 78),
    "Everton": ("Premier League", 45, 74),
    "Real Madrid": ("La Liga", 180, 88),
    "Barcelona": ("La Liga", 145, 86),
    "Atletico Madrid": ("La Liga", 95, 84),
    "Athletic Bilbao": ("La Liga", 55, 79),
    "Real Sociedad": ("La Liga", 55, 79),
    "Sevilla": ("La Liga", 50, 77),
    "Valencia": ("La Liga", 45, 76),
    "Villarreal": ("La Liga", 60, 79),
    "Real Betis": ("La Liga", 50, 77),
    "Girona": ("La Liga", 40, 75),
}

# 이름, 포지션, 나이, 능력치, 원래 소속
RAW_PLAYERS = [
    ("Lionel Messi", "RW", 39, 100, "Barcelona"),
    ("Cristiano Ronaldo", "ST", 41, 97, "Real Madrid"),
    ("Andres Iniesta", "CM", 42, 97, "Barcelona"),
    ("Xavi", "CM", 46, 97, "Barcelona"),
    ("Ronaldinho", "LW", 46, 97, "Barcelona"),
    ("Luis Suarez", "ST", 39, 95, "Barcelona"),
    ("Lamine Yamal", "RW", 19, 91, "Barcelona"),
    ("Pedri", "CM", 23, 89, "Barcelona"),
    ("Robert Lewandowski", "ST", 38, 86, "Barcelona"),
    ("Zinedine Zidane", "AM", 54, 98, "Real Madrid"),
    ("Iker Casillas", "GK", 45, 95, "Real Madrid"),
    ("Sergio Ramos", "CB", 40, 95, "Real Madrid"),
    ("Luka Modric", "CM", 41, 94, "Real Madrid"),
    ("Kylian Mbappe", "ST", 27, 94, "Real Madrid"),
    ("Vinicius Junior", "LW", 26, 92, "Real Madrid"),
    ("Jude Bellingham", "CM", 23, 91, "Real Madrid"),
    ("Thierry Henry", "ST", 49, 97, "Arsenal"),
    ("Dennis Bergkamp", "AM", 57, 95, "Arsenal"),
    ("Patrick Vieira", "DM", 50, 94, "Arsenal"),
    ("Bukayo Saka", "RW", 25, 89, "Arsenal"),
    ("David Seaman", "GK", 63, 91, "Arsenal"),
    ("Wayne Rooney", "ST", 41, 94, "Manchester United"),
    ("Paul Scholes", "CM", 51, 94, "Manchester United"),
    ("David Beckham", "RW", 51, 93, "Manchester United"),
    ("Rio Ferdinand", "CB", 47, 92, "Manchester United"),
    ("Bruno Fernandes", "AM", 32, 87, "Manchester United"),
    ("Erling Haaland", "ST", 26, 93, "Manchester City"),
    ("Kevin De Bruyne", "AM", 35, 90, "Manchester City"),
    ("Rodri", "DM", 30, 92, "Manchester City"),
    ("Phil Foden", "LW", 26, 89, "Manchester City"),
    ("Sergio Aguero", "ST", 38, 94, "Manchester City"),
    ("Steven Gerrard", "CM", 46, 96, "Liverpool"),
    ("Mohamed Salah", "RW", 34, 91, "Liverpool"),
    ("Virgil van Dijk", "CB", 35, 89, "Liverpool"),
    ("Alisson Becker", "GK", 33, 89, "Liverpool"),
    ("Kenny Dalglish", "ST", 75, 96, "Liverpool"),
    ("John Terry", "CB", 46, 95, "Chelsea"),
    ("Frank Lampard", "CM", 48, 95, "Chelsea"),
    ("Eden Hazard", "LW", 35, 94, "Chelsea"),
    ("Cole Palmer", "AM", 24, 89, "Chelsea"),
    ("Harry Kane", "ST", 33, 95, "Tottenham"),
    ("Son Heung-min", "LW", 34, 89, "Tottenham"),
    ("Gareth Bale", "RW", 37, 94, "Tottenham"),
    ("Alan Shearer", "ST", 56, 96, "Newcastle United"),
    ("Paul McGrath", "CB", 67, 92, "Aston Villa"),
    ("Bobby Moore", "CB", 85, 97, "West Ham"),
    ("Dixie Dean", "ST", 123, 97, "Everton"),
    ("Diego Godin", "CB", 40, 93, "Atletico Madrid"),
    ("Antoine Griezmann", "AM", 35, 90, "Atletico Madrid"),
    ("Nico Williams", "LW", 24, 88, "Athletic Bilbao"),
    ("David Silva", "AM", 40, 92, "Real Sociedad"),
    ("Jesus Navas", "RB", 41, 88, "Sevilla"),
    ("David Villa", "ST", 45, 94, "Valencia"),
    ("Juan Roman Riquelme", "AM", 48, 94, "Villarreal"),
    ("Isco", "AM", 34, 88, "Real Betis"),
    ("Daley Blind", "CB", 36, 83, "Girona"),
]

POSITIONS = ["GK", "CB", "LB", "RB", "DM", "CM", "AM", "LW", "RW", "ST"]

FORMATIONS = {
    "4-3-3": [
        ["GK"],
        ["LB", "CB", "CB", "RB"],
        ["CM", "DM", "CM"],
        ["LW", "ST", "RW"],
    ],
    "4-4-2": [
        ["GK"],
        ["LB", "CB", "CB", "RB"],
        ["LM", "CM", "CM", "RM"],
        ["ST", "ST"],
    ],
    "4-2-3-1": [
        ["GK"],
        ["LB", "CB", "CB", "RB"],
        ["DM", "DM"],
        ["LW", "AM", "RW"],
        ["ST"],
    ],
    "3-5-2": [
        ["GK"],
        ["CB", "CB", "CB"],
        ["LM", "CM", "DM", "CM", "RM"],
        ["ST", "ST"],
    ],
}

def player_price(rating, age):
    price = max(0.5, (rating - 50) ** 2 * 0.12)
    if age <= 21:
        price *= 1.5
    elif age <= 24:
        price *= 1.25
    if age >= 30:
        price *= max(0.35, 1 - (age - 29) * 0.08)
    return round(price, 1)

def make_player(name, pos, age, rating, club, pid):
    return {
        "id": pid,
        "name": name,
        "pos": pos,
        "age": age,
        "rating": rating,
        "value": player_price(rating, age),
        "club": club,
        "goals": 0,
        "apps": 0,
    }

@st.cache_data(ttl=86400, show_spinner=False)
def get_face(name):
    try:
        url = (
            "https://en.wikipedia.org/api/rest_v1/page/summary/"
            + requests.utils.quote(name.replace(" ", "_"))
        )
        response = requests.get(
            url, timeout=4,
            headers={"User-Agent": "FootballDirector/1.0"}
        )
        if response.ok:
            data = response.json()
            return data.get("thumbnail", {}).get("source")
    except Exception:
        pass
    return None

def player_avatar(player, size=66):
    url = get_face(player["name"])
    if url:
        st.markdown(
            f"""<div style="text-align:center">
            <img src="{url}" width="{size}" height="{size}"
            style="border-radius:50%;object-fit:cover;
            border:3px solid #67d69b;">
            </div>""",
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            f"""<div style="margin:auto;width:{size}px;height:{size}px;
            border-radius:50%;background:#244532;display:flex;
            align-items:center;justify-content:center;
            font-size:28px;">⚽</div>""",
            unsafe_allow_html=True
        )

def money(value):
    return f"€{value:.1f}m"

def make_squad(club):
    squad = []
    pid = 1
    for name, pos, age, rating, team in RAW_PLAYERS:
        if team == club:
            squad.append(make_player(name, pos, age, rating, club, pid))
            pid += 1

    # 구단별 선수가 부족하면 가상 선수로 보충
    while len(squad) < 18:
        pos = random.choice(POSITIONS)
        rating = random.randint(64, 79)
        age = random.randint(17, 30)
        name = random.choice([
            "Alex Kim", "Min-jae Park", "Leo Silva",
            "Daniel Costa", "Noah Martin", "Kai Tanaka",
            "Marco Rossi", "Ethan Cole"
        ])
        squad.append(
            make_player(f"{name} {pid}", pos, age, rating, club, pid)
        )
        pid += 1

    market = []
    for name, pos, age, rating, team in RAW_PLAYERS:
        if team != club:
            market.append(make_player(name, pos, age, rating, team, pid))
            pid += 1

    for _ in range(25):
        pos = random.choice(POSITIONS)
        rating = random.randint(60, 84)
        age = random.randint(17, 30)
        market.append(
            make_player(
                f"{random.choice(['A. Kim','J. Silva','M. Novak','T. Ito'])} {pid}",
                pos, age, rating, "Free Agent", pid
            )
        )
        pid += 1

    return squad, market, pid

def init_career(club):
    squad, market, pid = make_squad(club)
    st.session_state.club = club
    st.session_state.budget = float(CLUBS[club][1])
    st.session_state.squad = squad
    st.session_state.market = market
    st.session_state.pid = pid
    st.session_state.formation = "4-3-3"
    st.session_state.week = 1
    st.session_state.points = 0
    st.session_state.wins = 0
    st.session_state.draws = 0
    st.session_state.losses = 0
    st.session_state.log = [f"{club} 감독 커리어 시작!"]
    st.session_state.season = 2026
    st.session_state.youth = []

def team_strength(squad):
    best = sorted(squad, key=lambda p: p["rating"], reverse=True)[:11]
    return round(sum(p["rating"] for p in best) / max(1, len(best)), 1)

# -------------------------
# 새 커리어
# -------------------------
if "club" not in st.session_state:
    st.subheader("새로운 감독 커리어")
    chosen = st.selectbox("구단 선택", list(CLUBS.keys()))
    league, budget, rating = CLUBS[chosen]

    st.markdown(f"### {chosen}")
    a, b, c = st.columns(3)
    a.metric("리그", league)
    b.metric("초기 예산", money(budget))
    c.metric("팀 평점", rating)

    if st.button("커리어 시작", type="primary", use_container_width=True):
        init_career(chosen)
        st.rerun()
    st.stop()

club = st.session_state.club
squad = st.session_state.squad

# -------------------------
# 상단 대시보드
# -------------------------
st.markdown(f"## 🏟️ {club}")
st.caption(
    f"{CLUBS[club][0]} · {st.session_state.season} 시즌 · "
    f"{st.session_state.week - 1}/38 경기"
)

m1, m2, m3, m4 = st.columns(4)
m1.metric("이적 예산", money(st.session_state.budget))
m2.metric("선수단", f"{len(squad)}명")
m3.metric("팀 전력", f"{team_strength(squad)} OVR")
m4.metric("리그 승점", st.session_state.points)

tabs = st.tabs([
    "전술 보드", "선수단", "이적시장", "경기", "유스 & 기록"
])

# -------------------------
# 전술 보드
# -------------------------
with tabs[0]:
    st.subheader("🧠 선발 라인업")
    st.caption(
        "아래 컨테이너 사이에서 선수 이름을 드래그해 옮겨 봐. "
        "각 줄은 포메이션의 골키퍼·수비·미드필더·공격수 구역이야."
    )

    formation = st.selectbox(
        "포메이션",
        list(FORMATIONS.keys()),
        index=list(FORMATIONS.keys()).index(st.session_state.formation),
        key="formation_choice"
    )
    st.session_state.formation = formation
    rows = FORMATIONS[formation]

    if "lineup_ids" not in st.session_state:
        st.session_state.lineup_ids = [
            p["id"] for p in sorted(
                squad, key=lambda x: x["rating"], reverse=True
            )[:11]
        ]

    by_id = {p["id"]: p for p in squad}
    lineup_ids = [
        pid for pid in st.session_state.lineup_ids if pid in by_id
    ]
    bench_ids = [p["id"] for p in squad if p["id"] not in lineup_ids]

    # 슬롯 수를 포메이션에 맞춰 계산
    total_slots = sum(len(line) for line in rows)
    lineup_ids = lineup_ids[:total_slots]
    while len(lineup_ids) < total_slots and bench_ids:
        lineup_ids.append(bench_ids.pop(0))

    labels = []
    cursor = 0
    for row in rows:
        row_ids = lineup_ids[cursor:cursor + len(row)]
        cursor += len(row)
        labels.append([
            f"{by_id[pid]['name']} | {by_id[pid]['pos']} | {by_id[pid]['rating']}"
            for pid in row_ids
        ])

    # 나머지 선수는 대기석 컨테이너로
    bench_labels = [
        f"{by_id[pid]['name']} | {by_id[pid]['pos']} | {by_id[pid]['rating']}"
        for pid in bench_ids
    ]

    headers = []
    if len(rows) == 4:
        headers = ["골키퍼", "수비수", "미드필더", "공격수"]
    elif len(rows) == 5:
        headers = ["골키퍼", "수비수", "수비형 미드필더", "공격형 미드필더", "공격수"]

    containers = [
        {"header": headers[i], "items": labels[i]}
        for i in range(len(labels))
    ]
    containers.append({"header": "선수 대기석", "items": bench_labels})

    custom_css = """
    .sortable-component {
        background-color: #10271b;
        border: 1px solid #3c7652;
        border-radius: 12px;
        padding: 8px;
    }
    .sortable-container {
        background-color: #16472e;
        border-radius: 10px;
        margin: 6px;
    }
    .sortable-container-header {
        color: white;
        font-weight: bold;
        background-color: #21653e;
        padding: 8px;
    }
    .sortable-container-body {
        min-height: 55px;
    }
    .sortable-item {
        color: white;
        background-color: #28764b;
        border: 1px solid #70c992;
        border-radius: 8px;
        font-weight: bold;
        margin: 5px;
    }
    """

    sorted_containers = sort_items(
        containers,
        multi_containers=True,
        custom_style=custom_css,
        key=f"formation_board_{formation}"
    )

    if sorted_containers:
        new_lineup = []
        new_bench = []
        for i, container in enumerate(sorted_containers):
            names = container.get("items", [])
            for item in names:
                name = item.split(" | ")[0]
                player = next(
                    (p for p in squad if p["name"] == name),
                    None
                )
                if player:
                    if i < len(rows):
                        new_lineup.append(player["id"])
                    else:
                        new_bench.append(player["id"])

        if new_lineup:
            st.session_state.lineup_ids = new_lineup

    st.info(
        "현재 Streamlit 드래그 보드는 구역 사이의 선수 이동을 지원해. "
        "각 선수를 축구장 위의 임의 좌표로 직접 끌어 놓는 방식과는 달라."
    )

    if st.button("선발 라인업 저장", type="primary"):
        st.success("선발 라인업을 저장했어!")

    current_xi = [
        by_id[pid] for pid in st.session_state.lineup_ids
        if pid in by_id
    ]
    st.write(f"선발 인원: {min(11, len(current_xi))}/11")
    cols = st.columns(4)
    for i, player in enumerate(current_xi[:11]):
        with cols[i % 4]:
            player_avatar(player, 52)
            st.caption(
                f"{player['name']}\n"
                f"{player['pos']} · OVR {player['rating']}"
            )

# -------------------------
# 선수단
# -------------------------
with tabs[1]:
    st.subheader("👥 1군 선수단")
    show_faces = st.checkbox("얼굴 사진 표시", True)

    cols = st.columns(4)
    for i, p in enumerate(
        sorted(squad, key=lambda x: x["rating"], reverse=True)
    ):
        with cols[i % 4]:
            with st.container(border=True):
                if show_faces:
                    player_avatar(p, 76)
                else:
                    st.markdown("### ⚽")
                st.markdown(f"**{p['name']}**")
                st.caption(f"{p['pos']} · {p['age']}세")
                st.metric("OVR", p["rating"])
                st.write("시장 가치:", money(p["value"]))

    st.divider()
    sell_options = {
        f"{p['name']} · OVR {p['rating']}": p["id"]
        for p in squad
    }
    selected_sell = st.selectbox("판매할 선수", list(sell_options.keys()))
    if st.button("선수 판매"):
        player = next(
            p for p in squad if p["id"] == sell_options[selected_sell]
        )
        fee = round(player["value"] * 0.85, 1)
        st.session_state.budget += fee
        st.session_state.squad = [
            p for p in squad if p["id"] != player["id"]
        ]
        st.session_state.market.append(player)
        st.session_state.lineup_ids = [
            pid for pid in st.session_state.get("lineup_ids", [])
            if pid != player["id"]
        ]
        st.session_state.log.insert(0, f"{player['name']} 판매: {money(fee)}")
        st.rerun()

# -------------------------
# 이적시장
# -------------------------
with tabs[2]:
    st.subheader("🔁 이적시장")
    query = st.text_input("선수 이름 검색")
    position = st.selectbox("포지션", ["전체"] + POSITIONS)

    available = [
        p for p in st.session_state.market
        if query.lower() in p["name"].lower()
        and (position == "전체" or p["pos"] == position)
    ]
    available.sort(key=lambda p: p["rating"], reverse=True)

    st.caption(f"검색 결과 {len(available)}명")
    for p in available:
        with st.container(border=True):
            left, mid, right = st.columns([4, 2, 1])
            with left:
                player_avatar(p, 54)
                st.markdown(f"**{p['name']}**")
                st.caption(f"{p['pos']} · {p['age']}세 · OVR {p['rating']}")
            with mid:
                fee = round(p["value"] * 1.15, 1)
                st.write("영입료")
                st.markdown(f"### {money(fee)}")
                st.caption(f"시장 가치 {money(p['value'])}")
            with right:
                if st.button("영입", key=f"buy_{p['id']}"):
                    if len(st.session_state.squad) >= 30:
                        st.error("선수단은 최대 30명이야.")
                    elif st.session_state.budget < fee:
                        st.error("이적 예산이 부족해.")
                    else:
                        st.session_state.budget -= fee
                        p["club"] = club
                        st.session_state.squad.append(p)
                        st.session_state.market = [
                            x for x in st.session_state.market
                            if x["id"] != p["id"]
                        ]
                        st.session_state.log.insert(
                            0, f"{p['name']} 영입: {money(fee)}"
                        )
                        st.rerun()

# -------------------------
# 경기
# -------------------------
with tabs[3]:
    st.subheader("⚽ 다음 경기")
    st.write(f"라운드: {st.session_state.week}/38")

    league = CLUBS[club][0]
    opponents = [
        name for name in CLUBS
        if name != club and CLUBS[name][0] == league
    ]

    if st.button("경기 진행", type="primary"):
        opponent = random.choice(opponents)
        strength = team_strength(st.session_state.squad)
        opp_strength = CLUBS[opponent][2]
        goals_for = max(
            0, min(5, round(random.gauss(1.5 + (strength - opp_strength) / 12, 1)))
        )
        goals_against = max(
            0, min(5, round(random.gauss(1.2 + (opp_strength - strength) / 12, 1)))
        )

        if goals_for > goals_against:
            result = "승리"
            st.session_state.wins += 1
            st.session_state.points += 3
        elif goals_for == goals_against:
            result = "무승부"
            st.session_state.draws += 1
            st.session_state.points += 1
        else:
            result = "패배"
            st.session_state.losses += 1

        st.session_state.week += 1
        st.session_state.budget += 2.5

        for p in st.session_state.squad:
            p["apps"] += 1
            if p["pos"] in ["ST", "LW", "RW", "AM"] and random.random() < 0.22:
                p["goals"] += 1

        st.session_state.log.insert(
            0,
            f"{club} {goals_for}-{goals_against} {opponent} · {result}"
        )
        st.rerun()

    if st.session_state.log:
        st.markdown("### 최근 소식")
        for item in st.session_state.log[:8]:
            st.write("• " + item)

    a, b, c = st.columns(3)
    a.metric("승리", st.session_state.wins)
    b.metric("무승부", st.session_state.draws)
    c.metric("패배", st.session_state.losses)

# -------------------------
# 유스 및 기록
# -------------------------
with tabs[4]:
    st.subheader("🌱 유스 아카데미")
    st.write("유스 발굴 비용: €1.0m")

    if st.button("유스 선수 발굴"):
        if st.session_state.budget >= 1:
            pid = st.session_state.pid
            pos = random.choice(POSITIONS)
            age = random.randint(15, 18)
            rating = random.randint(55, 72)
            youth = make_player(
                random.choice(["Min-jun Kim", "Ji-ho Park", "Alex Lee"]) + f" {pid}",
                pos, age, rating, club, pid
            )
            st.session_state.pid += 1
            st.session_state.budget -= 1
            st.session_state.youth.append(youth)
            st.rerun()
        else:
            st.error("예산이 부족해.")

    if st.session_state.youth:
        for p in st.session_state.youth:
            with st.container(border=True):
                player_avatar(p, 52)
                st.write(f"**{p['name']}** · {p['pos']}")
                st.write(f"나이 {p['age']} · OVR {p['rating']}")
                if st.button("1군 승격", key=f"promote_{p['id']}"):
                    st.session_state.squad.append(p)
                    st.session_state.youth = [
                        x for x in st.session_state.youth
                        if x["id"] != p["id"]
                    ]
                    st.rerun()

    st.divider()
    st.subheader("📊 시즌 선수 기록")
    st.dataframe(
        [
            {
                "선수": p["name"],
                "포지션": p["pos"],
                "OVR": p["rating"],
                "출전": p["apps"],
                "골": p["goals"],
                "시장 가치": money(p["value"]),
            }
            for p in sorted(
                st.session_state.squad,
                key=lambda x: (x["goals"], x["rating"]),
                reverse=True
            )
        ],
        hide_index=True,
        use_container_width=True
    )

st.divider()
if st.button("새 커리어 시작"):
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.rerun()

st.caption("FOOTBALL DIRECTOR · 팬 제작 게임")

"""
TurisGraph Brasil — Planejador de Rotas por Rodovias
Interface gráfica com Pygame + Algoritmo de Dijkstra
Mapa vetorial real do Brasil (GeoJSON simplificado)
"""

import pygame
import heapq
import sys
import math
import json
import os
import urllib.request

# ─────────────────────────────────────────────
#  CARREGAR / BAIXAR GEOJSON DOS ESTADOS
# ─────────────────────────────────────────────

_GEOJSON_URL  = "https://raw.githubusercontent.com/codeforamerica/click_that_hood/master/public/data/brazil-states.geojson"
_CACHE_PATH   = os.path.join(os.path.expanduser("~"), ".turisgraph_brazil.geojson")

def _load_geojson():
    if os.path.exists(_CACHE_PATH):
        with open(_CACHE_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    req = urllib.request.Request(_GEOJSON_URL, headers={"User-Agent": "TurisGraph/1.0"})
    with urllib.request.urlopen(req, timeout=15) as r:
        data = json.loads(r.read())
    with open(_CACHE_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f)
    return data

def _simplify(coords, tol=0.12):
    if len(coords) <= 3:
        return coords
    out = [coords[0]]
    for pt in coords[1:]:
        if math.hypot(pt[0]-out[-1][0], pt[1]-out[-1][1]) >= tol:
            out.append(pt)
    if out[-1] != coords[-1]:
        out.append(coords[-1])
    return out

def _build_poly_dict(geo):
    """Returns {state_name: [ [[lon,lat], ...], ... ]} — multiple rings per state."""
    d = {}
    for feat in geo["features"]:
        name = feat["properties"]["name"]
        rings = []
        for poly in feat["geometry"]["coordinates"]:
            ring = _simplify(poly[0], 0.12)
            if len(ring) >= 3:
                rings.append(ring)
        if rings:
            d[name] = rings
    return d

# ─────────────────────────────────────────────
#  COORDENADAS GEOGRÁFICAS REAIS DOS ESTADOS
# ─────────────────────────────────────────────

ESTADOS_GEO = {
    "Acre":               {"lon": -70.5,  "lat": -9.0,   "uf": "AC"},
    "Alagoas":            {"lon": -36.6,  "lat": -9.7,   "uf": "AL"},
    "Amapá":              {"lon": -52.0,  "lat": 1.4,    "uf": "AP"},
    "Amazonas":           {"lon": -64.5,  "lat": -4.0,   "uf": "AM"},
    "Bahia":              {"lon": -41.7,  "lat": -12.5,  "uf": "BA"},
    "Ceará":              {"lon": -39.3,  "lat": -5.2,   "uf": "CE"},
    "Distrito Federal":   {"lon": -47.9,  "lat": -15.8,  "uf": "DF"},
    "Espírito Santo":     {"lon": -40.3,  "lat": -19.2,  "uf": "ES"},
    "Goiás":              {"lon": -49.2,  "lat": -15.9,  "uf": "GO"},
    "Maranhão":           {"lon": -45.3,  "lat": -5.0,   "uf": "MA"},
    "Mato Grosso":        {"lon": -55.0,  "lat": -13.5,  "uf": "MT"},
    "Mato Grosso do Sul": {"lon": -54.5,  "lat": -20.5,  "uf": "MS"},
    "Minas Gerais":       {"lon": -44.7,  "lat": -18.5,  "uf": "MG"},
    "Pará":               {"lon": -53.0,  "lat": -4.0,   "uf": "PA"},
    "Paraíba":            {"lon": -36.8,  "lat": -7.2,   "uf": "PB"},
    "Paraná":             {"lon": -51.6,  "lat": -24.8,  "uf": "PR"},
    "Pernambuco":         {"lon": -37.9,  "lat": -8.3,   "uf": "PE"},
    "Piauí":              {"lon": -42.8,  "lat": -6.6,   "uf": "PI"},
    "Rio de Janeiro":     {"lon": -43.2,  "lat": -22.4,  "uf": "RJ"},
    "Rio Grande do Norte":{"lon": -36.5,  "lat": -5.8,   "uf": "RN"},
    "Rio Grande do Sul":  {"lon": -53.2,  "lat": -30.0,  "uf": "RS"},
    "Rondônia":           {"lon": -63.0,  "lat": -10.8,  "uf": "RO"},
    "Roraima":            {"lon": -61.4,  "lat": 2.0,    "uf": "RR"},
    "Santa Catarina":     {"lon": -50.5,  "lat": -27.5,  "uf": "SC"},
    "São Paulo":          {"lon": -48.6,  "lat": -22.5,  "uf": "SP"},
    "Sergipe":            {"lon": -37.4,  "lat": -10.6,  "uf": "SE"},
    "Tomantins":          {"lon": -48.3,  "lat": -10.2,  "uf": "TO"}, # Mantido para compatibilidade com o GeoJSON original se necessário, ajustado abaixo
    "Tocantins":          {"lon": -48.3,  "lat": -10.2,  "uf": "TO"},
}

# AJUSTE GEOGRÁFICO: Pesos recalculados com base em distâncias rodoviárias reais (Capitais/Principais rotas)
ARESTAS = [
    # ── Norte ─────────────────────────────────────────────────────────────────
    ("Roraima",            "Amazonas",             780,  "BR-174"),
    ("Roraima",            "Pará",                 1350, "BR-210/174"),
    ("Roraima",            "Amapá",                1850, "BR-156/174"),
    ("Amapá",              "Pará",                 650,  "BR-156/010"),
    ("Pará",               "Amazonas",             1290, "BR-230 Transamazônica"),
    ("Pará",               "Maranhão",             810,  "BR-316"),
    ("Pará",               "Mato Grosso",          1100, "BR-163"),
    ("Pará",               "Tocantins",            1020, "BR-153/226"),
    ("Amazonas",           "Acre",                 1450, "BR-317"),
    ("Amazonas",           "Rondônia",             900,  "BR-319"),
    ("Amazonas",           "Mato Grosso",          1600, "BR-230/163"),
    ("Acre",               "Rondônia",             510,  "BR-364"),

    # ── Centro-Oeste ───────────────────────────────────────────────────────────
    ("Rondônia",           "Mato Grosso",          1450, "BR-364"),
    ("Mato Grosso",        "Tocantins",            1150, "BR-158"),
    ("Mato Grosso",        "Goiás",                930,  "BR-070"),
    ("Mato Grosso",        "Mato Grosso do Sul",   710,  "BR-163"),
    ("Goiás",              "Tocantins",            820,  "BR-153"),
    ("Goiás",              "Bahia",                1150, "BR-020/242"), # Aumentado para refletir a travessia real do Centro-Oeste ao litoral Baiano
    ("Goiás",              "Minas Gerais",         880,  "BR-050/040"),
    ("Goiás",              "Mato Grosso do Sul",   830,  "BR-060"),
    ("Goiás",              "São Paulo",            870,  "BR-153"),     # Rota corrigida SP-GO real
    ("Goiás",              "Distrito Federal",     210,  "BR-060"),
    ("Distrito Federal",   "Minas Gerais",         740,  "BR-040"),
    ("Distrito Federal",   "Bahia",                1100, "BR-020"),
    ("Mato Grosso do Sul", "Minas Gerais",         980,  "BR-262"),
    ("Mato Grosso do Sul", "São Paulo",            1010, "BR-267/374"),
    ("Mato Grosso do Sul", "Paraná",               990,  "BR-163"),

    # ── Nordeste ───────────────────────────────────────────────────────────────
    ("Maranhão",           "Piauí",                440,  "BR-316"),
    ("Maranhão",           "Tocantins",            650,  "BR-010"),
    ("Maranhão",           "Ceará",                1000, "BR-222"),
    ("Piauí",              "Ceará",                595,  "BR-343/222"),
    ("Piauí",              "Pernambuco",           1100, "BR-316"),
    ("Piauí",              "Bahia",                1170, "BR-135"),
    ("Piauí",              "Tocantins",            920,  "BR-230/153"),
    ("Ceará",              "Rio Grande do Norte",  530,  "BR-304"),
    ("Ceará",              "Paraíba",              680,  "BR-116/230"),
    ("Ceará",              "Pernambuco",           800,  "BR-116/232"),
    ("Rio Grande do Norte","Paraíba",              180,  "BR-101"),
    ("Rio Grande do Norte","Pernambuco",           290,  "BR-101"),
    ("Paraíba",            "Pernambuco",           120,  "BR-101"),
    ("Pernambuco",         "Alagoas",              260,  "BR-101"),
    ("Pernambuco",         "Bahia",                840,  "BR-116"),
    ("Pernambuco",         "Sergipe",              500,  "BR-101"),
    ("Alagoas",            "Sergipe",              200,  "BR-101"),
    ("Alagoas",            "Bahia",                640,  "BR-101"),
    ("Sergipe",            "Bahia",                320,  "BR-101"),

    # ── Sudeste (O miolo que corrige o seu problema) ──────────────────────────
    ("São Paulo",          "Minas Gerais",         580,  "BR-381 Fernão Dias"), # SP para BH
    ("Minas Gerais",       "Bahia",                870,  "BR-116/251"),          # BH para Salvador/Sul da BA
    ("Bahia",              "Espírito Santo",       1100, "BR-101"),
    ("Bahia",              "Tocantins",            1200, "BR-242/020"),
    ("Minas Gerais",       "Espírito Santo",       520,  "BR-262"),
    ("Minas Gerais",       "Rio de Janeiro",       440,  "BR-040"),
    ("Rio de Janeiro",     "Espírito Santo",       510,  "BR-101"),
    ("Rio de Janeiro",     "São Paulo",            430,  "BR-116 Pres. Dutra"),
    ("São Paulo",          "Paraná",               410,  "BR-116 Régis Bittencourt"),

    # ── Sul ────────────────────────────────────────────────────────────────────
    ("Paraná",             "Santa Catarina",       300,  "BR-101/376"),
    ("Santa Catarina",     "Rio Grande do Sul",    450,  "BR-101/116"),
]

# ─────────────────────────────────────────────
#  GRAFO E DIJKSTRA
# ─────────────────────────────────────────────

class Grafo:
    def __init__(self):
        self.adjacencia  = {}
        self.info_arestas = {}

    def adicionar_aresta(self, u, v, peso, rodovia):
        for n in (u, v):
            if n not in self.adjacencia:
                self.adjacencia[n] = []
        self.adjacencia[u].append((v, peso))
        self.adjacencia[v].append((u, peso))
        self.info_arestas[tuple(sorted([u, v]))] = {"km": peso, "rodovia": rodovia}

    def info_aresta(self, u, v):
        return self.info_arestas.get(tuple(sorted([u, v])), {"km": 0, "rodovia": "?"})


def dijkstra(grafo, inicio, fim):
    dist = {v: float("inf") for v in grafo.adjacencia}
    prev = {v: None for v in grafo.adjacencia}
    dist[inicio] = 0
    pq = [(0, inicio)]
    while pq:
        d, u = heapq.heappop(pq)
        if u == fim:
            break
        if d > dist[u]:
            continue
        for v, peso in grafo.adjacencia.get(u, []):
            nd = d + peso
            if nd < dist[v]:
                dist[v] = nd
                prev[v] = u
                heapq.heappush(pq, (nd, v))
    if dist[fim] == float("inf"):
        return None, []
    cam, cur = [], fim
    while cur:
        cam.insert(0, cur)
        cur = prev[cur]
    return dist[fim], cam

# ─────────────────────────────────────────────
#  PALETA MINIMALISTA
# ─────────────────────────────────────────────

C = {
    "bg":            (15,  20,  32),
    "panel":         (20,  26,  42),
    "panel2":        (26,  34,  52),
    "panel_border":  (40,  50,  72),
    "map_bg":        (15,  20,  32),
    "state_fill":    (28,  52,  36),
    "state_alt":     (24,  46,  32),
    "state_border":  (55,  95,  65),
    "state_hover":   (38,  72,  52),
    "state_path":    (30,  64,  80),
    "state_orig":    (25,  75,  55),
    "state_dest":    (80,  30,  45),
    "edge":          (50,  70, 100),
    "edge_path":     (56, 210, 160),
    "edge_glow":     (20, 100,  75),
    "node_normal":   (70, 110, 160),
    "node_border":   (90, 135, 195),
    "node_path":     (56, 210, 160),
    "node_origin":   (56, 210, 160),
    "node_dest":     (240,  75,  85),
    "text_main":     (215, 225, 240),
    "text_muted":    (110, 130, 165),
    "text_light":    (62,  82, 120),
    "text_accent":   (56, 210, 160),
    "text_danger":   (250,  95, 105),
    "accent":        (56, 210, 160),
    "accent_dark":   (28, 120,  88),
    "accent_light":  (18,  50,  46),
    "danger":        (210,  65,  75),
    "danger_light":  (55,  22,  28),
    "btn":           (36, 155, 110),
    "btn_hover":     (56, 210, 160),
    "btn_text":      (8,   18,  26),
    "select":        (24,  32,  50),
    "select_hover":  (32,  42,  64),
    "select_open":   (22,  46,  50),
    "divider":       (36,  48,  72),
    "step_mid":      (55,  75, 110),
    "road_bg":       (12,  30,  40),
    "road_border":   (56, 210, 160),
    "label_uf":      (150, 185, 230),
}

# Bounding box EXATO do GeoJSON do Brasil
LON_MIN, LON_MAX = -73.99, -32.39
LAT_MIN, LAT_MAX = -33.75,   5.27

def _merc(lat):
    lr = math.radians(max(-85.0511, min(85.0511, lat)))
    return math.log(math.tan(math.pi / 4 + lr / 2))

_MY0 = _merc(LAT_MAX)
_MY1 = _merc(LAT_MIN)

def geo_to_px(lon, lat, ox, oy, ow, oh, pad=32):
    mx = (lon - LON_MIN) / (LON_MAX - LON_MIN)
    my = (_MY0 - _merc(lat)) / (_MY0 - _MY1)
    return (int(ox + pad + mx * (ow - 2*pad)),
            int(oy + pad + my * (oh - 2*pad)))


class TurisGraphApp:
    W, H    = 1120, 720
    PANEL_W = 310
    MAP_X   = PANEL_W
    MAP_W   = W - PANEL_W
    MAP_H   = H
    PAD     = 28

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((self.W, self.H))
        pygame.display.set_caption("TurisGraph Brasil — Planejador de Rotas")
        self.clock = pygame.time.Clock()

        self.f_title = pygame.font.SysFont("Arial", 15, bold=True)
        self.f_body  = pygame.font.SysFont("Arial", 13)
        self.f_small = pygame.font.SysFont("Arial", 11)
        self.f_micro = pygame.font.SysFont("Arial", 9)
        self.f_uf    = pygame.font.SysFont("Arial", 9,  bold=True)
        self.f_btn   = pygame.font.SysFont("Arial", 13, bold=True)
        self.f_big   = pygame.font.SysFont("Arial", 20, bold=True)
        self.f_lbl   = pygame.font.SysFont("Arial", 10, bold=True)

        self.grafo = Grafo()
        for de, para, km, rod in ARESTAS:
            self.grafo.adicionar_aresta(de, para, km, rod)
        self.estados_list = sorted([k for k in self.grafo.adjacencia.keys() if k in ESTADOS_GEO])

        self.origem    = None
        self.destino   = None
        self.caminho   = []
        self.distancia = 0
        self.error_msg = ""
        self.scroll_y  = 0
        self.scroll_max = 0
        self.hover_state     = None
        self.hover_btn_calc  = False
        self.hover_btn_swap  = False
        self.hover_edge      = None
        self.clicked_edge    = None
        self.calc_rect = pygame.Rect(0,0,1,1)
        self.swap_rect = pygame.Rect(0,0,1,1)
        self.anim_t    = 0.0

        self.dd_orig = Dropdown(self, self.estados_list, 18, 108, 274, 36)
        self.dd_dest = Dropdown(self, self.estados_list, 18, 190, 274, 36)

        self.screen.fill(C["bg"])
        lf = pygame.font.SysFont("Arial", 18, bold=True)
        ls = pygame.font.SysFont("Arial", 12)
        self.screen.blit(lf.render("Carregando mapa do Brasil...", True, C["text_accent"]),
                         lf.render("Carregando mapa do Brasil...", True, C["text_accent"]).get_rect(center=(self.W//2, self.H//2)))
        self.screen.blit(ls.render("(necessário somente na primeira execução)", True, C["text_muted"]),
                         ls.render("(necessário somente na primeira execução)", True, C["text_muted"]).get_rect(center=(self.W//2, self.H//2+32)))
        pygame.display.flip()

        geo = _load_geojson()
        self.poly_dict = _build_poly_dict(geo)
        self.map_surf = self._build_map_surface()

    def _gp(self, lon, lat):
        return geo_to_px(lon, lat, 0, 0, self.MAP_W, self.MAP_H, self.PAD)

    def state_px(self, nome):
        g = ESTADOS_GEO[nome]
        return geo_to_px(g["lon"], g["lat"], self.MAP_X, 0, self.MAP_W, self.MAP_H, self.PAD)

    def _build_map_surface(self):
        surf = pygame.Surface((self.MAP_W, self.MAP_H))
        surf.fill(C["map_bg"])
        fill_colors = [(28,52,36), (24,48,33), (30,55,38), (22,44,30), (32,58,40)]
        state_names = sorted(self.poly_dict.keys())

        for i, name in enumerate(state_names):
            if name not in ESTADOS_GEO: continue
            rings = self.poly_dict[name]
            fc = fill_colors[i % len(fill_colors)]
            for ring in rings:
                pts = [self._gp(lon, lat) for lon, lat in ring]
                if len(pts) < 3: continue
                p_surf = pygame.Surface((self.MAP_W, self.MAP_H), pygame.SRCALPHA)
                pygame.draw.polygon(p_surf, (*fc, 255), pts)
                surf.blit(p_surf, (0, 0))
                pygame.draw.polygon(surf, C["state_border"], pts, 1)
        return surf

    def draw_map(self):
        self.anim_t += 0.04
        pygame.draw.rect(self.screen, C["map_bg"], pygame.Rect(self.MAP_X, 0, self.MAP_W, self.MAP_H))
        self.screen.blit(self.map_surf, (self.MAP_X, 0))

        path_set   = set(self.caminho)
        path_edges = set()
        for i in range(len(self.caminho)-1):
            path_edges.add(tuple(sorted([self.caminho[i], self.caminho[i+1]])))

        if self.hover_state and self.hover_state in self.poly_dict:
            for ring in self.poly_dict[self.hover_state]:
                pts = [(p[0] + self.MAP_X, p[1]) for p in [self._gp(lon, lat) for lon, lat in ring]]
                if len(pts) >= 3:
                    hs = pygame.Surface((self.MAP_W, self.MAP_H), pygame.SRCALPHA)
                    pygame.draw.polygon(hs, (*C["state_hover"], 80), [(p[0]-self.MAP_X, p[1]) for p in pts])
                    self.screen.blit(hs, (self.MAP_X, 0))
                    pygame.draw.polygon(self.screen, C["accent"], pts, 1)

        for nome in path_set:
            is_orig = self.caminho and self.caminho[0]  == nome
            is_dest = self.caminho and self.caminho[-1] == nome
            col = C["state_orig"] if is_orig else C["state_dest"] if is_dest else C["state_path"]
            if nome in self.poly_dict:
                for ring in self.poly_dict[nome]:
                    pts = [(p[0] + self.MAP_X, p[1]) for p in [self._gp(lon, lat) for lon, lat in ring]]
                    if len(pts) >= 3:
                        rs = pygame.Surface((self.MAP_W, self.MAP_H), pygame.SRCALPHA)
                        pygame.draw.polygon(rs, (*col, 100), [(p[0]-self.MAP_X, p[1]) for p in pts])
                        self.screen.blit(rs, (self.MAP_X, 0))

        mx_cur, my_cur = pygame.mouse.get_pos()
        for aresta in ARESTAS:
            de, para, km, rod = aresta
            if de not in ESTADOS_GEO or para not in ESTADOS_GEO: continue
            a = self.state_px(de)
            b = self.state_px(para)
            is_path    = tuple(sorted([de, para])) in path_edges
            is_hover   = self.hover_edge == aresta
            is_clicked = self.clicked_edge == aresta

            if is_path:
                pygame.draw.line(self.screen, C["edge_glow"], a, b, 7)
                pygame.draw.line(self.screen, C["edge_path"],  a, b, 3)
                mx2, my2 = (a[0]+b[0])//2, (a[1]+b[1])//2
                lbl = self.f_micro.render(rod, True, C["text_accent"])
                lw, lh = lbl.get_size()
                bg = pygame.Surface((lw+10, lh+6), pygame.SRCALPHA)
                pygame.draw.rect(bg, (*C["road_bg"], 220), bg.get_rect(), border_radius=3)
                pygame.draw.rect(bg, (*C["road_border"], 160), bg.get_rect(), 1, border_radius=3)
                self.screen.blit(bg,  (mx2 - lw//2 - 5, my2 - lh//2 - 3))
                self.screen.blit(lbl, (mx2 - lw//2,     my2 - lh//2))
            elif is_clicked:
                pygame.draw.line(self.screen, (*C["accent"], 255), a, b, 4)
                pygame.draw.line(self.screen, (255, 255, 255),     a, b, 1)
            elif is_hover:
                pygame.draw.line(self.screen, C["edge_glow"], a, b, 5)
                pygame.draw.line(self.screen, (130, 200, 240),     a, b, 2)
            else:
                pygame.draw.line(self.screen, C["edge"], a, b, 1)

        if self.clicked_edge:
            de, para, km, rod = self.clicked_edge
            if de in ESTADOS_GEO and para in ESTADOS_GEO:
                a = self.state_px(de)
                b = self.state_px(para)
                mid = ((a[0]+b[0])//2, (a[1]+b[1])//2)
                self._draw_edge_tooltip(de, para, km, rod, mid[0], mid[1])
        elif self.hover_edge:
            de, para, km, rod = self.hover_edge
            self._draw_edge_tooltip(de, para, km, rod, mx_cur, my_cur)

        for nome, info in ESTADOS_GEO.items():
            if nome not in self.grafo.adjacencia: continue
            x, y     = self.state_px(nome)
            in_path  = nome in path_set
            is_orig  = self.caminho and self.caminho[0]  == nome
            is_dest  = self.caminho and self.caminho[-1] == nome
            is_hover = nome == self.hover_state

            if is_orig or is_dest:
                pulse = abs(math.sin(self.anim_t)) * 6
                col   = C["node_origin"] if is_orig else C["node_dest"]
                rs = pygame.Surface((60, 60), pygame.SRCALPHA)
                alpha = int(80 + 60 * abs(math.sin(self.anim_t)))
                pygame.draw.circle(rs, (*col, alpha), (30, 30), int(14+pulse), 2)
                self.screen.blit(rs, (x-30, y-30))

            if is_hover and not is_orig and not is_dest:
                hs = pygame.Surface((40, 40), pygame.SRCALPHA)
                pygame.draw.circle(hs, (*C["node_normal"], 80), (20, 20), 16, 2)
                self.screen.blit(hs, (x-20, y-20))

            r    = 8 if (is_orig or is_dest) else 6 if in_path else 5
            fill = (C["node_origin"] if is_orig else C["node_dest"] if is_dest
                    else C["node_path"] if in_path else C["node_normal"])
            bord = (220,240,255) if (is_orig or is_dest) else C["node_border"]

            pygame.draw.circle(self.screen, fill, (x, y), r)
            pygame.draw.circle(self.screen, bord, (x, y), r, 1)

            uf  = info["uf"]
            tc  = ((220,255,220) if is_orig else (255,160,160) if is_dest else C["text_accent"] if in_path else C["label_uf"])
            lbl = self.f_uf.render(uf, True, tc)
            lw, lh = lbl.get_size()
            lbg = pygame.Surface((lw+6, lh+3), pygame.SRCALPHA)
            lbg.fill((*C["map_bg"], 150))
            self.screen.blit(lbg, (x - lw//2 - 3, y - 20))
            self.screen.blit(lbl, (x - lw//2,     y - 19))

        if self.hover_state and self.hover_state in ESTADOS_GEO and self.hover_state in self.grafo.adjacencia:
            hx, hy = self.state_px(self.hover_state)
            nome = self.hover_state
            uf   = ESTADOS_GEO[nome]["uf"]
            conns = len(self.grafo.adjacencia.get(nome, []))
            lines = [f"{uf} — {nome}", f"Conexões: {conns}"]
            tw = max(self.f_body.size(l)[0] for l in lines) + 20
            th = len(lines) * 18 + 10
            tip = pygame.Surface((tw, th), pygame.SRCALPHA)
            pygame.draw.rect(tip, (*C["panel"], 230), tip.get_rect(), border_radius=6)
            pygame.draw.rect(tip, (*C["panel_border"], 200), tip.get_rect(), 1, border_radius=6)
            self.screen.blit(tip, (hx+12, hy-10))
            self._txt(self.f_body,  lines[0], C["text_main"],  hx+22, hy-5)
            self._txt(self.f_small, lines[1], C["text_muted"], hx+22, hy+12)

        leg = pygame.Surface((165, 88), pygame.SRCALPHA)
        pygame.draw.rect(leg, (*C["panel"], 200), leg.get_rect(), border_radius=8)
        pygame.draw.rect(leg, (*C["panel_border"], 150), leg.get_rect(), 1, border_radius=8)
        self.screen.blit(leg, (self.W - 178, self.H - 100))
        lx, ly = self.W - 165, self.H - 88
        self._txt(self.f_lbl, "LEGENDA", C["text_muted"], lx, ly); ly += 18
        for col, thick, label in [
            (C["edge"],       1, "Rodovias"),
            (C["edge_path"],  3, "Rota calculada"),
            (C["node_origin"],0, "Origem"),
            (C["node_dest"],  0, "Destino"),
        ]:
            if thick:
                pygame.draw.line(self.screen, col, (lx, ly+5), (lx+20, ly+5), thick)
            else:
                pygame.draw.circle(self.screen, col, (lx+5, ly+5), 4)
            self._txt(self.f_small, label, C["text_muted"], lx+26, ly)
            ly += 17

    def draw_panel(self):
        pygame.draw.rect(self.screen, C["panel"], (0, 0, self.PANEL_W, self.H))
        pygame.draw.line(self.screen, C["panel_border"], (self.PANEL_W, 0), (self.PANEL_W, self.H), 1)

        hdr = pygame.Surface((self.PANEL_W, 64), pygame.SRCALPHA)
        for i in range(64):
            a = int(120 + 80 * (1 - i/64))
            pygame.draw.line(hdr, (*C["accent_dark"], a), (0, i), (self.PANEL_W, i))
        self.screen.blit(hdr, (0, 0))
        pygame.draw.line(self.screen, C["panel_border"], (0, 64), (self.PANEL_W, 64), 1)
        pygame.draw.rect(self.screen, C["accent"], (16, 14, 34, 34), border_radius=8)
        self._txt(self.f_title, "🗺", C["btn_text"], 22, 18)
        self._txt(self.f_title, "TurisGraph Brasil", C["text_main"], 58, 17)
        self._txt(self.f_small, "Dijkstra · Rodovias · 27 estados", C["text_muted"], 58, 36)

        y = 82
        self._txt(self.f_lbl, "ORIGEM", C["text_muted"], 18, y); y += 15
        self.dd_orig.y = y
        self.dd_orig.draw(self.screen); y += 44

        self.swap_rect = pygame.Rect(18, y, 274, 28)
        bc = C["select_hover"] if self.hover_btn_swap else C["select"]
        self._rect(bc, self.swap_rect, 6, C["panel_border"])
        self._txt(self.f_small, "⇅  Inverter rota", C["text_muted"], self.PANEL_W//2, y+8, "midtop")
        y += 38

        self._txt(self.f_lbl, "DESTINO", C["text_muted"], 18, y); y += 15
        self.dd_dest.y = y
        self.dd_dest.draw(self.screen); y += 44

        self.calc_rect = pygame.Rect(18, y, 274, 40)
        bc = C["btn_hover"] if self.hover_btn_calc else C["btn"]
        self._rect(bc, self.calc_rect, 8)
        self._txt(self.f_btn, "▶  Calcular Rota Mais Curta", C["btn_text"], self.PANEL_W//2, y+12, "midtop")
        y += 52

        pygame.draw.line(self.screen, C["panel_border"], (18, y), (self.PANEL_W-18, y), 1)
        y += 14

        if self.error_msg:
            er = pygame.Rect(18, y, 274, 38)
            self._rect(C["danger_light"], er, 8, C["danger"])
            self._txt(self.f_small, "✗  " + self.error_msg, C["text_danger"], 28, y+13)
            return

        if not self.caminho:
            self._txt(self.f_small, "Selecione dois estados", C["text_light"], self.PANEL_W//2, y+6,  "midtop")
            self._txt(self.f_small, "ou clique no mapa", C["text_light"], self.PANEL_W//2, y+22, "midtop")
            return

        stat_w = 84
        for i, (lbl, val) in enumerate([
            ("km",      f"{self.distancia:,}".replace(",",".")),
            ("estados", str(len(self.caminho))),
            ("trechos", str(len(self.caminho)-1)),
        ]):
            sx = 18 + i * (stat_w + 7)
            sr = pygame.Rect(sx, y, stat_w, 54)
            self._rect(C["panel2"], sr, 6, C["panel_border"])
            self._txt(self.f_lbl, lbl, C["text_muted"],  sx+stat_w//2, y+7,  "midtop")
            self._txt(self.f_big, val, C["text_accent"],  sx+stat_w//2, y+24, "midtop")
        y += 62

        pygame.draw.line(self.screen, C["panel_border"], (18, y), (self.PANEL_W-18, y), 1)
        y += 8

        STEP_H = 40
        area_h = self.H - y - 6
        total_h = len(self.caminho) * STEP_H
        self.scroll_max = max(0, total_h - area_h)
        clip = pygame.Surface((self.PANEL_W, area_h), pygame.SRCALPHA)

        for i, estado in enumerate(self.caminho):
            ey = -self.scroll_y + i * STEP_H
            if ey + STEP_H < 0 or ey > area_h: continue
            is_orig = i == 0
            is_dest = i == len(self.caminho)-1
            dot_col = (C["node_origin"] if is_orig else C["node_dest"] if is_dest else C["step_mid"])
            if i < len(self.caminho)-1:
                pygame.draw.line(clip, C["panel_border"], (30, ey+28), (30, ey+STEP_H+4), 1)
            pygame.draw.circle(clip, dot_col, (30, ey+16), 6)
            if is_orig or is_dest:
                pygame.draw.circle(clip, (220,240,255), (30, ey+16), 6, 2)
            nc = ((180,255,210) if is_orig else (255,160,160) if is_dest else C["text_main"])
            clip.blit(self.f_body.render(estado, True, nc), (46, ey+5))
            if i < len(self.caminho)-1:
                info = self.grafo.info_aresta(estado, self.caminho[i+1])
                rt = f"{info['rodovia']}  - {info['km']:,} km".replace(",",".")
                clip.blit(self.f_small.render(rt, True, C["text_accent"]), (46, ey+22))

        self.screen.blit(clip, (0, y))
        if self.scroll_max > 0:
            sb_h = max(25, int(area_h * area_h / total_h))
            sb_y = y + int(self.scroll_y / self.scroll_max * (area_h - sb_h))
            pygame.draw.rect(self.screen, C["panel_border"], pygame.Rect(self.PANEL_W-5, sb_y, 3, sb_h), border_radius=2)

    @staticmethod
    def _dist_seg(px, py, ax, ay, bx, by):
        dx, dy = bx - ax, by - ay
        if dx == dy == 0:
            return math.hypot(px - ax, py - ay)
        t = max(0.0, min(1.0, ((px-ax)*dx + (py-ay)*dy) / (dx*dx + dy*dy)))
        return math.hypot(px - (ax + t*dx), py - (ay + t*dy))

    def _draw_edge_tooltip(self, de, para, km, rod, mx, my):
        lines = [rod, f"{de}  →  {para}", f"{km:,} km".replace(",", ".")]
        pad = 10
        lw = max(self.f_body.size(l)[0] for l in lines) + pad*2
        lh = len(lines) * 19 + pad*2 - 4

        tx = mx + 14
        ty = my - lh // 2
        if tx + lw > self.W - 4: tx = mx - lw - 10
        ty = max(4, min(ty, self.H - lh - 4))

        bg = pygame.Surface((lw, lh), pygame.SRCALPHA)
        pygame.draw.rect(bg, (*C["panel"], 235), bg.get_rect(), border_radius=8)
        pygame.draw.rect(bg, (*C["accent"], 180), bg.get_rect(), 1, border_radius=8)
        self.screen.blit(bg, (tx, ty))
        pygame.draw.rect(self.screen, C["accent"], (tx, ty+6, 3, lh-12), border_radius=2)

        y0 = ty + pad
        self._txt(self.f_btn,   lines[0], C["text_accent"], tx+pad+4, y0)
        self._txt(self.f_small, lines[1], C["text_main"],   tx+pad+4, y0+19)
        self._txt(self.f_small, lines[2], C["text_muted"],  tx+pad+4, y0+38)

    def _txt(self, font, text, color, x, y, anchor="topleft"):
        s = font.render(text, True, color)
        self.screen.blit(s, s.get_rect(**{anchor: (x, y)}))

    def _rect(self, color, rect, radius=6, border_col=None):
        pygame.draw.rect(self.screen, color, rect, border_radius=radius)
        if border_col:
            pygame.draw.rect(self.screen, border_col, rect, 1, border_radius=radius)

    def handle_event(self, ev):
        mx, my = pygame.mouse.get_pos()
        if ev.type == pygame.QUIT: return False
        if ev.type == pygame.MOUSEWHEEL:
            self.scroll_y = max(0, min(self.scroll_max, self.scroll_y - ev.y*22))

        if ev.type == pygame.MOUSEMOTION:
            self.hover_btn_calc = self.calc_rect.collidepoint(mx, my)
            self.hover_btn_swap = self.swap_rect.collidepoint(mx, my)
            self.hover_state = None
            self.hover_edge  = None
            if mx > self.MAP_X:
                for nome in ESTADOS_GEO:
                    if nome not in self.grafo.adjacencia: continue
                    px, py = self.state_px(nome)
                    if math.hypot(mx-px, my-py) < 14:
                        self.hover_state = nome
                        break
                if not self.hover_state:
                    THRESH = 7
                    best_d = THRESH + 1
                    best_e = None
                    for aresta in ARESTAS:
                        de, para = aresta[0], aresta[1]
                        if de not in ESTADOS_GEO or para not in ESTADOS_GEO: continue
                        ax, ay = self.state_px(de)
                        bx, by = self.state_px(para)
                        d = self._dist_seg(mx, my, ax, ay, bx, by)
                        if d < best_d:
                            best_d = d
                            best_e = aresta
                    self.hover_edge = best_e

        if ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
            if mx > self.MAP_X:
                hit_node = False
                for nome in ESTADOS_GEO:
                    if nome not in self.grafo.adjacencia: continue
                    px, py = self.state_px(nome)
                    if math.hypot(mx-px, my-py) < 14:
                        hit_node = True
                        if not self.dd_orig.selected:
                            self.dd_orig.selected = nome
                        elif not self.dd_dest.selected:
                            self.dd_dest.selected = nome
                        else:
                            self.dd_orig.selected = nome
                            self.dd_dest.selected = None
                        self.origem  = self.dd_orig.selected
                        self.destino = self.dd_dest.selected
                        break

                if not hit_node:
                    THRESH = 7
                    best_d = THRESH + 1
                    best_e = None
                    for aresta in ARESTAS:
                        de, para = aresta[0], aresta[1]
                        if de not in ESTADOS_GEO or para not in ESTADOS_GEO: continue
                        ax, ay = self.state_px(de)
                        bx, by = self.state_px(para)
                        d = self._dist_seg(mx, my, ax, ay, bx, by)
                        if d < best_d:
                            best_d = d
                            best_e = aresta
                    if best_e and best_e == self.clicked_edge: self.clicked_edge = None
                    elif best_e: self.clicked_edge = best_e
                    else: self.clicked_edge = None

            if self.swap_rect.collidepoint(mx, my):
                self.dd_orig.selected, self.dd_dest.selected = self.dd_dest.selected, self.dd_orig.selected
                self.origem  = self.dd_orig.selected
                self.destino = self.dd_dest.selected
                if self.origem and self.destino: self._calcular()
            if self.calc_rect.collidepoint(mx, my):
                self.origem  = self.dd_orig.selected
                self.destino = self.dd_dest.selected
                self._calcular()

        if self.dd_orig.handle_event(ev): self.origem  = self.dd_orig.selected
        if self.dd_dest.handle_event(ev): self.destino = self.dd_dest.selected
        return True

    def _calcular(self):
        self.error_msg = ""
        self.caminho   = []
        self.scroll_y  = 0
        if not self.origem or not self.destino:
            self.error_msg = "Selecione origem e destino."; return
        if self.origem == self.destino:
            self.error_msg = "Origem e destino são iguais."; return
        dist, cam = dijkstra(self.grafo, self.origem, self.destino)
        if not cam:
            self.error_msg = "Sem rota conectada."
        else:
            self.caminho   = cam
            self.distancia = dist

    def run(self):
        running = True
        while running:
            for ev in pygame.event.get():
                if not self.handle_event(ev): running = False
            self.screen.fill(C["bg"])
            self.draw_map()
            self.draw_panel()
            self.dd_orig.draw_dropdown(self.screen)
            self.dd_dest.draw_dropdown(self.screen)
            pygame.display.flip()
            self.clock.tick(60)
        pygame.quit()
        sys.exit()


class Dropdown:
    ROW_H = 28
    MAX_V = 9

    def __init__(self, app, options, x, y, w, h):
        self.app     = app
        self.options = options
        self.x, self.y, self.w, self.h = x, y, w, h
        self.selected = None
        self.open     = False
        self.scroll   = 0
        self.fb = pygame.font.SysFont("Arial", 13)
        self.fs = pygame.font.SysFont("Arial", 10)

    def draw(self, surface):
        r  = pygame.Rect(self.x, self.y, self.w, self.h)
        bc = C["select_open"] if self.open else C["select"]
        pygame.draw.rect(surface, bc, r, border_radius=6)
        pygame.draw.rect(surface, C["accent"] if self.open else C["panel_border"], r, 1, border_radius=6)
        txt = self.selected or "Selecione..."
        col = C["text_main"] if self.selected else C["text_light"]
        surface.blit(self.fb.render(txt, True, col), (self.x+10, self.y+10))
        surface.blit(self.fs.render("▲" if self.open else "▼", True, C["accent"]), (self.x+self.w-18, self.y+12))

    def draw_dropdown(self, surface):
        if not self.open: return
        vis = self.options[self.scroll:self.scroll+self.MAX_V]
        dh  = len(vis)*self.ROW_H + 6
        dr  = pygame.Rect(self.x, self.y+self.h+2, self.w, dh)
        bg  = pygame.Surface((self.w, dh), pygame.SRCALPHA)
        pygame.draw.rect(bg, (*C["panel"], 245), bg.get_rect(), border_radius=6)
        pygame.draw.rect(bg, (*C["panel_border"], 200), bg.get_rect(), 1, border_radius=6)
        surface.blit(bg, (dr.x, dr.y))
        mx, my = pygame.mouse.get_pos()
        for i, opt in enumerate(vis):
            ry  = dr.y + 3 + i*self.ROW_H
            row = pygame.Rect(self.x+2, ry, self.w-4, self.ROW_H)
            is_hover = row.collidepoint(mx, my)
            is_sel   = opt == self.selected
            if is_sel: pygame.draw.rect(surface, C["accent"], row, border_radius=4)
            elif is_hover: pygame.draw.rect(surface, C["select_hover"], row, border_radius=4)
            uf = ESTADOS_GEO[opt]["uf"] if opt in ESTADOS_GEO else ""
            tc = C["btn_text"] if is_sel else C["text_main"]
            surface.blit(self.fb.render(f"{uf}  {opt}", True, tc), (self.x+10, ry+6))

    def handle_event(self, ev):
        mx, my = pygame.mouse.get_pos()
        box = pygame.Rect(self.x, self.y, self.w, self.h)
        if ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
            if box.collidepoint(mx, my):
                self.open = not self.open
                return False
            if self.open:
                vis = self.options[self.scroll:self.scroll+self.MAX_V]
                dh  = len(vis)*self.ROW_H + 6
                dr  = pygame.Rect(self.x, self.y+self.h+2, self.w, dh)
                if dr.collidepoint(mx, my):
                    i = (my - dr.y - 3) // self.ROW_H
                    if 0 <= i < len(vis):
                        self.selected = vis[i]
                        self.open = False
                        return True
                else: self.open = False
        if ev.type == pygame.MOUSEWHEEL and self.open:
            self.scroll = max(0, min(len(self.options)-self.MAX_V, self.scroll-ev.y))
        return False


if __name__ == "__main__":
    TurisGraphApp().run()
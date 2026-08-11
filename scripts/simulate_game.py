
from __future__ import annotations
from dataclasses import dataclass, field
from pathlib import Path
from collections import Counter, deque
import argparse, csv, json, random, statistics, yaml

ROOT = Path(__file__).resolve().parents[1]

def load_yaml(path: Path):
    with path.open(encoding="utf-8") as f:
        return yaml.safe_load(f)

GAME = load_yaml(ROOT/"data/rules/game.yaml")["game"]
LOCATIONS = load_yaml(ROOT/"data/rules/locations.yaml")["locations"]
CRYSTALS = load_yaml(ROOT/"data/rules/crystals.yaml")["crystals"]
SHADOW_MASTER = load_yaml(ROOT/"data/rules/shadow-master.yaml")["shadow_master"]
HEROES = load_yaml(ROOT/"data/heroes/heroes.yaml")["heroes"]["items"]
BOARD = load_yaml(ROOT/"data/board/board.yaml")["board"]
ADV_DECK = load_yaml(ROOT/"data/cards/adventure.yaml")["deck"]["cards"]
SHADOW_DECK = load_yaml(ROOT/"data/cards/shadow.yaml")["deck"]["cards"]
CONFIG = load_yaml(ROOT/"data/simulation/pass.yaml")["simulation_pass"]

HERO_IDS = [h["id"] for h in HEROES]
ELEMENT_LOCATIONS = ["fire", "water", "wind", "earth"]
CRYSTAL_BY_LOCATION = {x["location"]: x["id"] for x in CRYSTALS["items"]}
LOCATION_BY_CRYSTAL = {x["id"]: x["location"] for x in CRYSTALS["items"]}
ADJ = {x["id"]: [] for x in LOCATIONS}
for a,b in BOARD["paths"]:
    ADJ[a].append(b); ADJ[b].append(a)

def shortest_path(start: str, goal: str) -> list[str]:
    if start == goal: return [start]
    q=deque([[start]])
    seen={start}
    while q:
        path=q.popleft()
        for nxt in ADJ[path[-1]]:
            if nxt in seen: continue
            np=path+[nxt]
            if nxt==goal: return np
            seen.add(nxt); q.append(np)
    raise RuntimeError((start,goal))

def expanded(cards):
    out=[]
    for c in cards:
        out += [dict(c) for _ in range(c.get("count",1))]
    return out

@dataclass
class Hero:
    id: str
    location: str = "training"
    energy: int = 3
    shields: int = 0
    blocked: bool = False
    crystal_fights: int = 0
    boss_fights: int = 0
    energy_lost: int = 0
    shields_used: int = 0

@dataclass
class GameState:
    strategy: str
    light: int
    rng: random.Random
    disabled: set[str]
    heroes: dict[str,Hero] = field(default_factory=dict)
    crystals: set[str] = field(default_factory=set)
    shadow_health: int = 4
    turn: int = 0
    action_counts: Counter = field(default_factory=Counter)
    card_counts: Counter = field(default_factory=Counter)
    crystal_turn: dict[str,int] = field(default_factory=dict)
    crystal_order: list[str] = field(default_factory=list)
    location_power_uses: Counter = field(default_factory=Counter)
    hero_ability_uses: Counter = field(default_factory=Counter)
    crystal_reward_uses: Counter = field(default_factory=Counter)
    light_loss_sources: Counter = field(default_factory=Counter)
    zero_energy_events: int = 0
    boss_phase_start: int|None = None
    log: list[dict] = field(default_factory=list)
    adv_draw: list[dict] = field(default_factory=list)
    adv_discard: list[dict] = field(default_factory=list)
    shadow_draw: list[dict] = field(default_factory=list)
    shadow_discard: list[dict] = field(default_factory=list)

    def __post_init__(self):
        self.starting_light=self.light
        self.heroes={hid:Hero(hid) for hid in HERO_IDS}
        self.adv_draw=expanded(ADV_DECK); self.rng.shuffle(self.adv_draw)
        self.shadow_draw=expanded(SHADOW_DECK); self.rng.shuffle(self.shadow_draw)

def draw_from(state, kind):
    draw = state.adv_draw if kind=="adv" else state.shadow_draw
    discard = state.adv_discard if kind=="adv" else state.shadow_discard
    if not draw:
        draw.extend(discard); discard.clear(); state.rng.shuffle(draw)
    card=draw.pop()
    return card

def discard_to(state,kind,card,bottom=False):
    if kind=="adv":
        if bottom: state.adv_draw.insert(0,card)
        else: state.adv_discard.append(card)
    else:
        state.shadow_discard.append(card)

def choose_low_energy(state):
    return min(state.heroes.values(),key=lambda h:(h.energy,h.shields)).id

def gain_energy(state,hid,amount):
    h=state.heroes[hid]; h.energy=min(5,h.energy+amount)

def gain_shield(state,hid,amount):
    h=state.heroes[hid]; h.shields=min(2,h.shields+amount)

def lose_light(state,source,amount=1):
    state.light=max(0,state.light-amount)
    state.light_loss_sources[source]+=amount

def prevent_energy_loss(state,h,allow_shield=True):
    if allow_shield and h.shields>0:
        h.shields-=1; h.shields_used+=1
        return True
    return False

def lose_energy(state,h,amount=1,allow_shield=True):
    for _ in range(amount):
        if prevent_energy_loss(state,h,allow_shield):
            continue
        h.energy-=1; h.energy_lost+=1
        if h.energy<=0:
            state.zero_energy_events+=1
            h.location="training"; h.energy=2
            h.blocked=False


def card_value(card, state, h):
    cid=card["id"]
    base={
      "adventure_element_power":6,
      "adventure_weak_point":7 if h.location in ELEMENT_LOCATIONS and CRYSTAL_BY_LOCATION[h.location] not in state.crystals else 3,
      "adventure_teamwork":5,
      "adventure_old_map":5,
      "adventure_energy":5 if h.energy<4 else 2,
      "adventure_passage":4, "adventure_help":4,
      "adventure_shadow_guard":-2, "adventure_rocks":-2,
      "adventure_whisper":-7,
    }.get(cid,0)
    if state.strategy=="aggressive" and cid in {"adventure_element_power","adventure_weak_point","adventure_passage"}: base+=2
    if state.strategy=="cautious" and cid in {"adventure_old_map","adventure_energy","adventure_help"}: base+=2
    return base


def resolve_adventure(state,h,card):
    cid=card["id"]; state.card_counts[cid]+=1
    if cid=="adventure_element_power":
        gain_energy(state,h.id,1)
        goal=choose_target(state,h); path=shortest_path(h.location,goal)
        if len(path)>1: h.location=path[1]
    elif cid=="adventure_weak_point":
        if h.location in ELEMENT_LOCATIONS and CRYSTAL_BY_LOCATION[h.location] not in state.crystals:
            fight_guardian(state,h,extra_bonus=1,counts_as_action=False)
        else:
            gain_energy(state,h.id,1)
    elif cid=="adventure_teamwork":
        target=min(state.heroes.values(),key=lambda x:(len(shortest_path(x.location,choose_target(state,x))),x.energy))
        same_before=target.location==h.location
        goal=choose_target(state,target); path=shortest_path(target.location,goal)
        if len(path)>1: target.location=path[1]
        if same_before: gain_energy(state,target.id,1)
    elif cid=="adventure_old_map":
        amount=2 if h.location=="workshop" else 1
        targets=[x for x in state.heroes.values() if x.location==h.location]
        for _ in range(amount):
            eligible=[x for x in targets if x.shields<2]
            if not eligible: break
            gain_shield(state,min(eligible,key=lambda x:(x.shields,x.energy)).id,1)
    elif cid=="adventure_shadow_guard":
        if state.rng.randint(1,6)<3: lose_energy(state,h)
    elif cid=="adventure_energy":
        # Strategy chooses between immediate energy and buying back time.
        missing_light=state.starting_light-state.light
        choose_light=False
        if missing_light>0:
            if state.strategy=="balanced":
                choose_light = state.light <= max(3, state.starting_light-2)
            elif state.strategy=="cautious":
                choose_light = state.light < state.starting_light
            else:
                choose_light = state.light <= 2 and h.energy>=3
        if choose_light:
            state.light=min(state.starting_light,state.light+1)
            state.card_counts["adventure_energy_light_choice"]+=1
        else:
            gain_energy(state,h.id,1)
            state.card_counts["adventure_energy_energy_choice"]+=1
    elif cid=="adventure_passage":
        goal=choose_target(state,h); path=shortest_path(h.location,goal)
        if len(path)>1: h.location=path[1]
    elif cid=="adventure_help":
        same=[x for x in state.heroes.values() if x.location==h.location]
        gain_energy(state,min(same,key=lambda x:x.energy).id if same else h.id,1)
    elif cid=="adventure_rocks":
        if state.rng.randint(1,6)<4: lose_energy(state,h)
    elif cid=="adventure_whisper":
        lose_light(state,"adventure_whisper")
    discard_to(state,"adv",card)


def explore(state,h):
    state.action_counts["explore"]+=1
    if h.id=="water_guardian" and "hero:water_guardian" not in state.disabled:
        state.hero_ability_uses["water_guardian"]+=1
        c1=draw_from(state,"adv"); c2=draw_from(state,"adv")
        chosen,other=(c1,c2) if card_value(c1,state,h)>=card_value(c2,state,h) else (c2,c1)
        discard_to(state,"adv",other,bottom=True)
        resolve_adventure(state,h,chosen)
    else:
        resolve_adventure(state,h,draw_from(state,"adv"))

def fight_bonus(state,h,guardian=True):
    bonus=0
    if h.id=="fire_guardian" and "hero:fire_guardian" not in state.disabled:
        bonus+=1; state.hero_ability_uses["fire_guardian"]+=1
    if guardian and h.location=="fire":
        fire_present=any(x.location=="fire" and x.id=="fire_guardian" for x in state.heroes.values())
        if fire_present and "location:fire" not in state.disabled and bonus==0:
            bonus+=1; state.location_power_uses["fire"]+=1
    return bonus

def collect_crystal(state,h,loc):
    cid=CRYSTAL_BY_LOCATION[loc]
    state.crystals.add(cid); state.crystal_turn[cid]=state.turn; state.crystal_order.append(cid)
    if len(state.crystals)==4 and state.boss_phase_start is None: state.boss_phase_start=state.turn
    if cid=="fire_crystal" and "reward:fire_crystal" not in state.disabled:
        gain_energy(state,choose_low_energy(state),1); state.crystal_reward_uses[cid]+=1
    elif cid=="water_crystal" and "reward:water_crystal" not in state.disabled:
        for hid in HERO_IDS: gain_energy(state,hid,1)
        state.crystal_reward_uses[cid]+=1
    elif cid=="wind_crystal" and "reward:wind_crystal" not in state.disabled:
        target=state.heroes[choose_low_energy(state)]
        goal=choose_target(state,target); path=shortest_path(target.location,goal)
        if len(path)>1: target.location=path[1]
        state.crystal_reward_uses[cid]+=1
    elif cid=="earth_crystal" and "reward:earth_crystal" not in state.disabled:
        for _ in range(2):
            target=min(state.heroes.values(),key=lambda x:(x.shields,x.energy))
            gain_shield(state,target.id,1)
        state.crystal_reward_uses[cid]+=1

def spend_shield_for_attack(state,h):
    """Spend 1 Shield before a combat roll for +1, if available."""
    if h.shields <= 0:
        return 0
    h.shields -= 1
    h.shields_used += 1
    state.action_counts["shield_attack_bonus"] += 1
    return 1

def fight_guardian(state,h,extra_bonus=0,counts_as_action=True):
    if counts_as_action: state.action_counts["fight_guardian"]+=1
    h.crystal_fights+=1
    bonus=fight_bonus(state,h,True)+extra_bonus+spend_shield_for_attack(state,h)
    roll=state.rng.randint(1,6)
    success=roll+bonus>=4
    if not success and h.location=="wind":
        wind_present=any(x.location=="wind" and x.id=="wind_guardian" for x in state.heroes.values())
        if wind_present and "location:wind" not in state.disabled:
            state.location_power_uses["wind"]+=1
            roll=state.rng.randint(1,6); success=roll+bonus>=4
    if success:
        collect_crystal(state,h,h.location)
        if h.location=="water":
            water_present=any(x.location=="water" and x.id=="water_guardian" for x in state.heroes.values())
            if water_present and "location:water" not in state.disabled:
                gain_energy(state,h.id,1); state.location_power_uses["water"]+=1
    else:
        earth_safe=(h.location=="earth" and
                    any(x.location=="earth" and x.id=="earth_guardian" for x in state.heroes.values()) and
                    "location:earth" not in state.disabled)
        if earth_safe: state.location_power_uses["earth"]+=1
        else: lose_energy(state,h)

def fight_shadow_master(state,h):
    state.action_counts["fight_shadow_master"]+=1; h.boss_fights+=1
    bonus=fight_bonus(state,h,False)+spend_shield_for_attack(state,h)
    if state.rng.randint(1,6)+bonus>=4:
        state.shadow_health-=1
    else:
        lose_energy(state,h)
        lose_light(state,"shadow_master_failure")

def resolve_shadow(state,h):
    card=draw_from(state,"shadow"); cid=card["id"]; state.card_counts[cid]+=1
    if cid=="shadow_rises":
        lose_light(state,"shadow_rises")
    elif cid=="shadow_ambush":
        if state.rng.randint(1,6)<3: lose_energy(state,h)
    elif cid in {"shadow_block", "shadow_fog"}:
        h.blocked=True
    elif cid=="shadow_grip":
        lose_energy(state,h)
    discard_to(state,"shadow",card)

def uncollected_locations(state):
    return [loc for loc in ELEMENT_LOCATIONS if CRYSTAL_BY_LOCATION[loc] not in state.crystals]

def target_score(state,h,loc):
    dist=len(shortest_path(h.location,loc))-1
    score=-dist*2
    # Hero/place synergies.
    if loc=="fire" and h.id=="fire_guardian": score+=3
    if loc=="water" and h.id=="water_guardian": score+=2
    if loc=="wind" and h.id=="wind_guardian": score+=3
    if loc=="earth" and h.id=="earth_guardian": score+=2
    # Crystal rewards.
    if loc=="water": score+=3
    if loc=="earth": score+=2
    if loc=="wind": score+=1
    if state.strategy=="aggressive": score+=2
    if state.strategy=="cautious" and h.energy<=2: score-=2
    return score

def choose_target(state,h):
    if len(state.crystals)==4: return "temple"
    options=uncollected_locations(state)
    return max(options,key=lambda loc:target_score(state,h,loc))

def should_prepare(state,h):
    if state.strategy=="aggressive":
        return h.energy<=1
    if state.strategy=="balanced":
        return h.energy<=2 or (h.shields==0 and len(state.crystals)>=2)
    return h.energy<=3 or h.shields==0

def action_goal(state,h):
    if len(state.crystals)==4: return "temple"
    if should_prepare(state,h):
        if h.energy<=2: return "training"
        if h.shields==0: return "workshop"
    return choose_target(state,h)

def move_toward(state,h,goal):
    if h.blocked:
        h.blocked=False
        return
    steps=2 if h.id=="wind_guardian" and "hero:wind_guardian" not in state.disabled else 1
    if steps==2: state.hero_ability_uses["wind_guardian"]+=1
    path=shortest_path(h.location,goal)
    h.location=path[min(steps,len(path)-1)]

def choose_action(state,h):
    # Immediate valid fights.
    if h.location in ELEMENT_LOCATIONS and CRYSTAL_BY_LOCATION[h.location] not in state.crystals:
        if state.strategy=="cautious" and h.energy<=2 and h.shields==0:
            return "explore"
        return "fight_guardian"
    if h.location=="temple" and len(state.crystals)==4:
        return "fight_shadow_master"
    if h.location=="training":
        if h.energy<5 and should_prepare(state,h): return "train"
        return None
    if h.location=="workshop":
        if h.shields<2 and should_prepare(state,h): return "build"
        if state.strategy!="aggressive": return "explore"
    if h.location in ELEMENT_LOCATIONS:
        if state.strategy=="aggressive" and h.energy>=2: return "explore"
        if state.strategy=="balanced" and (h.energy<=3): return "explore"
        if state.strategy=="cautious" and (h.energy<5): return "explore"
    return None

def take_turn(state,h):
    state.turn+=1
    before=(h.location,h.energy,h.shields,state.light,len(state.crystals),state.shadow_health)
    goal=action_goal(state,h)
    if h.location!=goal or h.blocked:
        move_toward(state,h,goal)
    action=choose_action(state,h)
    if action=="fight_guardian": fight_guardian(state,h)
    elif action=="fight_shadow_master": fight_shadow_master(state,h)
    elif action=="explore": explore(state,h)
    elif action=="train":
        state.action_counts["train"]+=1; gain_energy(state,h.id,2)
    elif action=="build":
        state.action_counts["build"]+=1
        earth_global=(h.id=="earth_guardian" and "hero:earth_guardian" not in state.disabled)
        targets=list(state.heroes.values()) if earth_global else [
            x for x in state.heroes.values() if x.location==h.location
        ]
        if earth_global:
            state.hero_ability_uses["earth_guardian"]+=1
        for _ in range(2):
            eligible=[x for x in targets if x.shields<2]
            if not eligible: break
            target=min(eligible,key=lambda x:(x.shields,x.energy))
            gain_shield(state,target.id,1)
    else:
        state.action_counts["move_only"]+=1
    if state.shadow_health>0 and state.light>0:
        resolve_shadow(state,h)
    after=(h.location,h.energy,h.shields,state.light,len(state.crystals),state.shadow_health)
    if len(state.log)<200:
        state.log.append({"turn":state.turn,"hero":h.id,"action":action or "move_only",
                          "before":before,"after":after})

def simulate(seed,strategy,light,disabled=None,log=False):
    state=GameState(strategy,light,random.Random(seed),set(disabled or []))
    max_turns=160
    while state.light>0 and state.shadow_health>0 and state.turn<max_turns:
        for hid in HERO_IDS:
            take_turn(state,state.heroes[hid])
            if state.light<=0 or state.shadow_health<=0: break
    win=state.shadow_health<=0
    total_actions=sum(v for k,v in state.action_counts.items() if k!="shield_attack_bonus") or 1
    return {
      "win":int(win), "turns":state.turn, "rounds":state.turn/4,
      "light_end":state.light, "crystals":len(state.crystals),
      "shadow_health_end":state.shadow_health,
      "boss_phase_turns":0 if state.boss_phase_start is None else state.turn-state.boss_phase_start+1,
      "zero_energy_events":state.zero_energy_events,
      "explore_share":state.action_counts["explore"]/total_actions,
      "fight_share":(state.action_counts["fight_guardian"]+state.action_counts["fight_shadow_master"])/total_actions,
      "build_share":state.action_counts["build"]/total_actions,
      "train_share":state.action_counts["train"]/total_actions,
      "action_counts":dict(state.action_counts),
      "card_counts":dict(state.card_counts),
      "crystal_turn":state.crystal_turn,
      "crystal_order":state.crystal_order,
      "hero_crystal_fights":{h.id:h.crystal_fights for h in state.heroes.values()},
      "hero_boss_fights":{h.id:h.boss_fights for h in state.heroes.values()},
      "hero_energy_lost":{h.id:h.energy_lost for h in state.heroes.values()},
      "hero_shields_used":{h.id:h.shields_used for h in state.heroes.values()},
      "hero_ability_uses":dict(state.hero_ability_uses),
      "location_power_uses":dict(state.location_power_uses),
      "crystal_reward_uses":dict(state.crystal_reward_uses),
      "light_loss_sources":dict(state.light_loss_sources),
      "log":state.log if log else []
    }

def mean(rows,key):
    return statistics.mean(r[key] for r in rows)

def flatten_summary(rows,strategy,difficulty,light):
    wins=sum(r["win"] for r in rows)
    actions=Counter(); cards=Counter(); light_sources=Counter()
    hero_crystal=Counter(); hero_boss=Counter(); abilities=Counter(); powers=Counter()
    for r in rows:
        actions.update(r["action_counts"]); cards.update(r["card_counts"])
        light_sources.update(r["light_loss_sources"]); hero_crystal.update(r["hero_crystal_fights"])
        hero_boss.update(r["hero_boss_fights"]); abilities.update(r["hero_ability_uses"])
        powers.update(r["location_power_uses"])
    total_actions=sum(actions.values()) or 1
    return {
      "strategy":strategy,"difficulty":difficulty,"start_light":light,"games":len(rows),
      "win_rate":wins/len(rows),"avg_rounds":mean(rows,"rounds"),
      "avg_turns":mean(rows,"turns"),"avg_light_end":mean(rows,"light_end"),
      "avg_crystals":mean(rows,"crystals"),"avg_boss_phase_turns":mean(rows,"boss_phase_turns"),
      "avg_zero_energy_events":mean(rows,"zero_energy_events"),
      "explore_share":actions["explore"]/total_actions,
      "fight_share":(actions["fight_guardian"]+actions["fight_shadow_master"])/total_actions,
      "build_share":actions["build"]/total_actions,"train_share":actions["train"]/total_actions,
      "shadow_light_loss_per_game":light_sources["shadow_rises"]/len(rows),
      "adventure_light_loss_per_game":light_sources["adventure_whisper"]/len(rows),
      "boss_light_loss_per_game":light_sources["shadow_master_failure"]/len(rows),
      "fire_crystal_fight_share":hero_crystal["fire_guardian"]/max(1,sum(hero_crystal.values())),
      "water_crystal_fight_share":hero_crystal["water_guardian"]/max(1,sum(hero_crystal.values())),
      "wind_crystal_fight_share":hero_crystal["wind_guardian"]/max(1,sum(hero_crystal.values())),
      "earth_crystal_fight_share":hero_crystal["earth_guardian"]/max(1,sum(hero_crystal.values())),
      "fire_ability_uses_per_game":abilities["fire_guardian"]/len(rows),
      "water_ability_uses_per_game":abilities["water_guardian"]/len(rows),
      "wind_ability_uses_per_game":abilities["wind_guardian"]/len(rows),
      "earth_ability_uses_per_game":abilities["earth_guardian"]/len(rows),
      "fire_place_uses_per_game":powers["fire"]/len(rows),
      "water_place_uses_per_game":powers["water"]/len(rows),
      "wind_place_uses_per_game":powers["wind"]/len(rows),
      "earth_place_uses_per_game":powers["earth"]/len(rows),
    }

def run_all(outdir:Path):
    outdir.mkdir(parents=True,exist_ok=True)
    seed=int(CONFIG["seed"])
    n=int(CONFIG["games_per_strategy_and_difficulty"])
    summary=[]; sample=[]
    for si,strategy in enumerate(CONFIG["strategies"]):
        for di,(difficulty,light) in enumerate(CONFIG["difficulties"].items()):
            rows=[]
            for i in range(n):
                rows.append(simulate(seed+si*1000000+di*100000+i,strategy,int(light)))
            summary.append(flatten_summary(rows,strategy,difficulty,int(light)))
            sample.append({"strategy":strategy,"difficulty":difficulty,
                           "result":simulate(seed+9000000+si*100+di,strategy,int(light),log=True)})
    with (outdir/"summary.csv").open("w",newline="",encoding="utf-8") as f:
        w=csv.DictWriter(f,fieldnames=list(summary[0])); w.writeheader(); w.writerows(summary)
    with (outdir/"sample-games.json").open("w",encoding="utf-8") as f:
        json.dump(sample,f,ensure_ascii=False,indent=2)

    # Ablation tests: balanced/normal baseline and one disabled feature.
    abl_n=int(CONFIG["ablation_games"])
    features=[
      "hero:fire_guardian","hero:water_guardian","hero:wind_guardian","hero:earth_guardian",
      "location:fire","location:water","location:wind","location:earth",
      "reward:fire_crystal","reward:water_crystal","reward:wind_crystal","reward:earth_crystal"
    ]
    base=[simulate(seed+20000000+i,"balanced",8) for i in range(abl_n)]
    base_win=statistics.mean(x["win"] for x in base)
    base_rounds=statistics.mean(x["rounds"] for x in base)
    ablations=[]
    for fi,feature in enumerate(features):
        rows=[simulate(seed+21000000+fi*100000+i,"balanced",8,{feature}) for i in range(abl_n)]
        wr=statistics.mean(x["win"] for x in rows)
        rounds=statistics.mean(x["rounds"] for x in rows)
        ablations.append({"feature":feature,"games":abl_n,"baseline_win_rate":base_win,
                          "disabled_win_rate":wr,"win_rate_delta":wr-base_win,
                          "baseline_rounds":base_rounds,"disabled_rounds":rounds,
                          "round_delta":rounds-base_rounds})
    with (outdir/"ablation.csv").open("w",newline="",encoding="utf-8") as f:
        w=csv.DictWriter(f,fieldnames=list(ablations[0])); w.writeheader(); w.writerows(ablations)
    return summary,ablations

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--output",default=str(ROOT/"output/simulation"))
    args=ap.parse_args()
    summary,ablations=run_all(Path(args.output))
    print(json.dumps({"summary_rows":len(summary),"ablation_rows":len(ablations)},indent=2))

if __name__=="__main__":
    main()

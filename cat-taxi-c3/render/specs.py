import os
# Sprite specs. Each code string runs against window.__api; the element is drawn around anchor (x,y).
import json
A = (210, 373)
S = []
def add(name, code, anchor=A, mode="alpha"):
    S.append({"name": name, "code": code, "ax": anchor[0], "ay": anchor[1], "mode": mode})
# vehicles
add("veh_taxi", "api.drawCar(210,373,1,'#edb847','taxi',0)")
add("veh_blue", "api.drawPlayerVehicle(210,373,1,0,'blue')")
add("veh_mint", "api.drawPlayerVehicle(210,373,1,0,'mint')")
# enemies
add("enemy_police", "api.policeVan(210,373,1,'#f2f1e9',false)")
add("enemy_ambulance", "api.policeVan(210,373,1,'#f1f4e3',true)")
add("enemy_van", "api.policeVan(210,373,1,'#6d92c4',false)")
for k in ["convoy", "armored", "green", "orange", "police"]:
    add(f"boss_{k}", f"api.bossTruck(210,373,1,'{k}')")
# pickups, hazards, icons
add("pick_crate", "api.supplyCrate(210,373,1)")
add("pick_coin", "api.coin(210,373,20)")
add("pick_gem", "api.gem(210,373,20)")
add("shot_dynamite", "api.dynamiteSprite(210,373,1,0)")
add("shot_warning", "api.roadWarning(210,373,30,1)")
for k in ["pistol", "bomb", "shot", "machine"]:
    add(f"wpn_{k}", f"api.weaponIcon('{k}',210,373,1)")
add("key_on", "api.keyIcon(210,373,true)")
add("key_off", "api.keyIcon(210,373,false)")
add("cloud_home", "api.cloud(210,373,1,'#fffef2','#bfc0b7',1)")
add("title_logo", "api.drawTitleLogo(373)", anchor=(210, 373))
# cats
for n, fur, expr in [("cat_a", "'#e9d0a0'", "'happy'"), ("cat_b", "'#ecc6ba'", "'cool'"), ("cat_c", "'#e8ca9f'", "'happy'"),
                     ("cat_d", "'#d2bda1'", "'happy'"), ("cat_e", "'#f3d5ac'", "'happy'"), ("cat_f", "'#f4e6c5'", "'happy'")]:
    add(name=n, code=f"api.kitty(210,373,1,{fur},{expr})")
# backgrounds (opaque)
for th in ["city", "blue", "mountain", "sunset", "rose"]:
    add(f"bg_{th}", f"api.drawBackdrop('{th}',false)", mode="opaque")
add("bg_paper", "api.backgroundPaper()", mode="opaque")
add("bg_garage", "api.garageBg()", mode="opaque")
add("bg_map", "api.mapDecor();api.mapSign();api.mapTrack();api.mapDecor2()", mode="opaque")
add("veh_taxi_home", "api.drawCar(210,373,1,'#f2bf4f','taxi',0)")
for st in ["normal", "active", "locked"]:
    add(f"node_{st}", f"api.node(210,373,'{st}')")
add("roulette_base", "api.rbase()", anchor=(210, 373))
add("bg_black", "api.ctx.fillStyle='#050505';api.ctx.fillRect(0,0,420,746)", mode="opaque")
add("wheel", "api.wheel(0)", anchor=(210, 315))
add("fx_blast", "api.cloud(210,373,1,'#fff7e9','#ba9985',1)")
add("fx_burst", "api.cloud(210,373,1,'#fffdfa','#9c9790',1)")
add("fx_hurt", "api.cloud(210,373,1,'#f2c4b4','#de7659',1)")
add("fx_miss", "api.cloud(210,373,0.65,'#fffdf7','#aea99b',1)")
json.dump(S, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "specs.json"), "w"), indent=1, ensure_ascii=False)
print("specs", len(S))

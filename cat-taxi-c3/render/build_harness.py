import os
# Builds render/harness.html from the user's HTML: same game code, plus an API object exposing draw functions.
# Only additions: DPR fixed at 1, requestAnimationFrame disabled, and window.__api before the IIFE closes.
import re
SRC = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "source", "cat_taxi_v9.html")
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "harness.html")
src = open(SRC, encoding="utf-8").read()
lines = src.split("\n")
def line(n):  # 1-based
    return lines[n - 1]
garage_bg = line(319).replace("function garageScreen(){", "function __garageBg(){", 1) + "}"
assert garage_bg.startswith("function __garageBg(){backgroundPaper();"), garage_bg[:60]
assert garage_bg.rstrip().endswith("}") or True
map_decor = "\n".join(line(n) for n in range(296, 302)) + "}"
map_decor = map_decor.replace("function drawMap(){", "function __mapDecor(){", 1)
assert map_decor.startswith("function __mapDecor(){ctx.save()")

map_nodes_fn = """function __node(x,y,st){const active=st==='active',locked=st==='locked';
 if(active)ell(x,y+4,34,18,'#fff08fb0',null);
 fillRound(x-17,y-7,34,24,locked?'#b98a58':'#c89258',4,'#5b4630',1.8);
 polygon([[x-22,y-6],[x,y-23],[x+22,y-6]],active?'#7fc96f':locked?'#8d6239':'#8d5a2e','#5b4630',2);
 fillRound(x-5,y+5,10,12,'#7a5230',2);ell(x-10,y+1,2.4,2.4,'#fff4d6',null);ell(x+10,y+1,2.4,2.4,'#fff4d6',null);
 if(locked){ell(x,y-2,7,8,null,'#3d3b38',2.5);fillRound(x-8,y-1,16,13,'#3d3b38',3)}}"""
map_decor2 = "function __mapDecor2(){" + "\n".join(line(n) for n in range(305, 307)) + "}"
map_sign = "function __mapSign(){" + line(303) + "}"
map_track = "function __mapTrack(){" + line(304) + "}"
rb = """function __rbase(){polygon([[171,483],[249,483],[262,554],[156,554]],'#676663','#4a4542',2);line([[100,554],[318,554]],'#5c5a54',4);polygon([[195,120],[225,120],[210,151]],'#e55a49','#b94c45',2);ell(210,116,11,11,'#e65c4a',null);}"""

extra = f"""
{garage_bg}
{map_decor}
{map_decor2}
{map_nodes_fn}
{map_sign}
{map_track}
{rb}
function __wheel(ang){{
  let radius=167,cx=210,cy=315;
  ctx.save();ctx.translate(cx,cy);ctx.rotate(ang);for(let i=0;i<8;i++){{let a=i*TAU/8-TAU/16- Math.PI/2;ctx.beginPath();ctx.moveTo(0,0);ctx.arc(0,0,radius,a,a+TAU/8);ctx.closePath();ctx.fillStyle=i%2===0?'#fffdfa':'#f8f6ed';ctx.fill();ctx.lineWidth=1.6;ctx.strokeStyle='#aaa69b';ctx.stroke();let mid=a+TAU/16,x=Math.cos(mid)*107,y=Math.sin(mid)*107;
  if(i===3||i===7)gem(x,y,17);else if(i===5){{weaponIcon('shot',x,y,.9)}}else coin(x,y,19);
  if(i!==3&&i!==7&&i!==5)txt(['50','90','150','1','250','?','400','2'][i],x,y+26,12,'#6e5843');}}
  ell(0,0,radius,radius,null,'#4c4b46',9);for(let i=0;i<12;i++){{let a=i*TAU/12;ell(Math.cos(a)*radius,Math.sin(a)*radius,5,5,i%2?'#83c65b':'#eed744',null)}}ell(0,0,20,20,'#626460','#383935',3);ell(0,0,12,12,'#65cb67',null);ctx.restore();
}}
window.__api={{ctx,canvas,drawCar,drawPlayerVehicle,policeVan,bossTruck,kitty,coin,gem,supplyCrate,dynamiteSprite,weaponIcon,keyIcon,cloud,drawBackdrop,drawTitleLogo,roadWarning,backgroundPaper,fillRound,ell,line,polygon,txt,shadow,card,drawBossBar:null,garageBg:__garageBg,mapDecor:__mapDecor,mapDecor2:__mapDecor2,mapSign:__mapSign,mapTrack:__mapTrack,node:__node,rbase:__rbase,wheel:__wheel,THEMES,W,H,TAU}};
"""
i = src.rfind("})();")
assert i > 0 and src.count("})();") == 1
html = src[:i] + extra + src[i:]
boot = "<script>window.requestAnimationFrame=function(){return 0};Object.defineProperty(window,'devicePixelRatio',{get(){return 1}});</script>\n<script>\n(()=>{"
assert html.count("<script>\n(()=>{") == 1
html = html.replace("<script>\n(()=>{", boot, 1)
open(OUT, "w", encoding="utf-8").write(html)
print("harness bytes", len(html))

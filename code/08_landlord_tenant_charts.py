import pandas as pd, numpy as np, ast, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon, Patch
from bokeh.sampledata import us_counties
u=pd.read_csv('units.csv'); u['codes']=u.codes.apply(ast.literal_eval)
exp={'Chesapeake':1964,'Virginia Beach':4934,'Richmond City':5699,'Henrico':5018,'Loudoun':1184,'Gloucester':177,'Waynesboro':217,'Staunton':117,'Charles City':7,'King & Queen':8,'Rappahannock':4}
u['exp']=u.court.map(exp).fillna(0)
u['flag']=((u.exp/u['lt'])>=0.25)|(u['lt']<25)
u['short']=u.court.str.replace('Richmond City','Richmond (city)').str.replace('Roanoke City','Roanoke (city)').str.replace('Roanoke County','Roanoke Co.')
u=u.sort_values('lt_rate',ascending=False).reset_index(drop=True)
u.to_csv('evict_units_final.csv',index=False)
tot=u['lt'].sum()/u.renter_hh.sum()*100; med=u.lt_rate.median()
print(round(tot,2),round(med,2),u.flag.sum())
INK,MUTE,GRID,ACC,GRAY='#1f2937','#6b7280','#e5e7eb','#1d4ed8','#9ca3af'
# ---------- ranked chart
fig,ax=plt.subplots(figsize=(12,6.75),dpi=150)
s=u[~u.flag]; h=u[u.flag]
ax.scatter(s.index,s.lt_rate,s=34,color=ACC,edgecolor='white',linewidth=1,zorder=3)
ax.scatter(h.index,h.lt_rate,s=40,facecolor='white',edgecolor=ACC,linewidth=1.5,zorder=3)
ax.axhline(tot,color=INK,lw=1,ls=(0,(4,3)),zorder=2)
ax.text(62,tot+0.5,f'Statewide: {tot:.1f} per 100 renter households',ha='center',color=INK,fontsize=11,fontweight='bold')
def lab(i,x,y,ha):
    r=u.loc[i]; ax.annotate(f"{r.short}  {r.lt_rate:.1f}  ({int(r['lt']):,} filings)",xy=(i,r.lt_rate),xytext=(x,y),fontsize=10.5,color=INK,ha=ha,va='center',
        arrowprops=dict(arrowstyle='-',color=GRAY,lw=0.8,shrinkA=2,shrinkB=4))
top=[i for i in u.index if not u.flag[i]][:5]
for k,i in enumerate(top): lab(i,30,24.8-k*1.7,"left")
ax.set_ylim(-1.5,26); ax.set_xlim(-2,125)
ax.set_xticks([]); ax.set_yticks([0,5,10,15,20,25]); ax.set_yticklabels([0,5,10,15,20,25],color=MUTE,fontsize=11)
ax.grid(axis='y',color=GRID,lw=0.8,zorder=0)
for sp in ax.spines.values(): sp.set_visible(False)
ax.tick_params(length=0)
ax.set_xlabel('123 court jurisdictions covering all 133 Virginia localities, ranked high to low',color=MUTE,fontsize=10)
ax.scatter(70,22.5,s=40,color=ACC,edgecolor='white'); ax.text(72,22.5,'Reliable count',va='center',fontsize=10.5,color=INK)
ax.scatter(70,21,s=44,facecolor='white',edgecolor=ACC,linewidth=1.5); ax.text(72,21,f'Less certain ({int(u.flag.sum())}): expunged cases missing, or under 25 filings',va='center',fontsize=10.5,color=INK)
fig.text(0.05,0.94,f'Petersburg landlords filed 24 court cases per 100 renter households in 2025. Statewide: {tot:.1f}',fontsize=15.5,fontweight='bold',color=INK)
fig.text(0.05,0.895,'2025 General District Court landlord/tenant filings ÷ renter households, by court jurisdiction. Filings are not evictions.',fontsize=11.5,color=MUTE)
fig.text(0.05,0.03,'Sources: Virginia Judicial System, GDC filings report (Oct. 2026; excludes expunged cases); Census ACS 2020–2024 5-yr (B25003). @thedocshango.bsky.social',fontsize=8.6,color=MUTE)
fig.subplots_adjust(left=0.06,right=0.97,top=0.85,bottom=0.1)
fig.savefig('evict_rank.png',facecolor='white')
# ---------- map
bins=[0,2,4,6,10,100]; labels=['Under 2','2–4','4–6','6–10','10 +']
cols=['#dbeafe','#93c5fd','#3b82f6','#1d4ed8','#1e3a8a']
print(pd.cut(u.lt_rate,bins,labels=labels,right=False).value_counts().sort_index().to_dict())
cm={}
for _,r in u.iterrows():
    for c in r.codes: cm[c]=(cols[np.digitize(r.lt_rate,bins)-1],bool(r.flag))
fig,ax=plt.subplots(figsize=(12,6.75),dpi=150); cent={}
for (st,c),v in us_counties.data.items():
    if st!=51: continue
    lons=np.array(v['lons'],float); lats=np.array(v['lats'],float)
    nan=np.where(np.isnan(lons)|np.isnan(lats))[0]; segs=np.split(np.c_[lons,lats],nan)
    fc,fl=cm.get(c,('#e5e7eb',False))
    for sg in segs:
        sg=sg[~np.isnan(sg).any(axis=1)]
        if len(sg)<3: continue
        ax.add_patch(Polygon(sg,closed=True,facecolor=fc,edgecolor='white',lw=0.6,hatch='////' if fl else None))
    cent[c]=np.nanmean(np.c_[lons,lats],axis=0)
ax.set_xlim(-83.8,-75.0); ax.set_ylim(36.25,39.55); ax.set_aspect(1/np.cos(np.radians(38))); ax.axis('off')
def call(code,txt,xy):
    ax.annotate(txt,xy=cent[code],xytext=xy,fontsize=10,color=INK,fontweight='bold',ha='left',va='center',arrowprops=dict(arrowstyle='-',color=MUTE,lw=0.8,shrinkB=2))
call(730,'Petersburg 24.2',(-79.0,36.33)); call(650,'Hampton 16.3',(-74.9,36.5)) if False else None
fig.text(0.04,0.945,'Landlord/tenant court filings per 100 renter households, 2025: highest around Petersburg and Hampton Roads',fontsize=14,fontweight='bold',color=INK)
fig.text(0.04,0.9,'Statewide: %.1f. Shared courts (e.g. Rockingham + Harrisonburg) shown as one color. Filings are not evictions.'%tot,fontsize=11.5,color=MUTE)
hs=[Patch(facecolor=c,edgecolor='white',label=l) for c,l in zip(cols,labels)]+[Patch(facecolor='white',edgecolor=MUTE,hatch='////',label='Less certain')]
fig.legend(handles=hs,loc='upper left',bbox_to_anchor=(0.03,0.82),frameon=False,fontsize=10,handlelength=1.6,labelcolor=INK)
fig.text(0.04,0.025,'Sources: Virginia Judicial System GDC filings (Oct. 2026; excludes expunged cases); Census ACS 2020–2024 (B25003). Boundaries: 2010 vintage. @thedocshango.bsky.social',fontsize=8.2,color=MUTE)
fig.subplots_adjust(left=0.02,right=0.98,top=0.88,bottom=0.05)
fig.savefig('evict_map.png',facecolor='white')
print(cent[730].round(2))

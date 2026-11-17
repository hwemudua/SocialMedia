import pandas as pd, numpy as np, ast, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon, Patch
from bokeh.sampledata import us_counties
u=pd.read_csv('units.csv'); u['codes']=u.codes.apply(ast.literal_eval)
u['flag']=u.garn<50
u['short']=u.court.str.replace('Richmond City','Richmond (city)').str.replace('Roanoke City','Roanoke (city)').str.replace('Roanoke County','Roanoke Co.').str.replace('Franklin City','Franklin (city)')
u=u.sort_values('garn_per1k',ascending=False).reset_index(drop=True)
u.to_csv('garn_units_final.csv',index=False)
tot=u.garn.sum()/u.households.sum()*1000; med=u.garn_per1k.median()
print(round(tot,1),round(med,1),u.flag.sum())
INK,MUTE,GRID,ACC,GRAY='#1f2937','#6b7280','#e5e7eb','#1d4ed8','#9ca3af'
fig,ax=plt.subplots(figsize=(12,6.75),dpi=150)
s=u[~u.flag]; h=u[u.flag]
ax.scatter(s.index,s.garn_per1k,s=34,color=ACC,edgecolor='white',linewidth=1,zorder=3)
ax.scatter(h.index,h.garn_per1k,s=40,facecolor='white',edgecolor=ACC,linewidth=1.5,zorder=3)
ax.axhline(tot,color=INK,lw=1,ls=(0,(4,3)),zorder=2)
ax.text(70,tot+10,f'Statewide: {tot:.0f} per 1,000 households',ha='center',color=INK,fontsize=11,fontweight='bold')
def lab(i,x,y,ha):
    r=u.loc[i]; ax.annotate(f"{r.short}  {r.garn_per1k:.0f}  ({int(r.garn):,} filings)",xy=(i,r.garn_per1k),xytext=(x,y),fontsize=10.5,color=INK,ha=ha,va='center',
        arrowprops=dict(arrowstyle='-',color=GRAY,lw=0.8,shrinkA=2,shrinkB=4))
rel=[i for i in u.index if not u.flag[i]]
for k,i in enumerate(rel[:5]): lab(i,24,335-k*30,'left')
big=[i for i in rel if u.garn[i]>=500][::-1][:3]
for k,i in enumerate(big): lab(i,112,-30+k*22,'right')
ax.set_ylim(-60,360); ax.set_xlim(-2,125)
ax.set_xticks([]); ax.set_yticks([0,100,200,300]); ax.set_yticklabels([0,100,200,300],color=MUTE,fontsize=11)
ax.grid(axis='y',color=GRID,lw=0.8,zorder=0)
for sp in ax.spines.values(): sp.set_visible(False)
ax.tick_params(length=0)
ax.set_xlabel('123 court jurisdictions covering all 133 Virginia localities, ranked high to low',color=MUTE,fontsize=10)
ax.scatter(72,290,s=40,color=ACC,edgecolor='white'); ax.text(74,290,'Reliable count',va='center',fontsize=10.5,color=INK)
ax.scatter(72,268,s=44,facecolor='white',edgecolor=ACC,linewidth=1.5); ax.text(74,268,f'Fewer than 50 filings ({int(u.flag.sum())})',va='center',fontsize=10.5,color=INK)
fig.text(0.05,0.94,f'Garnishment cases per 1,000 households, 2025: 195 in Newport News, 12 in Alexandria',fontsize=15.5,fontweight='bold',color=INK)
fig.text(0.05,0.895,f'Statewide {tot:.0f}. General District Court garnishment filings ÷ households. One debtor can have several filings.',fontsize=11.5,color=MUTE)
fig.text(0.05,0.03,'Sources: Virginia Judicial System, GDC filings report (Oct. 2026); Census ACS 2020–2024 5-yr (B25003). Filed in the court that issued the judgment. @thedocshango.bsky.social',fontsize=8.6,color=MUTE)
fig.subplots_adjust(left=0.06,right=0.97,top=0.85,bottom=0.1)
fig.savefig('garn_rank.png',facecolor='white')
bins=[0,25,50,100,150,1000]; labels=['Under 25','25–50','50–100','100–150','150 +']
cols=['#dbeafe','#93c5fd','#3b82f6','#1d4ed8','#1e3a8a']
print(pd.cut(u.garn_per1k,bins,labels=labels,right=False).value_counts().sort_index().to_dict())
cm={}
for _,r in u.iterrows():
    for c in r.codes: cm[c]=(cols[np.digitize(r.garn_per1k,bins)-1],bool(r.flag))
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
call(700,'Newport News 195',(-78.0,36.33)); call(595,'Emporia 334',(-79.0,36.52)) if False else None
call(13,'Arlington 13',(-76.7,39.4))
fig.text(0.04,0.945,'Garnishment cases per 1,000 households, 2025: highest in Hampton Roads and Southside',fontsize=14.5,fontweight='bold',color=INK)
fig.text(0.04,0.9,'Statewide: %.0f. Shared courts shown as one color. One debtor can have several filings; filed where the judgment was entered.'%tot,fontsize=11.5,color=MUTE)
hs=[Patch(facecolor=c,edgecolor='white',label=l) for c,l in zip(cols,labels)]+[Patch(facecolor='white',edgecolor=MUTE,hatch='////',label='Under 50 filings')]
fig.legend(handles=hs,loc='upper left',bbox_to_anchor=(0.03,0.82),frameon=False,fontsize=10,handlelength=1.6,labelcolor=INK)
fig.text(0.04,0.025,'Sources: Virginia Judicial System GDC filings (Oct. 2026); Census ACS 2020–2024 (B25003). Boundaries: 2010 vintage. @thedocshango.bsky.social',fontsize=8.2,color=MUTE)
fig.subplots_adjust(left=0.02,right=0.98,top=0.88,bottom=0.05)
fig.savefig('garn_map.png',facecolor='white')

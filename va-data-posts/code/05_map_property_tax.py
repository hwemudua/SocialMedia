import pandas as pd, numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon, Patch
from bokeh.sampledata import us_counties
d=pd.read_csv('data/va_tax_burden_merged.csv',dtype={'county':str})
d['code']=d.county.astype(int); m=d.set_index('code')
bins=[0,1,1.5,2,3,10]; labels=['Under 1%','1–1.5%','1.5–2%','2–3%','3% +']
cols=['#dbeafe','#93c5fd','#3b82f6','#1d4ed8','#1e3a8a']
print(pd.cut(d.pct,bins,labels=labels).value_counts().sort_index().to_dict())
INK,MUTE='#1f2937','#6b7280'
fig,ax=plt.subplots(figsize=(12,6.75),dpi=150)
cent={}
for (st,c),v in us_counties.data.items():
    if st!=51: continue
    lons=np.array(v['lons'],float); lats=np.array(v['lats'],float)
    nan=np.where(np.isnan(lons)|np.isnan(lats))[0]; segs=np.split(np.c_[lons,lats],nan)
    if c in m.index:
        r=m.loc[c]; fc=cols[np.digitize(r.pct,bins)-1]; hatch='////' if r.flag else None
    else: fc='#e5e7eb'; hatch=None
    for sg in segs:
        sg=sg[~np.isnan(sg).any(axis=1)]
        if len(sg)<3: continue
        ax.add_patch(Polygon(sg,closed=True,facecolor=fc,edgecolor='white',lw=0.6,hatch=hatch))
    cent[c]=np.nanmean(np.c_[lons,lats],axis=0)
ax.set_xlim(-83.8,-75.0); ax.set_ylim(36.25,39.55); ax.set_aspect(1/np.cos(np.radians(38))); ax.axis('off')
def call(code,txt,xy):
    ax.annotate(txt,xy=cent[code],xytext=xy,fontsize=10,color=INK,fontweight='bold',ha='left',va='center',
        arrowprops=dict(arrowstyle='-',color=MUTE,lw=0.8,shrinkB=2))
call(13,'Arlington 4.2%',(-76.7,39.4))
call(610,'Falls Church 4.9%',(-76.7,39.1))
call(111,'Lunenburg 0.5%',(-80.0,36.33))
call(27,'Buchanan 0.7%',(-83.3,37.2)) if 27 in cent else None
fig.text(0.04,0.945,'Property tax tops 3% of owner income in Northern Virginia, Hampton Roads, Richmond and Charlottesville',fontsize=14.3,fontweight='bold',color=INK)
fig.text(0.04,0.9,'Estimated annual tax (2025 effective rate × median home value) ÷ median homeowner household income',fontsize=11.5,color=MUTE)
hs=[Patch(facecolor=c,edgecolor='white',label=l) for c,l in zip(cols,labels)]
hs+=[Patch(facecolor='white',edgecolor=MUTE,hatch='////',label='Less certain (27)')]
fig.legend(handles=hs,loc='upper left',bbox_to_anchor=(0.03,0.82),frameon=False,fontsize=10,handlelength=1.6,labelcolor=INK)
fig.text(0.04,0.025,'Sources: VA Dept. of Taxation 2025 Assessment/Sales Ratio Study (Table 3); Census ACS 2020–2024 5-yr. Excludes town taxes and exemptions. Boundaries: 2010 vintage. @thedocshango.bsky.social',fontsize=8.2,color=MUTE)
fig.subplots_adjust(left=0.02,right=0.98,top=0.88,bottom=0.05)
fig.savefig('data/va_tax_burden_map.png',facecolor='white')
print({k:cent[k].round(2) for k in (13,610,111,27) if k in cent})

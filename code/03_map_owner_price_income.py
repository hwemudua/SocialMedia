import pandas as pd, numpy as np, addfips, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon, Patch
from bokeh.sampledata import us_counties
o=pd.read_csv('/mnt/user-data/uploads/7adf7297-va_owner_price_income.csv')
af=addfips.AddFIPS()
o['fips']=[af.get_county_fips(n.replace(', Virginia',''),'VA') for n in o.NAME]
assert o.fips.notna().all(), o[o.fips.isna()]
o['code']=o.fips.str[2:].astype(int); o['moe_pct']=o.owner_moe/o.owner_income*100
m=o.set_index('code')
bins=[0,2.5,3.0,3.5,4.0,10]; labels=['Under 2.5x','2.5–3.0x','3.0–3.5x','3.5–4.0x','4.0x +']
cols=['#dbeafe','#93c5fd','#3b82f6','#1d4ed8','#1e3a8a']
print(pd.cut(o.ratio,bins,labels=labels).value_counts().sort_index().to_dict())
INK,MUTE='#1f2937','#6b7280'
fig,ax=plt.subplots(figsize=(12,6.75),dpi=150)
cent={}
for (st,c),v in us_counties.data.items():
    if st!=51: continue
    lons=np.array(v['lons'],float); lats=np.array(v['lats'],float)
    nan=np.where(np.isnan(lons)|np.isnan(lats))[0]; segs=np.split(np.c_[lons,lats],nan)
    if c in m.index:
        r=m.loc[c]; ci=np.digitize(r.ratio,bins)-1; fc=cols[ci]; hatch='////' if r.moe_pct>20 else None
    else: fc='#e5e7eb'; hatch=None
    for sg in segs:
        sg=sg[~np.isnan(sg).any(axis=1)]
        if len(sg)<3: continue
        ax.add_patch(Polygon(sg,closed=True,facecolor=fc,edgecolor='white',lw=0.6,hatch=hatch))
    cent[c]=np.nanmean(np.c_[lons,lats],axis=0)
ax.set_xlim(-83.8,-75.0); ax.set_ylim(36.25,39.55); ax.set_aspect(1/np.cos(np.radians(38)))
ax.axis('off')
def call(code,txt,xy):
    ax.annotate(txt,xy=cent[code],xytext=xy,fontsize=10,color=INK,fontweight='bold',ha='left',va='center',
        arrowprops=dict(arrowstyle='-',color=MUTE,lw=0.8,shrinkB=2))
call(13,'Arlington 4.3x',(-76.7,39.4))
call(157,'Rappahannock 4.8x',(-82.3,39.0))
call(690,'Martinsville 1.5x',(-80.6,36.33))
fig.text(0.04,0.945,'Homes cost the most years of owner income in Northern Virginia and along the Chesapeake',fontsize=15.5,fontweight='bold',color=INK)
fig.text(0.04,0.9,'Median home value ÷ median income of homeowner households, by county and independent city',fontsize=11.5,color=MUTE)
hs=[Patch(facecolor=c,edgecolor='white',label=l) for c,l in zip(cols,labels)]
hs+= [Patch(facecolor='#e5e7eb',edgecolor='white',label='No data (Bedford city, merged 2013)'),
      Patch(facecolor='white',edgecolor=MUTE,hatch='////',label='Income margin of error >20%')]
leg=fig.legend(handles=hs,loc='upper left',bbox_to_anchor=(0.03,0.82),ncol=1,frameon=False,fontsize=10,handlelength=1.6,labelcolor=INK)
fig.text(0.04,0.025,'Source: Census ACS 2019–2023 5-yr (B25077, B25119). Boundaries: Bokeh sample data (2010 vintage). @thedocshango.bsky.social',fontsize=8.5,color=MUTE)
fig.subplots_adjust(left=0.02,right=0.98,top=0.88,bottom=0.05)
fig.savefig('out/va_owner_ratio_map.png',facecolor='white')
print([ (k,cent[k].round(2)) for k in (13,600,683,755) if k in cent])

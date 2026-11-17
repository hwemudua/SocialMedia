import pandas as pd, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
d=pd.read_csv('va_tax_burden_merged.csv').sort_values('pct',ascending=False).reset_index(drop=True)
d['short']=d.NAME.str.replace(', Virginia','').str.replace(' city',' (city)')
d['short']=d.short.where(d.short.str.replace(' County','').isin(['Fairfax','Richmond','Roanoke','Franklin'])==False,d.short.str.replace(' County',' Co.')).str.replace(' County','')
INK,MUTE,GRID,ACC,GRAY='#1f2937','#6b7280','#e5e7eb','#1d4ed8','#9ca3af'
fig,ax=plt.subplots(figsize=(12,6.75),dpi=150)
solid=d[~d.flag]; hol=d[d.flag]
ax.scatter(solid.index,solid.pct,s=34,color=ACC,edgecolor='white',linewidth=1,zorder=3)
ax.scatter(hol.index,hol.pct,s=40,facecolor='white',edgecolor=ACC,linewidth=1.5,zorder=3)
med=d.pct.median()
ax.axhline(med,color=INK,lw=1,ls=(0,(4,3)),zorder=2)
ax.text(62,med-0.28,f'Median locality: {med:.1f}%',ha='center',color=INK,fontsize=11,fontweight='bold')
def lab(i,x,y,ha):
    r=d.loc[i]; ax.annotate(f"{r.short}  {r.pct:.1f}%  (~${r.tax:,.0f}/yr)",xy=(i,r.pct),xytext=(x,y),fontsize=10.5,color=INK,ha=ha,va='center',
        arrowprops=dict(arrowstyle='-',color=GRAY,lw=0.8,shrinkA=2,shrinkB=4))
for k in range(5): lab(k,12,4.85-k*0.33,'left')
for k,i in enumerate([132,131,130]): lab(i,112,1.2-k*0.3 if False else 0.75-k*0.0,'right') if False else None
for k,i in enumerate([132,131,130]): lab(i,118,-0.22+k*0.3,'right')
ax.set_ylim(-0.45,5.4); ax.set_xlim(-2,134)
ax.set_xticks([]); ax.set_yticks([0,1,2,3,4,5]); ax.set_yticklabels([f'{v}%' for v in range(6)],color=MUTE,fontsize=11)
ax.grid(axis='y',color=GRID,lw=0.8,zorder=0)
for s in ax.spines.values(): s.set_visible(False)
ax.tick_params(length=0)
ax.set_xlabel('All 133 Virginia counties and independent cities, ranked high to low',color=MUTE,fontsize=10)
ax.scatter(60,4.75,s=40,color=ACC,edgecolor='white'); ax.text(62,4.75,'Reliable estimate',va='center',fontsize=10.5,color=INK)
ax.scatter(60,4.4,s=44,facecolor='white',edgecolor=ACC,linewidth=1.5); ax.text(62,4.4,'Less certain: wide income margin or big assessment shift (27)',va='center',fontsize=10.5,color=INK)
fig.text(0.05,0.94,'Property tax on a typical home: 4.9% of owner income in Falls Church, 0.5% in Lunenburg',fontsize=15.5,fontweight='bold',color=INK)
fig.text(0.05,0.895,'Estimated annual tax (2025 effective rate × median home value) ÷ median homeowner household income',fontsize=11.5,color=MUTE)
fig.text(0.05,0.03,'Sources: Virginia Dept. of Taxation 2025 Assessment/Sales Ratio Study (Table 3); Census ACS 2020–2024 5-yr (B25077, B25119). Excludes town taxes and exemptions.  @thedocshango.bsky.social',fontsize=8.3,color=MUTE)
fig.subplots_adjust(left=0.06,right=0.97,top=0.85,bottom=0.1)
fig.savefig('va_tax_burden.png',facecolor='white')

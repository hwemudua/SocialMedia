import pandas as pd, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
d=pd.read_csv('/mnt/user-data/uploads/850675c9-va_price_income.csv').sort_values('ratio',ascending=False).reset_index(drop=True)
d['short']=d.NAME.str.replace(', Virginia','').str.replace(' County','').str.replace(' city',' (city)')
INK,MUTE,GRID='#1f2937','#6b7280','#e5e7eb'; ACC='#1d4ed8'; GRAY='#9ca3af'
fig,ax=plt.subplots(figsize=(12,6.75),dpi=150)
hi=d.ratio>=5
ax.scatter(d.index[~hi],d.ratio[~hi],s=34,color=GRAY,edgecolor='white',linewidth=1,zorder=3)
ax.scatter(d.index[hi],d.ratio[hi],s=46,color=ACC,edgecolor='white',linewidth=1,zorder=3)
med=d.ratio.median()
ax.axhline(med,color=INK,lw=1,ls=(0,(4,3)),zorder=2)
ax.text(132,med+0.06,f'Median locality: {med:.1f}x',ha='right',color=INK,fontsize=11,fontweight='bold')
def lab(i,x,y,ha):
    r=d.loc[i]
    ax.annotate(f"{r.short} {r.ratio:.1f}x",xy=(i,r.ratio),xytext=(x,y),fontsize=10.5,color=INK,ha=ha,va='center',
                arrowprops=dict(arrowstyle='-',color=GRAY,lw=0.8,shrinkA=2,shrinkB=4))
for k in range(6): lab(k,14,6.65-k*0.3,'left')
for k,i in enumerate([130,131,132]): lab(i,118,2.4-k*0.28,'right')
ax.set_ylim(1.5,6.9); ax.set_xlim(-2,134)
ax.set_xticks([]); ax.set_yticks([2,3,4,5,6]); ax.set_yticklabels([f'{v}x' for v in [2,3,4,5,6]],color=MUTE,fontsize=11)
ax.grid(axis='y',color=GRID,lw=0.8,zorder=0)
for s in ['top','right','left','bottom']: ax.spines[s].set_visible(False)
ax.tick_params(length=0)
ax.set_xlabel('All 133 Virginia counties and independent cities, ranked from highest ratio (left) to lowest (right)',color=MUTE,fontsize=10)
fig.text(0.06,0.94,'In Falls Church, a typical home costs 6.5 years of a typical household\'s income. In Covington, 1.9.',fontsize=16,fontweight='bold',color=INK,ha='left')
fig.text(0.06,0.895,'Median home value ÷ median household income, by Virginia locality',fontsize=12,color=MUTE,ha='left')
fig.text(0.06,0.03,'Source: U.S. Census Bureau, ACS 2019–2023 5-year estimates (B25077, B19013). Ratio of medians; owner-estimated values.   @thedocshango.bsky.social',fontsize=9,color=MUTE)
fig.subplots_adjust(left=0.06,right=0.97,top=0.85,bottom=0.12)
fig.savefig('out/va_price_to_income.png',facecolor='white')

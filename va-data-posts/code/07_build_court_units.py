import pandas as pd, numpy as np
g=pd.read_csv('gdc_2025.csv')
a=pd.read_csv('/mnt/user-data/uploads/b67e71df-va_acs2024_hh.csv',dtype={'state':str,'county':str})
a['code']=a.county.astype(int); a['key']=a.NAME.str.replace(', Virginia','').str.lower()
cities=['alexandria','bristol','buena vista','charlottesville','chesapeake','colonial heights','danville','emporia','falls church','fredericksburg','galax','hampton','hopewell','lynchburg','martinsville','newport news','norfolk','petersburg','portsmouth','radford','salem','staunton','suffolk','virginia beach','waynesboro','winchester']
def keys(loc):
    l=loc.lower().replace('&','and')
    comb={'lexington/rockb':['lexington city','rockbridge county'],'rockingham/har':['rockingham county','harrisonburg city'],'williamsburg/ja':['williamsburg city','james city county'],
          'prince william':['prince william county','manassas city','manassas park city'],'york':['york county','poquoson city'],'wise':['wise county','norton city'],'alleghany':['alleghany county','covington city']}
    if l in comb: return comb[l]
    if l=='charles city': return ['charles city county']
    if l.endswith(' city') : return [l]
    if l.endswith(' county'): return [l]
    if l=='richmond': return ['richmond county']
    if l in cities: return [l+' city']
    return [l+' county']
rows=[]
for loc in g.locale.unique():
    if loc in ('District Total',) : continue
    ks=keys(loc); m=a[a.key.isin(ks)]
    if len(m)!=len(ks): print('NOMATCH',loc,ks,len(m)); continue
    r=g[g.locale==loc].set_index('cat').total2025
    if 'Landlord/Tenant' not in r: continue
    rows.append(dict(court=loc,codes=list(m.code),lt=r['Landlord/Tenant'],garn=r['Garnishment'],gencivil=r['General Civil & Civil Commitments'],
        renter_hh=m.renter_hh.sum(),renter_moe=float(np.sqrt((m.renter_moe**2).sum())),households=m.households.sum(),pop=m.population.sum(),n=len(ks)))
u=pd.DataFrame(rows)
fx=u[u.court.isin(['Fairfax County','Fairfax City','Falls Church'])]
num=['lt','garn','gencivil','renter_hh','households','pop','n']
new=dict(court='Fairfax Co./City/Falls Church',codes=sum(fx.codes.tolist(),[]),renter_moe=float(np.sqrt((fx.renter_moe**2).sum())),**{k:fx[k].sum() for k in num})
u=pd.concat([u[~u.court.isin(fx.court)],pd.DataFrame([new])],ignore_index=True)
used=set(c for cs in u.codes for c in cs); print(len(u),len(used),set(a.code)-used)
u['lt_rate']=u['lt']/u.renter_hh*100; u['garn_per1k']=u.garn/u.households*1000
u.to_csv('units.csv',index=False)
print(u.lt_rate.describe().round(1).to_dict())
print(u.sort_values('lt_rate',ascending=False).head(8)[['court','lt','renter_hh','lt_rate']].round(1).to_string())
print(u.sort_values('lt_rate').head(5)[['court','lt','renter_hh','lt_rate']].round(1).to_string())
print(u['lt'].sum(), u['lt'].sum()/u.renter_hh.sum()*100)

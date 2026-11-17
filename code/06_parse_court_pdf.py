import pdfplumber, re, pandas as pd
rows=[]; loc=None; dist=None
def num(s): return int(s.replace(',',''))
with pdfplumber.open('gdc.pdf') as p:
    for pn,pg in enumerate(p.pages[1:],start=2):
        ws=pg.extract_words(); 
        yrs=sorted([w for w in ws if w['text'] in('2025','2026') and 250<w['x0']<260],key=lambda w:w['top'])
        for i,y in enumerate(yrs):
            if y['text']!='2025': continue
            nxt=[z for z in yrs[i+1:] if z['text']=='2026']
            bot=nxt[0]['top'] if nxt else y['top']+16
            nums=[w for w in ws if abs(w['top']-y['top'])<3 and w['x0']>285]
            nums=sorted(nums,key=lambda w:w['x0'])
            if len(nums)<13: print('short row',pn,y['top'],len(nums)); continue
            vals=[num(w['text']) for w in nums[:12]]+[num(nums[-1]['text'])]
            cat=' '.join(w['text'] for w in sorted([w for w in ws if 130<w['x0']<250 and y['top']-5<=w['top']<=bot+5],key=lambda w:(round(w['top']),w['x0'])))
            lw=[w for w in ws if 68<w['x0']<130 and y['top']-6<=w['top']<=y['top']+3]
            dw=[w for w in ws if 40<w['x0']<68 and abs(w['top']-y['top'])<4]
            if lw:
                loc=' '.join(w['text'] for w in sorted(lw,key=lambda w:w['x0']))
                if dw: dist=dw[0]['text']
            rows.append(dict(page=pn,district=dist,locale=loc,cat=cat,total2025=vals[-1],jan_dec=sum(vals[:12]) ))
d=pd.DataFrame(rows); d.to_csv('gdc_2025.csv',index=False)
print(len(d)); print(d.cat.value_counts().head(15)); print(d.locale.nunique())

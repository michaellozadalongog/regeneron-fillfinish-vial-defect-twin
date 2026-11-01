"""Fill/finish vial twin: fill weight + visual inspection yield vs line speed, lighting, vision threshold."""
import numpy as np, matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt, json, os
rng=np.random.default_rng(11); N=200000; TARGET=2.25; LSL,USL=2.20,2.35  # mL, assumed spec
DEFECTS={"particulate":2e-4,"glass_crack":5e-5,"stopper_misplace":3e-4,"cosmetic_scratch":1.2e-3,"fill_level_low":0}
def run(speed,lux,thr):
    sd=0.012*(1+0.004*(speed-200)); fill=rng.normal(TARGET+0.03,sd,N)  # speed raises variability
    d={k:rng.random(N)<p*(1+0.002*(speed-200)) for k,p in DEFECTS.items()}
    d["fill_level_low"]=fill<LSL
    true_def=np.any([d[k] for k in d if k!="cosmetic_scratch"],axis=0)|((fill>USL))
    contrast=np.clip(lux/2000,0.3,1.2)
    score=np.where(true_def|d["cosmetic_scratch"],rng.normal(0.75*contrast,0.15,N),rng.normal(0.2,0.1,N))
    rej=(score>thr)|(fill<LSL)|(fill>USL)
    good=~true_def
    return dict(yield_=(~rej).mean(),false_reject=(rej&good&~d["cosmetic_scratch"]).mean()/good.mean(),
        escape_ppm=1e6*(true_def&~rej).sum()/N,cpk=min(fill.mean()-LSL,USL-fill.mean())/(3*fill.std()),
        mean=fill.mean(),sd=fill.std()), d
if __name__=="__main__":
    os.makedirs("figs",exist_ok=True); grid=[]
    for s in [150,200,300,400]:
        for lux in [1000,2000,3000]:
            for thr in [0.35,0.45,0.55]:
                r,_=run(s,lux,thr); grid.append(dict(speed=s,lux=lux,thr=thr,**{k:float(v) for k,v in r.items()}))
    ok=[g for g in grid if g["escape_ppm"]<50 and g["cpk"]>=1.33]; best=max(ok,key=lambda g:(g["speed"]*g["yield_"])) if ok else None
    base,d=run(200,2000,0.45); cnt={k:int(v.sum()) for k,v in d.items()}
    sd=base["sd"]; res={"grid":grid,"recommended":best,"baseline":{k:float(v) for k,v in base.items()},
        "xbar_limits_n5":[TARGET+0.03-3*sd/5**.5,TARGET+0.03+3*sd/5**.5],"defect_counts_baseline":cnt}
    json.dump(res,open("figs/results.json","w"),indent=1)
    print(json.dumps({k:v for k,v in res.items() if k!="grid"},indent=1))
    k=sorted(cnt,key=cnt.get,reverse=True); v=np.array([cnt[x] for x in k])
    fig,ax=plt.subplots(); ax.bar(k,v); ax2=ax.twinx(); ax2.plot(k,100*v.cumsum()/v.sum(),"r-o"); ax.tick_params(axis="x",rotation=30)
    ax.set_title("Defect Pareto (200 vpm, 2000 lux, thr 0.45)"); plt.tight_layout(); plt.savefig("figs/defect_pareto.png",dpi=150); plt.close()
    for lux in [1000,2000,3000]:
        g=[x for x in grid if x["lux"]==lux and x["thr"]==0.45]; plt.plot([x["speed"] for x in g],[x["escape_ppm"] for x in g],"-o",label=f"{lux} lux")
    plt.xlabel("line speed (vials/min)"); plt.ylabel("escape ppm"); plt.legend(); plt.title("Defect escapes vs speed"); plt.savefig("figs/escape_vs_speed.png",dpi=150); plt.close()
    g=[x for x in grid if x["lux"]==2000]
    for thr in [0.35,0.45,0.55]:
        h=[x for x in g if x["thr"]==thr]; plt.plot([x["false_reject"]*100 for x in h],[x["escape_ppm"] for x in h],"-o",label=f"thr {thr}")
    plt.xlabel("false reject %"); plt.ylabel("escape ppm"); plt.legend(); plt.title("Vision threshold tradeoff (2000 lux)"); plt.savefig("figs/threshold_tradeoff.png",dpi=150); plt.close()
    _,_=0,0; f=rng.normal(TARGET+0.03,sd,N); plt.hist(f,100); [plt.axvline(x,c="r") for x in (LSL,USL)]; plt.title(f"Fill weight, Cpk={base['cpk']:.2f}"); plt.savefig("figs/fill_weight.png",dpi=150)

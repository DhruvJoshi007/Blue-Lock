import re,subprocess,sys,itertools,math
T=["If I were strong enough to play for both of us... strong enough to find out who did this...","Where is Isagi, Vance? Beat me and I will not ask again. Lose, and you tell me everything.","Mendokusai. But I will go and get him.","Mendokusai. How do we get in?","Where is Isagi?","Isagi. It is me. Why are your eyes like that?","Mendokusai. ...But fine.","Finally. Less running.","Then I will do something I have never done.","Isagi. The river road. Training at eight. You told me not to be late.","Together. Now.","Watch him.","Mendokusai. I only came to get you. That is all.","I will come every day. ...Mendokusai.","Eleven. Show-off.","Your first touch is worse than mine.","The Twin Stars. ...Mendokusai, but okay.","Five months I waited for your passes.","In Japan we call it efficient.","And now you are going to win the World Cup. Mendokusai. Let's go.","World champions. ...Can I sleep now?"]
def seg(f,texts):
    o=subprocess.run(['ffmpeg','-hide_banner','-i',f,'-af','silencedetect=noise=-38dB:d=0.3','-f','null','-'],capture_output=True,text=True).stderr
    st=[float(x) for x in re.findall(r'silence_start: ([\d.]+)',o)];en=[float(x) for x in re.findall(r'silence_end: ([\d.]+)',o)]
    dur=float(subprocess.run(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',f],capture_output=True,text=True).stdout)
    # speech spans
    sp=[];t=0
    for s,e in zip(st,en+[None]*(len(st)-len(en))):
        if s>t+.05: sp.append((t,s))
        t=e if e else dur
    if t<dur-.05: sp.append((t,dur))
    return sp
def best(sp,texts):
    n=len(texts);m=len(sp);L=[len(t) for t in texts]
    tot=sum(sp[i][1]-sp[i][0] for i in range(m));tl=sum(L);rate=tot/tl
    pre=[0]
    for a,b in sp:pre.append(pre[-1]+b-a)
    INF=1e18;dp=[[INF]*(m+1) for _ in range(n+1)];bk=[[0]*(m+1) for _ in range(n+1)];dp[0][0]=0
    for i in range(1,n+1):
        for j in range(i,m+1):
            for k in range(i-1,j):
                d=pre[j]-pre[k];c=dp[i-1][k]+((d-L[i-1]*rate)/ (L[i-1]*rate+1))**2
                if c<dp[i][j]:dp[i][j]=c;bk[i][j]=k
    j=m;out=[]
    for i in range(n,0,-1):
        k=bk[i][j];out.append((sp[k][0],sp[j-1][1]));j=k
    return out[::-1],dp[n][m]/n
if __name__=='__main__':
    f=sys.argv[1];a=int(sys.argv[2]);b=int(sys.argv[3])
    sp=seg(f,None);r,c=best(sp,T[a:b]);print(len(sp),'spans cost',round(c,3))
    for i,(s,e) in enumerate(r):print(a+i+1,round(s,2),round(e,2),round(e-s,2),len(T[a+i]),T[a+i][:40])

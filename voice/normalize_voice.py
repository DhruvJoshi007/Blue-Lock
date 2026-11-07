import subprocess,json,glob,re,os,sys
from concurrent.futures import ThreadPoolExecutor
def run(f):
    o=subprocess.run(['ffmpeg','-hide_banner','-nostats','-i',f,'-af','loudnorm=I=-16:TP=-1.5:LRA=11:print_format=json','-f','null','-'],capture_output=True,text=True).stderr
    j=json.loads(o[o.rindex('{'):o.rindex('}')+1])
    flt='loudnorm=I=-16:TP=-1.5:LRA=11:measured_I=%s:measured_TP=%s:measured_LRA=%s:measured_thresh=%s:offset=%s:linear=true'%(j['input_i'],j['input_tp'],j['input_lra'],j['input_thresh'],j['target_offset'])
    t=f+'.tmp.mp3'
    subprocess.run(['ffmpeg','-y','-loglevel','error','-i',f,'-af',flt+',alimiter=limit=0.89','-ac','1','-ar','24000','-b:a','48k',t],check=True)
    os.replace(t,f);return f,j['input_i']
fs=sorted(glob.glob('*/*.mp3'))
with ThreadPoolExecutor(4) as ex:
    for f,i in ex.map(run,fs):pass
print(len(fs))

import cv2,numpy as np,subprocess
W,H=1080,1920
K=cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(9,9))
def bhat(f): return cv2.morphologyEx(cv2.cvtColor(f,cv2.COLOR_BGR2GRAY),cv2.MORPH_BLACKHAT,K).astype(np.float32)
def fit(bh,xs,pred,w):
  P=[]
  for x in xs:
    yc=int(round(pred(x))); lo=max(0,yc-w); col=bh[lo:yc+w+1,x]; y=int(np.argmax(col))
    if col[y]>10: P.append((x,lo+y))
  P=np.array(P,float); c=np.polyfit(P[:,0],P[:,1],2)
  for _ in range(2):
    r=np.abs(np.polyval(c,P[:,0])-P[:,1]); P=P[r<4]; c=np.polyfit(P[:,0],P[:,1],2)
  return c
p=subprocess.Popen(['ffmpeg','-v','error','-i','base0.mp4','-f','rawvideo','-pix_fmt','bgr24','-'],stdout=subprocess.PIPE)
o=subprocess.Popen(['ffmpeg','-v','error','-y','-f','rawvideo','-pix_fmt','bgr24','-s','1080x1920','-r','30','-i','-','-c:v','libx264','-crf','16','-preset','fast','-pix_fmt','yuv420p','base0-sem-fio.mp4'],stdin=subprocess.PIPE)
cL=np.polyfit([0,150,300],[645,690,728],2); cR=np.polyfit([668,780,900],[828,850,846],2)
XL=np.arange(0,300,2); XR=np.arange(666,900,2); n=0
while True:
  b=p.stdout.read(W*H*3)
  if len(b)<W*H*3: break
  f=np.frombuffer(b,np.uint8).reshape(H,W,3).copy(); bh=bhat(f)
  w=18 if n==0 else 7
  cL=fit(bh,XL,lambda x:np.polyval(cL,x),w); cR=fit(bh,XR,lambda x:np.polyval(cR,x),w)
  m=np.zeros((H,W),np.uint8)
  for c,xs in ((cL,np.arange(-5,298)),(cR,np.arange(668,905))):
    cv2.polylines(m,[np.stack([xs,np.polyval(c,xs)],1).astype(np.int32)],False,255,9)
  r=cv2.inpaint(f,m,5,cv2.INPAINT_TELEA)
  if n in(45,200): cv2.imwrite(f'v3-{n}.jpg',np.hstack([f[550:950,0:950],r[550:950,0:950]]))
  o.stdin.write(r.tobytes()); n+=1
o.stdin.close();o.wait();print('ok',n)

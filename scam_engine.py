import re
from urllib.parse import urlparse

WORDS={
 'Urgency & Pressure':['urgent','immediately','act now','last chance','within 24 hours','blocked'],
 'Financial Risk':['payment','bank','money','transfer','upi','refund','transaction','cash'],
 'Credential Requests':['otp','password','pin','cvv','verification code','login details'],
 'Fake Rewards / Offers':['you won','winner','congratulations','lottery','prize','reward','gift'],
 'Investment Scam':['guaranteed profit','double your money','crypto investment','high returns','quick profit']}
URLWORDS=['login','verify','secure','update','bank','payment','account','wallet','bonus','claim','gift']
SHORT=['bit.ly','tinyurl.com','t.co','goo.gl','cutt.ly']

def classify(score):
 score=round(max(0,min(100,score)))
 if score>=65:return score,'High Risk','🔴 HIGH RISK — POSSIBLE SCAM','HIGH RISK','#a83e35','red','Multiple strong scam indicators were detected. Treat this content as suspicious.'
 if score>=35:return score,'Moderate Risk','🟡 MODERATE RISK — VERIFY BEFORE TRUSTING','MODERATE RISK','#b47712','gold','Some suspicious indicators were detected. Verify the source independently.'
 return score,'Low Risk','🟢 LOW RISK — FEWER SUSPICIOUS INDICATORS','LOW RISK','#356a4c','green','Few rule-based scam indicators were detected. This does not guarantee safety.'

def pack(score,breakdown,signals,actions,typ):
 score,level,verdict,short,color,card,summary=classify(score)
 return {'score':score,'level':level,'verdict':verdict,'short_verdict':short,'color':color,'card_class':card,'summary':summary,'breakdown':breakdown,'signals':signals or ['No major rule-based scam indicators were detected.'],'actions':actions,'analysis_type':typ}

def analyze_message(message,source='Other'):
 t=message.lower(); b={}; signals=[]
 for cat,items in WORDS.items():
  hits=[w for w in items if w in t]
  b[cat]=min(100,len(hits)*(22 if cat=='Credential Requests' else 16))
  if hits: signals.append(f'{cat}: suspicious language was detected.')
 link=0
 if re.search(r'https?://\S+|www\.\S+',t): link=30;signals.append('The message contains an external link.')
 if any(x in t for x in ['whatsapp','telegram','dm us']): link+=15;signals.append('The message encourages contact through an informal channel.')
 b['Links & Contact Signals']=min(100,link)
 score=sum([b['Urgency & Pressure']*.15,b['Financial Risk']*.18,b['Credential Requests']*.27,b['Fake Rewards / Offers']*.16,b['Investment Scam']*.12,b['Links & Contact Signals']*.12])
 actions=['Do not share OTPs, passwords, PINs or banking details.','Do not send money because of an urgent message.','Verify organisations using independently found official contact details.','Avoid clicking unfamiliar links.','If money was transferred, contact your bank and cybercrime authorities promptly.']
 return pack(score,b,signals,actions,'Message')

def analyze_url(url):
 raw=url.strip(); raw=raw if raw.startswith(('http://','https://')) else 'http://'+raw
 p=urlparse(raw); domain=p.netloc.lower(); full=raw.lower(); b={}; signals=[]
 structure=0; phishing=0; domainrisk=0; link=0; security=0
 if len(full)>75: structure+=25;signals.append('The URL is unusually long.')
 if full.count('-')>=3: structure+=18;signals.append('The URL contains many hyphens.')
 if domain.count('.')>=3: structure+=20;signals.append('The domain contains multiple subdomains.')
 if re.fullmatch(r'\d{1,3}(\.\d{1,3}){3}(:\d+)?',domain): domainrisk+=45;signals.append('The URL uses an IP address instead of a normal domain.')
 hits=[w for w in URLWORDS if w in full]
 phishing=min(100,len(hits)*12)
 if hits: signals.append('The URL contains login, verification or payment-related phishing keywords.')
 if any(s in domain for s in SHORT): link+=40;signals.append('The URL uses a shortened-link service.')
 if '@' in raw: domainrisk+=25;signals.append('The URL contains an @ symbol that can obscure the destination.')
 if p.scheme=='http': security+=20;signals.append('The URL does not use HTTPS.')
 b={'URL Structure':min(100,structure),'Phishing Keywords':phishing,'Domain Pattern':min(100,domainrisk),'Link Behaviour':min(100,link),'Security Signals':min(100,security)}
 score=sum(v*w for v,w in zip(b.values(),[.22,.25,.23,.18,.12]))
 actions=['Do not enter passwords, OTPs or banking information until independently verified.','Check the official domain by searching separately.','Avoid downloading files from suspicious websites.','Use official apps or bookmarked sites for banking and important accounts.']
 return pack(score,b,signals,actions,'URL')

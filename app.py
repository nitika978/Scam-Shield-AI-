import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from scam_engine import analyze_message, analyze_url

st.set_page_config(page_title='ScamShield AI',page_icon='🛡️',layout='wide')
if 'history' not in st.session_state: st.session_state.history=[]

st.markdown('''<style>
html,body,[class*="css"],.stApp{font-family:"Times New Roman",Times,serif!important}.stApp{background:radial-gradient(circle at 90% 5%,rgba(201,154,59,.17),transparent 24%),radial-gradient(circle at 7% 55%,rgba(53,106,76,.13),transparent 25%),linear-gradient(135deg,#f8f1e5,#fffaf3,#eee1cc);color:#241f1b}#MainMenu,footer,header{visibility:hidden}section[data-testid="stSidebar"]{background:linear-gradient(#1f3d2d,#356a4c,#244836)}section[data-testid="stSidebar"] *{color:#fff9ee!important;font-family:"Times New Roman",Times,serif!important}.hero,.card,.verdict{background:rgba(255,252,246,.94);border:1px solid rgba(78,59,38,.14);border-radius:22px;box-shadow:0 10px 28px rgba(70,50,30,.07)}.hero{padding:38px;margin-bottom:24px;background:linear-gradient(115deg,#fffaf2,#f0dfc3)}.title{font-size:36px;font-weight:bold}.title span{color:#b65720}.desc{font-size:17px;color:#6d6257;margin-bottom:20px}.card{padding:20px}.feature{min-height:185px;text-align:center}.signal{background:#fffaf2;border-left:5px solid #a83e35;padding:13px 16px;margin:9px 0;border-radius:0 12px 12px 0;color:#5f5449}.action{background:#edf4ec;border-left:5px solid #356a4c;padding:12px 16px;margin:9px 0;border-radius:0 12px 12px 0;color:#43584a}.metric{border-top:5px solid #d97718}.metric.green{border-top-color:#356a4c}.metric.gold{border-top-color:#c69a3b}.metric.red{border-top-color:#a83e35}.metric h2{margin:7px 0}.verdict{text-align:center;padding:24px}.stButton button,.stFormSubmitButton button{width:100%;background:linear-gradient(135deg,#244836,#356a4c)!important;color:white!important;border:none!important;border-radius:11px!important;font-family:"Times New Roman",Times,serif!important;font-size:18px!important;font-weight:bold!important;padding:11px!important}</style>''',unsafe_allow_html=True)

with st.sidebar:
 if __import__('os').path.exists('assets/government-logo.png'): st.image('assets/government-logo.png',width=85)
 st.markdown('## 🛡️ ScamShield AI');st.caption('Cyber Fraud Intelligence')
 page=st.radio('NAVIGATION',['🏠 Home','💬 Analyze Message','🔗 Analyze URL','📊 Live Dashboard','🛡️ Safety Centre','ℹ️ About'])
 st.markdown('---');st.markdown('### 🔎 Threats Detected\n• Phishing\n• OTP & Banking Fraud\n• Fake Rewards\n• Investment Scams\n• Suspicious Links\n• Urgency Manipulation')

def gauge(score,color):
 f=go.Figure(go.Indicator(mode='gauge+number',value=score,number={'suffix':'%','font':{'size':48,'family':'Times New Roman'}},title={'text':'SCAM RISK SCORE','font':{'family':'Times New Roman'}},gauge={'axis':{'range':[0,100]},'bar':{'color':color},'steps':[{'range':[0,35],'color':'#dfeee2'},{'range':[35,65],'color':'#f5e5bc'},{'range':[65,100],'color':'#f1d9d5'}]}))
 f.update_layout(height=300,paper_bgcolor='rgba(0,0,0,0)',font={'family':'Times New Roman'},margin=dict(l=20,r=20,t=50,b=10));return f

def bar(r):
 f=go.Figure(go.Bar(x=list(r['breakdown']),y=list(r['breakdown'].values()),marker_color=['#356a4c','#c69a3b','#d97718','#a83e35','#7b342d','#b65720']))
 f.update_layout(height=360,yaxis={'range':[0,100],'title':'Risk Contribution'},paper_bgcolor='rgba(0,0,0,0)',plot_bgcolor='rgba(255,250,242,.55)',font={'family':'Times New Roman'});return f

def show(r,key):
 a,b=st.columns(2)
 with a:
  st.plotly_chart(gauge(r['score'],r['color']),use_container_width=True,key=key+'_g')
  st.markdown(f'<div class="verdict"><div style="font-size:27px;font-weight:bold;color:{r["color"]}">{r["verdict"]}</div><p style="color:#665b50;font-size:17px">{r["summary"]}</p></div>',unsafe_allow_html=True)
 with b:
  st.markdown('### 🧠 Why did the AI give this result?')
  for x in r['signals']: st.markdown(f'<div class="signal">✓ {x}</div>',unsafe_allow_html=True)
  st.markdown('### 🛡️ Recommended Action')
  for x in r['actions']: st.markdown(f'<div class="action">➤ {x}</div>',unsafe_allow_html=True)
 st.markdown('### 📊 Threat Signal Breakdown');st.plotly_chart(bar(r),use_container_width=True,key=key+'_b')

if page=='🏠 Home':
 c_logo,c_intro=st.columns([1,5])
 with c_logo:
  if __import__('os').path.exists('assets/government-logo.png'): st.image('assets/government-logo.png',width=115)
 with c_intro:
  st.markdown('<div class="eyebrow" style="color:#b65720;font-weight:bold;letter-spacing:2px">● GOVERNMENT OF INDIA • CYBER FRAUD AWARENESS</div>',unsafe_allow_html=True)
 st.markdown('''<div class="hero"><div style="font-size:70px;float:left;margin-right:25px">🛡️</div><div style="overflow:hidden"><div style="color:#b65720;font-weight:bold;letter-spacing:2px">● AI-POWERED CYBER FRAUD PROTECTION</div><h1 style="font-size:50px;margin:8px 0">Think Before You Click.<br><span style="color:#b65720">Detect the Scam.</span></h1><p style="font-size:18px;color:#665b50">ScamShield AI analyses suspicious messages and links for signs of phishing, online fraud and digital theft.</p></div></div>''',unsafe_allow_html=True)
 st.markdown('<div class="title">One platform. <span>Multiple scam threats.</span></div><div class="desc">Simple, interactive and designed for practical cybersecurity awareness.</div>',unsafe_allow_html=True)
 for c,(i,t,d) in zip(st.columns(3),[('💬','Scam Message Analyzer','Paste SMS, WhatsApp or email content.'),('🔗','Suspicious URL Analyzer','Check phishing-style website patterns.'),('📊','Live Dashboard','See dynamic risk trends and results.')]): c.markdown(f'<div class="card feature"><div style="font-size:42px">{i}</div><h3>{t}</h3><p style="color:#665b50">{d}</p></div>',unsafe_allow_html=True)
 st.markdown('<br><div class="title">How <span>ScamShield AI</span> works</div>',unsafe_allow_html=True)
 for c,(n,t,d) in zip(st.columns(4),[('1️⃣','Enter','Paste content.'),('2️⃣','Analyse','Check indicators.'),('3️⃣','Classify','Low/Moderate/High.'),('4️⃣','Protect','Get safety advice.')]): c.markdown(f'<div class="card metric"><small>{n}</small><h3>{t}</h3><p style="color:#665b50">{d}</p></div>',unsafe_allow_html=True)

elif page=='💬 Analyze Message':
 st.markdown('<div class="title">💬 Scam <span>Message Analyzer</span></div><div class="desc">Paste a suspicious SMS, WhatsApp message, email, job offer or financial message.</div>',unsafe_allow_html=True)
 with st.form('msg'):
  source=st.selectbox('Where did you receive it?',['SMS','WhatsApp','Email','Social Media','Unknown / Other'])
  message=st.text_area('Paste suspicious message *',height=190,placeholder='Congratulations! You have won ₹50,000. Click immediately to claim your reward...')
  run=st.form_submit_button('🛡️ Analyze Scam Risk')
 if run:
  if not message.strip():st.error('Please paste a message.')
  else:
   r=analyze_message(message,source);st.session_state.history.insert(0,r);st.session_state.history=st.session_state.history[:20];show(r,'message')

elif page=='🔗 Analyze URL':
 st.markdown('<div class="title">🔗 Suspicious <span>URL Analyzer</span></div><div class="desc">Analyse a website address for common phishing and scam patterns.</div>',unsafe_allow_html=True)
 with st.form('url'):
  url=st.text_input('Enter website URL *',placeholder='https://example.com');run=st.form_submit_button('🔍 Analyze URL Risk')
 if run:
  if not url.strip():st.error('Please enter a URL.')
  else:
   r=analyze_url(url);st.session_state.history.insert(0,r);st.session_state.history=st.session_state.history[:20];show(r,'url')

elif page=='📊 Live Dashboard':
 st.markdown('<div class="title">📊 Live <span>Cyber Fraud Dashboard</span></div><div class="desc">The dashboard updates dynamically after every analysis.</div>',unsafe_allow_html=True)
 h=st.session_state.history
 if not h:st.info('Analyse a message or URL first.')
 else:
  latest=h[0];low=sum(x['level']=='Low Risk' for x in h);mod=sum(x['level']=='Moderate Risk' for x in h);high=sum(x['level']=='High Risk' for x in h)
  for c,(lab,val,cl) in zip(st.columns(4),[('Latest Risk',str(latest['score'])+'%',latest['card_class']),('Total Analyses',len(h),''),('High Risk',high,'red'),('Latest Type',latest['analysis_type'],'green')]): c.markdown(f'<div class="card metric {cl}"><small>{lab}</small><h2>{val}</h2></div>',unsafe_allow_html=True)
  a,b=st.columns(2)
  with a:st.plotly_chart(gauge(latest['score'],latest['color']),use_container_width=True,key='dash_g')
  with b:
   f=go.Figure(go.Pie(labels=['Low Risk','Moderate Risk','High Risk'],values=[max(low,.01),max(mod,.01),max(high,.01)],hole=.58,marker_colors=['#356a4c','#c69a3b','#a83e35']));f.update_layout(height=330,paper_bgcolor='rgba(0,0,0,0)',font={'family':'Times New Roman'});st.plotly_chart(f,use_container_width=True,key='dash_pie')
  df=pd.DataFrame({'Analysis':range(1,len(h)+1),'Risk Score':[x['score'] for x in reversed(h)]});f=go.Figure(go.Scatter(x=df['Analysis'],y=df['Risk Score'],mode='lines+markers',line={'color':'#b65720'},marker={'color':'#356a4c','size':9}));f.update_layout(height=330,yaxis={'range':[0,100]},paper_bgcolor='rgba(0,0,0,0)',font={'family':'Times New Roman'});st.plotly_chart(f,use_container_width=True,key='dash_trend')
  st.markdown('### Latest Threat Signal Breakdown');st.plotly_chart(bar(latest),use_container_width=True,key='dash_bar')

elif page=='🛡️ Safety Centre':
 st.markdown('<div class="title">🛡️ Digital <span>Safety Centre</span></div>',unsafe_allow_html=True)
 for c,(i,t,d) in zip(st.columns(2),[('🔐','Protect Your Information','Never share OTPs, passwords, PINs or banking credentials.'),('🚨','Recognise Manipulation','Scammers use fear, urgency, excitement and pressure.'),('🔗','Check Before Clicking','Be cautious with unfamiliar and shortened links.'),('☎️','Verify Independently','Use official contact channels, not suspicious message numbers.')]): c.markdown(f'<div class="card feature" style="text-align:left"><div style="font-size:40px">{i}</div><h3>{t}</h3><p style="color:#665b50">{d}</p></div>',unsafe_allow_html=True)

else:
 st.markdown('<div class="title">About <span>ScamShield AI</span></div>',unsafe_allow_html=True);st.markdown('<div class="card"><h3>🎯 Project Objective</h3><p style="font-size:18px;color:#62574c">An academic cybersecurity project addressing online fraud and digital theft through explainable message and URL risk analysis.</p></div>',unsafe_allow_html=True);st.markdown('### Technologies Used');st.write('Python • Streamlit • Pandas • Plotly • Rule-Based Explainable AI');st.warning('This is an educational risk assessment. It cannot guarantee that content is safe or fraudulent.')

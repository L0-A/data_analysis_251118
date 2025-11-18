import streamlit as st;
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px

# font를 나눔고딕으로 세팅 'NanumGothic'  - windows
plt.rcParams['font.family'] =  'Malgun Gothic'

obs = pd.read_csv("OBS_ASOS_DD.csv", encoding='cp949')
obs['일강수량(mm)'] = obs['일강수량(mm)'].fillna(0) #강수량 NULL값 0으로 바꾸기

obs_data = obs.copy()
    
obs_data['일시2'] = pd.to_datetime(obs_data['일시'])

obs_data['년'] = obs_data['일시2'].dt.year
obs_data['월'] = obs_data['일시2'].dt.month
obs_data['일'] = obs_data['일시2'].dt.day

def footer():
    
    st.markdown(" ") #너무 위
    st.markdown(" ") 
    st.markdown(" ") 
    st.markdown(" ") 
    st.markdown("---") #footer가 없어서 구분선 만듬
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 데이터 출처")
        st.markdown("[기상자료개방포털](https://data.kma.go.kr/cmmn/main.do)")
        st.markdown("[국토지리정보원](https://www.ngii.go.kr/kor/main.do)")
    
    with col2:
        st.markdown("#### 개발자 정보")
        st.write("20221050_YC_안현건") 




    
def show_home():
    st.header(" 대한민국")
    st.text(" 기상관측 데이터 분석 입니다")
    st.image("img/대한민국전도(120만)_국문_A4.jpg", width=500) #출처 국토지리정보원 
    

    footer()
    
def show_spot():
    
    col1, col2 = st.columns(2)
    with col1:
       selected_year = st.selectbox("년",[" "] + sorted(obs_data['년'].unique().tolist()))

    with col2:
       selected_month = st.selectbox("월",[" "] + sorted(obs_data['월'].unique().tolist()))
    
    
    input2 = st.selectbox("계산할값",("평균기온(°C)","최저기온(°C)","최고기온(°C)","일강수량(mm)","평균 상대습도(%)"))
    input3 = st.selectbox("계산식",("mean","max","min","count","sum"))
    input4 = st.selectbox("정렬",("없음","오름차순","내림차순"))
    
    filtered_data = obs_data.copy()
    
    if selected_year != " ":
        filtered_data = filtered_data.query("년 == @selected_year")

    if selected_month != " ":
        filtered_data = filtered_data.query("월 == @selected_month")
    
    result1 = filtered_data.groupby("지점명", as_index= False).agg(value = (input2 , input3))

    if input4 == "오름차순":
        show_value = result1.sort_values(by="value", ascending=True)
    elif input4 == "내림차순":
        show_value = result1.sort_values(by="value", ascending=False)
    else: # input4가 "없음"일 경우
        show_value = result1
    
    st.text("지점명을 그룹핑해서 " +input2 +"을(를) "+input3 + "로 계산")
    st.dataframe(show_value)
    c2 = px.bar(data_frame= show_value,  x= "지점명" , y = "value")
    st.plotly_chart( c2 )
    
    footer()
    
def show_data():
    
    st.subheader("자료실")
    result_data = obs_data.copy() #둘다 공백인경우
    
    input_seach = st.selectbox("지점명:", [" "] + obs_data['지점명'].unique().tolist() )

    #result_period = st.selectbox("기간", (" ","년","월","일") )

    col1, col2, col3 = st.columns(3)
    with col1:
       selected_year2 = st.selectbox("년",[" "] + sorted(obs_data['년'].unique().tolist()))

    with col2:
       selected_month2 = st.selectbox("월",[" "] + sorted(obs_data['월'].unique().tolist()))
    with col3:
        selected_day2 = st.selectbox("일",[" "] + sorted(obs_data['일'].unique().tolist()))

    if input_seach != " ":
        result_data = result_data.query("지점명 == @input_seach")

    if selected_year2 != " ":
        result_data = result_data.query("년 == @selected_year2")

    if selected_month2 != " ":
        result_data = result_data.query("월 == @selected_month2")

    if selected_day2 != " ":
        result_data = result_data.query("일 == @selected_day2")
        
    #if result_period != " " : 
    #    input_period = st.selectbox( result_period,sorted(obs_data[result_period].unique().tolist()) )
    #    result_data = result_data.query(f"`{result_period}` == @input_period")

    input_sort = st.selectbox("정렬기준",(" ","평균기온(°C)","최저기온(°C)","최고기온(°C)","일강수량(mm)", "평균 상대습도(%)"))

    if input_sort != " " : 
       input_TF = st.selectbox("",("오름차순","내림차순"))
       if input_TF=="오름차순" : TF_value = True
       else: TF_value = False
       result_data= result_data.sort_values(by = input_sort,ascending=TF_value)
        
    st.dataframe(result_data.drop(columns=['일시2', '년', '월', '일']) ,height=844) #표가 한눈에 보일수 있도록 길이 조정

    footer()
    
st.sidebar.header("")

selectedmenu = st.sidebar.selectbox("메뉴 제목", ["home","자료실","지점별분석"])

if selectedmenu == "home" : show_home()
   
elif selectedmenu == "지점별분석" : show_spot()

elif selectedmenu == "자료실" : show_data()

else:
    st.header("home")
    

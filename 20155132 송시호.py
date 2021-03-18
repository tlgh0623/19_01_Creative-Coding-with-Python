from urllib.request import urlopen
from bs4 import BeautifulSoup
from tkinter import *
import webbrowser

infotitle = {}          # 타이틀과 주소를 넣을 딕셔너리
nextcount = 0   # 다음 페이지를 판단할 변수

def hyper_link(event):      # 리스트박스 클릭시 이벤트 실행
    url = "https://www.clien.net"+infotitle[titlelist.get(ACTIVE)]
    webbrowser.open(url)

def gorefresh():                # 새로고침
    global nextcount            # 전역변수
    nextcount=0
    clear()
    refresh()
    
def clear():            # 리스트박스  지우기
    global infotitle            # 전역변수
    titlelist.delete(0,END)
    infotitle = {}          # 딕셔너리 초기화

def gotoNext():         # 다음 페이지
    global nextcount    # 전역변수
    nextcount += 1
    clear()
    refresh()

def gotobefore():       #이전 페이지
    global nextcount        # 전역변수
    nextcount -= 1
    clear()
    refresh()

def refresh():      # 리스트박스 아이템 추가
    global infotitle        # 전역변수
    global nextcount
    if nextcount == 0 or nextcount < 0: 
        html = urlopen('https://www.clien.net/service/board/jirum')     # url 처리
        nextcount = 0
    else:
        html = urlopen('https://www.clien.net/service/board/jirum?&od=T31&po=' + str(nextcount))    # 다음페이지 이동
        
    soup = BeautifulSoup(html, "html.parser")           
    count=1
    
    for tag in soup.select('a[data-role = list-title-text]'):       # 타이틀과 주소 딕셔너리에 추가
        infotitle[tag.text] = tag.get('href')
    
              
    for key in infotitle:                       # 리스트박스에 딕셔너리 키값 삽입
        titlelist.insert(count,key)
        count+=1

    titlelist.pack(side='bottom')
    
    yscrollbar.config(command=titlelist.yview)
    xscrollbar.config(command=titlelist.xview)
        
    titlelist.bind('<Double-Button-1>',hyper_link) #리스트박스 더블클릭 이벤트
    

window = Tk()
window.title("핫딜 알리미")
yscrollbar=Scrollbar(window)         # 수직스크롤바
yscrollbar.pack(side=RIGHT,fill=Y)
xscrollbar=Scrollbar(window,orient=HORIZONTAL)         # 수평 스크롤바
xscrollbar.pack(side=BOTTOM,fill=X)

# 리스트박스에 스크롤바 연결
titlelist = Listbox(window,yscrollcommand=yscrollbar.set,xscrollcommand=xscrollbar.set, width =0, height =0) 

label = Label(window, text = "오늘의 핫딜은?")
label.pack()
refresh()       # 리스트 박스 불러오기
refre = Button(window, text = "새로고침", command=(lambda:gorefresh()))      #새로고침 버튼
nextpage = Button(window, text = "다음페이지",command=(lambda:gotoNext()))           # 다음페이지 
beforepage = Button(window, text = "이전페이지",command=(lambda:gotobefore()))       # 이전페이지

beforepage.pack(side='left',fill=X, expand=YES)
refre.pack(side='left',fill=X, expand=YES)
nextpage.pack(side='left',fill=X, expand=YES)

window.mainloop()


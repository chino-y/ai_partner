import streamlit as st
import os
import datetime
import json

from astropy.io.ascii import write
from openai import OpenAI
from streamlit import session_state

#设置页面的配置项
st.set_page_config(
    page_title="AI智能伴侣",
    page_icon="😇",
    #布局
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={}
)


#大标题
st.title("AI智能伴侣")

#生成会话标识函数
def generate_session_id():
    return datetime.datetime.now().strftime("%Y-%m-%d %H-%M-%S")



#保存会话信息
def save_session():
    if st.session_state.current_session:
        # 构建新的会话对象
        new_session = {"current_session": st.session_state.current_session,
                       "messages": st.session_state.messages,
                       "nick_name": st.session_state.nick_name,
                       "nature": st.session_state.nature}
        # 创建sessions目录
        if not os.path.exists("sessions"):
            os.mkdir("sessions")
        # 保存会话数据
        if st.session_state.messages:
            with open(f"sessions/{st.session_state.current_session}.json", "w", encoding="utf-8") as f:
                json.dump(new_session, f, ensure_ascii=False, indent=4)

#加载会话信息
def load_sessions():
    session_list = []
    if os.path.exists("sessions"):
        file_list = os.listdir("sessions")
        for filename in file_list:
            if filename.endswith(".json"):
                session_list.append(filename[:-5])
    session_list.sort(reverse=True)
    return session_list

#加载指定会话信息
def load_session(session_name):
    try:
        if os.path.exists(f"sessions/{session_name}.json"):
            with open(f"sessions/{session_name}.json", "r", encoding="utf-8") as f:
                session_date = json.load(f)
                st.session_state.current_session = session_date["current_session"]
                st.session_state.messages = session_date["messages"]
                st.session_state.nick_name = session_date["nick_name"]
                st.session_state.nature = session_date["nature"]
    except Exception:
        st.error("加载会话失败！")



#删除会话信息
def delete_session(session_name):
    if os.path.exists(f"sessions/{session_name}.json"):
        os.remove(f"sessions/{session_name}.json")
        st.success("会话删除成功！")
        if session_name == st.session_state.current_session:
            st.session_state.messages = []
            st.session_state.current_session = generate_session_id()
    else:
        st.error("会话不存在！")



#系统提示词
system_prompt = """
    你叫%s，现在是用户的真实伴侣，请完全带入伴侣角色。
    规则：
        1.每次只会一条消息
        2.禁止任何场景或状态描述性文字
        3.匹配用户的语言
        4.回复简短，像微信聊天一样
        5.用符合伴侣性格的方式对话
        6.回复的内容，要充分体现伴侣的性格特征
    伴侣性格：
        %s
    你必须严格遵守上述规则来回复用户。

"""

#初始化聊天信息
if "messages" not in st.session_state:
    st.session_state.messages = []
if "nick_name" not in st.session_state:
    st.session_state.nick_name = "乐乐"
if "nature" not in st.session_state:
    st.session_state.nature = "可爱"
if "current_session" not in st.session_state:
    st.session_state.current_session = generate_session_id()

#展示聊天信息
st.text(f"会话名称：{st.session_state.current_session}")
for message in st.session_state.messages:
    st.chat_message(message["role"]).write(message["content"])
    # if message["role"] == "user":
    #     st.chat_message("user").write(message["content"])
    # else:
    #     st.chat_message("assistant").write(message["content"])

#创建与AI大模型交互的客户端对象
client = OpenAI(
        api_key=os.environ.get("DEEPSEEK_API_KEY"),
        base_url="https://api.deepseek.com")

#侧边栏
with st.sidebar:
    #会话信息
    st.subheader("AI控制面板")
    col1,col2 = st.columns([1,1])
    with col1:
        if st.button("新建会话", width="stretch", icon="✏️"):
            # 1.保存当前会话
            save_session()

            # 2.创建新的会话
            st.session_state.messages = []
            st.session_state.current_session = generate_session_id()
            # save_session()
            st.rerun()  # 重新运行页面
    with col2:
        if st.button("保存会话",width="stretch",icon="⬇️"):
            #1.保存当前会话
            save_session()
            #2.创建新的会话
            st.session_state.messages = []
            st.session_state.current_session = generate_session_id()
            st.rerun()#重新运行页面

    #分割线
    st.divider()


    #会话历史
    st.text("会话历史")
    session_list = load_sessions()
    for session in session_list:
        col1,col2 = st.columns([4,1])
        with col1:
            if st.button(session,width="stretch",icon="📄",key=f"load_{session}",type="primary" if session == st.session_state.current_session else "secondary"):
                load_session(session)
                st.rerun()
        with col2:
            if st.button("",width="stretch",icon="❌",key=f"delete_{session}"):
                delete_session(session)
                st.rerun()

    st.divider()

    st.subheader("伴侣信息")

    #昵称输入框
    nick_name = st.text_input("昵称",placeholder="请输入昵称",value=st.session_state.nick_name)
    if nick_name:
        st.session_state.nick_name = nick_name
    #性格输入框
    nature = st.text_area("性格",placeholder="请输入性格",value=st.session_state.nature)
    if nature:
        st.session_state.nature = nature

#消息输入框
prompt = st.chat_input("请输入您要问的问题")
if prompt:
    st.chat_message("user").write(prompt)

    #保存用户输入的提示词
    st.session_state.messages.append({"role": "user", "content": prompt})

    response = client.chat.completions.create(
        model="deepseek-v4-flash",
        messages=[
            {"role": "system", "content": system_prompt % (st.session_state.nick_name, st.session_state.nature)},
            *st.session_state.messages,
        ],
        stream=True,
        #reasoning_effort="high",
        #extra_body={"thinking": {"type": "enabled"}}
    )
    #非流式输出
    # print(response.choices[0].message.content)
    # st.chat_message("assistant").write(response.choices[0].message.content)


    response_message = st.empty()#创建一个空组件,用于展示大模型返回结果
    full_response = ""
    for chunk in response:
        if chunk.choices[0].delta.content is not None:
            content = chunk.choices[0].delta.content
            full_response += content
            response_message.chat_message("assistant").write(full_response)

    #保存大模型返回的结果
    st.session_state.messages.append({"role": "assistant", "content": full_response})

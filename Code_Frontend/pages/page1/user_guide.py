import streamlit as st
from dotenv import load_dotenv
import os
load_dotenv()
API = os.getenv("BE_API")
from pages.page1 import support_function as sf
import datetime

def show_user_guide():
    api = API
    from streamlit_cookies_controller import CookieController
    controller = CookieController()
    import requests,time
    
    def get_message(result):
      res = result.json()['data']
      message = res["message"]
      return message
    
    
    token = controller.get('token_data')

    st.session_state["uid"] = ""
    st.session_state['current_photo_url'] = ""
    st.session_state['name_user'] = ""
    st.session_state['email'] = ""
    if token:
            sf.check_time_token(token)
            st.session_state["user_id"] = 0
            st.session_state["token"] = ""
            picture_user = ""
            url = f"{api}/default/is_me"
            response = requests.get(url,params={'token': token})
            if not sf.check_status_response(response):
                  return
            res_status = response.json()['status']
            res = response.json()['data']
            if res_status == 200:
                user_id = res["user_id"]
                st.session_state["user_id"] = user_id
                headers = {"Authorization": f"Bearer {token}",'Content-Type': 'application/json', 'accept': 'application/json'}
                url_info = f"{api}/default/info_user/{user_id}"
                user_info_data = requests.get(url_info,headers=headers)
                if not sf.check_status_response(user_info_data):
                       return
                if user_info_data.status_code == 403:
                    sf.refresh_token_account()
                    token = controller.get("token_data")
                    headers = {"Authorization": f"Bearer {token}",'Content-Type': 'application/json', 'accept': 'application/json'}
                    url_info = f"{api}/default/info_user/{user_id}"
                    user_info_data = requests.get(url_info,headers=headers)
                    if not sf.check_status_response(user_info_data):
                        return
                    user_info_status = user_info_data.json()['status']
                    res1 = user_info_data.json()['data']
                    if user_info_status == 404:
                      message = user_info_data.json()['data']['message']
                      st.toast(message,icon='❌')
                    if user_info_status == 400:
                       message = user_info_data.json()['data']['message']
                       st.toast(message,icon='❌')
                    if user_info_status == 500:
                      message = user_info_data.json()['data']['message']
                      st.toast(message,icon='❌')
                    elif user_info_status == 502:
                      message = "Bad Gateway"
                      st.toast(message, icon='❌')
                    res1 = user_info_data.json()['data']              
                    picture_user = res1["photo_url"]
                    st.session_state['current_photo_url'] = ""
                    st.session_state['current_photo_url'] = picture_user
                    st.session_state["name_user"] = res1["display_name"]
                    st.session_state["uid"] = ""
                    st.session_state["uid"]  = res1["uid"]
                    st.session_state["email"] = ""
                    st.session_state["email"]  = res1["email"]
                    st.session_state["token"] = token
  
                user_info_status = user_info_data.json()['status']
                res1 = user_info_data.json()['data']
                if user_info_status == 404:
                    message = user_info_data.json()['data']['message']
                    st.toast(message,icon='❌')
                if user_info_status == 400:
                    message = user_info_data.json()['data']['message']
                    st.toast(message,icon='❌')
                if user_info_status == 500:
                    message = user_info_data.json()['data']['message']
                    st.toast(message,icon='❌')
                elif user_info_status == 502:
                  message = "Bad Gateway"
                  st.toast(message, icon='❌')
                res1 = user_info_data.json()['data']              
                picture_user = res1["photo_url"]
                st.session_state['current_photo_url'] = ""
                st.session_state['current_photo_url'] = picture_user
                st.session_state["name_user"] = res1["display_name"]
                st.session_state["uid"] = ""
                st.session_state["uid"]  = res1["uid"]
                st.session_state["email"] = ""
                st.session_state["email"]  = res1["email"]
                st.session_state["token"] = token
            else:
                message = response.json()['data']['message']
                st.toast(f"{message}", icon='❌')
    
    
    def check_state_login():
     user_id = st.session_state.get("user_id")
     api_url = f"{api}/users/check_state_login"
     params = {
    'user_id': user_id,
    'session_id_now': controller.get('session_id')
}   
     response = requests.get(api_url, params=params)
     if not sf.check_status_response(response):
                  return
     status = response.json()['status']
     if status == 200:
       check_result = response.json()['data']['check']
       if check_result == False:
                st.toast("Your account was accessed from a different location.",icon="❌")
                controller.set('token_data', None )
                controller.set('session_id',None)
                controller.set('email',None)
                time.sleep(2)
                st.markdown('<meta http-equiv="refresh" content="0;URL=http://localhost:8501/login" />', unsafe_allow_html=True)
     else:
         message = response.json()['data']['message']
         st.toast(f"{message}", icon='❌')
    
    st.sidebar.title("Function category")
    page = st.sidebar.radio("Select the function that needs instructions: ", ["Load File", "Delete one file", 
                                        "Delete all file", "Delete Chat", "Update name chat","Create new chat"
                                        ,"Update User Information","Change Password","Chat with text","Chat with voice"
                                        ,"Some other functions"])
    if page == "Load File":
        st.header("Load file Instructions", divider='blue')
        st.markdown("**1. To use file loading, please click the 'Browse files' button below to upload a file.**")
        st.markdown(''':red[NOTE: This application only accepts the following file formats: PDF, TXT, DOCX, DOC, PPT, CSV, JSON, XLSX, MD.
                    And the maximum file size for upload is 28MB.]''')
        st.markdown(
        """
        <div style="text-align: center;">
            <img src="https://github.com/vonhuy1/KLTN_demo/blob/main/image_kltn/upload_file/1.%20upload_file.png?raw=true" alt="Your Image Caption">
            <p><i>Image 1. The 'Browse files' button to upload your file</i></p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("**2. After click the 'Browse file' button. The next, selecting your file in the file explorer. And click the 'Open' button to upload your file.**")
        st.markdown(
        """
        <div style="text-align: center;">
            <img src="https://github.com/vonhuy1/KLTN_demo/blob/main/image_kltn/select_file.png?raw=true" alt="Your Image Caption" style="width: 85%;">
            <p><i>Image 2. The file explorer to select your file</i></p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("**3. After the file has been displayed as shown below, click the 'Load File' button, the following cases may occur.**")
        st.markdown(
        """
        <div style="text-align: center;">
            <img src="https://github.com/vonhuy1/KLTN_demo/blob/main/image_kltn/upload_file/3.%20upload_file.png?raw=true" alt="Your Image Caption">
            <p><i>Image 3. Your file was selected</i></p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("**4. If your file is uploaded successfully, there will be a notification as shown below on the screen interface.**")
        st.markdown(
        """
        <div style="text-align: center;">
            <img src="https://github.com/vonhuy1/KLTN_demo/blob/main/image_kltn/load_file_success.png?raw=true" alt="Your Image Caption" style="width: 85%;">
            <p><i>Image 4. File upload success notification</i></p>
        </div>
        """, unsafe_allow_html=True)
    
    elif page == "Delete one file":
        st.header("Delete a file Instructions", divider='blue')
        st.markdown("**1. Select the file in the 'Select a file' selectBox to use the function to delete a file in the Settings page.**")
        st.markdown(
        """
        <div style="text-align: center;">
            <img src="https://github.com/vonhuy1/KLTN_demo/blob/main/image_kltn/delete_one_file/1.png?raw=true" alt="Your Image Caption" style="width: 70%;">
            <p><i>Image 1. The 'Select a file' selectBox</i></p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("**2. After selecting the file to delete, you will see a notification that you are selecting the file as shown below.**")
        st.markdown(
        """
        <div style="text-align: center;">
            <img src="https://github.com/vonhuy1/KLTN_demo/blob/main/image_kltn/delete_one_file/2.png?raw=true" alt="Your Image Caption" style="width: 70%;">
            <p><i>Image 2. The selected file notification</i></p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("**3. Next, click the :red['Delete File'] button as shown below.**")
        st.markdown(
        """
        <div style="text-align: center;">
            <img src="https://github.com/vonhuy1/KLTN_demo/blob/main/image_kltn/delete_one_file/3.png?raw=true" alt="Your Image Caption" style="width: 70%;">
            <p><i>Image 3. The 'Delete File' button</i></p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("**4. After clicking, wait a moment for the application to automatically regenerate the question, process the remaining data, and delete your file.**")
        st.markdown(
        """
        <div style="text-align: center;">
            <img src="https://github.com/vonhuy1/KLTN_demo/blob/main/image_kltn/delete_one_file/4.png?raw=true" alt="Your Image Caption" style="width: 70%;">
            <p><i>Image 4. The deleted file and extract data success notification</i></p>
        </div>
        """, unsafe_allow_html=True)
                        
    elif page == "Delete all file":
        st.header("Delete all file Instructions", divider='blue')
        st.markdown("**1. Click the :red['Delete All File'] button as shown below to delete all file in the Settings page.**")
        st.markdown(''':red[NOTE: Before using this function, please note that all files you previously downloaded will be deleted and you will no longer be able to recover them.]''')
        st.markdown(
        """
        <div style="text-align: center;">
            <img src="https://github.com/vonhuy1/KLTN_demo/blob/main/image_kltn/delete_all_file/2.png?raw=true" alt="Your Image Caption" style="width: 70%;">
            <p><i>Image 1. The 'Delete All File' button</i></p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("**2. If the deletion is successful, there will be a notification as shown below.**")
        st.markdown(
        """
        <div style="text-align: center;">
            <img src="https://github.com/vonhuy1/KLTN_demo/blob/main/image_kltn/delete_all_file/3.png?raw=true" alt="Your Image Caption" style="width: 70%;">
            <p><i>Image 2. The delete all file success notification</i></p>
        </div>
        """, unsafe_allow_html=True)

    elif page == "Delete Chat":
        st.header("Delete chat Instructions", divider='blue')
        st.markdown("**1. To use the delete chat function you used before. In the arrow in the sidebar, click the chats to delete. The selected chat segment will be highlighted in a more prominent color than the remaining chat segments.**")
        st.markdown(
        """
        <div style="text-align: center;">
            <img src="https://github.com/vonhuy1/KLTN_demo/blob/main/image_kltn/delete_chat/1.png?raw=true" alt="Your Image Caption" style="width: 70%;">
            <p><i>Image 1. The selected chats to delete</i></p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("**2. Click the button 🗑️ as shown above to delete the chat. It will be next to the current chat you are selecting. After the chats is deleted, the result will be as shown below.**")
        st.markdown(
        """
        <div style="text-align: center;">
            <img src="https://github.com/vonhuy1/KLTN_demo/blob/main/image_kltn/delete_all_file_success.png?raw=true" alt="Your Image Caption" style="width: 70%;">
            <p><i>Image 2. The deleted chat success notification</i></p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("**3. In your chat, the deleted chat will no longer appear.**")
        st.markdown(
        """
        <div style="text-align: center;">
            <img src="https://github.com/vonhuy1/KLTN_demo/blob/main/image_kltn/delete_chat/3.png?raw=true" alt="Your Image Caption" style="width: 70%;">
            <p><i>Image 3. The list of chats in the sidebar</i></p>
        </div>
        """, unsafe_allow_html=True)

    elif page == "Update name chat":
        st.header("Update name chat Instructions", divider='blue')
        st.markdown("**1. To use the update name chat function you used before. In the arrow in the sidebar, click the chats to delete. The selected chat segment will be highlighted in a more prominent color than the remaining chat segments.**")
        st.markdown(
        """
        <div style="text-align: center;">
            <img src="https://github.com/vonhuy1/KLTN_demo/blob/main/image_kltn/update_name_chat/1.png?raw=true" alt="Your Image Caption" style="width: 70%;">
            <p><i>Image 1. The selected chats to update</i></p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("**2. Click the button 📝 as shown below to update the chat's name.**")
        st.markdown(
        """
        <div style="text-align: center;">
            <img src="https://github.com/vonhuy1/KLTN_demo/blob/main/image_kltn/update_name_chat/2.png?raw=true" alt="Your Image Caption" style="width: 70%;">
            <p><i>Image 2. The current chat's name</i></p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("**3. Enter the new chat's name in the box containing the current chat's name. Click the ✅ button to edit the chat's name. Click ❌ button to cancel the change.**")
        st.markdown(
        """
        <div style="text-align: center;">
            <img src="https://github.com/vonhuy1/KLTN_demo/blob/main/image_kltn/update_name_chat/3.png?raw=true" alt="Your Image Caption" style="width: 70%;">
            <p><i>Image 3. The new chat's name</i></p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("**4. After clicking ✅ button, the result will be as shown below.**")
        st.markdown(
        """
        <div style="text-align: center;">
            <img src="https://github.com/vonhuy1/juice-shop/blob/main/images/update_chat_name_success.png?raw=true" alt="Your Image Caption" style="width: 70%;">
            <p><i>Image 4. The updated chat's name success notification</i></p>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("**5. In your chat, your chat has been changed to the new name.**")
        st.markdown(
        """
        <div style="text-align: center;">
            <img src="https://github.com/vonhuy1/KLTN_demo/blob/main/image_kltn/update_name_chat/4.png?raw=true" alt="Your Image Caption" style="width: 70%;">
            <p><i>Image 5. The chats in the sidebar</i></p>
        </div>
        """, unsafe_allow_html=True)

    elif page == "Create new chat":
        st.header("Create new chat Instructions", divider='blue')
        st.markdown("**1. Click the ➕ :red[New Chat] button as shown below to create a new chat. Once you start creating, you'll be redirected to that chat. If the deletion is successful, there will be a notification.**")
        st.markdown(
        """
        <div style="text-align: center;">
            <img src="https://github.com/vonhuy1/KLTN_demo/blob/main/image_kltn/create_new_chat.png?raw=true" alt="Your Image Caption" style="width: 85%;">
            <p><i>Image 1. The new chat in the Home page</i></p>
        </div>
        """, unsafe_allow_html=True)
    elif page == "Update User Information":
        
        st.markdown("**1. In the Settings page, chose the radio 'User Information' button in the left sidebar.**")
        st.markdown(
        """
        <div style="text-align: center;">
            <img src="https://github.com/vonhuy1/juice-shop/blob/main/images/display_user_information_in_settings.png?raw=true" alt="Your Image Caption" style="width: 85%;">
            <p><i>Image 1. The "User Information" radio button in the Settings page</i></p>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("**2. User Information interface when clicking the 'User Information' radio button in the Settings page.**")
        st.markdown(
        """
        <div style="text-align: center;">
            <img src="https://github.com/vonhuy1/KLTN_demo/blob/main/image_kltn/update_user_info/1.png?raw=true" alt="Your Image Caption" style="width: 85%;">
            <p><i>Image 2. The User Information in the Profile page</i></p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("**3. Click the 'Save' button to save the new your name or photo.**")
        st.markdown("***For example in the Profile page, change the User Name from 'Nhu Y 1234567' to 'Nhu Y 123456789'***")
        st.markdown(
        """
        <div style="text-align: center;">
            <img src="https://github.com/vonhuy1/KLTN_demo/blob/main/image_kltn/update_user_info/2.png?raw=true" alt="Your Image Caption" style="width: 85%;">
            <p><i>Image 3. Change the User Name in the Profile page</i></p>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("Click Save to update User Information.")
        st.markdown(
        """
        <div style="text-align: center;">
            <img src="https://github.com/vonhuy1/KLTN_demo/blob/main/image_kltn/update_user_info/3.png?raw=true" alt="Your Image Caption" style="width: 85%;">
            <p><i>Image 4. The new user's name had been changed</i></p>
        </div>
        """, unsafe_allow_html=True)
    elif page == "Change Password":
        st.markdown("**1. In the Profile page, chose the radio 'Change Password' button in the left sidebar.**")
        st.write("Change Password interface when clicking the 'Change Password' button in the Settings page.")
        st.markdown(
        """
        <div style="text-align: center;">
            <img src="https://github.com/vonhuy1/KLTN_demo/blob/main/image_kltn/change_1.png?raw=true" alt="Your Image Caption" style="width: 85%;">
            <p><i>Image 1. The Change Password in the Profile page</i></p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("**2. After the interface is displayed, fill in all the information and click the 'Update' button to change the password.**")
        
        st.markdown(
        """
        <div style="text-align: center;">
            <img src="https://github.com/vonhuy1/KLTN_demo/blob/main/image_kltn/change_2.png?raw=true" alt="Your Image Caption" style="width: 85%;">
            <p><i>Image 2. The password information in the Profile page</i></p>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("**3. If change password is successfully, there will be a notification as shown below.**")
        st.markdown(
        """
        <div style="text-align: center;">
            <img src="https://github.com/vonhuy1/KLTN_demo/blob/main/image_kltn/change_3.png?raw=true" alt="Your Image Caption" style="width: 85%;">
            <p><i>Image 3. Notification that user password information has been updated successfully</i></p>
        </div>
        """, unsafe_allow_html=True)
    elif page == "Chat with text":
        check_state_login()
        st.header("Chat with text Instructions", divider='blue')
        st.markdown("**1. To use chat with text, please enter a message into the chat box**")
        st.markdown(''':red[NOTE: Please enter a question related to the your uploaded files. To achieve better answer quality, attach the file name to your question.
                    The time to receive feedback depends on your file and the average response time will be 15s to 30s/1 question.]''')
        st.markdown(
        """
        <div style="text-align: center;">
            <img src="https://github.com/vonhuy1/juice-shop/blob/main/images/1_chat_with_text.png?raw=true" alt="Your Image Caption" style="width: 85%;">
            <p><i>Image 1. Enter the question in the chatbox</i></p>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("**2. Next, click the :red['↑'] button as shown below. Please wait.**")
        st.markdown(
        """
        <div style="text-align: center;">
            <img src="https://github.com/vonhuy1/KLTN_demo/blob/main/image_kltn/chat_with_text/1.png?raw=true" alt="Your Image Caption" style="width: 85%;">
            <p><i>Image 2. The question has been submitted</i></p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("**3. If you receive a successful response, the system will display a notification and on the chat screen you will receive a response.**")
        st.markdown(
        """
        <div style="text-align: center;">
            <img src="https://github.com/vonhuy1/juice-shop/blob/main/images/3_chat_with_text_success.png?raw=true" alt="Your Image Caption" style="width: 85%;">
            <p><i>Image 3. Notification that the question has been submitted successfully</i></p>
        </div>
        """, unsafe_allow_html=True)
        st.markdown(
        """
        <div style="text-align: center;">
            <img src="https://github.com/vonhuy1/KLTN_demo/blob/main/image_kltn/chat_with_text/4.png?raw=true" alt="Your Image Caption" style="width: 85%;">
            <p><i>Image 4. The system has sent a reply.</i></p>
        </div>
        """, unsafe_allow_html=True)
    elif page == "Chat with voice":
        st.header("Chat with voice Instructions", divider='blue')
        st.markdown("**1. To use chat with voice, please click button 🎙️**")
        st.markdown(''':red[NOTE: Please enter a question related to the your uploaded files. To achieve better answer quality, attach the file name to your question.
                    The time to receive feedback depends on your file and the average response time will be 15s to 30s/1 question.]''')
        st.markdown("Please click 'Allow this time' or 'Allow on very visit' to grant microphone permissions for application as shown below.")
        st.markdown(
        """
        <div style="text-align: center;">
            <img src="https://github.com/vonhuy1/juice-shop/blob/main/images/1_chat_with_voice_permission.png?raw=true" alt="Your Image Caption" style="width: 85%;">
            <p><i>Image 1. The microphone permission for application</i></p>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("Wait to see if an icon 🛑 appears on the button. And then you just clicked.")
        st.markdown(
        """
        <div style="text-align: center;">
            <img src="https://github.com/vonhuy1/KLTN_demo/blob/main/image_kltn/chat_with_voice/Picture2.png?raw=true" alt="Your Image Caption" style="width: 85%;">
            <p><i>Image 2. The 🛑 button to chat with voice</i></p>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("**2. The next, say the your question to the chatbot answer. And wait.**")
        st.markdown("**3. If you receive a successful response, the system will display a notification and on the chat screen you will receive a response.**")
        st.markdown(
        """
        <div style="text-align: center;">
            <img src="https://github.com/vonhuy1/juice-shop/blob/main/images/3_chat_with_text_success.png?raw=true" alt="Your Image Caption" style="width: 85%;">
            <p><i>Image 3. Notification that the question has been submitted successfully</i></p>
        </div>
        """, unsafe_allow_html=True)
        st.markdown(
        """
        <div style="text-align: center;">
            <img src="https://github.com/vonhuy1/KLTN_demo/blob/main/image_kltn/chat_with_voice/Picture1.png?raw=true" alt="Your Image Caption" style="width: 85%;">
            <p><i>Image 4. The system has sent a reply.</i></p>
        </div>
        """, unsafe_allow_html=True)
    elif page == "Some other functions":
        st.header("Some other functions Instructions",divider="blue")
        st.markdown("### 1. Regenerate",unsafe_allow_html=True)
        st.markdown("This is the function used to recreate the answer from the last question you asked in the chat.")
        st.markdown("Click the 'Regenerate' button to use this function as shown below. After waiting time to response, you will be get the similar chat with text function.")
        st.markdown(
        """
        <div style="text-align: center;">
            <img src="https://github.com/vonhuy1/juice-shop/blob/main/images/1.1_Regenerate.png?raw=true" alt="Your Image Caption" style="width: 85%;">
            <p><i>Image 1. The 'Regenerate' button above the chatbox</i></p>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("### 2. Stop",unsafe_allow_html=True)
        st.markdown("This is the function for stopping the reply from the chatbot during the reply process.") 
        st.markdown("Click the ■ button to use this function when you have a question that needs to be stopped during the asking process.")
        st.markdown(
        """
        <div style="text-align: center;">
            <img src="https://github.com/vonhuy1/juice-shop/blob/main/images/1.2_stop.png?raw=true" alt="Your Image Caption" style="width: 85%;">
            <p><i>Image 2. The question was be stopped during the asking process</i></p>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("### 3. Send messages from suggestions of files you upload",unsafe_allow_html=True)
        st.markdown("This is the function used to use the suggested questions available in each file (each file will have 2 questions).")
        st.markdown("The suggested questions will appear in the chat and have a ➤ before the question. Click on them to use this funtion. The question will be created and sent while just waiting for a response just like using the chat with text function.")
        st.markdown(
        """
        <div style="text-align: center;">
            <img src="https://github.com/vonhuy1/KLTN_demo/blob/main/image_kltn/orther_function_3.png?raw=true" alt="Your Image Caption" style="width: 85%;">
            <p><i>Image 3. The suggested questions in the chatbox</i></p>
        </div>
        """, unsafe_allow_html=True)
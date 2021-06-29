import requests
import os
import json
import traceback

from app.model import get_session, User


def process_user_details(username):
    app_session = get_session()
    try:
        """ Get user information from twitter account """
        url = os.getenv('TWITTER_BASE_URL')+"users/by/username/"+username
        headers = {"Authorization":"{}".format(os.getenv('TWITTER_BEARER_TOKEN'))}
        response = requests.request("GET", url, headers=headers)
        
        final_resp={}
        if response.status_code == 200:
            data = response.json()
            if "errors" in data and len(data['errors']) > 0:
                final_resp['status']=0
                final_resp['message']=data['errors'][0]['detail']  
            else:
                user_id = data['data']['id']
                name = data['data']['name']
                username = data['data']['username']
                user = app_session.query(User).filter(User.user_id==user_id).first()
                if user:
                    final_resp['status']=1
                    final_resp['message']='success' 
                    final_resp['id'] = user.id
                else:
                    """ Record the twitter user information in ourtable """
                    user = User(user_id=user_id,name=name, username=username)
                    app_session.add(user)
                    app_session.commit()

                    final_resp['status']=1
                    final_resp['message']='success' 
                    final_resp['id']=user.id
        else:
            final_resp['status']=0
            final_resp['message']='failure'  

    except Exception as ex:
        print("Exception:", traceback.format_exc())
        final_resp['status']=0
        final_resp['message']='Internal server error'  

    return final_resp       
        

    
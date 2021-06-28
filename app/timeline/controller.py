import requests
import os
import json
import traceback

from datetime import datetime, timezone 

from app.model import get_session, User, Sync, Timeline

def get_timeline_data(request):
    app_session = get_session()
    try:
        id = request.args.get('id')
        final_resp = {}
        user = app_session.query(User).filter(User.id==id).first()
        sync = app_session.query(Sync).filter(Sync.u_id==id).first()
        params = {
            "max_results":100,
            "tweet.fields":'attachments,author_id,conversation_id,created_at,entities,geo,id,in_reply_to_user_id,lang,referenced_tweets,reply_settings,source,text,withheld',
        }
        now = datetime.now()

        if sync:
            """ This params will be used to getting the recent tweets """
            params['start_time'] = convert_date_time(now, "%Y-%m-%d %H:%M:%S.%f", "%Y-%m-%dT%H:%M:%S")+".00Z"
            params['end_time'] = convert_date_time(sync.last_sync_at, "%Y-%m-%d %H:%M:%S", "%Y-%m-%dT%H:%M:%S")+".00Z"
        else:
            """ Recording the last sync datetime """
            sync = Sync(u_id=id,last_sync_at=now)
            app_session.add(sync)
            app_session.commit()    

        # print(params)
        
        """ user timeline tweets call """
        url = os.getenv('TWITTER_BASE_URL')+"users/"+str(user.user_id)+"/tweets"
        headers = {"Authorization":"{}".format(os.getenv('TWITTER_BEARER_TOKEN'))}
        response = requests.request("GET", url, headers=headers, params=params)
       
        """ once we got the result we will insert into Database using bulk insert """
        if response.status_code == 200:
            data = response.json()
            if 'errors' not in data:
                data_list = data['data']
                print("total_count", len(data_list))
                if len(data_list) > 0:
                    timeline = [Timeline(u_id = id, author_id=value['author_id'], conversation_id=value['conversation_id'],source=value['source'], reply_settings=value['reply_settings'],text=value['text'], timeline_at=convert_date_time(value['created_at'], "%Y-%m-%dT%H:%M:%S.%fZ", "%Y-%m-%d %H:%M:%S"), json=json.dumps(value)) for value in data_list]
                    app_session.add_all(timeline)
                    app_session.commit()

        order = ''
        qsearch = ''
        if request.form:
            order = request.form['sort_by']
            qsearch = request.form['qsearch']

        """ Get all timeline tweets for coressponding user """ 
        if order != '' and  qsearch != '':      
            all_timeline_data = app_session.query(Timeline).filter(Timeline.u_id==id, Timeline.text.like('%'+str(qsearch)+'%')).order_by(Timeline.timeline_at.asc() if order == 'asc' else  Timeline.timeline_at.desc()).all()
        elif order == '' and  qsearch != '': 
            all_timeline_data = app_session.query(Timeline).filter(Timeline.u_id==id, Timeline.text.like('%'+str(qsearch)+'%')).order_by(Timeline.timeline_at.desc()).all()    
        elif order != '' and  qsearch == '':      
            all_timeline_data = app_session.query(Timeline).filter(Timeline.u_id==id).order_by(Timeline.timeline_at.asc() if order == 'asc' else  Timeline.timeline_at.desc()).all()    
        else:
            all_timeline_data = app_session.query(Timeline).filter(Timeline.u_id==id).order_by(Timeline.timeline_at.desc()).all()    

        final_resp = {
            "status":1,
            "message":"success",
            "records" :{
                "data":formated_data(all_timeline_data, user.username),
                "user":{
                    "id":user.id,
                    "user_id":user.user_id,
                    "name":user.name,
                    "username":user.username
                },
                "forms":{
                    "qsearch":qsearch,
                    "sort_by":order
                }
            }
        }
        return final_resp
                
    except Exception as ex:
        print("Exception:", traceback.format_exc())
        final_resp['status']=0
        final_resp['message']='Internal server error'

        return final_resp


def convert_date_time(date_time, from_format, to_format = None):
    return datetime.strptime(str(date_time), from_format).strftime(to_format)

def formated_data(data, author):
    res_list = []
    for value in data:
        res_dict = {
            "id":value.id,
            "text":value.text,
            "created_at":convert_date_time(value.timeline_at,"%Y-%m-%d %H:%M:%S", "%d-%m-%Y %H:%M:%S"),
            "source":value.source,
            "author":author
        }
        res_list.append(res_dict)
    # print("res_list",res_list)
    return res_list       
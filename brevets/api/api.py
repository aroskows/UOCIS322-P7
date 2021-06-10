import os
from flask import Flask, request
from flask_restful import Resource, Api
from pymongo import MongoClient
import json


app = Flask(__name__)
api = Api(app)


client = MongoClient('mongodb://' + os.environ['MONGODB_HOSTNAME'], 27017)
db = client.tododb

#mydata = list(db.tododb.find())
#print(mydata)
#open_times_list = []
#close_times_list = []
#all_times_list = []
#for i in mydata:
    # i is an dictionary with km, open times, and close times
#    open_times_list.append(str(i['open_time'])) 
#    close_times_list.append(str(i['close_time']))
#    temp = [str(i['open_time']), str(i['close_time'])]
#    all_times_list.append(temp) 


   # print("km =", i['km'])
#mykeys = mydata.keys()
#print(mykeys)

class listAll(Resource):
    def get(self, dtype, topk):
        mydata = list(db.tododb.find())
        app.logger.debug("ALL")
        app.logger.debug(dtype)
        app.logger.debug(topk)
        all_times_list = []
        counter = 0
        for i in mydata:
            # i is an dictionary with km, open times, and close times
            #open_times_list.append(str(i['open_time']))
            #close_times_list.append(str(i['close_time']))
            counter += 1
            if counter > int(topk) and topk != "-1":
                break
            temp = [str(i['open_time']), str(i['close_time'])]
            all_times_list.append(temp)

        app.logger.debug(dtype)
        if dtype == "CSV" or dtype == "V":
            #return in CSV form?

            csv_all = ''
            counter = 0
            for i in all_times_list:
                csv_all += ", ".join(i)
                csv_all += "  "
                counter += 1
            #    if counter >= topk:
             #       break
            return csv_all



            
        else:
            #return in json form
            result = {
                    'json_all': all_times_list
                    }
            return json.dumps(result)
    

class listOpen(Resource):
    def get(self, dtype, topk):
        mydata = list(db.tododb.find())
        app.logger.debug("OPEN")
        #topnum = request.args.get('top', default=-1)
        open_times_list = []
        counter = 0
        for i in mydata:
            # i is an dictionary with km, open times, and close times
            counter += 1
            if counter > int(topk) and topk != "-1":
                break
            open_times_list.append(str(i['open_time']))


        if dtype == "CSV" or dtype == "V": 
            csv_open = ", ".join(open_times_list)
            return csv_open
        else:
            #return in json form
            result = {
                    'json_open': open_times_list
                    }
            return json.dumps(result)


class listClose(Resource):
    def get(self, dtype, topk):
        #print("hello")       
        mydata = list(db.tododb.find())
        
        app.logger.debug("CLOSE")
        #app.logger.debug(topk)
        #topnum = request.args.get('top', default=-1)
        #dtype = request.args.get('dtype')
        app.logger.debug(dtype)
        app.logger.debug(topk)
        counter = 0
        close_times_list = []
        for i in mydata:
            # i is an dictionary with km, open times, and close times
            counter += 1
            app.logger.debug("loop")
            app.logger.debug(counter)
            app.logger.debug(topk)
            if counter > int(topk) and (topk != '-1'):
                break
            close_times_list.append(str(i['close_time']))

        if dtype == "CSV" or dtype == "V":
            
            csv_close = ", ".join(close_times_list)
            return csv_close
        else:
            #return in json form
            result = {
                    'json_close': close_times_list
                    }
            return json.dumps(result)

class RegisterUser(Resource):
    def get(self, username, hashed): 
        app.logger.debug("MADE IT")
        app.logger.debug(username)
        app.logger.debug(hashed)
        mydata = list(db.tododb.find())
        user = [username, hashed]
        app.logger.debug(user)
        app.logger.debug(mydata)

        for item  in mydata:
            app.logger.debug(item)
            if item == user:
                return False
        user_id = len(mydata) + 1
        app.logger.debug(user_id)
        item_doc = { 
            str(user_id): user
            }
        app.logger.debug(item_doc)
        db.tododb.insert_one(item_doc)
        return item_doc

class getUser(Resource):
    def get(self, user_id, username, hashed):
        mydata = list(db.tododb.find())
       
        #for item in mydata:
        app.logger.debug("GETTING")
        if str(user_id) in mydata:
            app.logger.debug("IN THERE")
            return mydata[user_id]
        else:
            flask.abort(400)
        app.logger.debug(mydata[str(user_id)])
                


'''@app.route('/listClose'):
    def listClose(topk, dtype):
        app.logger.debug("CLOSE W/ ROUTE")
        if dtype == "JSON":
            app.logger.debug("json")
        return 1 '''

api.add_resource(listAll, '/listAll/<dtype>/<topk>')
api.add_resource(listOpen, '/listOpen/<dtype>/<topk>')
api.add_resource(listClose, '/listClose/<dtype>/<topk>')
api.add_resource(RegisterUser, '/RegisterUser/<username>/<hashed>')
api.add_resource(getUser, '/getUser/<user_id>/<username>/<hashed>')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)


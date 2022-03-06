import redis
from http.client import OK
from flask import json, Flask, request


app = Flask(__name__)


redis_cache = redis.Redis(host='redis', port=6379, db=0,
                          password='redis', charset="utf-8", decode_responses=True)


number = 0
my_list = []
my_dict = {}


@app.route('/', methods=['POST'])
def api_message():
    try:
        target = request.headers['CLIENT-KEY']
        global number
        if redis_cache.__contains__(target):
            a = int(redis_cache.get(target))
            redis_cache.set(target, a + 1)
            my_key_list = redis_cache.keys()
            my_list = []
            for i in my_key_list:
                my_list.append(redis_cache.get(i))
            zip_iterator = zip(my_key_list, my_list)
            a_dict = dict(zip_iterator)
            return {'state':
                    a_dict
                    }

        else:
            number = 0
            number += 1
            redis_cache.set(target, number)
            my_key_list = redis_cache.keys()
            my_list = []
            for i in my_key_list:
                my_list.append(redis_cache.get(i))
            zip_iterator = zip(my_key_list, my_list)
            a_dict = dict(zip_iterator)
            return {'state':
                    a_dict
                    }

    except:
        my_key_list = redis_cache.keys()
        my_list = []
        for i in my_key_list:
            my_list.append(redis_cache.get(i))
        zip_iterator = zip(my_key_list, my_list)
        a_dict = dict(zip_iterator)
        return {'state':
                a_dict
                }


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=8000)

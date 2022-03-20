from flask import Flask, request, make_response
from flask import jsonify
from flask_limiter import Limiter
import redis


def get_client_key():
    return request.headers.get('CLIENT-KEY')


app = Flask(__name__)
limiter = Limiter(app, key_func=get_client_key)


redis_cache = redis.Redis(host='redis', port=6379, db=0,
                          password='redis', charset="utf-8", decode_responses=True)


@app.errorhandler(429)
def ratelimit_handler(e):
    return make_response(
        jsonify(
            {"message": f"Too many request from {request.headers.get('CLIENT-KEY')}"}), 429
    )


number = 0
my_list = []
my_dict = {}


@app.route('/', methods=['POST'])
@limiter.limit('10/minute')
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

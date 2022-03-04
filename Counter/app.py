from flask import json, Flask, request
app = Flask(__name__)

number = 0
my_list = []
my_dict = {}


@app.route('/', methods=['POST'])
def api_message():
    try:
        target = request.headers['CLIENT-KEY']
        global number

        if target in my_list:
            number += 1
            my_dict[target] = number
            return {'state':
                    my_dict
                    }
        else:
            my_list.append(target)
            number = 0
            number += 1
            my_dict[target] = number
            return {'state':
                    my_dict
                    }
    except:
        return {'state':
                my_dict
                }


if __name__ == "__main__":
    app.run(debug=True, port=8000)

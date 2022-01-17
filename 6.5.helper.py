from flask import Flask

app = Flask(__name__)


@app.route("/")
def hello_word():
    testdata = '''
    [{
    "email": "d.naumov@slurm.io",
    "rsa_pub_key": "gtertertergeg",
    "access_until": "15-08-2021"
    },
    {
    "email": "a.egorov@slurm.io",
    "rsa_pub_key": "trhrterttegr",
    "access_until": "10-12-2021"
    }]
    '''
    return testdata


if __name__ == '__main__':
    app.run(port=5000)


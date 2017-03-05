from webofcomics import app

print 'OSL'

@app.route('/')
def index():
    return 'Hello World!'

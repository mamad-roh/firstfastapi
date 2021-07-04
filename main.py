from fastapi import FastAPI

app = FastAPI()

@app.get('/')
def index():
    return {
        'user': {
            'name': 'mamad',
            'phone': '09370317252'
        },
        'message': 'have a good day'
    }


@app.get('/about')
def about():
    return {
        'page': {
            'name': 'about',
            'link': '/about'
        },
        'message': 'you are in about page'
    }
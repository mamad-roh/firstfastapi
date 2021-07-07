from typing import Optional
from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel
from starlette.routing import Host
from uvicorn import *
import uvicorn

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


@app.get('/blog')
def blogList(limit: int = 10, published: bool = True, sort: Optional[str] = None):
    return {
        'page': {
            'name': 'blogs list',
            'link': '/blog'
        },
        'data': limit,
        'message': 'have a good day'
    }

@app.get('/blog/unpublished')
def unpublished():
    return {
        'page': {
            'name': 'blog',
            'link': '/blog/unpublished'
        },
        'message': 'have a good day'
    }


@app.get('/blog/{id}')
def show(id: int):
    return {
        'page': {
            'name': 'blog',
            'link': '/blog/{}'.format(id)
        },
        'data': id,
        'message': 'have a good day'
    }


@app.get('/blog/{id}/comments')
def comments(id: int):
    return {
        'page': {
            'name': 'blog comments',
            'link': '/blog/{}/comments'.format(id)
        },
        'data': 'blog comments '+str(id),
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


class Blog(BaseModel):
    title: str
    body: str
    published: Optional[bool]=False


@app.post('/blog')
def create(request: Blog):
    return {
        'page': {
            'name': 'create blog',
            'link': '/blog',
            'method': 'post'
        },
        'data': request,
        'message': 'you are in about page'
    }


if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port= 8098)
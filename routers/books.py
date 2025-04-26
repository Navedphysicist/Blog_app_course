from fastapi import APIRouter,Header,Response,Cookie
from typing import Optional, List
from fastapi.responses import Response, PlainTextResponse, HTMLResponse



router = APIRouter(
    prefix='/books',
    tags=['Books']
)


books = ['Math','Science','English']


@router.get('/header')
def get_header(response: Response,custom_header : Optional[List[str]] = Header(None),my_cookie : str = Cookie(None)):
    
    response.headers['Bearer'] = 'my_header'
    # response.set_cookie('token','MY_VALUE')
    # response.delete_cookie('token')
    return {
        'custome_header':custom_header,
        'cookie' : my_cookie
    }






@router.get('/{id}',responses={
    200:{
        'content' : {
            'text/html' : {
                "example" : "<div>English</div>"

            }
        },
        "description" : "Returns the Html Response"
    },
    404: {
        'content' : {
            'text/plain' : {
                "example" : "String"

            }
        },
        "description" : "Returns the Plain Response"
    }


})
def get_book(id:int):
    if id >= len(books):
        data = "Book is not available"
        return PlainTextResponse(content=data,status_code=404)
    
    book = books[id]

    data = f"""
 <head>
   <style>
        .book {{
        width : 600px;
        height : 40px;
        border : 2px green;
        background-color : teal;
        text-align: center;
        line-height: 30px;
        font-weight: bold;

        }}
        </style>
 </head>
        <body>
        <div class="book">{book}</div>
        </body>  
    """

    return HTMLResponse(content=data,status_code=200)


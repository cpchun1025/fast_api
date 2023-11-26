from fastapi import Header, HTTPException


async def get_token_header(x_token: str = Header()):
    print('get_token_header: {}'.format(x_token))
    # if x_token != "fake-super-secret-token":
    #     raise HTTPException(status_code=400, detail="X-Token header invalid")


async def get_query_token(token: str):
    print('get_query_token: {}'.format(token))
    # if token != "jessica":
    #     raise HTTPException(status_code=400, detail="No Jessica token provided")

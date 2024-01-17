from authenticate import client
from variables import FUNCTION_EXTERNAL_ID


func = client.functions.retrieve(external_id=FUNCTION_EXTERNAL_ID)
call = func.call()
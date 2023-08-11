import uvicorn
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from generators import GeneratorBase, StarCoder
import json
import time
from util import logger, get_parser

app = FastAPI()
app.add_middleware(
    CORSMiddleware
)
generator: GeneratorBase = ...


@app.post("/api/generate/")
async def api(request: Request):
    json_request: dict = await request.json()
    inputs: str = json_request['inputs']
    parameters: dict = json_request['parameters']
    logger.debug(f'{request.client.host}:{request.client.port} inputs = {json.dumps(inputs)}')
    start_time = time.time() 
    generated_text: str = generator.generate(inputs, parameters)
    end_time = time.time()
    elapsed_time = end_time - start_time 
    logger.info(f'{request.client.host}:{request.client.port} Elapsed time: {elapsed_time :.2f} seconds ')
    logger.debug(f'{request.client.host}:{request.client.port} generated_text = {json.dumps(generated_text)}')
    return {
        "generated_text": generated_text,
        "status": 200
    }


def main():
    global generator
    args = get_parser().parse_args()
    generator = StarCoder(args.pretrained, device_map='auto')
    uvicorn.run(app, host=args.host, port=args.port)


if __name__ == '__main__':
    main()

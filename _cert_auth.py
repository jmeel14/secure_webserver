import asyncio
import certification
from funcs import commons

async def activate_ca(ca_gen):
    return await ca_gen.live()


LOCAL_CA = certification.ca.CACertGenerator()
while True:
    run_loop = asyncio.new_event_loop()
    run_loop.run_until_complete(LOCAL_CA.live())
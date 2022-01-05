#!/usr/bin/env python3
import os
import faust

TOPIC = 'temperature'

class Temperature(faust.Record, serializer='json'):
    reading_ts: int
    sensor: str
    value: int

# host.docker.internal is how a docker container connects to the local machine.
# Don't use in production, this only works with Docker for Mac in development
kafka_broker = os.environ['KAFKA_BROKER']
kafka_broker = 'kafka://'+ kafka_broker
print(kafka_broker)

app = faust.App('temp-analyzer', broker=kafka_broker,)
topic = app.topic(TOPIC, value_type=Temperature)

print('test')
@app.agent(topic)
async def check(temperatures):
    async for temperature in temperatures:
        print(f'{temperature.value} reading at ts {temperature.reading_ts} taken from {temperature.sensor}.')
        #print(f'Reading time {temperature.reading_ts} from {temperature.sensor} value {temperature.value}')


if __name__ == '__main__':
    app.main()
from pyflink.common import Row
from pyflink.common.serialization import JsonRowDeserializationSchema
from pyflink.common.typeinfo import Types
from pyflink.datastream import StreamExecutionEnvironment
from pyflink.datastream.time_characteristic import TimeCharacteristic
from pyflink.table import StreamTableEnvironment
from pyflink.datastream.connectors import FlinkKafkaConsumer
from pyflink.table.schema import Schema
from pyflink.table.window import Tumble
from pyflink.table import expressions as expr
from redis import Redis

redis = Redis()

def datastream_api_demo():
    # 1. create a StreamExecutionEnvironment
    env = StreamExecutionEnvironment.get_execution_environment()
    table_env = StreamTableEnvironment.create(env)
    env.set_stream_time_characteristic(TimeCharacteristic.EventTime)

    # 2. create source DataStream
    deserialization_schema = JsonRowDeserializationSchema.builder() \
        .type_info(type_info=Types.ROW_NAMED(field_names=["user_id", "anime_id", "happened_at"], field_types=[Types.STRING(), Types.STRING(), Types.STRING()])) \
        .build()

    kafka_source = FlinkKafkaConsumer(
        topics='clicks',
        deserialization_schema=deserialization_schema,
        properties={'bootstrap.servers': 'localhost:9092', 'group.id': 'recall-flink'})

    ds = env.add_source(kafka_source)


    # 3. Convert stream to table
    schema = Schema.new_builder() \
        .column('user_id', 'string') \
        .column('anime_id', 'string') \
        .column('happened_at', 'string') \
        .column_by_metadata('rowtime', 'TIMESTAMP_LTZ(3)') \
        .watermark('rowtime', "rowtime - INTERVAL '5' SECOND") \
        .build()

    t = table_env.from_data_stream(ds, schema)
    t.print_schema()

    # 4. Consume stream
    res_table = t \
        .window(Tumble.over(expr.lit(5).seconds).on(t.rowtime).alias('w')) \
        .group_by(expr.col('w'), expr.col('user_id')) \
        .select(
            expr.col('w').start.alias('start_t'),
            expr.col('user_id'),
            expr.col('anime_id').collect
        ) \
        .execute()


    # 5. Save result
    redis_prefix = 'recent_clicks'
    with res_table.collect() as results:
        for result in results:
            user_id = result[1]
            clicks = result[2]
            print(f'user: {user_id}, clicks: {clicks}')
            redis.hset(f'{redis_prefix}:{user_id}', mapping=clicks)


    # 6. execute the job
    env.execute('datastream_api_demo')
    table_env.execute('table')


if __name__ == '__main__':
    datastream_api_demo()

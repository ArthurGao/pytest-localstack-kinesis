import json

import pytest_localstack
from tests.functional.test_service_fixture.consumer_thread import ConsumerThread

localstack = pytest_localstack.session_fixture(scope="module", autouse=True)


class TestKinesisStream:

    def test_stream_action_create(self, localstack):
        stream_name = "test"
        client = localstack.botocore.client("kinesis")
        stream_exists_waiter = client.get_waiter('stream_exists')
        client.create_stream(StreamName=stream_name, ShardCount=1)
        stream_exists_waiter.wait(StreamName=stream_name)
        response = client.describe_stream(StreamName=stream_name)
        details = response['StreamDescription']
        assert details['StreamName'] == stream_name
        assert details['StreamStatus'] == 'ACTIVE'

        test_object = {
            "TestName": "test name",
            "TestValue": "test value"
        }
        consumer = ConsumerThread(stream_name, client, details, test_object)
        consumer.start()
        client.put_record(StreamName=stream_name, Data=json.dumps(test_object), PartitionKey="test")

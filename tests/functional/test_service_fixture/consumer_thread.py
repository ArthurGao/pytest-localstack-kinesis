import json
import threading


class ConsumerThread(threading.Thread):
    def __init__(self, stream_name, client, details, test_object):
        super().__init__()
        self.stream_name = stream_name
        self.client = client
        self.details = details
        self.test_object = test_object

    def run(self):

        """
        Gets records from the stream. This function is a generator that first gets
        a shard iterator for the stream, then uses the shard iterator to get records
        in batches from the stream. Each batch of records is yielded back to the
        caller until the specified maximum number of records has been retrieved.

        :param max_records: The maximum number of records to retrieve.
        :return: Yields the current batch of retrieved records.
        """

        max_records = 1
        response = self.client.get_shard_iterator(
            StreamName=self.stream_name, ShardId=self.details['Shards'][0]['ShardId'],
            ShardIteratorType='LATEST')
        shard_iter = response['ShardIterator']
        record_count = 0
        while record_count < max_records:
            response = self.client.get_records(
                ShardIterator=shard_iter, Limit=10)
            shard_iter = response['NextShardIterator']
            records = response['Records']
            record_count += len(records)
            for record in records:
                assert json.loads(record['Data']) == self.test_object
                print("Got record: {}".format(record['Data']))

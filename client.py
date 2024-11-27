import grpc
import message_queue_pb2, message_queue_pb2_grpc


def publish_message(queue_name, message_body):
    with grpc.insecure_channel("localhost:50051") as channel:
        stub = message_queue_pb2_grpc.MessageQueueStub(channel)
        response = stub.PublishMessage(
            message_queue_pb2.PublishRequest(
                queue_name=queue_name, message_body=message_body
            )
        )
        print(f"PublishMessage Response: {response.message}")


def consume_message(queue_name):
    with grpc.insecure_channel("localhost:50051") as channel:
        stub = message_queue_pb2_grpc.MessageQueueStub(channel)
        response = stub.ConsumeMessage(
            message_queue_pb2.ConsumeRequest(queue_name=queue_name)
        )
        if response.message_id:
            print(
                f"ConsumeMessage Response: ID={response.message_id}, Body={response.message_body}"
            )
        else:
            print("No messages available")


if __name__ == "__main__":
    publish_message("test_queue", "Hello, this is a test message!")
    consume_message("test_queue")

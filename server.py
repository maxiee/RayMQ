from concurrent import futures
import grpc
import message_queue_pb2, message_queue_pb2_grpc

# 内存中的简单消息队列
queues = {}


# 服务实现
class MessageQueueService(message_queue_pb2_grpc.MessageQueueServicer):
    def PublishMessage(self, request, context):
        queue_name = request.queue_name
        message_body = request.message_body
        if queue_name not in queues:
            queues[queue_name] = []
        message_id = str(len(queues[queue_name]) + 1)
        queues[queue_name].append({"id": message_id, "body": message_body})
        return message_queue_pb2.PublishResponse(
            success=True, message=f"Message {message_id} published"
        )

    def ConsumeMessage(self, request, context):
        queue_name = request.queue_name
        if queue_name not in queues or len(queues[queue_name]) == 0:
            return message_queue_pb2.ConsumeResponse(
                message_id="", message_body="No messages available"
            )
        message = queues[queue_name].pop(0)  # FIFO 取出
        return message_queue_pb2.ConsumeResponse(
            message_id=message["id"], message_body=message["body"]
        )


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    message_queue_pb2_grpc.add_MessageQueueServicer_to_server(
        MessageQueueService(), server
    )
    server.add_insecure_port("[::]:50051")
    server.start()
    print("Server started on port 50051")
    server.wait_for_termination()


if __name__ == "__main__":
    serve()

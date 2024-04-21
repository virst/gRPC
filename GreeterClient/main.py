#  python -m grpc_tools.protoc -I protos --python_out=grpc_out --pyi_out=grpc_out --grpc_python_out=. protos/greet.proto
import grpc

import greet_pb2
import greet_pb2_grpc

import time


def run():
    with grpc.insecure_channel('localhost:5001') as channel:
        stub = greet_pb2_grpc.GreeterStub(channel)
        for x in range(6):
            response = stub.SayHello(greet_pb2.HelloRequest(name='you #' + str(x)))
            print("Greeter client received: " + response.message)
            time.sleep(3)


if __name__ == "__main__":
    run()

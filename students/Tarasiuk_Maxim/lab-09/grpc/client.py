import grpc
import logging

class MockPortfClient:
    def __init__(self, channel):
        self.channel = channel

def run():
    logging.basicConfig(level=logging.INFO)
    with grpc.insecure_channel('localhost:50051') as channel:
        # stub = portfolio_service_pb2_grpc.PortfolioServiceStub(channel)
        logging.info("Connected to gRPC server")
        
        # Unary call
        # response = stub.CreatePortfolio(portfolio_service_pb2.CreatePortfolioRequest(portfolio_id="port2", owner_id="owner2"))
        # print("Create Response:", response)
        
        # Unary call
        # response = stub.GetPortfolio(portfolio_service_pb2.GetPortfolioRequest(portfolio_id="port1"))
        # print("Get Response:", response)
        
        # Server-Side Streaming call
        # stream = stub.StreamActivePortfolios(portfolio_service_pb2.StreamRequest())
        # for msg in stream:
        #     print("Streaming Update received:", msg)

if __name__ == '__main__':
    run()

import grpc
from proto import recommendation_pb2 as pb2
from proto import recommendation_pb2_grpc as pb2_grpc

GRPC_TARGET = "127.0.0.1:50051"
_channel = grpc.insecure_channel(GRPC_TARGET)
_stub = pb2_grpc.RecommendationServiceStub(_channel)

def get_similar_articles(article_id: int, limit: int = 5) -> list[dict]:
    try:
        response = _stub.GetRecommendedArticles(
            pb2.RecommendationRequest(article_id=article_id)
        )
        return [
            {
                "article_id": a.article_id,
                "article_title": a.title,
                "common_likers": a.score,
            }
            for a in response.articles
        ]
    except grpc.RpcError as e:
        print(f"gRPC Error: {e.code()} - {e.details()}")
        return []
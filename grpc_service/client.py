import grpc
from proto import recommendation_pb2 as pb2
from proto import recommendation_pb2_grpc as pb2_grpc

_channel = grpc.insecure_channel("127.0.0.1:50051")
_stub = pb2_grpc.RecommendationServiceStub(_channel)

def get_similar_articles(target_article_id: int, all_likes: list) -> list[dict]:
    # Конвертируем список из БД в protobuf-сообщения
    proto_likes = [pb2.Like(user_id=l["user_id"], article_id=l["article_id"]) for l in all_likes]
    
    response = _stub.GetRecommendedArticles(
        pb2.RecommendationRequest(target_article_id=target_article_id, all_likes=proto_likes)
    )
    return [{"article_id": a.article_id, "score": a.score} for a in response.articles]
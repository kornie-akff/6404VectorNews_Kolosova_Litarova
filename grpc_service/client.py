import grpc
from grpc_service import recommendations_pb2, recommendations_pb2_grpc

GRPC_TARGET = "127.0.0.1:50051"  # позже вынесем в env для лаб. №5

_channel = grpc.insecure_channel(GRPC_TARGET)
_stub = recommendations_pb2_grpc.RecommendationServiceStub(_channel)


def get_similar_articles(article_id: int, limit: int = 5) -> list[dict]:
    response = _stub.GetSimilarArticles(
        recommendations_pb2.SimilarArticlesRequest(article_id=article_id, limit=limit)
    )
    return [
        {
            "article_id": a.article_id,
            "article_title": a.article_title,
            "author_id": a.author_id,
            "common_likers": a.common_likers,
        }
        for a in response.articles
    ]
import grpc
from concurrent import futures

from grpc_service import recommendations_pb2, recommendations_pb2_grpc

from db.connect import SessionLocal
from db.crud import get_similar_articles, get_article_by_id


class RecommendationService(recommendations_pb2_grpc.RecommendationServiceServicer):
    def GetSimilarArticles(self, request, context):
        print(f"[gRPC] GetSimilarArticles(article_id={request.article_id}, limit={request.limit})")
        limit = request.limit if request.limit > 0 else 5
        with SessionLocal() as session:
            try:
                get_article_by_id(session, request.article_id)
            except ValueError as e:
                context.abort(grpc.StatusCode.NOT_FOUND, str(e))

            rows = get_similar_articles(session, request.article_id, limit)

        print(f"[gRPC] -> {len(rows)} recommendations")
        response = recommendations_pb2.SimilarArticlesResponse()
        for r in rows:
            response.articles.append(
                recommendations_pb2.SimilarArticle(
                    article_id=r["article_id"],
                    article_title=r["article_title"],
                    author_id=r["author_id"],
                    common_likers=r["common_likers"],
                )
            )
        return response


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    recommendations_pb2_grpc.add_RecommendationServiceServicer_to_server(
        RecommendationService(), server
    )
    server.add_insecure_port("[::]:50051")
    server.start()
    print("gRPC RecommendationService started on :50051")
    server.wait_for_termination()


if __name__ == "__main__":
    serve()
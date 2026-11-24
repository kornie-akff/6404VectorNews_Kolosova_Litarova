import grpc
from concurrent import futures
import sys, os
from sqlalchemy import select, func

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from proto import recommendation_pb2 as pb2
from proto import recommendation_pb2_grpc as pb2_grpc
from db.connect import SessionLocal
from db.models import Article
from db.models.associations import likes


class RecommendationServicer(pb2_grpc.RecommendationServiceServicer):
    def GetRecommendedArticles(self, request, context):
        article_id = request.article_id
        print(f"[gRPC] Запрос похожих статей для article_id={article_id}")

        db = SessionLocal()
        try:
            likers_subq = (
                select(likes.c.user_id)
                .where(likes.c.article_id == article_id)
                .subquery()
            )
            stmt = (
                select(
                    Article.article_id,
                    Article.article_title,
                    func.count(likes.c.user_id).label("score"),
                )
                .join(likes, likes.c.article_id == Article.article_id)
                .where(
                    likes.c.user_id.in_(select(likers_subq.c.user_id)),
                    Article.article_id != article_id,
                )
                .group_by(Article.article_id, Article.article_title)
                .order_by(func.count(likes.c.user_id).desc())
                .limit(5)
            )
            rows = db.execute(stmt).all()

            results = [
                pb2.RecommendedArticle(
                    article_id=row.article_id,
                    title=row.article_title,
                    score=row.score,
                    reason=f"Лайкнули {row.score} чел. из тех, кому понравилась эта статья",
                )
                for row in rows
            ]
            print(f"[gRPC] -> Найдено {len(results)} похожих статей")
            return pb2.RecommendationResponse(articles=results)
        finally:
            db.close()


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    pb2_grpc.add_RecommendationServiceServicer_to_server(
        RecommendationServicer(), server
    )
    server.add_insecure_port("[::]:50051")
    server.start()
    print("gRPC Recommendation Service запущен на :50051")
    server.wait_for_termination()


if __name__ == "__main__":
    serve()
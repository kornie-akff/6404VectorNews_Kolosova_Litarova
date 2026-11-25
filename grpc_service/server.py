import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import grpc
from concurrent import futures
from proto import recommendation_pb2 as pb2
from proto import recommendation_pb2_grpc as pb2_grpc



class RecommendationServicer(pb2_grpc.RecommendationServiceServicer):
    def GetRecommendedArticles(self, request, context):
        print(f"[gRPC] Получены данные для вычисления рекомендаций к статье {request.target_article_id}")
        
        target_likers = {like.user_id for like in request.all_likes if like.article_id == request.target_article_id}
        
        scores = {}
        for like in request.all_likes:
            if like.article_id != request.target_article_id and like.user_id in target_likers:
                scores[like.article_id] = scores.get(like.article_id, 0) + 1

        sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)[:5]
        
        results = [
            pb2.RecommendedArticle(article_id=art_id, score=score)
            for art_id, score in sorted_scores
        ]
        
        print(f"[gRPC] Вычислено {len(results)} рекомендаций")
        return pb2.RecommendationResponse(articles=results)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    pb2_grpc.add_RecommendationServiceServicer_to_server(RecommendationServicer(), server)
    server.add_insecure_port("[::]:50051")
    server.start()
    print("gRPC Recommendation Service started on :50051")
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
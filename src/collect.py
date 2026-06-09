import pandas as pd
from googleapiclient.discovery import build
from src.utils import get_api_key

def search_videos(query, max_results=50, order="relevance"):
    api_key = get_api_key()
    youtube = build("youtube", "v3", developerKey=api_key)

    request = youtube.search().list(
        q=query,
        part="snippet",
        type="video",
        maxResults=min(max_results, 50),
        order=order
    )
    response = request.execute()

    video_ids = [item["id"]["videoId"] for item in response["items"]]

    stats_request = youtube.videos().list(
        part="statistics,snippet",
        id=",".join(video_ids)
    )
    stats_response = stats_request.execute()

    rows = []
    for item in stats_response["items"]:
        snippet = item["snippet"]
        stats = item.get("statistics", {})

        rows.append({
            "video_id": item["id"],
            "titulo": snippet.get("title", ""),
            "descricao": snippet.get("description", ""),
            "data_publicacao": snippet.get("publishedAt", ""),
            "visualizacoes": int(stats.get("viewCount", 0)),
            "curtidas": int(stats.get("likeCount", 0)),
            "comentarios": int(stats.get("commentCount", 0)),
            "canal": snippet.get("channelTitle", ""),
            "categoria": snippet.get("categoryId", "0")
        })

    return pd.DataFrame(rows)

def collect_multiple_queries(queries, videos_per_query=30):
    dfs = []
    for q in queries:
        df = search_videos(q, max_results=videos_per_query)
        if not df.empty:
            dfs.append(df)
    if dfs:
        result = pd.concat(dfs, ignore_index=True)
        result = result.drop_duplicates(subset="video_id")
        return result
    return pd.DataFrame()

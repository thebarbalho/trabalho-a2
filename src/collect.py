import pandas as pd
from googleapiclient.discovery import build
from src.utils import get_api_key

def search_videos(query, max_results=50, order="relevance"):
    api_key = get_api_key()
    youtube = build("youtube", "v3", developerKey=api_key)

    video_ids = []
    next_page_token = None

    while len(video_ids) < max_results:
        remaining = max_results - len(video_ids)
        request = youtube.search().list(
            q=query,
            part="snippet",
            type="video",
            maxResults=min(remaining, 50),
            order=order,
            pageToken=next_page_token,
        )
        response = request.execute()
        for item in response["items"]:
            video_ids.append(item["id"]["videoId"])
        next_page_token = response.get("nextPageToken")
        if not next_page_token:
            break

    video_ids = video_ids[:max_results]
    if not video_ids:
        return pd.DataFrame()

    stats_request = youtube.videos().list(
        part="statistics,snippet",
        id=",".join(video_ids)
    )
    stats_response = stats_request.execute()

    id_to_item = {}
    for item in stats_response["items"]:
        id_to_item[item["id"]] = item

    rows = []
    for vid in video_ids:
        item = id_to_item.get(vid)
        if item is None:
            continue
        snippet = item["snippet"]
        stats = item.get("statistics", {})

        rows.append({
            "video_id": vid,
            "titulo": snippet.get("title", ""),
            "descricao": snippet.get("description", ""),
            "tags": ", ".join(snippet.get("tags", [])),
            "category_id_nativo": snippet.get("categoryId", "0"),
            "data_publicacao": snippet.get("publishedAt", ""),
            "visualizacoes": int(stats.get("viewCount", 0)),
            "curtidas": int(stats.get("likeCount", 0)),
            "comentarios": int(stats.get("commentCount", 0)),
            "canal": snippet.get("channelTitle", ""),
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

import giphy_client
from giphy_client.rest import ApiException


# using API Giphy to take gifs
def gif(client_tag):
    api_instance = giphy_client.DefaultApi()
    api_key = 'dMuxvuGTGZmp7USqPGpO9NgorR5SAYxB'  # str | Giphy API Key.
    tag = client_tag
    rating = 'g'  # str | Filters results by specified rating. (optional)
    fmt = 'json'  # str | Used to indicate the expected response format. Default is Json. (optional) (default to json)

    try:
        api_response = api_instance.gifs_random_get(api_key, tag=tag, rating=rating, fmt=fmt)
        return(api_response.data.image_mp4_url)
    except ApiException as e:
        print("Exception when calling DefaultApi->gifs_search_get: %s\n" % e)



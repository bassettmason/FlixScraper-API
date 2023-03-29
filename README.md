Sure, here's a sample README file that includes a quick start guide and some information about the code:

# Movie Genie API

This Flask-based API was designed to help automate playlists for movie suggestions in Trakt, but it can be used for any software that would like automated playlists of the top streaming services or online suggested playlists from reddit.

## Top-Ten

Send a GET request to the `/api/topten` endpoint with the `data` and `token` parameters. For example:
Current available services list is "netflix", "amazon-prime", "hbo", "hulu", "disney", "paramount-plus

example:
api/topten?data=netflix&token=password12345
services to request: "netflix", "amazon-prime", "hbo", "hulu", "disney", "paramount-plus"
This will return a JSON response with the top ten movies for Netflix.
{
    "content": {
        "name": "netflix topten",
        "playlist": [
            [
                {
                    "title": "Luther: The Fallen Sun",
                    "year": "null"
                },
                {
                    "title": "The Magician's Elephant",
                    "year": "null"
                },
                {
                    "title": "Chor Nikal Ke Bhaga",
                    "year": "null"
                },
                {
                    "title": "Johnny",
                    "year": "null"
                },
                {
                    "title": "Still Time",
                    "year": "null"
                },
                {
                    "title": "Furies",
                    "year": "null"
                },
                {
                    "title": "All Quiet on the Western Front",
                    "year": "null"
                },
                {
                    "title": "In His Shadow",
                    "year": "null"
                },
                {
                    "title": "Perfume: The Story of a Murderer",
                    "year": "null"
                },
                {
                    "title": "PAW Patrol: The Movie",
                    "year": "null"
                }
            ]
        ],
        "url": "https://flixpatrol.com/top10"
    },
    "timestamp": "2023-03-27 21:07:57",
    "type": "netflix_topten"
}

## Genie

This route uses AI to collect movies suggestions from Reddit posts.
Send a GET request to the `/api/genie` endpoint with the `data` and `token` parameters. For example:

example:
api/topten?data={reddit url}&token=password12345
services to request: just url from reddit moviesuggestions have been tested.
This will return a JSON response with the movies suggested from url.
{
    "content": {
        "name": "movie_set_in_beautiful_historic_or_strange_places",
        "playlist": [
            {
                "title": "The Fall",
                "year": 2005
            },
            {
                "title": "Call Me By Your Name",
                "year": 2017
            },
            {
                "title": "The Grand Budapest Hotel",
                "year": "null"
            },
            {
                "title": "In Bruges",
                "year": 2008
            },
            {
                "title": "The Handmaiden",
                "year": "null"
            },
            {
                "title": "Power of the Dog",
                "year": "null"
            },
            {
                "title": "First Cow",
                "year": "null"
            }
        ],
        "url": "https://www.reddit.com/r/MovieSuggestions/comments/125srxi/movie_set_in_beautiful_historic_or_strange_places/"
    },
    "timestamp": "2023-03-29 19:58:22",
    "type": "genie"
}
from sqlalchemy.orm import Session
from models import Base, Platform, Movie, TVShow, TopMovie, TopTVShow
from database import SessionLocal, engine

def implement_test_data():
    session = SessionLocal()
    Base.metadata.drop_all(bind=engine)
    # Create tables
    Base.metadata.create_all(bind=engine)
    # Add test data for each platform
    create_test_data(session)
    # Commit the transaction and close the session
    session.commit()
    session.close()

def create_test_data(db: Session):
    # Create Platforms
    netflix = Platform(name="netflix")
    db.add(netflix)

    disney_plus = Platform(name="disney")
    db.add(disney_plus)

    hulu = Platform(name="hulu")
    db.add(hulu)

    amazon_prime = Platform(name="amazon-prime")
    db.add(amazon_prime)

    paramount_plus = Platform(name="paramount-plus")
    db.add(paramount_plus)

    hbo = Platform(name="hbo")
    db.add(hbo)

    apple_tv = Platform(name="apple-tv")
    db.add(apple_tv)

    # Create Movies
    avengers = Movie(title="Avengers: Endgame")
    db.add(avengers)

    star_wars = Movie(title="Star Wars: The Rise of Skywalker")
    db.add(star_wars)

    black_widow = Movie(title="Black Widow")
    db.add(black_widow)

    frozen = Movie(title="Frozen")
    db.add(frozen)

    the_lion_king = Movie(title="The Lion King")
    db.add(the_lion_king)

    spiderman = Movie(title="Spider-Man: No Way Home")
    db.add(spiderman)

    # Create TV Shows
    game_of_thrones = TVShow(title="Game of Thrones")
    db.add(game_of_thrones)

    friends = TVShow(title="Friends")
    db.add(friends)

    the_office = TVShow(title="The Office")
    db.add(the_office)

    the_mandalorian = TVShow(title="The Mandalorian")
    db.add(the_mandalorian)

    stranger_things = TVShow(title="Stranger Things")
    db.add(stranger_things)

    the_walking_dead = TVShow(title="The Walking Dead")
    db.add(the_walking_dead)

    # Create Top Movies for each platform
    netflix_top_movies = [
        TopMovie(platform=netflix, movie=avengers, rank=1),
        TopMovie(platform=netflix, movie=star_wars, rank=2),
        TopMovie(platform=netflix, movie=black_widow, rank=3)
    ]
    db.add_all(netflix_top_movies)

    disney_plus_top_movies = [
        TopMovie(platform=disney_plus, movie=frozen, rank=1),
        TopMovie(platform=disney_plus, movie=the_lion_king, rank=2),
        TopMovie(platform=disney_plus, movie=avengers, rank=3)
    ]
    db.add_all(disney_plus_top_movies)

    hulu_top_movies = [
        TopMovie(platform=hulu, movie=avengers, rank=1),
        TopMovie(platform=hulu, movie=black_widow, rank=2),
        TopMovie(platform=hulu, movie=star_wars, rank=3)
    ]
    db.add_all(hulu_top_movies)

    amazon_prime_top_movies = [
        TopMovie(platform=amazon_prime, movie=avengers, rank=1),
        TopMovie(platform=amazon_prime, movie=star_wars, rank=2),
        TopMovie(platform=amazon_prime, movie=the_lion_king, rank=3)
    ]
    db.add_all(amazon_prime_top_movies)

    paramount_plus_top_movies = [
        TopMovie(platform=paramount_plus, movie=star_wars, rank=1),
        TopMovie(platform=paramount_plus, movie=the_lion_king, rank=2)
    ]
    db.add_all(paramount_plus_top_movies)

    apple_tv_top_movies = [
        TopMovie(platform=apple_tv, movie=avengers, rank=1),
        TopMovie(platform=apple_tv, movie=star_wars, rank=2),
        TopMovie(platform=apple_tv, movie=the_lion_king, rank=3)
    ]   
    db.add_all(apple_tv_top_movies)
    hbo_top_movies = [
        TopMovie(platform=hbo, movie=avengers, rank=1),
        TopMovie(platform=hbo, movie=star_wars, rank=2),
        TopMovie(platform=hbo, movie=the_lion_king, rank=3)
    ]   
    db.add_all(hbo_top_movies) 
    
    #Create Top Tv_Shows for each platform
    netflix_top_tv_shows = [    TopTVShow(platform=netflix, tv_show=stranger_things, rank=1),    TopTVShow(platform=netflix, tv_show=the_walking_dead, rank=2),    TopTVShow(platform=netflix, tv_show=game_of_thrones, rank=3)]
    db.add_all(netflix_top_tv_shows)

    disney_plus_top_tv_shows = [    TopTVShow(platform=disney_plus, tv_show=the_mandalorian, rank=1),    TopTVShow(platform=disney_plus, tv_show=game_of_thrones, rank=2),    TopTVShow(platform=disney_plus, tv_show=stranger_things, rank=3)]
    db.add_all(disney_plus_top_tv_shows)

    hulu_top_tv_shows = [    TopTVShow(platform=hulu, tv_show=friends, rank=1),    TopTVShow(platform=hulu, tv_show=the_office, rank=2),    TopTVShow(platform=hulu, tv_show=the_walking_dead, rank=3)]
    db.add_all(hulu_top_tv_shows)

    amazon_prime_top_tv_shows = [    TopTVShow(platform=amazon_prime, tv_show=game_of_thrones, rank=1),    TopTVShow(platform=amazon_prime, tv_show=the_office, rank=2),    TopTVShow(platform=amazon_prime, tv_show=the_walking_dead, rank=3)]
    db.add_all(amazon_prime_top_tv_shows)

    paramount_plus_top_tv_shows = [    TopTVShow(platform=paramount_plus, tv_show=friends, rank=1),    TopTVShow(platform=paramount_plus, tv_show=stranger_things, rank=2),    TopTVShow(platform=paramount_plus, tv_show=the_office, rank=3)]
    db.add_all(paramount_plus_top_tv_shows)

    apple_tv_top_tv_shows = [    TopTVShow(platform=apple_tv, tv_show=the_mandalorian, rank=1),    TopTVShow(platform=apple_tv, tv_show=game_of_thrones, rank=2),    TopTVShow(platform=apple_tv, tv_show=stranger_things, rank=3)]
    db.add_all(apple_tv_top_tv_shows)

    hbo_top_tv_shows = [    TopTVShow(platform=hbo, tv_show=game_of_thrones, rank=1),    TopTVShow(platform=hbo, tv_show=the_office, rank=2),    TopTVShow(platform=hbo, tv_show=the_mandalorian, rank=3)]
    db.add_all(hbo_top_tv_shows)

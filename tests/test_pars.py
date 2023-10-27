from parsing import URL, picture, information, reiti, years


def test_url():
    assert URL == "https://www.kinoafisha.info/rating/movies/"

def test_type():
    assert (type(picture) == list)
    assert (type(information) == list)
    assert (type(reiti) == list)
    assert (type(years) == list)

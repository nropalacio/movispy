SearchMe = "The apple is red and the berry is blue!"
print(SearchMe.find("is"))
print(SearchMe.rfind("is"))
print(SearchMe.count("is"))
print(SearchMe.startswith("The"))
print(SearchMe.endswith("The"))
print(SearchMe.replace("apple", "car").replace("berry", "truck"))


url_img = 'https://cdnpim.cinepolis.com.sv/tmp/image-thumbnails/DigitalChannels/protected/Movies/Posters/image-thumb__494__belt_Estreno/El__Padre_Poster_675x1000@5x.png'
print(url_img.find("belt_Preventa"))
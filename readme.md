# Farmigo HW #2 -  Recommendation Engine

This is my engine. Uses Term Frequency on a included data set of 1,000,000 product transactions.

Note the input file must contain two specific headers: item_id & text

item_id is a unique identifier for a given product description. product descriptions are detailed in the text values.
i.e. item_id = 568, text = Vegan Blackburn Wheat

Using flask for the RESTful endpoint. Deploying this to Heroku. Anaconda is the only dependency. Redis to store the computational data.

engine.py - this is the recommendation algorithm.
rest.py - this is the python code for the two endpoints.

endpoint #1 - train, this will call the engine and do all of the similarity measurements.
endpoint #2 - score, this takes in an item_id, and returns the top 10 most similar items.
i.e. item_id = 568, text = Vegan Blackburn Wheat will return:
[(1.0, 568),
 (0.89635751541381425, 306),
 (0.21165819268462555, 260),
 (0.20168037159905644, 493),
 (0.19994092523250903, 542),
 (0.18984394573044502, 261),
 (0.18966874617443436, 314),
 (0.18475364396234775, 483),
 (0.184113462118597, 281),
 (0.18185792405855164, 233),
 (0.17599054984770088, 53)]

item_id = 306 is "Foccacia Loaf"

conda create -n crec --file conda.txt

Now, in the virtualenv (``source activate crec``):

>> python web.py

Then, in a separate terminal window, train the engine:

>> curl -X GET -H "X-API-TOKEN: FOOBAR1" -H "Content-Type: application/json; charset=utf-8" http://127.0.0.1:5000/train -d "{\"data-url\": \"sample-data.csv\"}"

And make a prediction!

>> curl -X POST -H "X-API-TOKEN: FOOBAR1" -H "Content-Type: application/json; charset=utf-8" http://127.0.0.1:5000/predict -d "{\"item\":18,\"num\":10}"

## Deploying

This engine is designed to be deployed to Heroku. First, create a new app:

>> heroku create

You'll then need to set the buildpack for the app to use Anaconda; a packaging system for scientific computing libraries in Python.

>> heroku buildpacks:set https://github.com/kennethreitz/conda-buildpack.git

Be sure to set your environmental variables (in settings.py) and provide your own training data. Then just:

>> git push heroku master

## Running tests

Well...technically it's running *test*, singular :)

>> python -m unittest tests

python3 -m venv venv

source venv/bin/activate

pip install fastapi uvicorn geopandas shapely

uvicorn main:app --reload


put the mongolia-251015-free.shp file here at the root, get it from the google drive. Dont forget to run the venv
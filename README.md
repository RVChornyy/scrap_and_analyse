# scrap_and_analyse
This project allows to scrape job vacancies from "https://work.ua/",
create file with parsed vacancies data and build visualised diagrams
for data analysis.

# Project initialization:
~~~
git clone https://github.com/RVChornyy/scrap_and_analyse.git
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
~~~
# Start:
1) run main.py in data_extraction package
2) input required job position

csv file, named as your required job position, is being created.
After process finished, you can observe csv file with appropriate name in
"data_analysis" directory. 

# Data analysis:
Run analysis.ipynb in "data_analysis" package.
Your graphics are available in "plots" directory.
To stop jupyter server:
~~~
jupyter notebook stop 8888
~~~

# Note:
If something goes wrong, restart main.py. 

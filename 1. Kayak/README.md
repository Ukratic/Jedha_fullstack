## JEDHA PROJECT INFORMATION. DATA MANAGEMENT

## Kayak

Participate in the development of an application that will recommend where people should plan their next holidays, based on real data about weather and hotels in the area.<br>
The application should then be able to recommend the best destinations and hotels based on the above variables at any given time.

The only data provided is a list of 35 "best" cities to travel to in France :<br>
["Mont Saint Michel","St Malo","Bayeux","Le Havre","Rouen","Paris","Amiens","Lille","Strasbourg","Chateau du Haut Koenigsbourg","Colmar","Eguisheim","Besancon","Dijon","Annecy","Grenoble","Lyon","Gorges du Verdon","Bormes les Mimosas","Cassis","Marseille","Aix en Provence","Avignon","Uzes","Nimes","Aigues Mortes","Saintes Maries de la mer","Collioure","Carcassonne","Ariege","Toulouse","Montauban","Biarritz","Bayonne","La Rochelle"]

In the scope of the project, only above cities should be used.<br>
Steps :
- Scrape data from destinations (coordinates)
- Get weather data from each destination
- Get hotels' info about each destination
- Store all the information above in a data lake
- ETL cleaned data from the data lake to a data warehouse

The final deliverables should include a .csv file in a S3 bucket containing enriched information about weather & hotels for each city, a SQL database from which we should be able to get the data with SQL requests and 2 maps with top destinations & top hotels in the area.

Libraries used :
Beautifulsoup, Requests, Boto3, SQL Alchemy, Plotly, Pandas

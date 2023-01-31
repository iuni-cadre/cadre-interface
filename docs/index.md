# CADRE User Guide

<!-- [Technical Documentation](technical_docs/tech_doc.md) -->

## Table of Contents

### About

### Getting Started

### Usage
- [Using Query Builder inside the CADRE platform](#using-query-builder-inside-the-cadre-platform)
- [View Query Results](#view-query-results)
- [Using Jupyter Notebook](#using-jupyter-notebook)

## About

The CADRE platform provides users with tools that facilitate the creation of datasets from user-generated queries as well as an interface (using Jupyter Notebooks) for displaying, processing, and even analyzing created datasets.

## Getting Started

- Go to the [CADRE gateway](https://cadre.iu.edu/gateway/jupyter) and login using your institutions credentials
    - Note: If your institution is not subscribed to CADRE, you will only have access to a subset of features.
    - Note 2: **If your institution uses Google or Gmail and you typically log into a Google account, you must still use CILogon and choose your appropriate institution to access all features granted to your institution.**
    
    ![Untitled](index/Untitled.png)
    

- After login, a user dashboard will be created for you

![Untitled](index/Untitled%201.png)

## Usage

The two main tools in the CADRE Dashboard are **Query Builder** and **Jupyter Notebook**. This guide focuses on using Query Builder and displaying query results using Jupyter Notebook. We also provide a few external resources that can help you use Jupyter notebook for more sophisticated data processing and analysis.

### Using Query Builder inside the CADRE platform

- To begin, click on the button `Query Builder.`
- Choose a Dataset: there are 3 data sources available, each with their own selection button.
    - **Microsoft Academic Graph (MAG)** contains metadata for scholarly papers and authorship, which is suitable for acquiring relational datasets used for creating citation networks. Here is link to the [MAG documentation](https://learn.microsoft.com/en-us/academic-services/graph/). Below are additional resources, including a repository of sample code, to help you begin your journey with MAG.
        - [MAG Entity Relationship Diagram](https://cadre.iu.edu/resources/documentation/mag_core_erd%20(1).pdf)
        - [GitHub: Academic Knowledge Analytics Visualization](https://github.com/Azure-Samples/academic-knowledge-analytics-visualization)
    - **US patent and trademark office (USPTO)**: contains metadata on [patents](https://www.uspto.gov/patents/search) and [trademarks](https://www.uspto.gov/trademarks) stored in the USPTO databases. Additional resources:
        - [USPTO Entity Relationship Diagram](https://cadre.iu.edu/resources/documentation/uspto_core_erd%20(3).pdf)
        - Familiarity with the different [patent classification systems](https://www.uspto.gov/patents/search/classification-standards-and-development) can be beneficial for building queries for this data.
    - **Web of Science (WoS)** contains metadata for scholarly papers and authorship.
        - [WoS Entity Relationship Diagram](https://cadre.iu.edu/resources/documentation/wos_core_erd%20(1).pdf)
        - [Web of Knowledge Schemas](https://cadre.iu.edu/resources/documentation/Web%20of%20Science-CCC-XML%20Guide_v2.2.pdf)
        - [WoS Data Dictionary](https://iuni.iu.edu/files/WoS_Documents/Web_of_Science_Data_Dictionary.pdf)
        - [Web of Knowledge User Guide](https://cadre.iu.edu/resources/documentation/Web%20of%20Science-CCC-XML%20Guide_v2.2.pdf)
- After choosing one of the datasets, click the button `Proceed to Query Builder`.

### Example: Query the Web of Science dataset

There are 4 sections to complete before submitting a query.

**Filters**

- These are searchable fields that determine what data is returned from the query. Selecting the appropriate fields and filter criteria is critical to returning the data you want. The more precision used in field selections and search criteria reduces the time it takes for CADRE to return results from the query.
- The searchable filter fields for **WoS** are: DOI, ISSN, Year, Author, Journal Name, Journal ISO, Conference Title, Paper Title. 
    - Exact string matches are performed against DOI, ISSN, JournalISO, and Year.
    - Fuzzy matches are performed against Journal Name, Conference Title, and Paper Title.
    - The Author Names are searched for as a regular expression.
        - Enter the author names as “last name, first name” or “last name, first initial middle initial”, or however the initials are given. The resulting regular expression will be “.*last, first.*” or “.*last, fm.*” for last followed by first and middle initials; the comma is matched and must be included by the user in the query. Also, the author’s names are converted to lower-case and compared against a lower-case field of author names. If an author’s name is given in a variety of ways in different publications, then the OR operator will need to be applied for that author.
        - For example:
            - If you are searching for papers from two authors: John James Smith and Robert Brian Doe. Entering “Smith, J” will find all papers with author last name Smith and first letter of the first name J, so it will find papers with authors like: Clinesmith, Jack or Smith, J where only the J is given in the paper name. In other words, you may get extraneous papers with author names that happened to meet the regular expression.
            - Filter 1:
                >                Author: smith, jj
                >                    OR
                >                Author: smith, john j
                >                    OR
                >                Author: smith, john james
                >                    AND
            - Filter 2:
                >                Author: doe, rb
                >                    OR
                >                Author: doe, robert b
                >                    OR
                >                Author: doe, robert brian

- Select a search **Field** from the pulldown and type the field value into the **Values** column next to the selected field.
    - Click “**Add Another Filter Value**” to add multiple **Values** associated with a selected filter
        - Select whether the additional Value should be “AND” or “OR” using the pulldown option.
    - Example:
        
        ![Untitled](index/Untitled%202.png)
        
- Click **+Add Additional Filter** to add extra filter fields (optional)
    - Select if added field should be “AND” or “OR” using the pulldown option.
        
        ![Untitled](index/Untitled%203.png)
        

**Output Fields**

- Here is where you select the fields or variables you would like returned for the data meeting the query filter criteria specified above (**Filters** section).
    - Several **Fields** will be preselected as default selections, which are indicated with checkbox next to the field.
        - To unselect a field, click the checkbox next to the field to remove checkmark
    - To add other Fields, click the button “**Show All Available Fields**” to display all the possible fields that can be returned from a query
        - Click the checkbox next the field(s) you wish to be included (or excluded) in the query results.
        
        ![Untitled](index/Untitled%204.png)
        

**Network Queries**

- In addition to returning an output table with selected fields, you can also select whether you want the query to return a citation or reference graph (edgelist). This relational output captures links between scholarly works (e.g., papers, patents/trademarks) based on their citations of other works.
- Click **Include Citation Network Graph** to return a network edgelist based on the *citations* of the query results (papers/patents).
    - A citations graph consists of the query results and any papers or patents the query results cite, with edges representing citations by the query result.
- Click **Include Reference Network Graph** to return a network edgelist based on *references* that cite the query results (papers/patents).
    - A references graph consists of the query results and any papers or patents referencing the query results, with edges representing references made to the query results.

**Job Name (recommended)**

- Type a unique **Name** for your query to easily identify it in a list of query jobs (recommended if you plan to submit additional queries).

**Submit Query and Check Job Status**

- Click **Submit Query** to put your query into a job queue that will be run and return results.
    
    ![Untitled](index/Untitled%205.png)
    
- Click the button **Check Job Statuses** to be redirected to a Jobs page that lists all your submitted queries and their current status.
    - The Jobs pages will display the query you just submitted, with the “Job Name” typed above in the “Name” column
        - Your submitted query will display “Running” soon (depending on the number of queries in the queue) and you can see the status of the job in the “Status” column.
        
        ![Untitled](index/Untitled%206.png)
        
    - Once the query is finished, the job will display “Completed” in the Status column and you will see links to the results of the query, which are displayed in a new row “**Result Files**”
    
    ![Untitled](index/Untitled%207.png)
    

### **View Query Results**

Once your query is “Completed”, your results are automatically saved to a personal workspace in a folder labeled “query-results”. There are two ways to display the query results using Jupyter Notebook.

- **Option 1**) Click the link(s) to the csv file shown next to “Result Files” on the Jobs page.
    - This will start the Jupyter Notebook server. There might be a short delay while initiating the server, which will display “Notebook status: **pending**”
        
        ![Untitled](index/Untitled%208.png)
        
    - Once you see “**Notebook status: running**”, click the button **Go To Notebook** to display your personal Jupyter Notebook workspace in a new browser tab.
        
        ![Untitled](index/Untitled%209.png)
        
    - The linked csv file you clicked on will automatically be displayed as spreadsheet within the workspace.
        - On the left side the workspace you will see a folder icon. When selected, you will see the current working directory (/query-results/) of your workspace and a list of all your query results csv files (automatically stored after a query is “completed”.
        - If you want to display multiple query results, simply click on the csv file you want to see and the file will be displayed in the list of nested tabs.
            
            ![Untitled](index/Untitled%2010.png)
            
- **Option 2**) As an alternative way to display the query results, you can click the button `**Go To Jupyter Notebook To View Results**`.
    
    ![Untitled](index/Untitled%2011.png)
    

- On next page, click the button **`Start Notebook Server`**.
    
    ![Untitled](index/Untitled%2012.png)
    

- Similar to Option 1 (above), this will launch Jupyter Notebook. Once you see “**Notebook status: running**”, click the button **Go To Notebook** to display your personal Jupyter Notebook workspace in a new browser tab.
    
    ![Untitled](index/Untitled%2013.png)
    
- However, you need to navigate to the query result files to display the results as a spreadsheet in the workspace.
    
    ![Untitled](index/Untitled%2014.png)
    

- On the left side the workspace you will see a folder icon. When selected, you will see the current working directory. Click on the folder “**query-results**” to navigate to this directory where your query results are automatically stored when a Job query is “completed”. You will then see a list of all your query results csv files.
    - The filenames of the results always begin with the unique Job Name you typed in the Query Builder. After you find the Job Name in the list, click on the file to display it as spreadsheet within the workspace.
    - If you want to display multiple query results, simply click on the additional csv file you want to see and the file will be displayed in a nested tab.
        
        ![Untitled](index/Untitled%2010.png)
        
- **Download Query Results**
    - Although you can use Jupyter Notebook to do more than display the query results, some might prefer to download the results files and use other programs to explore/analyze the data.
    - To download a csv file containing query results, click File>Download in the top menu bar. This will enable to choose the File Name and directory where you would like to save the file on your local machine.
        
        ![Untitled](index/Untitled%2015.png)
        

### Using Jupyter Notebook

- Rather than launching Jupyter Notebook through Query Builder, you can start the notebook server from your Dashboard immediately after login. You can either click Notebook link in the top menu or click the Jupyter Notebook button in the Quick Start section of the Dashboards.
    - This is helpful if have previously used CADRE’s Query Builder feature and already have results stored in the “query-results” folder, or if you have another csv file you would like to upload to you Notebook server.
        
        ![Untitled](index/Untitled%2016.png)
        
- Jupyter Notebook with CADRE is powerful platform that enables users to Python 3 to write code and import packages for activities like data processing, visualizations, and analysis.
    - Additional Resources for using Jupyter Notebook
        - ****[Python Data Science Handbook](https://jakevdp.github.io/PythonDataScienceHandbook/)****
        - ****[Complete guide to Jupyter Notebooks for Data Science](https://towardsdatascience.com/the-complete-guide-to-jupyter-notebooks-for-data-science-8ff3591f69a4)****
        - [Jupyter Notebook](https://jupyter-notebook.readthedocs.io/en/stable/) (official documentation)

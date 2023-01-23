# ENS492

Telegram and Security News Website Group
for Mac: source ./<'path to virtual environment'>/bin/activate
for Win: ./Scripts/activate

Crawled Websites (Who did which crawler)

# Bengisu

1. Threat Post (Search / Crawler)
2. BBC News
3. The Hacker News
4. Security Intelligence (Search / Crawler)

# Can

1. Packet Storm
2. ZDNet

# İdil

1. SC Magazine (Search / Crawler)
2. Reuters
3. Vice
4. Wordfence
5. Bleepingcomputer (Crawler / Search)

# Kerem

1. Gizmodo (Search / Crawler)
2. Guardian (Search / Crawler)
3. CNET
4. CNN
5. RealInfoSec
6. TechCrunch
7. ITGuru (Search / Crawler)
8. Bleepingcomputer (Search)

Searchers for Gizmodo-ITGuru-BleepingComputer-SCMag-Guardian can be accesed from Src/ColabNoteboks/ENS492-NewsSiteSearches.ipynb

CRAWLERS/SEARCHES:

-  In 'src' folder there are crawlers for different websites and the files are listed below:

   -  bbc_news.py (scrapeBBCNews)
   -  cnet.py (scrapeCnet)
   -  cnn.py (scrapeCnn)
   -  gizmodo.py (scrapeGizmodo)
   -  guardian.py (scrapeGuardian)
   -  real_info_sec.py (scrapeRIS)
   -  reuters.py (scrapeReuters)
   -  scmagazine.py (scrapeSCMag)
   -  scrape_itguru.py (scrapeITGuru)
   -  security_intelligence.py (scrapeSecurityIntelligence)
   -  tech_crunch.py (scrapeTechCrunch)
   -  the_hacker_news.py (scrapeTheHackerNews)
   -  threat_post.py (scrapeThreatPost)
   -  vice.py (scrapeVice)
   -  wordfence.py (scrapeWordfence)
   -  zdNet.py (scrapeZDNet)

   These crawlers can be used as follows:
   _ find the function with the given name in paranthesis in any file listed above
   _ run the function with a news url (either with the given url in file or any url found) from given website as parameter (also there are commented lines at the end of every file that calls the function with an initial url if needed)
   \_ print the returned value to see the text returned

*  In 'src' folder there are files that includes search functions which are listed below:

   -  threat_post.py (getSearchResults)
   -  security_intelligence.py (getSearchResults)
   -  scmagazine.py (search_scmag)
   <!-- -  bleeping_computer.py () -->
   -  search_gizmodo.py (search_gizmodo)
   -  search_guardian.py (search_guardian)
   -  search_itguru.py (getSearchResults)

   *  packet_storm.py

to install requirements:

-  pip install -r requirements.txt

if an error occured while installing about pip

-  python -m ensurepip

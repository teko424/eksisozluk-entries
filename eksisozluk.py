#kullanıcı arama, entry sıra numarası özelliği getirilecek

import requests
from bs4 import BeautifulSoup


def eksi():
    searchlist = []
    c_range = 150
    while 1:
        q = input("aramak istediğiniz başlık: ")
        searchlist.append(q)
        try:
            if q:
                headers = ""
                search = "https://eksisozluk.com/?q="
                num = 1
                page = 1
                otherpage = False
                url = search + q
                r = requests.get(url, headers=headers)
                source = BeautifulSoup(r.content, "lxml")
                header = source.title
                link = source.find("a", attrs={"itemprop": "url"}).get("href")
                search = "https://eksisozluk.com"
                url = search+link
                entries = source.find_all("div", attrs={"class": "content"})
                if not entries:
                    print("böyle bir şey yok. ama olabilir de.")
                    continue
                dates = source.find_all("a", attrs={"class": "entry-date permalink"})
                datelist = []
                nicks = source.find_all("a", attrs={"class": "entry-author"})
                nicklist = []
                nicknum = 0
                if len(entries) == 10:
                    pagecount = source.find("div", {"data-currentpage": str(page)})
                    pagecount = str(pagecount)[str(pagecount).find("data-pagecount"):str(pagecount).find(">")].split("=")[1]
                    pagecount = pagecount.strip("\"")
                else:
                    pagecount = 1
                print("\n", header.text)
                for entry in entries:
                    for nick in nicks:
                        nicklist.append(nick)
                    for date in dates:
                        datelist.append(date)
                    if nicknum < 11:
                        print("\n", num, "-)", entry.text + "\n",
                              datelist[nicknum].text, "\n", "\n", "-", nicklist[nicknum].text, "-")
                        if len(entry.text) <= c_range:
                            print("—" * len(entry.text))
                        else:
                            print("—" * c_range)
                        nicknum += 1
                    num += 1
                print("\nsayfa numarası: ", page, "\n", pagecount, "sayfa mevcut")
                otherpage = True
                while otherpage:
                    qa = input("""\nsonraki sayfaya geçmek içn (+) girin\n---------
                    \ngeri gitmek için (-) girin\n---------
                    \nsayfa numarası için bir sayı girin\n---------
                    \ngündemi görmek için (*) girin\n---------
                    \narama kaydı için (/) girin\n---------
                    \nson sayfa için (") girin\n---------
                    \nbaşka bir şey aramak için \"h\" girin: """)
                    page += 1
                    if qa == "+":
                        pass
                    elif qa == "-":
                        page -= 2
                        if page < 1:
                            print("\nçok geri gittin. biraz ileri gel.")
                            continue
                    elif qa.isdigit():
                        page = int(qa)
                    elif qa == "*":
                        page -= 1
                        pass
                    elif qa == "/":
                        print("\n")
                        for value in searchlist:
                            print(value)
                        page -= 1
                        continue
                    elif qa == "\"":
                        page -= 1
                        page = int(pagecount)
                    else:
                        otherpage = False
                        continue
                    num = 1
                    pageurl = "?p=" + str(page)
                    urls = url+pageurl
                    r = requests.get(urls, headers=headers)
                    source = BeautifulSoup(r.content, "lxml")
                    if qa == "*":
                        entries = source.find_all("ul", attrs={"class": "topic-list partial"})
                    else:
                        entries = source.find_all("div", attrs={"class": "content"})
                        if not entries:
                            print("entry kalmadı.\nbaşka bir başlık aratabilirsiniz.")
                            continue
                    nicks = source.find_all("a", attrs={"class": "entry-author"})
                    nicklist = []
                    nicknum = 0
                    dates = source.find_all("a", attrs={"class": "entry-date permalink"})
                    datelist = []
                    print("\n", header.text)
                    if qa != "*":
                        for entry in entries:
                                for nick in nicks:
                                    nicklist.append(nick)
                                for date in dates:
                                    datelist.append(date)
                                if nicknum < 11:
                                    print("\n", num, "-)", entry.text + "\n", datelist[nicknum].text,
                                          "\n", "\n", "-", nicklist[nicknum].text, "-")
                                    if len(entry.text) <= c_range:
                                        print("—" * len(entry.text))
                                    else:
                                        print("—" * c_range)
                                    nicknum += 1
                                num += 1
                        print("\nsayfa numarası: ", page, "\n", pagecount, "sayfa mevcut")
                    else:
                        for title in entries:
                            print(title.text)
            else:
                break
        except requests.exceptions.ConnectionError:
            print("bağlantınızı kontrol edin")

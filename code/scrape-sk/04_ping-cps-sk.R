library(httr)
library(rvest)
library(tidyverse)
library(here)

pre_search <- read_html("https://cps.sk.ca/")

hidden <- setNames(
  pre_search %>% html_nodes("input[type = 'text']") %>% html_attr("value"),
  pre_search %>% html_nodes("input[type = 'text']") %>% html_attr("name")
) 
str(hidden)

hkey <- pre_search %>% 
  html_node("script[type = 'text/javascript']") %>% 
  html_text %>% 
  str_extract("(?<=var gHKey = ').*(?=';)")
  
PageInstanceKey <- pre_search %>% 
  html_node("input[name='PageInstanceKey']") %>% 
  html_attr("value")

RequestVerificationToken <- pre_search %>% 
  html_node("input[name='__RequestVerificationToken']") %>% 
  html_attr("value")

VIEWSTATE <- pre_search %>% 
  html_node("input[name='__VIEWSTATE']") %>% 
  html_attr("value")

VIEWSTATEGENERATOR <- pre_search %>% 
  html_node("input[name='__VIEWSTATEGENERATOR']") %>% 
  html_attr("value")



res <- POST(
  url = "https://cps.sk.ca/",
  add_headers(
    "Host" = "cps.sk.ca",
    "User-Agent" = "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0",
    "Accept" = "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language" = "en-CA,en-US;q=0.7,en;q=0.3",
    "Accept-Encoding" = "gzip, deflate, br",
    "Referer" = paste0("https://www.cps.sk.ca/imis/CPSS/Home/CPSS/College_of_Physicians_and_Surgeons_of_Saskatchewan.aspx?hkey=", hkey),
    "Content-Type" = "application/x-www-form-urlencoded",
    "Content-Length" = 7715,
    "Connection" = "keep-alive",
    "Cookie" = "_ga=GA1.3.1625650879.1556915156; _gid=GA1.3.126922762.1557259528; ASP.NET_SessionId=2l0wvasid02nclxvhgd4ymwm; __RequestVerificationToken_L2lNSVM1=80N4o0oEYvhybsleWeCx15vwz1HqeucQf1QQd0RBRX_cvBADfFnp2sHeLnrALxWSVSCiePxSSZ1ZUBsdNXzx3XD-vMw2xP3YS1vG9d7Aha81; Asi.Web.Browser.CookiesEnabled=true; _gat=1; _gat_gtag_UA_120907549_1=1",
    "Upgrade-Insecure-Requests" = 1
  ),
  body = list(
    "__WPPS"="s",
    "__ClientContext"='{"baseUrl":"/iMIS/","isAnonymous":true,"websiteRoot":"https://www.cps.sk.ca/imis/"}',
    "ctl01_ScriptManager1_TSM"=';;AjaxControlToolkit,+Version=4.1.50508,+Culture=neutral,+PublicKeyToken=28f01b0e84b6d53e:en-CA:0c8c847b-b611-49a7-8e75-2196aa6e72fa:ea597d4b:b25378d2;Telerik.Web.UI,+Version=2014.3.1209.45,+Culture=neutral,+PublicKeyToken=121fae78165ba3d4:en-CA:cd668efa-682a-4e93-b784-26f0724f247c:16e4e7cd:f7645509:24ee1bba:e330518b:2003d0b8:c128760b:88144a7a:1e771326:c8618e41:1a73651d:333f8d94:ed16cbdc:874f8ea2:92fe8ea0:fa31b949:19620875:f46195d3:490a9d4e:bd8f85e4;AjaxControlToolkit,+Version=4.1.50508.0,+Culture=neutral,+PublicKeyToken=28f01b0e84b6d53e:en-CA:0c8c847b-b611-49a7-8e75-2196aa6e72fa:782b16ab',
    "PageInstanceKey" = PageInstanceKey,
    "__RequestVerificationToken"=RequestVerificationToken,
    "PageIsDirty"="false",
    "IsControlPostBackctl01$SearchField"=1,
    "IsControlPostBackctl01$HeaderLogo$NewContentHtml"=1,
    "NavMenuClientID"="ctl01_TemplateMainNavigation_Primary_NavMenu",
    "IsControlPostBackctl01$HomePageSearch$NewContentHtml"=1,
    "IsControlPostBackctl01$SidebarComplaints$NewContentHtml"=1,
    "IsControlPostBackctl01$SideBarDiscipline$NewContentHtml"=1,
    "IsControlPostBackctl01$SideBarLegislation$NewContentHtml"=1,
    "IsControlPostBackctl01$SideBarRegistration$NewContentHtml"=1,
    "IsControlPostBackctl01$SideBarPrograms$NewContentHtml"=1,
    "IsControlPostBackctl01$TemplateBody$ContentPage1"=1,
    "IsControlPostBackctl01$TemplateBody$ContentPageFooter1"=1,
    "IsControlPostBackctl01$FooterArea$NewContentHtml"=1,
    "__VIEWSTATE"=VIEWSTATE,
    "__VIEWSTATEGENERATOR"=VIEWSTATEGENERATOR,
    "ctl01$SearchField$SearchTerms"="Keyword+Search",
    "ctl01$HomePageSearch$Search$TB_Search"="ko",
    "ctl01$HomePageSearch$Search$TB_City"="",
    "ctl01$HomePageSearch$Search$ddlLanguagesSpoken"="",
    "ctl01$HomePageSearch$Search$ddlSpeciality"="",
    "ctl01$HomePageSearch$Search$Btn_Search"="Go"
  ),
  encode = "form"
)



search <- html_session("https://cps.sk.ca/")


one_doc <- search %>%
  html_node("input[id=ctl01_HomePageSearch_Search_TB_Search]") %>%

search %>% 
  html_node("table") %>% 
  html_

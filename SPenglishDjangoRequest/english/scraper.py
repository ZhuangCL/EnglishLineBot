# LINE訊息回復 取得每日更新英文
# 1.輸入指令
# 2.抓取網路每日英文單字 5個
# 3.之後搜尋英文句子並取得 5句
# 4.將整個資料整合到LINE用戶上
# 5.透過LINE輸入指令並返回資料
# 6.增加每日英文題目 1題
# 7.可額外取得每日新的一詞 多益 托福 雅思單字一個
# 台灣測驗中心-全民英檢參考字表:http://www.taiwantestcentral.com/WordList/WordListByName.aspx?MainCategoryID=4&Letter=A ,每日一題:http://www.taiwantestcentral.com/Grammar/MultipleChoice.aspx?MainCategoryID=4&ID=22625
# 劍橋翻譯:https://dictionary.cambridge.org/zht/translate/
# 每日一句:http://dict.eudic.net/home/dailysentence
# 多益常考單字:https://tw.amazingtalker.com/blog/zh-tw/zh-eng/10141/ 可增加托福 雅思 後續處理
# LINE BOT教學:https://www.learncodewithmike.com/2020/06/python-line-bot.html
import urllib.request as req
# import requests
import random as ra
import csv 
import bs4
# import json
from hanziconv import HanziConv
class EnglishLine():
    def scrape(self):
        content = ''
        # 每日隨機單字*5 
        word = []
        with open('en-word.txt','r',encoding='utf-8') as cf:
            lines = csv.reader(cf, delimiter='|')
            for line in lines:
                word.append(line)
        word = ra.sample(word,k=5)
        content += f'5個隨機單字\n'
        for w in word:
            w = ' '.join(w)
            content += f'{w}\n'
        content += '資料來源:大考中心字彙表-6480詞條\n\n'

        # 每日一詞 O
        url = "https://dictionary.cambridge.org/zht/"
        request=req.Request(url, headers={
            "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36"
        })
        with req.urlopen(request) as response:
            data=response.read().decode("utf-8") 
        root = bs4.BeautifulSoup(data, "html.parser")
        word = (root.find('p', class_='fs36 lmt-5 feature-w-big wotd-hw')).a.string
        content += f"{word}\n"
        try:
            url = "https://dictionary.cambridge.org/zht/%E8%A9%9E%E5%85%B8/%E8%8B%B1%E8%AA%9E-%E6%BC%A2%E8%AA%9E-%E7%B9%81%E9%AB%94/"+word
            request=req.Request(url, headers={
                "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36"
            })
            with req.urlopen(request) as response:
                data=response.read().decode("utf-8") 
            root = bs4.BeautifulSoup(data, "html.parser")
            pos = root.find_all('span', class_='pos dpos')
            if pos != None:
                for p in pos:
                    p = p.string
                    content += f'詞性 : {p}\n'
            example = root.find_all('div', class_='def-block ddef_block')
            if example != None:
                for ex in example:
                    ex = (ex.text).lstrip()
                    content += f'{ex}\n'
            content += '資料來源:劍橋辭典-每日一詞(單字若出現`比較`註記，代表反義詞單字)\n\n'
        except:
            content += '資料來源:劍橋辭典-每日一詞(若無範例或翻譯可直接到官方查找，代表今日非單詞條)\n\n'

        # 每日一句 
        url="http://dict.eudic.net/home/dailysentence"
        request=req.Request(url, headers={
            "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36"
        })
        with req.urlopen(request) as response:
            data=response.read().decode("utf-8") 
        root = bs4.BeautifulSoup(data, "html.parser")
        sentence = root.find("div", class_="sentence") 
        content += f'{sentence.p.string}\n'
        sentence = sentence.find("p", class_="sect-trans").string
        sentence = HanziConv.toTraditional(sentence)
        content += f'{sentence}\n資料來源:歐路辭典-每日一句\n\n'

        # 英檢 
        url="http://www.taiwantestcentral.com/Grammar/MultipleChoice.aspx?MainCategoryID=4&ID="
        requestData=[{"operationName":"TopicHandlerHomeFeed","variables":{"topicSlug":"editors-picks","feedPagingOptions":{"limit":25,"to":"1665860108987"}},"query":"query TopicHandlerHomeFeed($topicSlug: ID!, $feedPagingOptions: PagingOptions) {\n  topic(slug: $topicSlug) {\n    ...CuratedHomeFeedItems_topic\n    __typename\n  }\n}\n\nfragment CuratedHomeFeedItems_topic on Topic {\n  id\n  name\n  latestPosts(paging: $feedPagingOptions) {\n    postPreviews {\n      postId\n      post {\n        id\n        ...HomeFeedItem_post\n        __typename\n      }\n      __typename\n    }\n    pagingInfo {\n      next {\n        limit\n        to\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n  __typename\n}\n\nfragment HomeFeedItem_post on Post {\n  __typename\n  id\n  title\n  firstPublishedAt\n  mediumUrl\n  collection {\n    id\n    name\n    domain\n    logo {\n      id\n      __typename\n    }\n    __typename\n  }\n  creator {\n    id\n    name\n    username\n    imageId\n    mediumMemberAt\n    __typename\n  }\n  previewImage {\n    id\n    __typename\n  }\n  previewContent {\n    subtitle\n    __typename\n  }\n  readingTime\n  tags {\n    ...TopicPill_tag\n    __typename\n  }\n  ...BookmarkButton_post\n  ...OverflowMenuButtonWithNegativeSignal_post\n  ...PostPresentationTracker_post\n  ...PostPreviewAvatar_post\n  ...Star_post\n}\n\nfragment TopicPill_tag on Tag {\n  __typename\n  id\n  displayTitle\n  normalizedTagSlug\n}\n\nfragment BookmarkButton_post on Post {\n  visibility\n  ...SusiClickable_post\n  ...AddToCatalogBookmarkButton_post\n  __typename\n  id\n}\n\nfragment SusiClickable_post on Post {\n  id\n  mediumUrl\n  ...SusiContainer_post\n  __typename\n}\n\nfragment SusiContainer_post on Post {\n  id\n  __typename\n}\n\nfragment AddToCatalogBookmarkButton_post on Post {\n  ...AddToCatalogBase_post\n  __typename\n  id\n}\n\nfragment AddToCatalogBase_post on Post {\n  id\n  __typename\n}\n\nfragment OverflowMenuButtonWithNegativeSignal_post on Post {\n  id\n  ...OverflowMenuWithNegativeSignal_post\n  ...CreatorActionOverflowPopover_post\n  __typename\n}\n\nfragment OverflowMenuWithNegativeSignal_post on Post {\n  id\n  creator {\n    id\n    __typename\n  }\n  collection {\n    id\n    __typename\n  }\n  ...OverflowMenuItemUndoClaps_post\n  __typename\n}\n\nfragment OverflowMenuItemUndoClaps_post on Post {\n  id\n  clapCount\n  ...ClapMutation_post\n  __typename\n}\n\nfragment ClapMutation_post on Post {\n  __typename\n  id\n  clapCount\n  ...MultiVoteCount_post\n}\n\nfragment MultiVoteCount_post on Post {\n  id\n  ...PostVotersNetwork_post\n  __typename\n}\n\nfragment PostVotersNetwork_post on Post {\n  id\n  voterCount\n  recommenders {\n    name\n    __typename\n  }\n  __typename\n}\n\nfragment CreatorActionOverflowPopover_post on Post {\n  allowResponses\n  id\n  statusForCollection\n  isLocked\n  isPublished\n  clapCount\n  mediumUrl\n  pinnedAt\n  pinnedByCreatorAt\n  curationEligibleAt\n  mediumUrl\n  responseDistribution\n  visibility\n  inResponseToPostResult {\n    __typename\n  }\n  inResponseToCatalogResult {\n    __typename\n  }\n  pendingCollection {\n    id\n    name\n    creator {\n      id\n      __typename\n    }\n    avatar {\n      id\n      __typename\n    }\n    domain\n    slug\n    __typename\n  }\n  creator {\n    id\n    ...MutePopoverOptions_creator\n    ...auroraHooks_publisher\n    __typename\n  }\n  collection {\n    id\n    name\n    creator {\n      id\n      __typename\n    }\n    avatar {\n      id\n      __typename\n    }\n    domain\n    slug\n    ...MutePopoverOptions_collection\n    ...auroraHooks_publisher\n    __typename\n  }\n  ...useIsPinnedInContext_post\n  ...NewsletterV3EmailToSubscribersMenuItem_post\n  ...OverflowMenuItemUndoClaps_post\n  __typename\n}\n\nfragment MutePopoverOptions_creator on User {\n  id\n  __typename\n}\n\nfragment auroraHooks_publisher on Publisher {\n  __typename\n  ... on Collection {\n    isAuroraEligible\n    isAuroraVisible\n    viewerEdge {\n      id\n      isEditor\n      __typename\n    }\n    __typename\n    id\n  }\n  ... on User {\n    isAuroraVisible\n    __typename\n    id\n  }\n}\n\nfragment MutePopoverOptions_collection on Collection {\n  id\n  __typename\n}\n\nfragment useIsPinnedInContext_post on Post {\n  id\n  collection {\n    id\n    __typename\n  }\n  pendingCollection {\n    id\n    __typename\n  }\n  pinnedAt\n  pinnedByCreatorAt\n  __typename\n}\n\nfragment NewsletterV3EmailToSubscribersMenuItem_post on Post {\n  id\n  creator {\n    id\n    newsletterV3 {\n      id\n      subscribersCount\n      __typename\n    }\n    __typename\n  }\n  isNewsletter\n  isAuthorNewsletter\n  __typename\n}\n\nfragment PostPresentationTracker_post on Post {\n  id\n  visibility\n  previewContent {\n    isFullContent\n    __typename\n  }\n  collection {\n    id\n    slug\n    __typename\n  }\n  __typename\n}\n\nfragment PostPreviewAvatar_post on Post {\n  __typename\n  id\n  collection {\n    id\n    name\n    ...CollectionAvatar_collection\n    __typename\n  }\n  creator {\n    id\n    username\n    name\n    ...UserAvatar_user\n    ...userUrl_user\n    __typename\n  }\n}\n\nfragment CollectionAvatar_collection on Collection {\n  name\n  avatar {\n    id\n    __typename\n  }\n  ...collectionUrl_collection\n  __typename\n  id\n}\n\nfragment collectionUrl_collection on Collection {\n  id\n  domain\n  slug\n  __typename\n}\n\nfragment UserAvatar_user on User {\n  __typename\n  id\n  imageId\n  mediumMemberAt\n  name\n  username\n  ...userUrl_user\n}\n\nfragment userUrl_user on User {\n  __typename\n  id\n  customDomainState {\n    live {\n      domain\n      __typename\n    }\n    __typename\n  }\n  hasSubdomain\n  username\n}\n\nfragment Star_post on Post {\n  id\n  creator {\n    id\n    __typename\n  }\n  __typename\n}\n"}]
        request=req.Request(url, headers={
            "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36"
        })
        with req.urlopen(request) as response:
            data=response.read().decode("utf-8") 
        root = bs4.BeautifulSoup(data, 'html.parser')
        question = root.find('span', id='MainContent_QuestionAnnotator').text
        content += f'{question}\n'
        options = root.find_all('td', class_='Answer')
        title = ['(A)', '(B)', '(C)', '(D)']
        key = 0
        for op in options:
            op = op.string
            content += f'{title[key]} {op}\n'
            key += 1
        content += f'題目來源:台灣測驗中心-全民英檢考古題(題目空格處填入答案,需要正確答案請複製題目包括選項Google)'
        return content
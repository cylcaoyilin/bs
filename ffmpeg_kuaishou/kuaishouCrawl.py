import csv
import logging
import random
import re
import traceback
import requests
import json
import time

from jsonpath import jsonpath


class KuaishouInfo():
    """日志配置"""

    def __init__(self):

        logger = logging.getLogger()
        #fh = logging.FileHandler('kuaishouinfo.log', encoding='utf-8')
        sh = logging.StreamHandler()

        # formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        formatter2 = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s [line:%(lineno)d] : %(message)s')

        #fh.setFormatter(formatter)
        sh.setFormatter(formatter2)

        #logger.addHandler(fh)
        logger.addHandler(sh)
        logger.setLevel(logging.INFO)

        # 作者列表
        self.author_list = ["深圳公安","海淀公安","格尔木市森林公安局","人民网","新闻联播","人民日报","共青团中央","广东共青团","央视财经","央视国家记忆","中国军网","中国警察网","中国法院网",
                            "浙江中国蓝","中国军视网","中国火箭军","中国新闻网","新华社","中国网直播","中国日报","凤凰卫视"]

        self.channel_list = {
                "推荐":"__NS_sig3=2207563928d8cdf85e8d1dbfd218c3e6581b21ee69&__NStokensig=bd04e598f45d279fd5705d5aca8742b7ded59ad9766cb4eaac074ebf3e075e56&client_key=56c3713c&count=20&country_code=cn&global_id=DFP36A51E345C782CAB4E9187F8E3212BB184D19EF84D9C41EB4A25352F5161B&id=143&kuaishou.api_st=&language=zh-Hans-CN%3Bq%3D1&needInterestTag=0&newUserRefreshTimes=25&newerAction=%7B%22like%22%3A%5B%225222768217233255214%22%5D%2C%22follow%22%3A%5B%5D%2C%22click%22%3A%5B5222768215206098313%2C5221360842189468811%2C5222768217233255214%2C5233464266420691880%2C5201657587144643879%2C5253448985513032424%2C5232338361343220952%2C5200531691519795402%2C5205316762699000857%2C5232056890799408730%5D%7D&pv=false&refreshTimes=9&sig=038dd3c22e2b14c998487a9450d540fc&source=1&token=25ec70fc84fe4bd9bde96cd08cb5ff99-1303986856&type=7",
                "肺炎防治":  "__NS_sig3=2207564468d8077b8dfb085662e7b7fd95ab29482b&__NStokensig=c192cdd064f5c500e412278c2ba66f7bc3c6ee373ae4a992a566fd441e8fe438&client_key=56c3713c&count=20&country_code=cn&global_id=DFP36A51E345C782CAB4E9187F8E3212BB184D19EF84D9C41EB4A25352F5161B&hotChannelId=34&id=155&isLive=0&kuaishou.api_st=&language=zh-Hans-CN%3Bq%3D1&refreshTimes=1&sig=496558cae0459c03fb5600de013a16bf&source=1&token=25ec70fc84fe4bd9bde96cd08cb5ff99-1303986856&type=41",

                "短剧":"__NS_sig3=2207571908d81bb4981f23767e34bb21a7338becfe&__NStokensig=61a3f2185dc4dff1af794ec53d8f47b3eb1f0f6cff83a8a692eac7d8d4587e1d&client_key=56c3713c&count=20&country_code=cn&global_id=DFP36A51E345C782CAB4E9187F8E3212BB184D19EF84D9C41EB4A25352F5161B&hotChannelId=3&id=160&isLive=0&kuaishou.api_st=&language=zh-Hans-CN%3Bq%3D1&refreshTimes=5&sig=da357dd0a0e154780779a4c137373851&source=1&token=25ec70fc84fe4bd9bde96cd08cb5ff99-1303986856&type=41",

                "探店": "__NS_sig3=2207571898d824445e21facd2bb2cf44c48fbdc24a&__NStokensig=ee82d1bb03d2106abdc2b0e43ad2c7dd1a9d3f8eb46e9c0e97b8c8f643b6b27e&client_key=56c3713c&count=20&country_code=cn&global_id=DFP36A51E345C782CAB4E9187F8E3212BB184D19EF84D9C41EB4A25352F5161B&hotChannelId=9&id=161&isLive=0&kuaishou.api_st=&language=zh-Hans-CN%3Bq%3D1&refreshTimes=2&sig=af26ad1b31489f6decdf85711ea8000d&source=1&token=25ec70fc84fe4bd9bde96cd08cb5ff99-1303986856&type=41",

                "美食":  "__NS_sig3=2207571658d88e348adccae5cfb0f12fb09bac0227&__NStokensig=60c25a31f7a310e1f258cb4884270e1e08fec6205646f36740af7bf49b7154f8&client_key=56c3713c&count=20&country_code=cn&global_id=DFP36A51E345C782CAB4E9187F8E3212BB184D19EF84D9C41EB4A25352F5161B&hotChannelId=11&id=163&isLive=0&kuaishou.api_st=&language=zh-Hans-CN%3Bq%3D1&refreshTimes=2&sig=510d84ddaa98d713dcfb65ba2af29814&source=1&token=25ec70fc84fe4bd9bde96cd08cb5ff99-1303986856&type=41",

                "旅行":"__NS_sig3=2207277738d82d6b0df19160a8e19fea89b9e48355&__NStokensig=945048c47a45a3504c355e87bfd9f31b3eacb443562812b32aeafcca5000e691&autoRefresh=true&client_key=56c3713c&coldStart=true&count=20&country_code=cn&global_id=DFP36A51E345C782CAB4E9187F8E3212BB184D19EF84D9C41EB4A25352F5161B&hotChannelId=10&id=171&isLive=0&kuaishou.api_st=&language=zh-Hans-CN%3Bq%3D1&refreshTimes=0&sig=8abe390355fcf7f369a42e8c1cbc02a3&source=1&token=25ec70fc84fe4bd9bde96cd08cb5ff99-1303986856&type=41",

                "音乐":  "__NS_sig3=2207277708d8195a37847c2a84cd3bc13c48092483&__NStokensig=8a72f8cb3303918856f81afffbdeb829370c96f8d075dcea50a46d689072acdc&autoRefresh=true&client_key=56c3713c&coldStart=true&count=20&country_code=cn&global_id=DFP36A51E345C782CAB4E9187F8E3212BB184D19EF84D9C41EB4A25352F5161B&hotChannelId=24&id=172&isLive=0&kuaishou.api_st=&language=zh-Hans-CN%3Bq%3D1&refreshTimes=0&sig=69b2edd362cd007b80cab2c78d7ba3bf&source=1&token=25ec70fc84fe4bd9bde96cd08cb5ff99-1303986856&type=41",

                "视界": "__NS_sig3=2207564508d85855e22c54e9b894bfd6817c1fa90c&__NStokensig=67ba49924e96733087366312f18ff13a201e0410eb48275b90a3f3844d3e74df&autoRefresh=true&client_key=56c3713c&coldStart=true&count=20&country_code=cn&global_id=DFP36A51E345C782CAB4E9187F8E3212BB184D19EF84D9C41EB4A25352F5161B&hotChannelId=20&id=154&isLive=0&kuaishou.api_st=&language=zh-Hans-CN%3Bq%3D1&refreshTimes=0&sig=51d981d1c2ee1ff7a66336278e14a916&source=1&token=25ec70fc84fe4bd9bde96cd08cb5ff99-1303986856&type=41",

                "影视":  "__NS_sig3=2207277638d8b34811bb055b19dea68637405b82ff&__NStokensig=7d43104379735a2b285c07ec2fd11c5a376b7fd1c133bf6cc9cf9141d0fb5204&autoRefresh=true&client_key=56c3713c&coldStart=true&count=20&country_code=cn&global_id=DFP36A51E345C782CAB4E9187F8E3212BB184D19EF84D9C41EB4A25352F5161B&hotChannelId=25&id=174&isLive=0&kuaishou.api_st=&language=zh-Hans-CN%3Bq%3D1&refreshTimes=0&sig=9341d4d4956c5da6107fe7dedf523090&source=1&token=25ec70fc84fe4bd9bde96cd08cb5ff99-1303986856&type=41",

                "风景":  "__NS_sig3=2207277658d8b1630385d6f47cebce0141ed60836c&__NStokensig=36ff11d03c2f397bbadff95d7b6fe744d39cdcdce0874c383958057584b9488c&autoRefresh=true&client_key=56c3713c&coldStart=true&count=20&country_code=cn&global_id=DFP36A51E345C782CAB4E9187F8E3212BB184D19EF84D9C41EB4A25352F5161B&hotChannelId=5&id=175&isLive=0&kuaishou.api_st=&language=zh-Hans-CN%3Bq%3D1&refreshTimes=0&sig=4205fdac298392f36a13c8f714c61f21&source=1&token=25ec70fc84fe4bd9bde96cd08cb5ff99-1303986856&type=41",

                "工艺": "__NS_sig3=2207277618d8465b26a9a296a551cde9358db8f6d8&__NStokensig=b49516adb2c157464fed522cefedf8b646affd3bb0a7fa35e303355b8eed098a&autoRefresh=true&client_key=56c3713c&coldStart=true&count=20&country_code=cn&global_id=DFP36A51E345C782CAB4E9187F8E3212BB184D19EF84D9C41EB4A25352F5161B&hotChannelId=6&id=176&isLive=0&kuaishou.api_st=&language=zh-Hans-CN%3Bq%3D1&refreshTimes=0&sig=ea64bc7824c093d3e53f74e0cf61f4fb&source=1&token=25ec70fc84fe4bd9bde96cd08cb5ff99-1303986856&type=41",

                "海外":  "__NS_sig3=2207277638d830b37fe1b3650caf48cbb201859d74&__NStokensig=e1e1fa3f2dba70115f0479718e729b7c2fba27f7501f3914b438b25de7c6779a&autoRefresh=true&client_key=56c3713c&coldStart=true&count=20&country_code=cn&global_id=DFP36A51E345C782CAB4E9187F8E3212BB184D19EF84D9C41EB4A25352F5161B&hotChannelId=28&id=177&isLive=0&kuaishou.api_st=&language=zh-Hans-CN%3Bq%3D1&refreshTimes=0&sig=c1c2f5253e6420eeca611b8dc66d497c&source=1&token=25ec70fc84fe4bd9bde96cd08cb5ff99-1303986856&type=41",

                "情感": "__NS_sig3=2207277628d8aa8593aab6c63569375a229fd3b911&__NStokensig=1b1b6b994c76805d666562b12db94709be823cb10bf220611272ae9162d2397c&autoRefresh=true&client_key=56c3713c&coldStart=true&count=20&country_code=cn&global_id=DFP36A51E345C782CAB4E9187F8E3212BB184D19EF84D9C41EB4A25352F5161B&hotChannelId=18&id=178&isLive=0&kuaishou.api_st=&language=zh-Hans-CN%3Bq%3D1&refreshTimes=0&sig=4381ce4e42d26a0e70a90341690b3f25&source=1&token=25ec70fc84fe4bd9bde96cd08cb5ff99-1303986856&type=41",

                "明星": "__NS_sig3=2207277578d8133070d03802552482cb505aaa6e13&__NStokensig=1d7002ff012d08d62029ba80d87fd8614e771912713dafd094636f402c96a35a&autoRefresh=true&client_key=56c3713c&coldStart=true&count=20&country_code=cn&global_id=DFP36A51E345C782CAB4E9187F8E3212BB184D19EF84D9C41EB4A25352F5161B&hotChannelId=14&id=179&isLive=0&kuaishou.api_st=&language=zh-Hans-CN%3Bq%3D1&refreshTimes=0&sig=184a77bf8bf6887f688e476c5f015ce1&source=1&token=25ec70fc84fe4bd9bde96cd08cb5ff99-1303986856&type=41",

                "萌宠":  "__NS_sig3=2207277598d84493b2217ec60abb593b720e56ba14&__NStokensig=c292f2bd7ee3aefc16adfce7e50da38ca34c386c93371cd8933fa7ab20e7f2b9&autoRefresh=true&client_key=56c3713c&coldStart=true&count=20&country_code=cn&global_id=DFP36A51E345C782CAB4E9187F8E3212BB184D19EF84D9C41EB4A25352F5161B&hotChannelId=13&id=181&isLive=0&kuaishou.api_st=&language=zh-Hans-CN%3Bq%3D1&refreshTimes=0&sig=02d8f84bb521a310c4b5e22de1ec8f05&source=1&token=25ec70fc84fe4bd9bde96cd08cb5ff99-1303986856&type=41",

                "vlog":  "__NS_sig3=2207284738d8aa3ac7700066ec3b41d09b8c847867&__NStokensig=c809de7eefcd32dc7d71e9524a5780f7589d0c7831d2debfc78c887dc5e258fa&autoRefresh=true&client_key=56c3713c&coldStart=true&count=20&country_code=cn&global_id=DFP36A51E345C782CAB4E9187F8E3212BB184D19EF84D9C41EB4A25352F5161B&hotChannelId=1&id=182&isLive=0&kuaishou.api_st=&language=zh-Hans-CN%3Bq%3D1&refreshTimes=0&sig=23ddc6f3f54b6a0a9de0301c81b5b33e&source=1&token=25ec70fc84fe4bd9bde96cd08cb5ff99-1303986856&type=41",

                "美妆":  "__NS_sig3=2207284728d874c3f7b560b37c145c3ad8041c5e6b&__NStokensig=c085f3aae3494e3708b13cc76feaf6acc234e666a5e7d96175a9d4f68282aee2&autoRefresh=true&client_key=56c3713c&coldStart=true&count=20&country_code=cn&global_id=DFP36A51E345C782CAB4E9187F8E3212BB184D19EF84D9C41EB4A25352F5161B&hotChannelId=12&id=183&isLive=0&kuaishou.api_st=&language=zh-Hans-CN%3Bq%3D1&refreshTimes=0&sig=cce978298ba9abc89cc9b60e9a735f6b&source=1&token=25ec70fc84fe4bd9bde96cd08cb5ff99-1303986856&type=41",

                "游戏": "__NS_sig3=2207284678d8d62cad206b542d7616f9c9e6c48abe&__NStokensig=2bc6e9c37a9f7b319372d2da176edec455453c9b37a83681d3fde9face5c2cdd&autoRefresh=true&client_key=56c3713c&coldStart=true&count=20&country_code=cn&global_id=DFP36A51E345C782CAB4E9187F8E3212BB184D19EF84D9C41EB4A25352F5161B&hotChannelId=26&id=184&isLive=0&kuaishou.api_st=&language=zh-Hans-CN%3Bq%3D1&refreshTimes=0&sig=94567539f03c29401794442ad6661a76&source=1&token=25ec70fc84fe4bd9bde96cd08cb5ff99-1303986856&type=41",

                "萌娃":  "__NS_sig3=2207284708d88e9b7f8d55f32c272861bfd040ee77&__NStokensig=4b59f32d5df925137d56b3285277e1eb3b90159d622b53c28c5e740f3ed91400&autoRefresh=true&client_key=56c3713c&coldStart=true&count=20&country_code=cn&global_id=DFP36A51E345C782CAB4E9187F8E3212BB184D19EF84D9C41EB4A25352F5161B&hotChannelId=27&id=185&isLive=0&kuaishou.api_st=&language=zh-Hans-CN%3Bq%3D1&refreshTimes=0&sig=4259f5c90e581442bd86c8f40cc3ffde&source=1&token=25ec70fc84fe4bd9bde96cd08cb5ff99-1303986856&type=41",

                "运动":  "__NS_sig3=2207284698d8084544a24cef3f5cc40dd54e6dc13a&__NStokensig=31f49bce02169afd778188f787468c3e1fa2055f0d6077c1ecc9e86b0333f140&autoRefresh=true&client_key=56c3713c&coldStart=true&count=20&country_code=cn&global_id=DFP36A51E345C782CAB4E9187F8E3212BB184D19EF84D9C41EB4A25352F5161B&hotChannelId=30&id=186&isLive=0&kuaishou.api_st=&language=zh-Hans-CN%3Bq%3D1&refreshTimes=0&sig=c53fb920e8174f428a7072801bad356c&source=1&token=25ec70fc84fe4bd9bde96cd08cb5ff99-1303986856&type=41",

                "舞蹈": "__NS_sig3=2207284658d8a85c2d203484f73487f27468d3c128&__NStokensig=b05b6913999a33613c6e7bbdbf8dbfe966c38080762dd456c7fab2c41bd4fe71&autoRefresh=true&client_key=56c3713c&coldStart=true&count=20&country_code=cn&global_id=DFP36A51E345C782CAB4E9187F8E3212BB184D19EF84D9C41EB4A25352F5161B&hotChannelId=31&id=187&isLive=0&kuaishou.api_st=&language=zh-Hans-CN%3Bq%3D1&refreshTimes=0&sig=aee647db76edb20b6a7037989e7ea896&source=1&token=25ec70fc84fe4bd9bde96cd08cb5ff99-1303986856&type=41",

                "汽车":  "__NS_sig3=2207284648d801ab72f588d80b07cc13c1742bd884&__NStokensig=9437b1ef03c2ab6837030a7311f15186a250356903012d8fdb8997fd1c7d26ac&autoRefresh=true&client_key=56c3713c&coldStart=true&count=20&country_code=cn&global_id=DFP36A51E345C782CAB4E9187F8E3212BB184D19EF84D9C41EB4A25352F5161B&hotChannelId=17&id=188&isLive=0&kuaishou.api_st=&language=zh-Hans-CN%3Bq%3D1&refreshTimes=0&sig=cbbd470677f4ba22d1e0248732ba8b40&source=1&token=25ec70fc84fe4bd9bde96cd08cb5ff99-1303986856&type=41",

                "二次元": "__NS_sig3=2207284668d8bb1aee4ce000512239175cbe8ff938&__NStokensig=8dadfe85a3908af78223950d619cdd4593a24760d0694b75f3d1d6b55a36c19c&autoRefresh=true&client_key=56c3713c&coldStart=true&count=20&country_code=cn&global_id=DFP36A51E345C782CAB4E9187F8E3212BB184D19EF84D9C41EB4A25352F5161B&hotChannelId=4&id=189&isLive=0&kuaishou.api_st=&language=zh-Hans-CN%3Bq%3D1&refreshTimes=0&sig=a959374f56297d32c9fab7ed9ecd974a&source=1&token=25ec70fc84fe4bd9bde96cd08cb5ff99-1303986856&type=41",

                "穿搭":  "__NS_sig3=2207284668d8df1c85640f48e357ed423d19e2d1af&__NStokensig=51ba3b75970ad2b530753534161e62c6b3f99486bc90627bd73b24ef286b6636&autoRefresh=true&client_key=56c3713c&coldStart=true&count=20&country_code=cn&global_id=DFP36A51E345C782CAB4E9187F8E3212BB184D19EF84D9C41EB4A25352F5161B&hotChannelId=2&id=190&isLive=0&kuaishou.api_st=&language=zh-Hans-CN%3Bq%3D1&refreshTimes=0&sig=121917c2a541def8ef11d5ca3905fff3&source=1&token=25ec70fc84fe4bd9bde96cd08cb5ff99-1303986856&type=41",

                "书画": "__NS_sig3=2207284628d81146949d53ac8bf7a2c3ea8758fdf2&__NStokensig=fb6bd028d2045da92226ba652bc0c5f4fb7939caebf81c253a35039d27190802&autoRefresh=true&client_key=56c3713c&coldStart=true&count=20&country_code=cn&global_id=DFP36A51E345C782CAB4E9187F8E3212BB184D19EF84D9C41EB4A25352F5161B&hotChannelId=21&id=191&isLive=0&kuaishou.api_st=&language=zh-Hans-CN%3Bq%3D1&refreshTimes=0&sig=4c223890c466827ec5fa61e44b1b5b3b&source=1&token=25ec70fc84fe4bd9bde96cd08cb5ff99-1303986856&type=41",

                "颜值":  "__NS_sig3=2207284618d8cfcece8ec236b782b36648a3708b33&__NStokensig=a1fd096aeced098ead44bd72270f3097d6fec572a26b93f2faa111019789466f&autoRefresh=true&client_key=56c3713c&coldStart=true&count=20&country_code=cn&global_id=DFP36A51E345C782CAB4E9187F8E3212BB184D19EF84D9C41EB4A25352F5161B&hotChannelId=23&id=192&isLive=0&kuaishou.api_st=&language=zh-Hans-CN%3Bq%3D1&refreshTimes=0&sig=bb8bf4dab6f750fc51be89cb27477418&source=1&token=25ec70fc84fe4bd9bde96cd08cb5ff99-1303986856&type=41",

                "摄影":"__NS_sig3=2207277728d8a4eaf76d7d36a70e6b214ba431b634&__NStokensig=93211a667fd5c41b226233b78b16bcb49840da056a03d77d401641d42ff51fe9&autoRefresh=true&client_key=56c3713c&coldStart=true&count=20&country_code=cn&global_id=DFP36A51E345C782CAB4E9187F8E3212BB184D19EF84D9C41EB4A25352F5161B&hotChannelId=19&id=173&isLive=0&kuaishou.api_st=&language=zh-Hans-CN%3Bq%3D1&refreshTimes=0&sig=e284a2273b9d03ee5abbcaafac6bd5f5&source=1&token=25ec70fc84fe4bd9bde96cd08cb5ff99-1303986856&type=41",
            }

    def start_requests(self,channel,post_data): # 初始构建POST请求获取相应
        try:
            ua = self.get_ua()
            # 2019/11/1修改data

            headers = {
                "User-Agent": ua,
                "Content-Type": "application/x-www-form-urlencoded",
                "Host": "api.gifshow.com",
            }
            #url = "http://api.gifshow.com/rest/n/feed/hot?extId=b84ddbb8712f95bf71a7caa90e6de58f&kpf=IPHONE&net=%E4%B8%AD%E5%9B%BD%E7%A7%BB%E5%8A%A8_5&appver=6.6.6.1036&kpn=KUAISHOU&c=a&mod=iPhone10%2C3&sys=ios12.3.1&did_gt=1553564894977&ver=6.6&isp=CMCC&did=C1155C04-4769-4C7B-AB35-71ABBC02373C&egid=DFP52CEE5771F883201CEB9CB9E93884CE255CE35CD976BB550081477FF5AD23"
            # url = "http://api.gifshow.com/rest/n/feed/hot?mod=HUAWEI%28HUAWEI%20NXT-AL10%29&lon=113.916723&country_code=CN&extId=54b3ddcc3a5a68b0824f010acc397ebd&kpn=KUAISHOU&oc=360APP%2C1&egid=&hotfix_ver=&sh=1920&appver=6.9.0.11026&max_memory=384&isp=CTCC&kpf=ANDROID_PHONE&did=ANDROID_d378c14e12ad99c8&app=0&net=WIFI&ud=0&c=360APP%2C1&sys=ANDROID_7.0&sw=1080&ftt=&language=zh-cn&lat=22.492756&iuid=&ver=6.9&did_gt=1572227606346"
            # url = "http://api.gifshow.com/rest/n/feed/hot?isp=CMCC&mod=Xiaomi%20%28MI%206%20%29&lon=115.569237&country_code=CN&kpf=ANDROID_PHONE&extId=d085b7507ada79f8a6ae9f628be7cc0f&did=ANDROID_1c872c434ffa2434&kpn=KUAISHOU&net=WIFI&app=0&oc=MYAPP%2C1&ud=0&hotfix_ver=&c=MYAPP%2C1&sys=ANDROID_5.1.1&appver=6.2.0.8246&ftt=&language=zh-cn&iuid=&lat=36.00109&did_gt=1552545766578&ver=6.2&max_memory=192"
            #url = "https://apissl.gifshow.com/rest/n/feed/hot?extId=b84ddbb8712f95bf71a7caa90e6de58f&kcv=188&kpf=IPHONE&net=%E4%B8%AD%E5%9B%BD%E7%A7%BB%E5%8A%A8_5&appver=7.1.5.1577&kpn=KUAISHOU&c=a&mod=iPhone10%2C3&sys=ios13.3.1&sh=2436&ver=7.1&isp=CMCC&did=C1155C04-4769-4C7B-AB35-71ABBC02373C&ud=1303986856&did_gt=1553564894977&sw=1125&browseType=1&egid=DFPE13C35187A48B12003DF553C06C7FE1A46DF2AA117FEC41FA798107DC6D6D"
            #2019/11/1 10:00 修改url
            tuijian_url = "http://apissl.gifshow.com/rest/n/feed/hot?extId=b84ddbb8712f95bf71a7caa90e6de58f&kcv=188&kpf=IPHONE&net=%E4%B8%AD%E5%9B%BD%E7%A7%BB%E5%8A%A8_5&appver=7.1.2.1527&kpn=KUAISHOU&c=a&mod=iPhone10%2C3&sys=ios13.3.1&sh=2436&ver=7.1&isp=CMCC&did=C1155C04-4769-4C7B-AB35-71ABBC02373C&ud=1303986856&did_gt=1553564894977&sw=1125&browseType=1&egid=DFP36A51E345C782CAB4E9187F8E3212BB184D19EF84D9C41EB4A25352F5161B"
            other_url = "https://api3.ksapisrv.com/rest/n/feed/hot/channel?kcv=188&kpf=IPHONE&net=%E4%B8%AD%E5%9B%BD%E7%A7%BB%E5%8A%A8_5&appver=7.1.2.1527&kpn=KUAISHOU&mod=iPhone10%2C3&c=a&sys=ios13.3.1&sh=2436&ver=7.1&isp=CMCC&did=C1155C04-4769-4C7B-AB35-71ABBC02373C&ud=1303986856&did_gt=1553564894977&sw=1125&browseType=1&egid=DFP36A51E345C782CAB4E9187F8E3212BB184D19EF84D9C41EB4A25352F5161B"
            if channel == "推荐":
                url = tuijian_url
            else:
                url = other_url
            res = requests.post(url, headers=headers, data=post_data,timeout=20)
            if json.loads(res.text).get('result') == 1:
                logging.info("==================获取视频数据流成功===================")
                return res.text
            else:
                logging.info("无数据")
        except Exception as e:
            logging.info("报错start_requests:{}".format(e))
            return None

    def parse(self,channel,post_data): # 解析响应，获取数据
        res = self.start_requests(channel,post_data)
        data = json.loads(res)
        feeds = jsonpath(data, '$..feeds')[0]
        try:
            for feed in feeds:
                title = jsonpath(feed, '$..caption')

                if not title or len(title) < 1:
                    logging.info("===============过滤标题不存在===============")
                    continue
                newsId = str(jsonpath(feed, '$..photo_id')[0])
                if not newsId or len(newsId) < 1:
                    logging.info("===============过滤视频ID不存在===============")
                    continue
                authorNickname = jsonpath(feed, '$..user_name')
                if not authorNickname or len(authorNickname) < 1:
                    authorNickname = ''
                    logging.info("===============作者名字不存在，修改信息===============")
                else:
                    authorNickname = authorNickname[0]
                authorId = jsonpath(feed, '$..user_id')
                if not authorId or len(authorId) < 1:
                    logging.info("===============作者ID不存在，修改信息===============")
                    authorId = ''
                else:
                    authorId = authorId[0]

                publishDate = jsonpath(feed, '$..timestamp')
                if not publishDate or len(publishDate) < 1:
                    logging.info("===============提交时间不存在，修改信息===============")
                    publishDate = int(time.time())
                else:
                    publishDate = publishDate[0]
                try:
                    videoUrl = jsonpath(feed, '$..main_mv_urls..url')[0]
                except TypeError:
                    continue
                if not videoUrl or len(videoUrl) < 1:
                    logging.info("===============过滤播放MP4链接不存在===============")
                    continue
                videoUrl = re.match(r'^(http.*?mp4)?.*', videoUrl).group(1)
                protogen_images = jsonpath(feed, '$..cover_thumbnail_urls..url')
                if not protogen_images or len(protogen_images) < 1:
                    logging.info("===============过滤图片不存在===============")
                    continue
                else:
                    protogen_images=protogen_images[0]

                # logging.info("---------------提取音频第一帧-------------------")
                readCount = jsonpath(feed, '$..view_count')
                if not readCount or len(readCount) < 1:
                    logging.info("===============阅读信息不存在，修改信息===============")
                    readCount = 0
                else:
                    readCount = readCount[0]
                transpondCount = jsonpath(feed,'$..share_count')
                if not transpondCount or len(transpondCount) < 1:
                    logging.info("===============评论信息不存在，修改信息===============")
                    transpondCount = 0
                else:
                    transpondCount = transpondCount[0]
                commentCount = jsonpath(feed, '$..comment_count')
                if not commentCount or len(commentCount) < 1:
                    logging.info("===============评论信息不存在，修改信息===============")
                    commentCount = 0
                else:
                    commentCount = commentCount[0]

                praiseCount = jsonpath(feed, '$..like_count')
                if not praiseCount or len(praiseCount) < 1:
                    logging.info("===============点赞信息不存在，修改信息===============")
                    praiseCount = 0
                else:
                    praiseCount = praiseCount[0]
                item_dict = {}
                video_type = jsonpath(feed, '$..type')[0]
                sex = jsonpath(feed, '$..user_sex')[0]
                if sex == 'F':
                    sex = '女'
                else:
                    sex = "男"
                tag = jsonpath(feed, '$..tag')
                item_dict['sex'] = sex
                item_dict['title'] = title[0].replace('快手','')  # 标题  string
                item_dict['type'] = video_type
                item_dict['newsId'] = newsId  # 新闻id  string
                item_dict['authorNickname'] = authorNickname  # 作者名字  string
                item_dict['introduce'] = ''  # 正文  string
                item_dict['createTime'] = int(time.time())  # 创建时间  int
                item_dict['publishDate'] = int(re.findall('(\d{10})',str(publishDate))[0])  # 发布时间  int
                item_dict['protogen_images'] = protogen_images  # 原生图片
                item_dict['authorId'] = str(authorId)  # 作者ID  string
                item_dict['readCount'] = int(readCount)  # 阅读数  int
                item_dict['commentCount'] = int(commentCount)  # 评论数 int
                item_dict['transpondCount'] = transpondCount  # 转发数  int
                item_dict['collectionCount'] = 0  # 收藏数  int
                item_dict['praiseCount'] = int(praiseCount)  # 点赞数  int
                item_dict['channelNames'] = "小视频"  # 一级标签  string
                item_dict['tagNames'] = self.get_tag(item_dict['title'],tag)  # 二级标签  string  多个以逗号隔开
                item_dict['fromDesc'] = '快手'  # 来源
                item_dict['fromCode'] = '小视频'  # 来源
                item_dict['abstractContent'] = ''  # 摘要
                item_dict['imageCount'] = 1
                item_dict['videoUrl'] = videoUrl
                item_dict['channelfield'] = channel
                # print(item_dict['title'],item_dict['type'],item_dict['channelNames'],item_dict['tagNames'],item_dict['videoUrl'])

                csv_file = '../TuiJian/result.csv'
                # 写入CSV文件
                with open(csv_file, 'a+', encoding='utf-8-sig', newline='') as f:
                    f_csv = csv.writer(f)
                    f_csv.writerow([
                        item_dict['title'],
                        item_dict['type'],
                        item_dict['channelNames'],
                        item_dict['tagNames'],
                        item_dict['videoUrl']
                    ])

                # print(item_dict)

        except:
            logging.info(traceback.format_exc())
            return None


    def get_ua(self):   # 构建随机UA池
        user_agent_list = [
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 "
            "(KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
            "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 "
            "(KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 "
            "(KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 "
            "(KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
            "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 "
            "(KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 "
            "(KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
            "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 "
            "(KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 "
            "(KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
            "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 "
            "(KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 "
            "(KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 "
            "(KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 "
            "(KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 "
            "(KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 "
            "(KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 "
            "(KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 "
            "(KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 "
            "(KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
            "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24"
            "(KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"
        ]
        ua = random.choices(user_agent_list)[0]
        return ua

    def get_tag(self,title, tag):
        if tag:
            tag = [i.strip('#') for i in tag]
        else:
            tag = []
        if "#" in title:
            tag_add = [i.strip('#') for i in re.findall('#(.*?) ', title + " ")]
        else:
            tag_add = []
        tag = tag + tag_add
        if tag:
            tagNames = ','.join(sorted(set(tag)))
        else:
            tagNames = ''
        return tagNames

if __name__ == '__main__':
    kuaishou = KuaishouInfo()
    row = 0
    while True:
        #
        try:
            for channel, post_data in kuaishou.channel_list.items():
                print("=============================== 下载{}行数据 ===============================".format(row))
                item_dict = kuaishou.parse(channel,post_data)
                row = row + 1
                # print("\n")
                # time.sleep(1)
        except Exception as e:
            # logging.info("388报错================>{}<=================".format(e))
            continue

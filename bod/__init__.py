#
# Inspired by jd/jdout from CloudGenix SDK.
#
import json
import requests
from typing import Any
from bs4 import BeautifulSoup as bs

import sys

class MyModule(sys.modules[__name__].__class__):
    def __call__(self, *args, **kwargs):  # module callable
        print(f"call {args} {kwargs}")
        return Test(*args, **kwargs)

sys.modules[__name__].__class__ = MyModule

def test2(*args, **kwargs):
    print(f"test2 {args} {kwargs}")
    return

class Test(object):

    def __init__(self, *args, **kwargs):
        print(f"Hi {args} {kwargs}")
        return

    def test(self):
        print("test")
        return

#
# def jd(api_response: Any, indent: str | int=4, sort_keys: bool=True) -> None:
#     """
#     JD (JSON Dump) function. Meant for quick pretty-printing of a CloudGenix Response body.
#
#     Example: `jd(sdk.get.sites())`
#
#       **Parameters:**
#
#       - **api_response:** A CloudGenix-attribute extended `requests.Response` object
#
#     **Returns:** No Return, directly prints all output.
#     """
#     print(jdout(api_response, indent=4, sort_keys=True))
#     return
#
#
# def jdout(api_response: Any, indent: str | int=4, sort_keys: bool=True) -> str:
#     """
#     JD Output function. Does quick pretty printing of a JSON body. This function returns a string
#     instead of directly printing content.
#
#       **Parameters:**
#
#       - **api_response:** A Dictionary or `requests.Response` object
#
#     **Returns:** Pretty-formatted text of the Response body
#     """
#
#     # first check for requests.Response
#     try:
#         working_data_ = api_response.content
#     except (TypeError, ValueError, AttributeError):
#         working_data = api_response
#
#
#     # quick check for bytes, decode to string.
#     if isinstance(api_response, bytes):
#         working_data = api_response.decode('utf-8')
#     else:
#         working_data = api_response
#
#     # check if is str, if so - parse based on how it's interpreted
#     if isinstance(working_data, str):
#         # check if JSON serializable
#         try:
#             working_data_parsed = json.loads(working_data)
#         except json.JSONDecodeError:
#             working_data_parsed = None
#         if working_data_parsed:
#
#     try:
#         # attempt to output the cgx_content. should always be a Dict if it exists.
#         output = json.dumps(api_response.cgx_content, indent=4)
#     except (TypeError, ValueError, AttributeError):
#         # cgx_content did not exist, or was not JSON serializable. Try pretty output the base obj.
#         try:
#             output = json.dumps(api_response, indent=4)
#         except (TypeError, ValueError, AttributeError):
#             # Same issue, just raw output the passed data. Let any exceptions happen here.
#             output = api_response
#     return output
#
#
# def jd_detailed(api_response, sensitive=False):
#     """
#     JD (JSON Dump) Detailed function. Meant for quick DETAILED pretty-printing of CloudGenix Request and Response
#     objects for troubleshooting.
#
#     Example: `jd_detailed(cgx_sess.get.sites())`
#
#       **Parameters:**
#
#       - **api_response:** A CloudGenix-attribute extended `requests.Response` object
#       - **sensitive:** Boolean, if True will print sensitive content (specifically, authentication cookies/headers).
#
#     **Returns:** No Return, directly prints all output.
#     """
#     print(jdout_detailed(api_response, sensitive=sensitive))
#     return
#
#
# def jdout_detailed(api_response, sensitive=False):
#     """
#     JD Output Detailed function. Meant for quick DETAILED pretty-printing of CloudGenix Request and Response
#     objects for troubleshooting. This function returns a string instead of directly printing content.
#
#       **Parameters:**
#
#       - **api_response:** A CloudGenix-attribute extended `requests.Response` object
#       - **sensitive:** Boolean, if True will print sensitive content (specifically, authentication cookies/headers).
#
#     **Returns:** Pretty-formatted text of the Request, Request Headers, Request body, Response, Response Headers,
#     and Response Body.
#     """
#     try:
#         # try to be super verbose.
#         output = "REQUEST: {0} {1}\n".format(api_response.request.method, api_response.request.path_url)
#         output += "REQUEST HEADERS:\n"
#         for key, value in api_response.request.headers.items():
#             # look for sensitive values
#             if key.lower() in ['cookie'] and not sensitive:
#                 # we need to do some work to watch for the AUTH_TOKEN cookie. Split on cookie separator
#                 cookie_list = value.split('; ')
#                 muted_cookie_list = []
#                 for cookie in cookie_list:
#                     # check if cookie starts with a permutation of AUTH_TOKEN/whitespace.
#                     if cookie.lower().strip().startswith('auth_token='):
#                         # first 11 chars of cookie with whitespace removed + mute string.
#                         newcookie = cookie.strip()[:11] + "\"<SENSITIVE - NOT SHOWN BY DEFAULT>\""
#                         muted_cookie_list.append(newcookie)
#                     else:
#                         muted_cookie_list.append(cookie)
#                 # got list of cookies, muted as needed. recombine.
#                 muted_value = "; ".join(muted_cookie_list)
#                 output += "\t{0}: {1}\n".format(key, muted_value)
#             elif key.lower() in ['x-auth-token'] and not sensitive:
#                 output += "\t{0}: {1}\n".format(key, "<SENSITIVE - NOT SHOWN BY DEFAULT>")
#             else:
#                 output += "\t{0}: {1}\n".format(key, value)
#         # if body not present, output blank.
#         if not api_response.request.body:
#             output += "REQUEST BODY:\n{0}\n\n".format({})
#         else:
#             try:
#                 # Attempt to load JSON from string to make it look beter.
#                 output += "REQUEST BODY:\n{0}\n\n".format(json.dumps(json.loads(api_response.request.body), indent=4))
#             except (TypeError, ValueError, AttributeError):
#                 # if pretty call above didn't work, just toss it to jdout to best effort it.
#                 output += "REQUEST BODY:\n{0}\n\n".format(jdout(api_response.request.body))
#         output += "RESPONSE: {0} {1}\n".format(api_response.status_code, api_response.reason)
#         output += "RESPONSE HEADERS:\n"
#         for key, value in api_response.headers.items():
#             output += "\t{0}: {1}\n".format(key, value)
#         try:
#             # look for CGX content first.
#             output += "RESPONSE DATA:\n{0}".format(json.dumps(api_response.cgx_content, indent=4))
#         except (TypeError, ValueError, AttributeError):
#             # look for standard response data.
#             output += "RESPONSE DATA:\n{0}".format(json.dumps(json.loads(api_response.content), indent=4))
#     except (TypeError, ValueError, AttributeError, UnicodeDecodeError):
#         # cgx_content did not exist, or was not JSON serializable. Try pretty output the base obj.
#         try:
#             output = json.dumps(api_response, indent=4)
#         except (TypeError, ValueError, AttributeError):
#             # Same issue, just raw output the passed data. Let any exceptions happen here.
#             output = api_response
#     return output
#
#
# testcontent = '<!doctype html><html itemscope="" itemtype="http://schema.org/WebPage" lang="en"><head><meta content="Search the world\'s information, including webpages, images, videos and more. Google has many special features to help you find exactly what you\'re looking for." name="description"><meta content="noodp, " name="robots"><meta content="text/html; charset=UTF-8" http-equiv="Content-Type"><meta content="/images/branding/googleg/1x/googleg_standard_color_128dp.png" itemprop="image"><title>Google</title><script nonce="pJ2BM1u4uGddcyvZQjgA3Q">(function(){var _g={kEI:\'S5LIZ5WPHN6ikPIP_Z3YaQ\',kEXPI:\'0,18168,184623,3497543,615,435,538661,2872,2891,73050,16105,78219,266577,247320,42724,5241754,8834893,78,3,3,2,3,1,3,23933874,4043710,25228681,46383,65738,10983,884,14280,8182,5933,43496,19011,2661,3433,3319,23878,9139,4600,328,6225,34310,16265,12881,709,1250,1,90,5328,8379,8211,3286,4134,21306,33,9041,17667,10666,10904,10440,2987,5354,41,5595,8044,1,6741,2895,1211,2620,1834,17896,3,2749,951,2146,4610,7,5774,4310,2371,8227,1743,9171,1789,911,769,3039,837,1033,679,4895,2677,50,1634,2460,801,459,2531,28,7,1,1293,2126,713,850,554,386,360,1,893,56,1023,1,831,218,1,2947,1362,5,1602,1681,569,1791,88,488,151,272,1,1401,1294,467,7,1,371,1891,192,1,926,1435,407,354,658,525,3,81,3143,200,477,590,6,91,8,2191,21,2216,1887,1,732,88,2,272,96,295,113,254,615,1807,723,10,897,241,1587,1474,570,87,250,846,2,522,814,902,22,239,1210,4,280,7,1,989,167,1026,293,132,1,68,5,897,88,898,1,12,1039,582,348,602,412,343,261,677,30,193,97,95,2,6,21,755,3,5,3,3,2,224,7,6,594,12,327,101,296,277,663,3,2,648,160,603,220,4,574,121,40,1234,5,239,107,10,835,167,115,530,26,273,119,59,264,36,316,7,620,496,79,54,546,134,1,80,103,92,780,356,135,276,2,160,31,780,94,284,218,267,1482,38,242,1018,1,9,19,577,2,239,284,464,3,19,877,2,1,6,590,152,505,2,1,2,2,2,320,1668,21338114,18,2017,1207,510,806,8,3873,12,1888,3792,2690,756,28,6011132,2500107\',kBL:\'hfr-\',kOPI:89978449};(function(){var a;((a=window.google)==null?0:a.stvsc)?google.kEI=_g.kEI:window.google=_g;}).call(this);})();(function(){google.sn=\'webhp\';google.kHL=\'en\';})();(function(){\nvar g=this||self;function k(){return window.google&&window.google.kOPI||null};var l,m=[];function n(a){for(var b;a&&(!a.getAttribute||!(b=a.getAttribute("eid")));)a=a.parentNode;return b||l}function p(a){for(var b=null;a&&(!a.getAttribute||!(b=a.getAttribute("leid")));)a=a.parentNode;return b}function q(a){/^http:/i.test(a)&&window.location.protocol==="https:"&&(google.ml&&google.ml(Error("a"),!1,{src:a,glmm:1}),a="");return a}\nfunction r(a,b,d,c,h){var e="";b.search("&ei=")===-1&&(e="&ei="+n(c),b.search("&lei=")===-1&&(c=p(c))&&(e+="&lei="+c));var f=b.search("&cshid=")===-1&&a!=="slh";c="&zx="+Date.now().toString();g._cshid&&f&&(c+="&cshid="+g._cshid);(d=d())&&(c+="&opi="+d);return"/"+(h||"gen_204")+"?atyp=i&ct="+String(a)+"&cad="+(b+e+c)};l=google.kEI;google.getEI=n;google.getLEI=p;google.ml=function(){return null};google.log=function(a,b,d,c,h,e){e=e===void 0?k:e;d||(d=r(a,b,e,c,h));if(d=q(d)){a=new Image;var f=m.length;m[f]=a;a.onerror=a.onload=a.onabort=function(){delete m[f]};a.src=d}};google.logUrl=function(a,b){b=b===void 0?k:b;return r("",a,b)};}).call(this);(function(){google.y={};google.sy=[];var d;(d=google).x||(d.x=function(a,b){if(a)var c=a.id;else{do c=Math.random();while(google.y[c])}google.y[c]=[a,b];return!1});var e;(e=google).sx||(e.sx=function(a){google.sy.push(a)});google.lm=[];var f;(f=google).plm||(f.plm=function(a){google.lm.push.apply(google.lm,a)});google.lq=[];var g;(g=google).load||(g.load=function(a,b,c){google.lq.push([[a],b,c])});var h;(h=google).loadAll||(h.loadAll=function(a,b){google.lq.push([a,b])});google.bx=!1;var k;(k=google).lx||(k.lx=function(){});var l=[],m;(m=google).fce||(m.fce=function(a,b,c,n){l.push([a,b,c,n])});google.qce=l;}).call(this);google.f={};(function(){\ndocument.documentElement.addEventListener("submit",function(b){var a;if(a=b.target){var c=a.getAttribute("data-submitfalse");a=c==="1"||c==="q"&&!a.elements.q.value?!0:!1}else a=!1;a&&(b.preventDefault(),b.stopPropagation())},!0);document.documentElement.addEventListener("click",function(b){var a;a:{for(a=b.target;a&&a!==document.documentElement;a=a.parentElement)if(a.tagName==="A"){a=a.getAttribute("data-nohref")==="1";break a}a=!1}a&&b.preventDefault()},!0);}).call(this);</script><style>#gbar,#guser{font-size:13px;padding-top:1px !important;}#gbar{height:22px}#guser{padding-bottom:7px !important;text-align:right}.gbh,.gbd{border-top:1px solid #c9d7f1;font-size:1px}.gbh{height:0;position:absolute;top:24px;width:100%}@media all{.gb1{height:22px;margin-right:.5em;vertical-align:top}#gbar{float:left}}a.gb1,a.gb4{text-decoration:underline !important}a.gb1,a.gb4{color:#00c !important}.gbi .gb4{color:#dd8e27 !important}.gbf .gb4{color:#900 !important}\n</style><style>body,td,a,p,.h{font-family:sans-serif}body{margin:0;overflow-y:scroll}#gog{padding:3px 8px 0}td{line-height:.8em}.gac_m td{line-height:17px}form{margin-bottom:20px}.h{color:#1967d2}em{font-weight:bold;font-style:normal}.lst{height:25px;width:496px}.gsfi,.lst{font:18px sans-serif}.gsfs{font:17px sans-serif}.ds{display:inline-box;display:inline-block;margin:3px 0 4px;margin-left:4px}input{font-family:inherit}body{background:#fff;color:#000}a{color:#681da8;text-decoration:none}a:hover,a:active{text-decoration:underline}.fl a{color:#1967d2}a:visited{color:#681da8}.sblc{padding-top:5px}.sblc a{display:block;margin:2px 0;margin-left:13px;font-size:11px}.lsbb{background:#f8f9fa;border:solid 1px;border-color:#dadce0 #70757a #70757a #dadce0;height:30px}.lsbb{display:block}#WqQANb a{display:inline-block;margin:0 12px}.lsb{background:url(/images/nav_logo229.png) 0 -261px repeat-x;color:#000;border:none;cursor:pointer;height:30px;margin:0;outline:0;font:15px sans-serif;vertical-align:top}.lsb:active{background:#dadce0}.lst:focus{outline:none}</style><script nonce="pJ2BM1u4uGddcyvZQjgA3Q">(function(){window.google.erd={jsr:1,bv:2178,de:true,dpf:\'jGUd7TG_xAoI4ZP50KVouaIgNT0cKa38dy4rlcs3vQo\'};\nvar g=this||self;var k,l=(k=g.mei)!=null?k:1,m,p=(m=g.diel)!=null?m:0,q,r=(q=g.sdo)!=null?q:!0,t=0,u,w=google.erd,x=w.jsr;google.ml=function(a,b,d,n,e){e=e===void 0?2:e;b&&(u=a&&a.message);d===void 0&&(d={});d.cad="ple_"+google.ple+".aple_"+google.aple;if(google.dl)return google.dl(a,e,d,!0),null;b=d;if(x<0){window.console&&console.error(a,b);if(x===-2)throw a;b=!1}else b=!a||!a.message||a.message==="Error loading script"||t>=l&&!n?!1:!0;if(!b)return null;t++;d=d||{};b=encodeURIComponent;var c="/gen_204?atyp=i&ei="+b(google.kEI);google.kEXPI&&(c+="&jexpid="+b(google.kEXPI));c+="&srcpg="+b(google.sn)+"&jsr="+b(w.jsr)+\n"&bver="+b(w.bv);w.dpf&&(c+="&dpf="+b(w.dpf));var f=a.lineNumber;f!==void 0&&(c+="&line="+f);var h=a.fileName;h&&(h.indexOf("-extension:/")>0&&(e=3),c+="&script="+b(h),f&&h===window.location.href&&(f=document.documentElement.outerHTML.split("\\n")[f],c+="&cad="+b(f?f.substring(0,300):"No script found.")));google.ple&&google.ple===1&&(e=2);c+="&jsel="+e;for(var v in d)c+="&",c+=b(v),c+="=",c+=b(d[v]);c=c+"&emsg="+b(a.name+": "+a.message);c=c+"&jsst="+b(a.stack||"N/A");c.length>=12288&&(c=c.substr(0,12288));a=c;n||google.log(0,"",a);return a};window.onerror=function(a,b,d,n,e){u!==a&&(a=e instanceof Error?e:Error(a),d===void 0||"lineNumber"in a||(a.lineNumber=d),b===void 0||"fileName"in a||(a.fileName=b),google.ml(a,!1,void 0,!1,a.name==="SyntaxError"||a.message.substring(0,11)==="SyntaxError"||a.message.indexOf("Script error")!==-1?3:p));u=null;r&&t>=l&&(window.onerror=null)};})();</script></head><body bgcolor="#fff"><script nonce="pJ2BM1u4uGddcyvZQjgA3Q">(function(){var src=\'/images/nav_logo229.png\';var iesg=false;document.body.onload = function(){window.n && window.n();if (document.images){new Image().src=src;}\nif (!iesg){document.f&&document.f.q.focus();document.gbqf&&document.gbqf.q.focus();}\n}\n})();</script><div id="mngb"><div id=gbar><nobr><b class=gb1>Search</b> <a class=gb1 href="https://www.google.com/imghp?hl=en&tab=wi">Images</a> <a class=gb1 href="https://maps.google.com/maps?hl=en&tab=wl">Maps</a> <a class=gb1 href="https://play.google.com/?hl=en&tab=w8">Play</a> <a class=gb1 href="https://www.youtube.com/?tab=w1">YouTube</a> <a class=gb1 href="https://news.google.com/?tab=wn">News</a> <a class=gb1 href="https://mail.google.com/mail/?tab=wm">Gmail</a> <a class=gb1 href="https://drive.google.com/?tab=wo">Drive</a> <a class=gb1 style="text-decoration:none" href="https://www.google.com/intl/en/about/products?tab=wh"><u>More</u> &raquo;</a></nobr></div><div id=guser width=100%><nobr><span id=gbn class=gbi></span><span id=gbf class=gbf></span><span id=gbe></span><a href="http://www.google.com/history/optout?hl=en" class=gb4>Web History</a> | <a  href="/preferences?hl=en" class=gb4>Settings</a> | <a target=_top id=gb_70 href="https://accounts.google.com/ServiceLogin?hl=en&passive=true&continue=https://www.google.com/&ec=GAZAAQ" class=gb4>Sign in</a></nobr></div><div class=gbh style=left:0></div><div class=gbh style=right:0></div></div><center><br clear="all" id="lgpd"><div id="XjhHGf"><img alt="Google" height="92" src="/images/branding/googlelogo/1x/googlelogo_white_background_color_272x92dp.png" style="padding:28px 0 14px" width="272" id="hplogo"><br><br></div><form action="/search" name="f"><table cellpadding="0" cellspacing="0"><tr valign="top"><td width="25%">&nbsp;</td><td align="center" nowrap=""><input name="ie" value="ISO-8859-1" type="hidden"><input value="en" name="hl" type="hidden"><input name="source" type="hidden" value="hp"><input name="biw" type="hidden"><input name="bih" type="hidden"><div class="ds" style="height:32px;margin:4px 0"><input class="lst" style="margin:0;padding:5px 8px 0 6px;vertical-align:top;color:#000" autocomplete="off" value="" title="Google Search" maxlength="2048" name="q" size="57"></div><br style="line-height:0"><span class="ds"><span class="lsbb"><input class="lsb" value="Google Search" name="btnG" type="submit"></span></span><span class="ds"><span class="lsbb"><input class="lsb" id="tsuid_S5LIZ5WPHN6ikPIP_Z3YaQ_1" value="I\'m Feeling Lucky" name="btnI" type="submit"><script nonce="pJ2BM1u4uGddcyvZQjgA3Q">(function(){var id=\'tsuid_S5LIZ5WPHN6ikPIP_Z3YaQ_1\';document.getElementById(id).onclick = function(){if (this.form.q.value){this.checked = 1;if (this.form.iflsig)this.form.iflsig.disabled = false;}\nelse top.location=\'/doodles/\';};})();</script><input value="ACkRmUkAAAAAZ8igWwyCRxXfZsKEGU8lcoi9xiJoN4Mo" name="iflsig" type="hidden"></span></span></td><td class="fl sblc" align="left" nowrap="" width="25%"><a href="/advanced_search?hl=en&amp;authuser=0">Advanced search</a></td></tr></table><input id="gbv" name="gbv" type="hidden" value="1"><script nonce="pJ2BM1u4uGddcyvZQjgA3Q">(function(){var a,b="1";if(document&&document.getElementById)if(typeof XMLHttpRequest!="undefined")b="2";else if(typeof ActiveXObject!="undefined"){var c,d,e=["MSXML2.XMLHTTP.6.0","MSXML2.XMLHTTP.3.0","MSXML2.XMLHTTP","Microsoft.XMLHTTP"];for(c=0;d=e[c++];)try{new ActiveXObject(d),b="2"}catch(h){}}a=b;if(a=="2"&&location.search.indexOf("&gbv=2")==-1){var f=google.gbvu,g=document.getElementById("gbv");g&&(g.value=a);f&&window.setTimeout(function(){location.href=f},0)};}).call(this);</script></form><div style="font-size:83%;min-height:3.5em"><br></div><span id="footer"><div style="font-size:10pt"><div style="margin:19px auto;text-align:center" id="WqQANb"><a href="/intl/en/ads/">Advertising</a><a href="/services/">Business Solutions</a><a href="/intl/en/about.html">About Google</a></div></div><p style="font-size:8pt;color:#70757a">&copy; 2025 - <a href="/intl/en/policies/privacy/">Privacy</a> - <a href="/intl/en/policies/terms/">Terms</a></p></span></center><script nonce="pJ2BM1u4uGddcyvZQjgA3Q">(function(){window.google.cdo={height:757,width:1440};(function(){var a=window.innerWidth,b=window.innerHeight;if(!a||!b){var c=window.document,d=c.compatMode=="CSS1Compat"?c.documentElement:c.body;a=d.clientWidth;b=d.clientHeight}if(a&&b&&(a!=google.cdo.width||b!=google.cdo.height)){var e=google,f=e.log,g="/client_204?&atyp=i&biw="+a+"&bih="+b+"&ei="+google.kEI,h="",k=window.google&&window.google.kOPI||null;k&&(h+="&opi="+k);f.call(e,"","",g+h)};}).call(this);})();</script>   <script nonce="pJ2BM1u4uGddcyvZQjgA3Q">(function(){google.xjs={basecomb:\'/xjs/_/js/k\\x3dxjs.hp.en.G8H7yvG16Fg.es5.O/ck\\x3dxjs.hp.H75EtcLUFR4.L.X.O/am\\x3dBAAAAAAQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAQBAAAAAAAAAAAHAAAYDYAAAAIABAgAAAAAAAAAAAAAABAAgAgAAACQAAAEN8RAAiARQAAeAE/d\\x3d1/ed\\x3d1/dg\\x3d0/ujg\\x3d1/rs\\x3dACT90oEI8aW5-cdYLjuuSRani-tbQvB_rg\',basecss:\'/xjs/_/ss/k\\x3dxjs.hp.H75EtcLUFR4.L.X.O/am\\x3dBAAAAAAQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAABAAAAAAAAAAAAAAAYAYAAAAIABAgAAAAAAAAAAAAAABAAgAgAAACQA/rs\\x3dACT90oF5hFG8engADMDzHlauM_xFJ4jSxQ\',basejs:\'/xjs/_/js/k\\x3dxjs.hp.en.G8H7yvG16Fg.es5.O/am\\x3dAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAQAAAAAAAAAAAAHAAAADAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAEN8RAAiARQAAeAE/dg\\x3d0/rs\\x3dACT90oH-4Sv687ft60vs2OqoSTUJzcP0wQ\',excm:[]};})();</script>        <script nonce="pJ2BM1u4uGddcyvZQjgA3Q">(function(){var u=\'/xjs/_/js/k\\x3dxjs.hp.en.G8H7yvG16Fg.es5.O/am\\x3dAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAQAAAAAAAAAAAAHAAAADAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAEN8RAAiARQAAeAE/d\\x3d1/ed\\x3d1/dg\\x3d3/rs\\x3dACT90oH-4Sv687ft60vs2OqoSTUJzcP0wQ/m\\x3dsb_he,d\';var st=1;var amd=1000;var mmd=0;var pod=true;var fp=\'\';\nvar e=this||self;function f(){var a,b,d;if(b=a=(b=window.google)==null?void 0:(d=b.ia)==null?void 0:d.r.B2Jtyd)b=a.m,b=b===1||b===5;return b&&a.cbfd!=null&&a.cbvi!=null?a:void 0};function g(){var a=[u];if(!google.dp){for(var b=0;b<a.length;b++){var d=a[b],c=document.createElement("link");c.as="script";c.href=d;c.rel="preload";document.body.appendChild(c)}google.dp=!0}};google.ps===void 0&&(google.ps=[]);function h(){var a=u,b=function(){};google.lx=google.stvsc?b:function(){k(a);google.lx=b};google.bx||google.lx()}function l(a,b){b&&(a.src=b);fp&&(a.fetchPriority=fp);var d=a.onload;a.onload=function(c){d&&d(c);google.ps=google.ps.filter(function(C){return a!==C})};google.ps.push(a);document.body.appendChild(a)}google.as=l;function k(a){google.timers&&google.timers.load&&google.tick&&google.tick("load","xjsls");var b=document.createElement("script");b.onerror=function(){google.ple=1};b.onload=function(){google.ple=0};google.xjsus=void 0;l(b,a);google.aple=-1;google.dp=!0};function m(a){var b=a.getAttribute("jscontroller");return(b==="UBXHI"||b==="R3fhkb"||b==="TSZEqd")&&a.hasAttribute("data-src")}function n(){for(var a=document.getElementsByTagName("img"),b=0,d=a.length;b<d;b++){var c=a[b];if(c.hasAttribute("data-lzy_")&&Number(c.getAttribute("data-atf"))&1&&!m(c))return!0}return!1}for(var p=document.getElementsByTagName("img"),q=0,r=p.length;q<r;++q){var t=p[q];Number(t.getAttribute("data-atf"))&1&&m(t)&&(t.src=t.getAttribute("data-src"))};var w,x,y,z,A,B;function D(){google.xjsu=u;e._F_jsUrl=u;A=function(){h()};w=!1;x=(st===1||st===3)&&!!google.caft&&!n();y=f();z=(st===2||st===3)&&!!y&&!n();B=pod}function E(){w||x||z||(A(),w=!0)}setTimeout(function(){google&&google.tick&&google.timers&&google.timers.load&&google.tick("load","xjspls");D();if(x||z){if(x){var a=function(){x=!1;E()};google.caft(a);window.setTimeout(a,amd)}z&&(a=function(){z=!1;E()},y.cbvi.push(a),window.setTimeout(a,mmd));B&&(w||g())}else A()},0);})();window._ = window._ || {};window._DumpException = _._DumpException = function(e){throw e;};window._s = window._s || {};_s._DumpException = _._DumpException;window._qs = window._qs || {};_qs._DumpException = _._DumpException;(function(){var t=[4,16384,0,0,0,0,0,67633152,4,524288,116736,671979572,524288,32832,128,0,37748736,32768,262176,74957824,92538880,98566145];window._F_toggles = window._xjs_toggles = t;})();window._F_installCss = window._F_installCss || function(css){};(function(){google.jl={bfl:0,dw:false,ine:false,ubm:false,uwp:true,vs:false};})();(function(){var pmc=\'{\\x22d\\x22:{},\\x22sb_he\\x22:{\\x22agen\\x22:false,\\x22cgen\\x22:false,\\x22client\\x22:\\x22heirloom-hp\\x22,\\x22dh\\x22:true,\\x22ds\\x22:\\x22\\x22,\\x22fl\\x22:true,\\x22host\\x22:\\x22google.com\\x22,\\x22jsonp\\x22:true,\\x22msgs\\x22:{\\x22cibl\\x22:\\x22Clear Search\\x22,\\x22dym\\x22:\\x22Did you mean:\\x22,\\x22lcky\\x22:\\x22I\\\\u0026#39;m Feeling Lucky\\x22,\\x22lml\\x22:\\x22Learn more\\x22,\\x22psrc\\x22:\\x22This search was removed from your \\\\u003Ca href\\x3d\\\\\\x22/history\\\\\\x22\\\\u003EWeb History\\\\u003C/a\\\\u003E\\x22,\\x22psrl\\x22:\\x22Remove\\x22,\\x22sbit\\x22:\\x22Search by image\\x22,\\x22srch\\x22:\\x22Google Search\\x22},\\x22ovr\\x22:{},\\x22pq\\x22:\\x22\\x22,\\x22rfs\\x22:[],\\x22stok\\x22:\\x229KDb1iLiglTGeLY6nbhj1MOl2vM\\x22}}\';google.pmc=JSON.parse(pmc);})();</script>       </body></html>'
#
# soup = bs(testcontent)
# soup.prettify()
#
#
# def _sort_content(data: Any) -> str:

import pb
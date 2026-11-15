"""Build NianRi's static, multilingual documentation. No external packages."""
from pathlib import Path
from html import escape
from urllib.parse import quote
import json,posixpath
root=Path(__file__).resolve().parents[1]
data=json.loads((root/'content/policy.json').read_text(encoding='utf-8'))
config=json.loads((root/'site-config.json').read_text(encoding='utf-8'))
assert config['publisher'] and '@' in config['email']
locales=data['locales']
ui={
'zh-Hans':{'eyebrow':'PRIVACY & CARE','skip':'跳至正文','toc':'本页内容','publisher':'发布者','updated':'最近更新','aside':'你的日期留在设备上。\n了解信息如何被处理，随时作出自己的选择。','note':'关于隐私仍有疑问？请通过支持邮箱联系我们。无需提供完整日期备份或敏感账户资料。','top':'返回顶部 ↑','homeTitle':'关于你的数据，\n我们说清楚。','homeBody':'这里是念日的隐私与支持中心。了解你的日子如何保存、提醒如何工作，以及需要帮助时如何联系开发者。','privacyBody':'从本地记录到 Apple 购买，清楚说明信息的使用、保存与删除。','supportBody':'查找提醒、购买恢复与备份的常见问题，或直接联系开发者。','facts':['无需应用账号','没有广告分析脚本','三种语言，清晰阅读'],'copy':'复制邮箱地址','copied':'邮箱地址已复制','failed':'暂时无法复制，请选中上方邮箱地址复制。','language':'语言','notFound':'这个页面暂时找不到','back':'返回隐私与支持中心','refund':'在 Apple 查看订单或申请退款'},
'zh-Hant':{'eyebrow':'PRIVACY & CARE','skip':'跳至內文','toc':'本頁內容','publisher':'發布者','updated':'最近更新','aside':'你的日期留在裝置上。\n了解資訊如何被處理，隨時作出自己的選擇。','note':'對隱私仍有疑問？請透過支援信箱聯絡我們。無需提供完整日期備份或敏感帳號資料。','top':'返回頂端 ↑','homeTitle':'關於你的資料，\n我們說清楚。','homeBody':'這裡是念日的隱私與支援中心。了解你的日子如何儲存、提醒如何運作，以及需要協助時如何聯絡開發者。','privacyBody':'從本機紀錄到 Apple 購買，清楚說明資訊的使用、保存與刪除。','supportBody':'查找提醒、恢復購買與備份的常見問題，或直接聯絡開發者。','facts':['無需應用程式帳號','沒有廣告分析指令碼','三種語言，清楚閱讀'],'copy':'複製信箱地址','copied':'信箱地址已複製','failed':'暫時無法複製，請選取上方信箱地址複製。','language':'語言','notFound':'暫時找不到這個頁面','back':'返回隱私與支援中心','refund':'在 Apple 查看訂單或申請退款'},
'en':{'eyebrow':'PRIVACY & CARE','skip':'Skip to content','toc':'ON THIS PAGE','publisher':'Publisher','updated':'Last updated','aside':'Your dates stay on your device.\nUnderstand how information is handled, and choose what works for you.','note':'Still have a privacy question? Contact us by email. You do not need to share a full date backup or sensitive account details.','top':'Back to top ↑','homeTitle':'Your data.\nClearly explained.','homeBody':'Welcome to DayMemo’s privacy and support centre. Learn how your dates are stored, how reminders work, and how to get help.','privacyBody':'From local records to Apple purchases: how information is used, kept and deleted.','supportBody':'Find answers about reminders, restoring purchases and backups, or contact the developer.','facts':['No app account required','No advertising or analytics scripts','Clear reading in three languages'],'copy':'Copy email address','copied':'Email address copied','failed':'Could not copy. Please select and copy the email address above.','language':'Language','notFound':'This page could not be found','back':'Back to privacy and support','refund':'View purchases or request a refund with Apple'}
}
prefixes={'zh-Hans':'','zh-Hant':'zh-Hant/','en':'en/'}
apple='https://www.apple.com/legal/internet-services/itunes/dev/stdeula/'
github='https://docs.github.com/en/site-policy/privacy-policies/github-general-privacy-statement'
mark='<svg class="brand-icon" viewBox="0 0 48 48" fill="none" aria-hidden="true"><rect x="2" y="2" width="44" height="44" rx="13" fill="currentColor" opacity=".09"/><rect x="12" y="12" width="24" height="26" rx="6" stroke="currentColor" stroke-width="1.6"/><path d="M12 21h24M18 9v7M30 9v7M24 32s-6-3.3-6-6a3.2 3.2 0 0 1 6-1.5 3.2 3.2 0 0 1 6 1.5c0 2.7-6 6-6 6Z" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/></svg>'
shield='<svg viewBox="0 0 24 24" fill="none" aria-hidden="true"><path d="m12 3 8 3v6c0 5-8 9-8 9s-8-4-8-9V6l8-3Z" stroke="currentColor" stroke-width="1.5"/><path d="m8 12 3 3 5-6" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></svg>'
def text(value):
 return escape(str(value).replace('{{publisher}}',config['publisher']).replace('{{email}}',config['email']))
def target(code,page):return prefixes[code]+(page+'/' if page else '')
def rel(current,dest):
 value=posixpath.relpath(dest or '.',current or '.')
 return './' if value=='.' else value+'/'
def page(code,kind):
 L=locales[code];U=ui[code];current=target(code,kind)
 url=config['siteURL']+'/'+current
 css=rel(current,'assets')+'site.css'
 js=rel(current,'assets')+'site.js'
 icon=rel(current,'assets')+'mark.svg'
 nav=''.join('<a href="'+rel(current,target(code,k))+'"'+(' aria-current="page"' if kind==k else '')+'>'+text(L['nav'][k])+'</a>' for k in ['privacy','support'])
 languages=''.join('<a href="'+rel(current,target(c,kind))+'" lang="'+c+'" hreflang="'+c+'"'+(' aria-current="true"' if c==code else '')+'>'+text(v['languageName'])+'</a>' for c,v in locales.items())
 head='<header class="site-header"><div class="shell header-inner"><a class="brand" href="'+rel(current,target(code,''))+'" aria-label="'+text(L['siteTitle'])+'">'+mark+'<span><span class="brand-name">'+text(L['appName'])+'</span><span class="brand-caption">DATES THAT MATTER</span></span></a><nav class="primary-nav" aria-label="'+text(L['siteTitle'])+'">'+nav+'</nav><details class="language"><summary aria-label="'+text(U['language'])+'">'+text(L['languageName'])+'</summary><nav class="language-menu" aria-label="'+text(U['language'])+'">'+languages+'</nav></details></div></header>'
 mail='mailto:'+config['email']+'?subject='+quote(L['appName']+' · '+L['support']['title'])
 footer='<footer class="site-footer"><div class="shell footer-inner"><div><div class="footer-title">'+text(L['appName'])+'</div>'+text(L['tagline'])+'<br>© '+text(config['publisher'])+'</div><nav class="footer-links" aria-label="'+text(L['siteTitle'])+'"><a href="'+rel(current,target(code,'privacy'))+'">'+text(L['nav']['privacy'])+'</a><a href="'+rel(current,target(code,'support'))+'">'+text(L['nav']['support'])+'</a><a href="'+mail+'">'+text(config['email'])+'</a><a href="'+apple+'">'+text(L['footer']['terms'])+'</a><a href="'+github+'">'+text(L['footer']['githubPrivacy'])+'</a></nav></div></footer>'
 if kind=='privacy':
  P=L['privacy'];title=P['title'];description=P['intro']
  toc='<aside class="toc" aria-label="'+text(U['toc'])+'"><p class="toc-title">'+text(U['toc'])+'</p><ol>'+''.join('<li><a href="#'+s['id']+'">'+text(s['title'])+'</a></li>' for s in P['sections'])+'</ol><p class="aside-note">'+text(U['aside'])+'</p></aside>'
  article=''.join('<section class="policy-section" id="'+s['id']+'"><div class="section-heading"><span class="section-number" aria-hidden="true">'+f'{i:02}'+'</span><h2>'+text(s['title'])+'</h2></div>'+''.join('<p>'+text(p)+'</p>' for p in s['paragraphs'])+'</section>' for i,s in enumerate(P['sections'],1))
  article+='<div class="callout">'+shield+'<p>'+text(U['note'])+' <a href="'+mail+'">'+text(config['email'])+'</a></p></div><a class="top-link" href="#top">'+text(U['top'])+'</a>'
  content='<div class="hero"><p class="eyebrow">'+U['eyebrow']+'</p><h1>'+text(title)+'</h1><p class="lede">'+text(description)+'</p><div class="meta"><span>'+text(U['updated'])+'<b><time datetime="'+config['updated']+'">'+config['updated']+'</time></b></span><span>'+text(U['publisher'])+'<b>'+text(config['publisher'])+'</b></span></div></div><div class="reading-layout">'+toc+'<article>'+article+'</article></div>'
 elif kind=='support':
  P=L['support'];title=P['title'];description=P['intro']
  faqs='<p class="faq-intro">'+text(P['faqTitle'])+'</p>'+''.join('<details class="faq-item"'+(' open' if i==0 else '')+' id="'+f['id']+'"><summary>'+text(f['question'])+'</summary><p>'+text(f['answer'])+'</p></details>' for i,f in enumerate(P['faqs']))
  notes='<div class="support-notes"><h2>'+text(P['includeTitle'])+'</h2><ul class="contact-list">'+''.join('<li>'+text(i)+'</li>' for i in P['includeItems'])+'</ul><p class="small">'+text(P['sensitiveWarning'])+'</p></div>'
  contact='<aside class="contact-card"><div class="contact-kicker">HERE TO HELP</div><h2>'+text(P['contactTitle'])+'</h2><p>'+text(P['contactBody'])+'</p><a class="email-address" href="'+mail+'">'+text(config['email'])+'</a><a class="button" href="'+mail+'">'+text(P['emailLabel'])+' <span aria-hidden="true">↗</span></a><button class="copy-button" hidden data-copy="'+text(config['email'])+'" data-success="'+text(U['copied'])+'" data-failure="'+text(U['failed'])+'">'+text(U['copy'])+'</button><p class="live-status" aria-live="polite"></p></aside>'
  content='<div class="hero"><p class="eyebrow">'+U['eyebrow']+'</p><h1>'+text(title)+'</h1><p class="lede">'+text(description)+'</p></div><div class="support-layout"><div>'+faqs+notes+'<a class="top-link" href="https://reportaproblem.apple.com/">'+text(U['refund'])+' ↗</a></div>'+contact+'</div>'
 else:
  title=L['siteTitle'];description=U['homeBody']
  content='<section class="home-hero"><div><p class="eyebrow">'+U['eyebrow']+'</p><h1>'+text(U['homeTitle'])+'</h1><p class="lede">'+text(description)+'</p></div><div class="home-emblem" aria-hidden="true">'+mark+'</div></section><div class="home-options">'+''.join('<a class="link-panel" href="'+rel(current,target(code,k))+'"><h2>'+text(L['nav'][k])+'<span aria-hidden="true">↗</span></h2><p>'+text(U[k+'Body'])+'</p></a>' for k in ['privacy','support'])+'</div><div class="home-facts">'+''.join('<span>'+text(f)+'</span>' for f in U['facts'])+'</div>'
 alternates=''.join('<link rel="alternate" hreflang="'+c+'" href="'+config['siteURL']+'/'+target(c,kind)+'">' for c in locales)
 html='<!doctype html><html lang="'+code+'"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="color-scheme" content="light dark"><meta name="referrer" content="no-referrer"><meta http-equiv="Content-Security-Policy" content="default-src \'none\'; style-src \'self\'; script-src \'self\'; img-src \'self\' data:; connect-src \'none\'; base-uri \'self\'; form-action \'none\'"><title>'+text(title)+' · '+text(L['appName'])+'</title><meta name="description" content="'+text(description)+'"><meta property="og:title" content="'+text(title)+' · '+text(L['appName'])+'"><meta property="og:description" content="'+text(description)+'"><meta property="og:type" content="website"><meta property="og:url" content="'+url+'"><link rel="canonical" href="'+url+'">'+alternates+'<link rel="icon" href="'+icon+'" type="image/svg+xml"><link rel="stylesheet" href="'+css+'"><script src="'+js+'" defer></script></head><body id="top"><a class="skip" href="#main">'+text(U['skip'])+'</a>'+head+'<main class="shell" id="main">'+content+'</main>'+footer+'</body></html>'
 path=root/'docs'/current/'index.html';path.parent.mkdir(parents=True,exist_ok=True);path.write_text(html,encoding='utf-8')
for code in locales:
 for kind in ['', 'privacy','support']:page(code,kind)
mark=mark.replace('class="brand-icon"','xmlns="http://www.w3.org/2000/svg"').replace('currentColor','#315b46')
(root/'docs/assets/mark.svg').write_text(mark,encoding='utf-8')
# A static, multilingual return link works even without JavaScript on unknown routes.
(root/'docs/404.html').write_text('<!doctype html><html lang="zh-Hans"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>页面未找到 · 念日</title><body><main><h1>这个页面暂时找不到 / Page not found</h1><p><a href="'+config['siteURL']+'/">返回念日隐私与支持中心 · Back to privacy and support</a></p></main></body></html>',encoding='utf-8')
urls=[config['siteURL']+'/'+target(c,k) for c in locales for k in ['','privacy','support']]
(root/'docs/sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'+''.join('<url><loc>'+u+'</loc><lastmod>'+config['updated']+'</lastmod></url>' for u in urls)+'</urlset>',encoding='utf-8')
print(json.dumps({'pages':9,'languages':list(locales),'publisher':config['publisher'],'site':config['siteURL']},ensure_ascii=False))

if (typeof $WH == "undefined") { $WH = { wowheadRemote: !0 };
var g_host = "https://base.opiums.eu";
var g_staticUrl = "https://base.opiums.eu/static"; }
if (typeof $WowheadPower == "undefined") {
    var $WowheadPower = new function () {
        var isRemote = $WH.wowheadRemote; var opt = { applyto: 3 }, head = document.getElementsByTagName("head")[0], whcss, currentType, currentId, currentLocale, currentDomain, currentParams, currentA, cursorX, cursorY, mode = 0, eventAttached = !1, npcs = {}, objects = {}, items = {}, quests = {}, spells = {}, achievements = {}, holidays = {}, itemsets = {}, currencies = {}, profiles = {}, showLogo = 1, STATUS_NONE = 0, STATUS_QUERYING = 1, STATUS_ERROR = 2, STATUS_NOTFOUND = 3, STATUS_OK = 4, STATUS_SCALES = 5, SCALES_NONE = 0, SCALES_LOADED = 1, SCALES_QUERYING = 2, TYPE_NPC = 1, TYPE_OBJECT = 2, TYPE_ITEM = 3, TYPE_ITEMSET = 4, TYPE_QUEST = 5, TYPE_SPELL = 6, TYPE_ACHIEVEMENT = 10, TYPE_HOLIDAY = 12, TYPE_CURRENCY = 17, TYPE_PROFILE = 100, CURSOR_HSPACE = 15, CURSOR_VSPACE = 15, _LANG = { loading: "Loading...", noresponse: "<img alt=\"No response from server :(\" src=\"data:image/gif;base64,R0lGODlhFAAUAPMIAIeHhz8/P1dXVycnJ8/Pz7e3t5+fn29vb////wAAAAAAAAAAAAAAAAAAAAAAAAAAACH/C05FVFNDQVBFMi4wAwEAAAAh+QQFBwAIACwAAAAAFAAUAEAEUxDJSatFxtwaggWAdIyHJAhXoRYSQUhDPGx0TbmujahbXGWZWqdDAYEsp5NupLPkdDwE7oXwWVasimzWrAE1tKFHErQRK8eL8mMUlRBJVI307uoiACH5BAUHAAgALAEAAQASABIAAAROEMkpS6E4W5upMdUmEQT2feFIltMJYivbvhnZ3R0A4NMwIDodz+cL7nDEn5CH8DGZh8MtEMBEoxkqlXKVIgQCibbK9YLBYvLtHH5K0J0IACH5BAUHAAgALAEAAQASABIAAAROEMkpjaE4W5spANUmFQX2feFIltMJYivbvhnZ3d1x4BNBIDodz+cL7nDEn5CH8DGZAsFtMMBEoxkqlXKVIgIBibbK9YLBYvLtHH5K0J0IACH5BAUHAAgALAEAAQASABIAAAROEMkpAaA4W5vpOdUmGQb2feFIltMJYivbvhnZ3Z0g4FNRIDodz+cL7nDEn5CH8DGZgcCNQMBEoxkqlXKVIgYDibbK9YLBYvLtHH5K0J0IACH5BAUHAAgALAEAAQASABIAAAROEMkpz6E4W5upENUmAQD2feFIltMJYivbvhnZ3V0Q4JNhIDodz+cL7nDEn5CH8DGZg8GtUMBEoxkqlXKVIggEibbK9YLBYvLtHH5K0J0IACH5BAUHAAgALAEAAQASABIAAAROEMkphaA4W5tpCNUmHQf2feFIltMJYivbvhnZ3d0w4BMAIDodz+cL7nDEn5CH8DGZBMLNYMBEoxkqlXKVIgoFibbK9YLBYvLtHH5K0J0IACH5BAUHAAgALAEAAQASABIAAAROEMkpQ6A4W5vpGNUmCQL2feFIltMJYivbvhnZ3R1B4NNxIDodz+cL7nDEn5CH8DGZhcINAMBEoxkqlXKVIgwGibbK9YLBYvLtHH5K0J0IACH5BAUHAAcALAEAAQASABIAAANCeLo6wzA6FxkhbaoQ4L3ZxnXLh0EjWZ4RV71VUcCLIByyTNt2PsO8m452sBGJBsNxkUwuD03lAQBASqnUJ7aq5UYSADs=\" />", achievementcomplete: "Achievement earned by $1 on $2/$3/$4" }, LOOKUPS = { 1: [npcs, "npc", "NPC"], 2: [objects, "object", "Object"], 3: [items, "item", "Item"], 4: [itemsets, "itemset", "Item Set"], 5: [quests, "quest", "Quest"], 6: [spells, "spell", "Spell"], 10: [achievements, "achievement", "Achievement"], 12: [holidays, "event", "Holiday"], 17: [currencies, "currency", "Currency"], 100: [profiles, "profile", "Profile"] }, SCALES = { 3: { url: "?data=item-scaling" }, 6: { url: "?data=item-scaling" } }, LOCALES = { 0: "enus", 2: "frfr", 3: "dede", 4: "zhcn", 6: "eses", 8: "ruru" }, REDIRECTS = { wotlk: "www", ptr: "www", www: "ru" }; if (isRemote) { var Locale = { getId: function () { return 8 }, getName: function () { return "ruru" } } }
        function init() {
            if (isRemote) { var script = document.createElement("script"); script.src = g_staticUrl + "/js/basic.js"; head.appendChild(script) } else { attachEvent() }
            for (var type in SCALES) { for (var localeId in LOCALES) { SCALES[type][localeId] = SCALES_NONE } }
        }
        function initCSS() {
            if (typeof aowow_tooltips == "undefined") { return }
            if (!("hide" in aowow_tooltips)) { return }
            if (typeof whcss != "undefined") { return }
            if (!document.styleSheets) { return }
            var style = document.createElement("style"); style.type = "text/css"; head.appendChild(style); if (!window.createPopup) { head.appendChild(document.createTextNode("")) }
            whcss = document.styleSheets[document.styleSheets.length - 1]; for (var k in aowow_tooltips.hide) {
                if (!aowow_tooltips.hide[k]) { continue }
                if (whcss.insertRule) { whcss.insertRule(".wowhead-tooltip .whtt-" + k + "{display : none}", whcss.cssRules.length) } else if (whcss.addRule) { whcss.addRule(".wowhead-tooltip .whtt-" + k, "display : none", -1) }
            }
        }
        function attachEvent() {
            if (eventAttached) { return }
            eventAttached = !0; $WH.aE(document, "mouseover", onMouseOver)
        }
        function onDOMReady(func) {
            if (typeof jQuery != "undefined") { jQuery(func); return }
            /in/.test(document.readyState) ? setTimeout(onDOMReady.bind(null, func), 9) : func()
        }
        this.init = function () {
            if (isRemote) { $WH.ae(head, $WH.ce("link", { type: "text/css", href: g_staticUrl + "/css/basic.css", rel: "stylesheet" })) }
            attachEvent(); onDOMReady(function () {
                if (typeof aowow_tooltips != "undefined") {
                    for (var i = 0; i < document.links.length; i++) { var link = document.links[i]; scanElement(link) }
                    initCSS()
                }
            })
        }; function updateCursorPos(e) { var pos = $WH.g_getCursorPos(e); cursorX = pos.x; cursorY = pos.y }
        function scanElement(t, e) {
            if (t.nodeName != "A" && t.nodeName != "AREA") { return -2323 }
            var rel = t.rel; try { if (t.dataset && t.dataset.hasOwnProperty("wowhead")) { rel = t.dataset.wowhead } else if (t.getAttribute && t.getAttribute("data-wowhead")) { rel = t.getAttribute("data-wowhead") } } catch (e) { void (0) }
            if (!t.href.length && !rel) { return }
            if (rel && /^np\b/.test(rel)) { return }
            if (t.getAttribute("data-disable-wowhead-tooltip") == "true") { return }
            var i0, i1, i2, url, params = {}; currentParams = params; var p = function (url, k, v) { if (k == "buff" || k == "sock" || k == "map") { params[k] = !0 } else if (k == "rand" || k == "ench" || k == "lvl" || k == "c") { params[k] = parseInt(v) } else if (k == "gems" || k == "pcs" || k == "know" || k == "cri") { params[k] = v.split(":") } else if (k == "who" || k == "domain") { params[k] = v } else if (k == "when") { params[k] = new Date(parseInt(v)) } else if (k == "premium") { params[k] = !0 } else if (k == "text") { params[k] = !0 } }; if (opt.applyto & 1) {
                i1 = 2; i2 = 3; if (t.href.indexOf("http://") == 0 || t.href.indexOf("https://") == 0) {
                    i0 = 1; url = t.href.match(/^https?:\/\/(.*)\/?\??(item|quest|spell|achievement|event|npc|object|itemset|currency)=(-?[0-9]+)/); if (url == null) { url = t.href.match(/^https?:\/\/(.*)\/?\??(profile)=([^&#]+)/) }
                    showLogo = 0
                } else {
                    url = t.href.match(/()\?(item|quest|spell|achievement|event|npc|object|itemset|currency)=(-?[0-9]+)/); if (url == null) { url = t.href.match(/()\?(profile)=([^&#]+)/) }
                    showLogo = 1
                }
            }
            if (url == null && rel && (opt.applyto & 2)) { i0 = 0; i1 = 1; i2 = 2; url = rel.match(/(item|quest|spell|achievement|event|npc|object|itemset|currency).?(-?[0-9]+)/); showLogo = 1 }
            t.href.replace(/([a-zA-Z]+)=?([a-zA-Z0-9:-]*)/g, p); if (rel) { rel.replace(/([a-zA-Z]+)=?([a-zA-Z0-9:-]*)/g, p) }
            if (params.gems && params.gems.length > 0) {
                var i; for (i = Math.min(3, params.gems.length - 1); i >= 0; --i) { if (parseInt(params.gems[i])) { break } }
                ++i; if (i == 0) { delete params.gems } else if (i < params.gems.length) { params.gems = params.gems.slice(0, i) }
            }
            if (url) {
                var
                locale, domain = "www"; currentA = t; if (params.domain) { domain = params.domain } else if (i0 && url[i0]) { domain = url[i0].split(".")[0] }
                if (REDIRECTS[domain]) { domain = REDIRECTS[domain] }
                locale = $WH.g_getLocaleFromDomain(domain); if ($WH.in_array(['fr', 'de', 'cn', 'es', 'ru', 'en'], domain) == -1) {
                    for (i in document.scripts) {
                        if (!document.scripts[i].src)
                            continue; var dmn = document.scripts[i].src.match(/widgets\/power.js\?(lang|locale)=(en|fr|de|cn|es|ru)/i); if (dmn) { domain = dmn[2]; locale = $WH.g_getLocaleFromDomain(dmn[2]); break }
                    }
                }
                currentDomain = domain; if (t.href.indexOf("#") != -1 && document.location.href.indexOf(url[i1] + "=" + url[i2]) != -1) { return }
                mode = t.parentNode.className.indexOf("icon") == 0 && t.parentNode.nodeName == "DIV" ? 1 : 0; if (!t.onmouseout) {
                    if (mode == 0) { t.onmousemove = onMouseMove }
                    t.onmouseout = onMouseOut
                }
                if (e) { updateCursorPos(e) }
                var type = $WH.g_getIdFromTypeName(url[i1]), typeId = url[i2]; display(type, typeId, locale, params); if (e || typeof aowow_tooltips == "undefined") { return }
                var data = LOOKUPS[type][0][getFullId(typeId, params)]; var timeout = function (t) {
                    if (data.status[locale] != STATUS_OK && data.status[locale] != STATUS_NOTFOUND) { window.setTimeout(function () { timeout(t) }, 5); return }
                    if (aowow_tooltips.renamelinks) { eval("name = data.name_" + LOCALES[locale]); if (name) { t.innerHTML = '<span>' + name + '</span>' } }
                    if (aowow_tooltips.iconizelinks && (type == TYPE_ITEM || type == TYPE_ACHIEVEMENT || type == TYPE_SPELL) && data.icon) { t.className += " icontinyl"; t.setAttribute("style", t.getAttribute("style") + "; padding-left:18px !important;"); t.style.verticalAlign = "center"; t.style.background = "url(" + g_staticUrl + "/images/wow/icons/tiny/" + data.icon.toLocaleLowerCase() + ".gif) left center no-repeat" }
                    if (aowow_tooltips.colorlinks) { if (type == TYPE_ITEM) { t.className += " q" + data.quality } }
                }; timeout(t)
            }
        }
        function onMouseOver(e) { e = $WH.$E(e); var t = e._target; var i = 0; while (t != null && i < 5 && scanElement(t, e) == -2323) { t = t.parentNode; ++i } }
        function onMouseMove(e) { e = $WH.$E(e); updateCursorPos(e); $WH.Tooltip.move(cursorX, cursorY, 0, 0, CURSOR_HSPACE, CURSOR_VSPACE) }
        function onMouseOut() { currentType = null; currentA = null; $WH.Tooltip.hide() }
        function getTooltipField(locale, n) {
            var prefix = "tooltip"; if (currentParams && currentParams.buff) { prefix = "buff" }
            if (currentParams && currentParams.text) { prefix = "text" }
            if (currentParams && currentParams.premium) { prefix = "tooltip_premium" }
            return prefix + (n ? n : "") + "_" + LOCALES[locale]
        }
        function getIconField() { return (currentParams && currentParams.text) ? "text_icon" : "icon" }
        function getSpellsField(locale) { return (currentParams && currentParams.buff ? "buff" : "") + "spells_" + LOCALES[locale] }
        function initElement(type, id, locale) {
            var arr = LOOKUPS[type][0]; if (arr[id] == null) { arr[id] = {} }
            if (arr[id].status == null) { arr[id].status = {} }
            if (arr[id].response == null) { arr[id].response = {} }
            if (arr[id].status[locale] == null) { arr[id].status[locale] = STATUS_NONE }
        }
        function display(type, id, locale, params) {
            if (!params) { params = {} }
            var fullId = getFullId(id, params); currentType = type; currentId = fullId; currentLocale = locale; currentParams = params; initElement(type, fullId, locale); var arr = LOOKUPS[type][0]; if (arr[fullId].status[locale] == STATUS_OK || arr[fullId].status[locale] == STATUS_NOTFOUND) { showTooltip(arr[fullId][getTooltipField(locale)], arr[fullId][getIconField()], arr[fullId].map, arr[fullId][getSpellsField(locale)], arr[fullId][getTooltipField(locale, 2)]) } else if (arr[fullId].status[locale] == STATUS_QUERYING || arr[fullId].status[locale] == STATUS_SCALES) { showTooltip(_LANG.loading) } else { request(type, id, locale, null, params) }
        }
        function request(type, id, locale, stealth, params) {
            var fullId = getFullId(id, params); var arr = LOOKUPS[type][0]; if (arr[fullId].status[locale] != STATUS_NONE && arr[fullId].status[locale] != STATUS_ERROR) { return }
            arr[fullId].status[locale] = STATUS_QUERYING; if (!stealth) { arr[fullId].timer = setTimeout(function () { showLoading.apply(this, [type, fullId, locale]) }, 333) }
            var p = ""; for (var i in params) {
                if (i != "rand" && i != "ench" && i != "gems" && i != "sock" && i != "lvl") { continue }
                if (typeof params[i] == "object") { p += "&" + i + "=" + params[i].join(":") } else if (params[i] === !0) { p += "&" + i } else { p += "&" + i + "=" + params[i] }
            }
            var localeDomain = $WH.g_getDomainFromLocale(locale), url = g_host + "/"; $WH.g_ajaxIshRequest(url + "?" + LOOKUPS[type][1] + "=" + id + "&domain=" + localeDomain + "&power" + p); if (SCALES[type] && SCALES[type][locale] == SCALES_NONE) { $WH.g_ajaxIshRequest(url + SCALES[type].url); SCALES[type][locale] = SCALES_QUERYING }
        }
        function showTooltip(html, icon, map, spellData, html2) {
            if (currentA && currentA._fixTooltip) { html = currentA._fixTooltip(html, currentType, currentId, currentA) }
            initCSS(); var notFound = !1; if (!html) { html = LOOKUPS[currentType][2] + " not found :("; icon = "inv_misc_questionmark"; notFound = !0 } else {
                if (currentParams != null) {
                    if (currentParams.pcs && currentParams.pcs.length) {
                        var n = 0; for (var i = 0, len = currentParams.pcs.length; i < len; ++i) { var m; if (m = html.match(new RegExp("<span><!--si([0-9]+:)*" + currentParams.pcs[i] + '(:[0-9]+)*--><a href="\\?item=(\\d+)">(.+?)</a></span>'))) { html = html.replace(m[0], '<span class="q8"><!--si' + currentParams.pcs[i] + '--><a href="?item=' + m[3] + '">' + (($WH.isset("g_items") && g_items[currentParams.pcs[i]]) ? g_items[currentParams.pcs[i]]["name_" + LOCALES[currentLocale]] : m[4]) + "</a></span>"); ++n } }
                        if (n > 0) { html = html.replace("(0/", "(" + n + "/"); html = html.replace(new RegExp("<span>\\(([0-" + n + "])\\)", "g"), '<span class="q2">($1)') }
                    }
                    if (currentParams.c) { html = html.replace(/<span class="c([0-9]+?)">(.+?)<\/span><br \/>/g, '<span class="c$1" style="display: none">$2</span>'); html = html.replace(new RegExp('<span class="c(' + currentParams.c + ')" style="display: none">(.+?)</span>', "g"), '<span class="c$1">$2</span><br />') }
                    if (currentParams.know && currentParams.know.length) { html = $WH.g_setTooltipSpells(html, currentParams.know, spellData) }
                    if (currentParams.lvl) { html = $WH.g_setTooltipLevel(html, currentParams.lvl, currentParams.buff) } else if ($WH.gc('compare_level') && window.location.href.match(/\?compare/i)) { html = $WH.g_setTooltipLevel(html, $WH.gc('compare_level'), currentParams.buff) }
                    if (currentParams.who && currentParams.when) { html = html.replace("<table><tr><td><br />", '<table><tr><td><br /><span class="q2">' + $WH.sprintf(_LANG.achievementcomplete, currentParams.who, currentParams.when.getMonth() + 1, currentParams.when.getDate(), currentParams.when.getFullYear()) + "</span><br /><br />"); html = html.replace(/class="q0"/g, 'class="r3"') }
                    if ((currentType == TYPE_ACHIEVEMENT) && currentParams.cri) { for (var i = 0; i < currentParams.cri.length; i++) { html = html.replace(new RegExp("<!--cr" + parseInt(currentParams.cri[i]) + ":[^<]+", "g"), '<span class="q2">$&</span>') } }
                }
            }
            if (currentParams.map && map && map.getMap) { html2 = map.getMap() }
            if (mode == 1) { $WH.Tooltip.setIcon(null); $WH.Tooltip.show(currentA, html, null, null, null, html2) } else { $WH.Tooltip.setIcon(icon); $WH.Tooltip.showAtXY(html, cursorX, cursorY, CURSOR_HSPACE, CURSOR_VSPACE, html2) }
            if (isRemote && $WH.Tooltip.logo) { $WH.Tooltip.logo.style.display = (showLogo ? "block" : "none") }
        }
        function showLoading(type, id, locale) { if (currentType == type && currentId == id && currentLocale == locale) { showTooltip(_LANG.loading); var arr = LOOKUPS[type][0]; arr[id].timer = setTimeout(function () { notFound.apply(this, [type, id, locale]) }, 3850) } }
        function notFound(type, id, locale) { var arr = LOOKUPS[type][0]; arr[id].status[locale] = STATUS_ERROR; if (currentType == type && currentId == id && currentLocale == locale) { showTooltip(_LANG.noresponse) } }
        function getFullId(id, params) { return id + (params.rand ? "r" + params.rand : "") + (params.ench ? "e" + params.ench : "") + (params.gems ? "g" + params.gems.join(",") : "") + (params.sock ? "s" : "") }
        this.loadScales = function (type, locale) { var arr = LOOKUPS[type][0]; for (var i in LOCALES) { if (locale == i || (!locale && !isNaN(i))) { SCALES[type][i] = SCALES_LOADED; for (var id in arr) { if (arr[id].status[i] == STATUS_SCALES && arr[id].response[i]) { arr[id].response[i]() } } } } }; this.register = function (type, id, locale, json) {
            var arr = LOOKUPS[type][0]; initElement(type, id, locale); if (SCALES[type] && SCALES[type][locale] != SCALES_LOADED) { arr[id].status[locale] = STATUS_SCALES; arr[id].response[locale] = this.register.bind(this, type, id, locale, json); return }
            if (arr[id].timer) { clearTimeout(arr[id].timer); arr[id].timer = null }
            if (!$WH.wowheadRemote && !$.isEmptyObject(json.map)) {
                if (arr[id].map == null) { arr[id].map = new Mapper({ parent: $WH.ce("div"), zoom: 3, zoomable: !1, buttons: !1 }, !0) }
                arr[id].map.update(json.map, !0); delete json.map
            }
            $WH.cO(arr[id], json); if (arr[id].status[locale] == STATUS_QUERYING || arr[id].status[locale] == STATUS_SCALES) { if (arr[id][getTooltipField(locale)]) { arr[id].status[locale] = STATUS_OK } else { arr[id].status[locale] = STATUS_NOTFOUND } }
            if (currentType == type && id == currentId && currentLocale == locale) { showTooltip(arr[id][getTooltipField(locale)], arr[id].icon, arr[id].map, arr[id][getSpellsField(locale)], arr[id][getTooltipField(locale, 2)]) }
        }; this.registerNpc = function (id, locale, json) { this.register(TYPE_NPC, id, locale, json) }; this.registerCurrency = function (id, locale, json) { this.register(TYPE_CURRENCY, id, locale, json) }; this.registerObject = function (id, locale, json) { this.register(TYPE_OBJECT, id, locale, json) }; this.registerItem = function (id, locale, json) { this.register(TYPE_ITEM, id, locale, json) }; this.registerHoliday = function (id, locale, json) { this.register(TYPE_HOLIDAY, id, locale, json) }; this.registerItemSet = function (id, locale, json) { this.register(TYPE_ITEMSET, id, locale, json) }; this.registerQuest = function (id, locale, json) { this.register(TYPE_QUEST, id, locale, json) }; this.registerSpell = function (id, locale, json) { this.register(TYPE_SPELL, id, locale, json) }; this.registerAchievement = function (id, locale, json) { this.register(TYPE_ACHIEVEMENT, id, locale, json) }; this.registerProfile = function (id, locale, json) { this.register(TYPE_PROFILE, id, locale, json) }; this.displayTooltip = function (type, id, locale, params) { display(type, id, locale, params) }; this.request = function (type, id, locale, params) {
            if (!params) { params = {} }
            var fullId = getFullId(id, params); initElement(type, fullId, locale); request(type, id, locale, 1, params)
        }; this.requestItem = function (id, params) { this.request(TYPE_ITEM, id, Locale.getId(), params) }; this.requestSpell = function (id) { this.request(TYPE_SPELL, id, Locale.getId()) }; this.getStatus = function (type, id, locale) { var arr = LOOKUPS[type][0]; if (arr[id] != null) { return arr[id].status[locale] } else { return STATUS_NONE } }; this.getItemStatus = function (id, locale) { this.getStatus(TYPE_ITEM, id, locale) }; this.getSpellStatus = function (id, locale) { this.getStatus(TYPE_SPELL, id, locale) }; this.refreshLinks = function () {
            if (typeof aowow_tooltips != "undefined") {
                for (var i = 0; i < document.links.length; i++) {
                    var link = document.links[i]; var node = link.parentNode; var isTooltipChild = !1; while (node != null) {
                        if ((" " + node.className + " ").replace(/[\n\t]/g, " ").indexOf(" wowhead-tooltip ") > -1) { isTooltipChild = !0; break }
                        node = node.parentNode
                    }
                    if (!isTooltipChild) { scanElement(link) }
                }
            }
            this.hideTooltip()
        }; this.setParent = function (newParent) { $WH.Tooltip.reset(); $WH.Tooltip.prepare(newParent) }; if (isRemote) { this.set = function (foo) { $WH.cO(opt, foo) }; this.showTooltip = function (e, tooltip, icon) { updateCursorPos(e); showTooltip(tooltip, icon) }; this.hideTooltip = function () { $WH.Tooltip.hide() }; this.moveTooltip = function (e) { onMouseMove(e) } }
        init()
    }
}
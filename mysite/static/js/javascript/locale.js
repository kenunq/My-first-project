var LOCALE_ENUS = 0; var LOCALE_FRFR = 2; var LOCALE_DEDE = 3; var LOCALE_ZHCN = 4; var LOCALE_ESES = 6; var LOCALE_RURU = 8; var Locale = {
    current: {}, locales: { 0: { id: LOCALE_ENUS, name: 'enus', domain: 'www', description: 'English' }, 8: { id: LOCALE_RURU, name: 'ruru', domain: 'ru', description: String.fromCharCode(1056, 1091, 1089, 1089, 1082, 1080, 1081) } }, getAll: function () {
        var result = []; for (var id in Locale.locales) { result.push(Locale.locales[id]) }
        return result
    }, getAllByName: function () { var result = Locale.getAll(); result.sort(function (a, b) { return $WH.strcmp(a.description, b.description) }); return result }, getId: function () { return Locale.current.id }, getName: function () { var localeId = Locale.getId(); return Locale.locales[localeId].name }, get: function () { var localeId = Locale.getId(); return Locale.locales[localeId] }, set: function (localeId) { $.extend(Locale.current, Locale.locales[localeId]) }
}; Locale.set(LOCALE_ENUS)
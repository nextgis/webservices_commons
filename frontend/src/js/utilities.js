
export function htmlToArray(el) {
    var arr = [];
    var arrayList = el.children();
    arrayList.each(function () {
        arr.push($(this).text().toLowerCase())
    });
    return arr;
}

export function getURLParameter(name) {
    return decodeURIComponent((new RegExp('[?|&]' + name + '=' + '([^&;]+?)(&|#|;|$)').exec(location.search) || [null, ''])[1].replace(/\+/g, '%20')) || null;
}

//Get query string parameters

export function get_query_value(name, url) {
    if (!url) url = location.href;
    name = name.replace(/[\[]/, "\\\[").replace(/[\]]/, "\\\]");

    var regexS_attr = "[\\?&]" + name,
        regexS_value = "[\\?&]" + name + "=([^&#]*)",
        regex_attr = new RegExp(regexS_attr),
        regex_value = new RegExp(regexS_value),
        results_attr = regex_attr.exec(url),
        results_value = regex_value.exec(url);

    if (results_attr && !results_value) {
        return "";
    } else {
        return results_value == null ? null : results_value[1];
    }
}

// Remove get parameters
export function removeURLParameters(url) {
    var urlparts = url.split('?');
    return urlparts[0];
}

// Returns a function, that, as long as it continues to be invoked, will not
// be triggered. The function will be called after it stops being called for
// N milliseconds. If `immediate` is passed, trigger the function on the
// leading edge, instead of the trailing.
export function debounce(f, ms) {
    let timer = null;

    return function (...args) {
        const onComplete = () => {
              f.apply(this, args);
              timer = null;
        }

        if (timer) {
            clearTimeout(timer);
        }

        timer = setTimeout(onComplete, ms);
    };
}
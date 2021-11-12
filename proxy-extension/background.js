var proxy_host = "zproxy.lum-superproxy.io";
var proxy_port = 22225;

var config = {
    mode: "fixed_servers",
    rules: {
      singleProxy: {
        scheme: "http",
        host: proxy_host,
        port: proxy_port
      },
      bypassList: []
    }
 };


function proxyRequest(request_data) {
    return {
        type: "http",
        host: proxy_host, 
        port: proxy_port
    };
}

chrome.proxy.settings.set({value: config, scope: "regular"}, function() {;});

function callbackFn(details) {
return {
    authCredentials: {
        username: "lum-customer-c_cc92928e-zone-isp-154.17.72.0",
        password: "y2w81jxpeu7y"
    }
};
}

chrome.webRequest.onAuthRequired.addListener(
        callbackFn,
        {urls: ["<all_urls>"]},
        ['blocking']
);

chrome.proxy.onRequest.addListener(proxyRequest, {urls: ["<all_urls>"]});
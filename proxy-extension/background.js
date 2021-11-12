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
    console.log("proxyRequest");
    console.log(request_data);
    return {
        type: "http",
        host: proxy_host, 
        port: proxy_port
    };
}

browser.proxy.settings.set({value: config, scope: "regular"}, function() {;});

function callbackFn(details) {
    console.log("callbackFn");
    console.log(details);
return {
    authCredentials: {
        username: "lum-customer-c_cc92928e-zone-isp-ip-154.17.72.0",
        password: "y2w81jxpeu7y"
    }
};
}

browser.webRequest.onAuthRequired.addListener(
        callbackFn,
        {urls: ["<all_urls>"]},
        ['blocking']
);

browser.proxy.onRequest.addListener(proxyRequest, {urls: ["<all_urls>"]});
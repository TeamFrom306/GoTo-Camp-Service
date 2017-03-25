export default function (baseUrl) {
	var endpoint = baseUrl;

	function ajax (type, url, data, successCallback, errorCallback) {
		var xhr = new XMLHttpRequest();
		xhr.open(type, endpoint + url, true);
		xhr.onload = function() {
			if (xhr.response) {
				if (xhr.status >= 200 && xhr.status < 400 && xhr.response.result) {
					console.log(xhr.status);
					var result = xhr.response.result;
					if (successCallback)
						successCallback(result);
				} else {
					console.error(xhr.response.error);
					if (errorCallback)
						errorCallback(xhr.status, xhr.response.error);
				}
			} else {
				console.error('Response is absent!');
			}	
		}
		xhr.onerror = function() {
			console.error(xhr.status);
			if (errorCallback)
				errorCallback(xhr.status);
		}
		xhr.responseType = 'json';
		xhr.send(JSON.stringify(data));
	}

	function get(url, successCallback, errorCallback) { ajax("GET", url, '', successCallback, errorCallback); }
	function post(url, data, successCallback, errorCallback) { ajax("GET", url, data, successCallback, errorCallback); }
	function del(url, successCallback, errorCallback) { ajax("DELETE", url, '', successCallback, errorCallback); }
	function put(url, data, successCallback, errorCallback) { ajax("PUT", url, data, successCallback, errorCallback); }

	return {
		get,
		post,
		delete: del,
		put,
		request: ajax,
		endpoint,
		setEndpoint: function(newEndpoint) {
			this.endpoint = newEndpoint;
		}
	}
}

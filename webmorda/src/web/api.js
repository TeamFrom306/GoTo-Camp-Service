import ajax from './ajax';
import {token} from './../user';

export default function(baseUrl) {
	function amp(name, argument) {
		return argument ? '?' + name + '=' + argument : '';
	}

	return {
		login: function(password, successCallback, errorCallback) {
			ajax(baseUrl).get('login/' + password, successCallback, errorCallback);
		},

		users: {
			url: token + '/users',
			get: function(successCallback, errorCallback) {
				ajax(baseUrl).get(this.url, successCallback, errorCallback);
			},

			delete: function(id, successCallback, errorCallback) {
				ajax(baseUrl).delete(this.url + id, successCallback, errorCallback);
			},
		},

		achievements: {
			url: token + '/achievements/',
			get: function(id, successCallback, errorCallback) {
				ajax(baseUrl).get(this.url + id, successCallback, errorCallback);
			},

			add: function(achievement, successCallback, errorCallback) {
				ajax(baseUrl).post(this.url, achievement, successCallback, errorCallback);
			},

			delete: function(id, successCallback, errorCallback) {
				ajax(baseUrl).delete(this.url + id, successCallback, errorCallback);
			},

			addToUser: function(userId, achievementId, successCallback, errorCallback) {
				ajax(baseUrl).post(this.url + userId, {achievement}, successCallback, errorCallback);
			},
		},

		schedule: {
			url: token + '/schedule/',
			get: function(userId, date, successCallback, errorCallback) {
				ajax(baseUrl).get(this.url + userId + amp('date', date), successCallback, errorCallback);
			}
		},
		
		groups: {
			url: token + '/groups/',
			get: function(id, successCallback, errorCallback) {
				ajax(baseUrl).get(this.url + id, successCallback, errorCallback);
			},

			add: function(achievement, successCallback, errorCallback) {
				ajax(baseUrl).post(this.url, achievement, successCallback, errorCallback);
			},

			delete: function(id, successCallback, errorCallback) {
				ajax(baseUrl).delete(this.url + id, successCallback, errorCallback);
			},

			addUsers: function(id, users, successCallback, errorCallback) {
				ajax(baseUrl).post(this.url, {users}, successCallback, errorCallback);
			}
		},
		
		teams: {
			url: token + '/teams/',
			get: function(id, successCallback, errorCallback) {
				ajax(baseUrl).get(this.url + id, successCallback, errorCallback);
			},

			add: function(achievement, successCallback, errorCallback) {
				ajax(baseUrl).post(this.url, achievement, successCallback, errorCallback);
			},

			delete: function(id, successCallback, errorCallback) {
				ajax(baseUrl).delete(this.url + id, successCallback, errorCallback);
			},
		},

		message: {
			url: token + '/messages/',
			send: function(message, ids, successCallback, errorCallback) {
				ajax(baseUrl).post(this.url, {text:message}, successCallback, errorCallback);
			}
		}
	}
}

import config from './../config';
import setajax from './ajax';
import setapi from './api';

var ajax = setajax(config.web.url);
var api = setapi(config.web.url);

export default {
    api,
    ajax
}

export { ajax };
export { api };

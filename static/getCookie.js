/**
 * This function is used for getting the cookie value from cookie key
 * @param name: the key from cookie that we need to get the value
 * @returns {?string}: the value of the cookie key, or null if no value is found
 */
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        // Cookies are stored as a string separated with ;. We need to split them out to find the value
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            let cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

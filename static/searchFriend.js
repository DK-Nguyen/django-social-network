/**
 * This function handle ajax request to search for friend using a string query
 * @param searchQuery(string): Query to find the friend using name
 * @param callback: ((error, Friends) => any): Callback that will be called after the ajax
 * is completed. Friends will be presented as we can find in the app 'friends' and the correct
 * view that this function is requesting
 */
function performFriendSearch(searchQuery, callback) {
    $.get('/friends/search?query=' + searchQuery)
        .done(function searchFriendSuccess(data) {
            callback(null, data.data)
        })
        .fail(function seachFriendFailed(error) {
            callback(error, null)
        })
}

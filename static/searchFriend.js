function performFriendSearch(searchQuery, callback) {
    $.get('/friends/search?query=' + searchQuery)
        .done(function searchFriendSuccess(data) {
            callback(null, data.data)
        })
        .fail(function seachFriendFailed(error) {
            callback(error, null)
        })
}

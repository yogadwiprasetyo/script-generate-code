package com.example.api.endpoint

internal object UserApiEndPoint {
    const val GET_USERS = "users"
    const val GET_USERS_USERID = "users/{userId}"
    const val POST_USERS = "users"
    const val PUT_USERS_USERID = "users/{userId}"
    const val PATCH_USERS_USERID_STATUS = "users/{userId}/status"
    const val GET_USERS_SEARCH = "users/search"
    const val POST_USERS_VALIDATE_EMAIL = "users/validate-email"
}

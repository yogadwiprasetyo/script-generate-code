package com.example.api.dtos

/**
 * Generated on 2025-04-18 10:36:54
 */
data class UserGetResponse(
    val id: String,
    val username: String,
    val email: String,
    val firstName: String,
    val lastName: String,
    val phoneNumber: String,
    val createdAt: String,
    val updatedAt: String,
    val status: String,
    val preferences: Object
)

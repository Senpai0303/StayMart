package com.staymart.controller;

import com.staymart.common.ApiResponse;
import com.staymart.common.PageResponse;
import com.staymart.dto.request.ChatMessageRequest;
import com.staymart.dto.response.ChatResponse;
import com.staymart.dto.response.ConversationResponse;
import com.staymart.service.ChatService;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.security.SecurityRequirement;
import io.swagger.v3.oas.annotations.tags.Tag;
import jakarta.validation.Valid;
import org.springframework.data.domain.PageRequest;
import org.springframework.data.domain.Pageable;
import org.springframework.data.domain.Sort;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import java.util.List;

@RestController
@RequestMapping("/api/chats")
@Tag(name = "Chats", description = "User to user messaging")
@SecurityRequirement(name = "bearerAuth")
public class ChatController {

    private final ChatService chatService;

    public ChatController(ChatService chatService) {
        this.chatService = chatService;
    }

    @PostMapping
    @Operation(summary = "Send a message")
    public ApiResponse<ChatResponse> send(@Valid @RequestBody ChatMessageRequest request) {
        return ApiResponse.ok("Message sent", chatService.send(request));
    }

    @GetMapping("/conversations")
    @Operation(summary = "List my conversations")
    public ApiResponse<List<ConversationResponse>> conversations() {
        return ApiResponse.ok(chatService.conversations());
    }

    @GetMapping("/unread-count")
    @Operation(summary = "Total unread messages received by me")
    public ApiResponse<Long> unreadCount() {
        return ApiResponse.ok(chatService.unreadCount());
    }

    @GetMapping("/with/{userId}")
    @Operation(summary = "Get conversation thread with a user")
    public ApiResponse<PageResponse<ChatResponse>> conversationWith(
            @PathVariable Long userId,
            @RequestParam(defaultValue = "0") int page,
            @RequestParam(defaultValue = "50") int size) {
        return ApiResponse.ok(chatService.conversationWith(userId, pageable(page, size)));
    }

    @PostMapping("/read/{userId}")
    @Operation(summary = "Mark all messages from a user as read")
    public ApiResponse<Void> markRead(@PathVariable Long userId) {
        chatService.markRead(userId);
        return ApiResponse.ok("Messages marked as read", null);
    }

    private Pageable pageable(int page, int size) {
        return PageRequest.of(Math.max(page, 0), Math.min(size, 100), Sort.by(Sort.Direction.ASC, "timestamp"));
    }
}
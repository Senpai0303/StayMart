package com.staymart.service;

import com.staymart.common.PageResponse;
import com.staymart.dto.request.ChatMessageRequest;
import com.staymart.dto.response.ChatResponse;
import com.staymart.dto.response.ConversationResponse;
import com.staymart.dto.response.UserSummary;
import com.staymart.entity.Chat;
import com.staymart.entity.User;
import com.staymart.entity.enums.BehaviorAction;
import com.staymart.entity.enums.BehaviorItemType;
import com.staymart.exception.BadRequestException;
import com.staymart.exception.ResourceNotFoundException;
import com.staymart.repository.ChatRepository;
import com.staymart.repository.UserRepository;
import com.staymart.util.SecurityUtils;
import org.springframework.data.domain.Pageable;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.time.LocalDateTime;
import java.util.Comparator;
import java.util.LinkedHashMap;
import java.util.LinkedHashSet;
import java.util.List;
import java.util.Map;
import java.util.Set;

@Service
public class ChatService {

    private final ChatRepository chatRepository;
    private final UserRepository userRepository;
    private final BehaviorService behaviorService;

    public ChatService(ChatRepository chatRepository,
                       UserRepository userRepository,
                       BehaviorService behaviorService) {
        this.chatRepository = chatRepository;
        this.userRepository = userRepository;
        this.behaviorService = behaviorService;
    }

    @Transactional
    public ChatResponse send(ChatMessageRequest request) {
        User sender = SecurityUtils.currentUser();
        User receiver = userRepository.findById(request.receiverId())
                .orElseThrow(() -> new ResourceNotFoundException("Receiver not found with id: " + request.receiverId()));

        if (sender.getId().equals(receiver.getId())) {
            throw new BadRequestException("You cannot message yourself");
        }

        Chat chat = Chat.builder()
                .sender(sender)
                .receiver(receiver)
                .listingType(request.listingType())
                .listingId(request.listingId())
                .message(request.message().trim())
                .isRead(false)
                .timestamp(LocalDateTime.now())
                .build();

        if (request.listingType() != null && request.listingId() != null) {
            behaviorService.record(sender.getId(),
                    request.listingType() == com.staymart.entity.enums.ChatListingType.PROPERTY
                            ? BehaviorItemType.PROPERTY : BehaviorItemType.PRODUCT,
                    request.listingId(), BehaviorAction.CONTACT, null, null);
        }

        return ChatResponse.from(chatRepository.save(chat));
    }

    @Transactional(readOnly = true)
    public PageResponse<ChatResponse> conversationWith(Long userId, Pageable pageable) {
        Long me = SecurityUtils.currentUserId();
        if (me.equals(userId)) {
            throw new BadRequestException("Cannot open a conversation with yourself");
        }
        userRepository.findById(userId)
                .orElseThrow(() -> new ResourceNotFoundException("User not found with id: " + userId));
        return PageResponse.of(chatRepository.conversationPage(me, userId, pageable), ChatResponse::from);
    }

    @Transactional(readOnly = true)
    public List<ConversationResponse> conversations() {
        Long me = SecurityUtils.currentUserId();

        Set<Long> partnerIds = new LinkedHashSet<>();
        partnerIds.addAll(chatRepository.findDistinctReceivers(me));
        partnerIds.addAll(chatRepository.findDistinctSenders(me));

        Map<Long, ConversationResponse> byPartner = new LinkedHashMap<>();
        for (Long partnerId : partnerIds) {
            List<Chat> messages = chatRepository.conversation(me, partnerId);
            if (messages.isEmpty()) {
                continue;
            }
            Chat last = messages.get(messages.size() - 1);
            long unread = chatRepository.countByReceiverIdAndSenderIdAndIsReadFalse(me, partnerId);
            UserSummary partner = UserSummary.from(userRepository.findById(partnerId).orElse(null));
            byPartner.put(partnerId,
                    new ConversationResponse(partner, last.getMessage(), last.getTimestamp(), unread));
        }

        return byPartner.values().stream()
                .sorted(Comparator.comparing(ConversationResponse::lastMessageAt).reversed())
                .toList();
    }

    @Transactional(readOnly = true)
    public long unreadCount() {
        return chatRepository.countByReceiverIdAndIsReadFalse(SecurityUtils.currentUserId());
    }

    @Transactional
    public void markRead(Long partnerId) {
        Long me = SecurityUtils.currentUserId();
        List<Chat> messages = chatRepository.conversation(me, partnerId);
        messages.stream()
                .filter(c -> c.getReceiver().getId().equals(me) && !Boolean.TRUE.equals(c.getIsRead()))
                .forEach(c -> c.setIsRead(true));
    }
}
package com.staymart.repository;

import com.staymart.entity.Chat;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;

import java.util.List;

public interface ChatRepository extends JpaRepository<Chat, Long> {

    @Query("SELECT c FROM Chat c WHERE (c.sender.id = :user1 AND c.receiver.id = :user2) OR (c.sender.id = :user2 AND c.receiver.id = :user1) ORDER BY c.timestamp ASC")
    List<Chat> conversation(@Param("user1") Long user1, @Param("user2") Long user2);

    @Query("SELECT c FROM Chat c WHERE (c.sender.id = :user1 AND c.receiver.id = :user2) OR (c.sender.id = :user2 AND c.receiver.id = :user1) ORDER BY c.timestamp ASC")
    Page<Chat> conversationPage(@Param("user1") Long user1, @Param("user2") Long user2, Pageable pageable);

    long countByReceiverIdAndIsReadFalse(Long receiverId);

    long countByIsReadFalse();

    long countByReceiverIdAndSenderIdAndIsReadFalse(Long receiverId, Long senderId);

    @Query("SELECT c.receiver.id FROM Chat c WHERE c.sender.id = :userId AND c.receiver.id <> :userId")
    List<Long> findDistinctReceivers(@Param("userId") Long userId);

    @Query("SELECT c.sender.id FROM Chat c WHERE c.receiver.id = :userId AND c.sender.id <> :userId")
    List<Long> findDistinctSenders(@Param("userId") Long userId);
}
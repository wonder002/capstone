package com.wizard.api_server.repository;

import com.wizard.api_server.domain.entity.Commentary;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.List;
import java.util.UUID;

public interface CommentaryRepository extends JpaRepository<Commentary, Long> {
    List<Commentary> findByCommentaryRequestId(UUID commentaryRequestId);
}

package com.delegate.service;

import com.delegate.model.AuditLog;
import com.delegate.repository.AuditLogRepository;
import com.fasterxml.jackson.databind.ObjectMapper;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import java.time.LocalDateTime;
import java.util.List;
import java.util.UUID;

@Service
@RequiredArgsConstructor
public class AuditLogService {
    private final AuditLogRepository auditLogRepository;
    private final ObjectMapper objectMapper;

    @Transactional
    public void logCreation(String entityType, UUID entityId, UUID actorId, Object entity) {
        try {
            AuditLog log = new AuditLog();
            log.setEntityType(entityType);
            log.setEntityId(entityId);
            log.setAction("CREATE");
            log.setActorId(actorId);
            log.setTimestamp(LocalDateTime.now());
            log.setChanges(objectMapper.writeValueAsString(entity));
            auditLogRepository.save(log);
        } catch (Exception e) {
            throw new RuntimeException("Failed to create audit log", e);
        }
    }

    @Transactional
    public void logUpdate(String entityType, UUID entityId, UUID actorId, Object oldEntity, Object newEntity) {
        try {
            AuditLog log = new AuditLog();
            log.setEntityType(entityType);
            log.setEntityId(entityId);
            log.setAction("UPDATE");
            log.setActorId(actorId);
            log.setTimestamp(LocalDateTime.now());
            
            var changes = new Object() {
                public final Object old = oldEntity;
                public final Object new_ = newEntity;
            };
            log.setChanges(objectMapper.writeValueAsString(changes));
            
            auditLogRepository.save(log);
        } catch (Exception e) {
            throw new RuntimeException("Failed to create audit log", e);
        }
    }

    @Transactional
    public void logDeletion(String entityType, UUID entityId, UUID actorId, Object entity) {
        try {
            AuditLog log = new AuditLog();
            log.setEntityType(entityType);
            log.setEntityId(entityId);
            log.setAction("DELETE");
            log.setActorId(actorId);
            log.setTimestamp(LocalDateTime.now());
            log.setChanges(objectMapper.writeValueAsString(entity));
            auditLogRepository.save(log);
        } catch (Exception e) {
            throw new RuntimeException("Failed to create audit log", e);
        }
    }

    @Transactional(readOnly = true)
    public List<AuditLog> findByEntityTypeAndEntityId(String entityType, UUID entityId) {
        return auditLogRepository.findByEntityTypeAndEntityId(entityType, entityId);
    }

    @Transactional(readOnly = true)
    public List<AuditLog> findByActorId(UUID actorId) {
        return auditLogRepository.findByActorId(actorId);
    }

    @Transactional(readOnly = true)
    public List<AuditLog> findByTimestampBetween(LocalDateTime start, LocalDateTime end) {
        return auditLogRepository.findByTimestampBetween(start, end);
    }

    @Transactional(readOnly = true)
    public List<AuditLog> findByEntityTypeAndTimestampBetween(
        String entityType, LocalDateTime start, LocalDateTime end
    ) {
        return auditLogRepository.findByEntityTypeAndTimestampBetween(entityType, start, end);
    }
} 